"""LINE Messaging API webhook — the Module 3 inclusion interface.

Flow (zh-TW, zero ESG vocabulary) — the four sights from one photo set:
    owner sends photos of bills/invoices  -> stored in the user's session folder
    owner types 「產生報告」               -> Sight ①: ingest + CBAM pack + ranked fix-list
    owner types 「浪費」/「損耗」          -> Sight ②: waste map (gross AND net) + drift
    owner types 「排程」                   -> Sight ③: grid-aware shift plan
    owner types 「我正常嗎」               -> Sight ④: percentile vs (labelled) seed band
    owner types 「狀態」                   -> what's been received so far

Modes:
    real      LINE_CHANNEL_SECRET + LINE_CHANNEL_ACCESS_TOKEN set in .env:
              X-Line-Signature verified; images fetched from the LINE content
              API; replies pushed via the reply API.
    simulator secret unset: signature check skipped, image events carry a local
              file path, and replies are returned in the HTTP response so
              scripts/line_simulator.py can print them. Wiring a real channel
              later = filling two .env values, nothing else.

Session state: one folder per LINE user under out/line_sessions/<user_id>/ with
a firm.json copied from onboarding (the PoC seeds it from the mock corpus firm;
at pilot this comes from the LINE onboarding Q&A).
"""
from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import shutil
from pathlib import Path

import httpx
from fastapi import APIRouter, Header, HTTPException, Request

router = APIRouter(prefix="/line", tags=["line"])

SESSIONS = Path("out/line_sessions")
LINE_API = "https://api.line.me/v2/bot"
LINE_CONTENT_API = "https://api-data.line.me/v2/bot"


def _secret() -> str:
    return os.environ.get("LINE_CHANNEL_SECRET", "").strip()


def _token() -> str:
    return os.environ.get("LINE_CHANNEL_ACCESS_TOKEN", "").strip()


def verify_signature(body: bytes, signature: str | None) -> bool:
    secret = _secret()
    if not secret:      # simulator mode
        return True
    if not signature:
        return False
    mac = hmac.new(secret.encode(), body, hashlib.sha256).digest()
    return hmac.compare_digest(base64.b64encode(mac).decode(), signature)


def _session_dir(user_id: str) -> Path:
    d = SESSIONS / user_id
    (d / "bills").mkdir(parents=True, exist_ok=True)
    (d / "invoices").mkdir(parents=True, exist_ok=True)
    if not (d / "firm.json").exists():
        # PoC onboarding stand-in: seed identity/machines from the mock firm, and
        # the e-invoice XMLs + production log via the e-GUI consent path (docs/archive/10
        # G11: steel & fuel arrive as structured XML, not photos; the photo flow
        # is for the Taipower bill).
        seed = Path("data/mock_corpus/firm_a")
        if (seed / "firm.json").exists():
            shutil.copy(seed / "firm.json", d / "firm.json")
            for xml in (seed / "invoices").glob("*.xml"):
                shutil.copy(xml, d / "invoices" / xml.name)
            if (seed / "production_log.csv").exists():
                shutil.copy(seed / "production_log.csv", d / "production_log.csv")
    return d


def _classify_and_store(session: Path, image_bytes: bytes, hint: str) -> str:
    """Very light routing: filename hint decides bill vs invoice folder."""
    sub = "bills" if ("taipower" in hint or "bill" in hint or "電費" in hint) else "invoices"
    n = len(list((session / sub).glob("*.png"))) + 1
    dest = session / sub / f"{sub[:-1]}_{n:03d}.png"
    dest.write_bytes(image_bytes)
    return f"{sub}/{dest.name}"


def _reply_text(reply_token: str, texts: list[str]) -> None:
    if not _token():
        return  # simulator mode: reply travels back in the HTTP response
    httpx.post(f"{LINE_API}/message/reply",
               headers={"Authorization": f"Bearer {_token()}"},
               json={"replyToken": reply_token,
                     "messages": [{"type": "text", "text": t[:4900]} for t in texts[:5]]},
               timeout=15.0)


def _fetch_line_content(message_id: str) -> bytes:
    r = httpx.get(f"{LINE_CONTENT_API}/message/{message_id}/content",
                  headers={"Authorization": f"Bearer {_token()}"}, timeout=30.0)
    r.raise_for_status()
    return r.content


