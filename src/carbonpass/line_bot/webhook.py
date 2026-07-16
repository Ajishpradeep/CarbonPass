"""LINE Messaging API webhook — the Module 3 inclusion interface.

Flow (zh-TW, zero ESG vocabulary):
    owner sends photos of bills/invoices  -> stored in the user's session folder
    owner types 「產生報告」               -> ingest + pack + costdelta, reply summary
    owner types 「排程」                   -> Module 2 shift plan summary
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
        # the e-invoice XMLs + production log via the e-GUI consent path (docs/10
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
    from carbonpass.costdelta.screen import cost_delta, render_text
    from carbonpass.ingestion.pipeline import ingest_firm
    from carbonpass.writer.fill import fill_template

    n_bills = len(list((session / "bills").glob("*")))
    n_inv = len(list((session / "invoices").glob("*")))
    if n_bills == 0 and n_inv == 0:
        return ["還沒有收到任何單據喔！請先拍電費單或發票的照片傳給我 📸"]
    activity = ingest_firm(session, use_vlm=True)
    xlsx = session / "communication_template.xlsx"
    sidecar = fill_template(activity, xlsx)
    delta = cost_delta(activity)
    lines = [f"✅ 報告完成！CBAM 資料包已產生（{xlsx.name}）"]
    for p in sidecar["products"]:
        lines.append(f"CN {p['cn_code']}：每噸碳含量 {p['see_total']['value']:.2f} tCO2e"
                     f"（預設值占 {p['share_default_values']:.0%}）")
    for n in sidecar["needs_attention"][:2]:
        lines.append(f"⚠️ {n}")
    return ["\n".join(lines), render_text(delta)]


def _handle_schedule(session: Path) -> list[str]:
    from carbonpass.scheduler.ledger import schedule_firm

    res = schedule_firm(session)
    led = res["ledger"]
    return [(f"🕐 排程建議（依台電時間電價＋即時電網碳強度）\n"
             f"每週可省 NT${led['delta_week']['cost_ntd']:,.0f}，"
             f"一年約 NT${led['delta_year_est']['cost_ntd']:,.0f}\n"
             f"減碳 {led['delta_year_est']['emissions_tco2e']} tCO2e/年"
             f"（屬用電間接排放；不影響 CBAM 憑證金額）")]


def _handle_status(session: Path) -> list[str]:
    n_bills = len(list((session / "bills").glob("*")))
    n_inv = len(list((session / "invoices").glob("*")))
    return [f"目前收到：電費單 {n_bills} 張、發票 {n_inv} 張。\n"
            f"傳「產生報告」開始計算；傳「排程」看省電建議。"]


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
            elif "排程" in text or "省電" in text:
                out_texts = _handle_schedule(session)
            elif "狀態" in text:
                out_texts = _handle_status(session)
            else:
                out_texts = ["你好！我是 CarbonPass 🌱\n"
                             "拍電費單／發票的照片傳給我；輸入「產生報告」拿 CBAM 資料包，"
                             "「排程」看省電建議，「狀態」看進度。"]

        if out_texts:
            _reply_text(reply_token, out_texts)
            replies.append({"to": user_id, "texts": out_texts})

    return {"ok": True, "replies": replies}