def _handle_report(session: Path) -> list[str]:
    import json as _json

    from carbonpass.costdelta.fixlist import fixlist, render_fixlist_zh
    from carbonpass.ingestion.pipeline import ingest_firm
    from carbonpass.writer.fill import fill_template

    n_bills = len(list((session / "bills").glob("*")))
    n_inv = len(list((session / "invoices").glob("*")))
    if n_bills == 0 and n_inv == 0:
        return ["還沒有收到任何單據喔！請先拍電費單或發票的照片傳給我 📸"]
    activity = ingest_firm(session, use_vlm=True)
    xlsx = session / "communication_template.xlsx"
    sidecar = fill_template(activity, xlsx)
    lines = [f"✅ 報告完成！CBAM 資料包已產生（{xlsx.name}）"]
    for p in sidecar["products"]:
        lines.append(f"CN {p['cn_code']}：每噸碳含量 {p['see_total']['value']:.2f} tCO2e"
                     f"（預設值占 {p['share_default_values']:.0%}）")
    for n in sidecar["needs_attention"][:2]:
        lines.append(f"⚠️ {n}")
    # the ranked fix-list replaces the old cost-delta screen (docs/archive/21 §1.3)
    act_path = session / "activity.json"
    act_path.write_text(_json.dumps(activity, ensure_ascii=False), encoding="utf-8")
    try:
        from carbonpass.scheduler.ledger import schedule_firm
        schedule = schedule_firm(session)
    except Exception:            # offline / no machine list — lever degrades honestly
        schedule = None
    fl = fixlist(str(act_path), str(session), schedule)
    return ["\n".join(lines), render_fixlist_zh(fl)]


def _handle_schedule(session: Path) -> list[str]:
    from carbonpass.scheduler.ledger import schedule_firm

    res = schedule_firm(session)
    led = res["ledger"]
    return [(f"🕐 排程建議（依台電時間電價＋即時電網碳強度）\n"
             f"每週可省 NT${led['delta_week']['cost_ntd']:,.0f}，"
             f"一年約 NT${led['delta_year_est']['cost_ntd']:,.0f}\n"
             f"減碳 {led['delta_year_est']['emissions_tco2e']} tCO2e/年"
             f"（屬用電間接排放；不影響 CBAM 憑證金額）")]


def _handle_waste(session: Path) -> list[str]:
    """Sight ②: 「浪費」/「損耗」 — per-line waste map, gross AND net, + drift alerts."""
    import json as _json

    from carbonpass.ingestion.pipeline import ingest_firm
    from carbonpass.waste import monthly_series, scan as waste_scan

    n_inv = len(list((session / "invoices").glob("*.xml")))
    if n_inv == 0 or not (session / "production_log.csv").exists():
        return ["需要鋼材發票（XML）和生產日誌才能算損耗喔！請先完成資料同意設定 📄"]
    activity = ingest_firm(session, use_vlm=False)   # invoices + log only — fast
    act_path = session / "waste_activity.json"
    act_path.write_text(_json.dumps(activity, ensure_ascii=False), encoding="utf-8")
    r = waste_scan(str(act_path), str(session))
    drift = monthly_series(str(session), activity)

    lines = [f"🧮 物料損耗地圖（{r['period_year']} 年）"]
    for l in r["lines"]:
        tag = "⚠️不鏽鋼 " if l["stainless"] else ""
        lines.append(f"{tag}{l['product']}：投入 {l['consumed_t']:,.0f} t → "
                     f"產出 {l['produced_t']:,.0f} t → 邊角料 {l['scrap_t']:,.0f} t"
                     f"（{l['loss_pct']:.1f}%）")
        lines.append(f"　內含碳 {l['embodied_tco2e_per_yr_gross']:,.0f} tCO2e/年——買進但沒出貨")
        if l["money_loss"]:
            m = l["money_loss"]
            lo, hi = m["net_of_resale_ntd_range"]
            lines.append(f"　金額：進料價 NT${m['purchase_value_ntd']:,.0f}／"
                         f"扣廢料轉售後淨損 NT${lo:,.0f}–{hi:,.0f}")
    t = r["totals"]
    lines.append(f"👉 5% 情境：每年少買 {t['scenario_embodied_reduction_tco2e_per_yr']:,.0f} tCO2e "
                 f"的內含碳、NT${t['scenario_ntd_not_spent_per_yr']:,.0f} 不用花")
    for dl in drift["lines"]:
        for a in dl["alerts"]:
            lines.append(a["message_zh"])
    lines.append("註：質量以「裁切前」計（IR 2025/2547 附件三 F 節）；廢料是賣掉回爐的，"
                 "看得見的是那一堆、看不見的是這些資訊。合成語料示意，試點實測後更新。")
    return ["\n".join(lines)]


def _handle_benchmark(session: Path) -> list[str]:
    """Sight ④: 「我正常嗎」 — percentile vs the (labelled) synthetic seed band."""
    import json as _json

    from carbonpass.benchmark import percentile_screen
    from carbonpass.ingestion.pipeline import ingest_firm
    from carbonpass.waste import scan as waste_scan

    if not (session / "production_log.csv").exists():
        return ["需要生產日誌和鋼材發票才能比較同業喔！請先完成資料同意設定 📄"]
    activity = ingest_firm(session, use_vlm=False)
    act_path = session / "waste_activity.json"
    act_path.write_text(_json.dumps(activity, ensure_ascii=False), encoding="utf-8")
    r = waste_scan(str(act_path), str(session))
    if not r["lines"]:
        return ["找不到可比較的產線資料。"]
    # weight by consumed mass for the firm-level loss rate
    tot_c = sum(l["consumed_t"] for l in r["lines"])
    loss = sum(l["loss_pct"] * l["consumed_t"] for l in r["lines"]) / tot_c
    screen = percentile_screen(loss)
    return [screen["message_zh"] + "\n（k≥5 匿名底線：您的原始資料永遠不離開這台機器；"
            "只有 n≥5 家的匿名彙總才可能對外發布。）"]


def _handle_status(session: Path) -> list[str]:
    n_bills = len(list((session / "bills").glob("*")))
    n_inv = len(list((session / "invoices").glob("*")))
    return [f"目前收到：電費單 {n_bills} 張、發票 {n_inv} 張。\n"
            f"四種看見：「產生報告」CBAM 資料包＋改善清單、「浪費」物料損耗地圖、"
            f"「排程」省電建議、「我正常嗎」同業比較。"]


@router.post("/webhook")
async def webhook(request: Request,
                  x_line_signature: str | None = Header(default=None)) -> dict:
    body = await request.body()
    if not verify_signature(body, x_line_signature):
        raise HTTPException(403, "bad X-Line-Signature")
    payload = json.loads(body)
    replies: list[dict] = []

    for event in payload.get("events", []):
        user_id = (event.get("source") or {}).get("userId", "anonymous")
        reply_token = event.get("replyToken", "")
        session = _session_dir(user_id)
        msg = event.get("message") or {}
        out_texts: list[str] = []

        if msg.get("type") == "image":
            if msg.get("_local_path"):                # simulator extension
                img = Path(msg["_local_path"]).read_bytes()
                hint = Path(msg["_local_path"]).name
            else:
                img = _fetch_line_content(msg["id"])
                hint = msg.get("fileName", "")
            stored = _classify_and_store(session, img, hint)
            out_texts = [f"收到 📸（存為 {stored}）。繼續傳，或輸入「產生報告」。"]
        elif msg.get("type") == "text":
            text = msg.get("text", "").strip()
            if "產生報告" in text or "報告" in text:
                out_texts = _handle_report(session)
            elif "浪費" in text or "損耗" in text:
                out_texts = _handle_waste(session)
            elif "正常" in text or "同業" in text:
                out_texts = _handle_benchmark(session)
            elif "排程" in text or "省電" in text:
                out_texts = _handle_schedule(session)
            elif "狀態" in text:
                out_texts = _handle_status(session)
            else:
                out_texts = ["你好！我是 CarbonPass 🌱\n"
                             "拍電費單／發票的照片傳給我；輸入「產生報告」拿 CBAM 資料包，"
                             "「浪費」看物料損耗地圖，「排程」看省電建議，「狀態」看進度。"]

        if out_texts:
            _reply_text(reply_token, out_texts)
            replies.append({"to": user_id, "texts": out_texts})

    return {"ok": True, "replies": replies}
