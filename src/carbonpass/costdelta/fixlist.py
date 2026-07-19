"""The fix-list: one ranked screen per firm — what to fix, what it's worth, and
whether it's worth it THIS YEAR.

Levers in measured order (docs/18 §4, docs/20 §4): ① yield → ② mill EPD /
precursor route → ③ process energy → ④ load shifting. The order is the
project's honesty ranking — yield moved 80× what the scheduler did on the same
synthetic firm — and the screen keeps it fixed rather than re-sorting by NT$.

A lever that answers "not worth it this year" is a FEATURE (the Thailand-row
discipline, docs/21 §1.3): a tool that can say "don't bother" is a compliance
instrument, not a sales brochure. Verdicts:
    worth_it | not_worth_it_this_year | insufficient_data
Materiality thresholds below are CarbonPass product heuristics (dated, stated
in output) — they are NOT regulatory thresholds; no such thresholds exist in
the CBAM rules (docs/15 §8.2.3: do not invent one).
"""
from __future__ import annotations

import json
from pathlib import Path

from carbonpass.benchmark.percentile import SEED_PROVENANCE
from carbonpass.costdelta.screen import cost_delta
from carbonpass.pack import load_activity
from carbonpass.waste import monthly_series, scan as waste_scan

# --- CarbonPass materiality heuristics (ours, dated 2026-07; shown in output) --
NTD_MATERIALITY_PER_YR = 100_000    # below this, a lever is noise for a 30-person firm
EUR_PER_T_MATERIALITY = 10.0        # buyer-side €/t below which new verification
                                    # effort is unlikely to pay this year
HEURISTICS_NOTE = ("verdict thresholds are CarbonPass product heuristics "
                   f"(NT${NTD_MATERIALITY_PER_YR:,}/yr; €{EUR_PER_T_MATERIALITY}/t, "
                   "set 2026-07) — NOT regulatory thresholds; CBAM has none")


def _yield_lever(waste: dict) -> dict:
    t = waste["totals"]
    ntd = t.get("scenario_ntd_not_spent_per_yr") or 0
    tco2e = t.get("scenario_embodied_reduction_tco2e_per_yr") or 0
    lines_at_target = all(
        l["loss_pct"] <= l["scenario_target_loss_pct"] for l in waste["lines"])
    if lines_at_target:
        verdict, rationale = "not_worth_it_this_year", \
            "loss already at or below the 5% scenario target — maintain, don't chase"
    elif ntd >= NTD_MATERIALITY_PER_YR:
        verdict, rationale = "worth_it", \
            "moves the declared SEE 1:1 (mass counted before cutting — IR 2025/2547 " \
            "Annex III §F) and is real cash: steel never bought"
    else:
        verdict, rationale = "not_worth_it_this_year", \
            f"scenario saving NT${ntd:,.0f}/yr is below materiality — revisit at scale"
    return {
        "id": "yield", "title": "Cut material loss toward the 5% scenario",
        "title_zh": "降低物料損耗（5% 情境）",
        "ntd_per_yr": ntd, "tco2e_per_yr": tco2e,
        "carbon_scope_note": "embodied carbon purchased but never shipped — reductions "
                             "flow 1:1 into the declared SEE (direct scope)",
        "money_loss_context": t.get("money_loss"),
        "verdict": verdict, "rationale": rationale,
        "provenance": [waste["certificate_price_provenance"], waste["data_provenance"]],
    }


def _epd_lever(delta: dict) -> dict:
    prods = [p for p in delta["products"] if p.get("delta_eur_per_t") is not None]
    if not prods:
        return {"id": "mill_epd", "title": "Mill EPD / precursor route",
                "title_zh": "向鋼廠要 EPD（原料路線）",
                "ntd_per_yr": None, "tco2e_per_yr": None,
                "carbon_scope_note": "precursor direct emissions (inside the certificate)",
                "verdict": "insufficient_data",
                "rationale": "no default-value comparison available for any product",
                "provenance": [delta["certificate_price_provenance"]]}
    best = max(prods, key=lambda p: p["delta_eur_per_t"])
    eur_t = best["delta_eur_per_t"]
    eur_yr = best["delta_eur_per_year_at_full_volume"]
    if eur_t >= EUR_PER_T_MATERIALITY:
        verdict = "worth_it"
        rationale = (f"one document from the mill is worth €{eur_t:,.2f}/t to your buyer "
                     f"(CN {best['cn_code']}) — the firm_c pattern: route/EPD dominates")
    else:
        verdict = "not_worth_it_this_year"
        rationale = (f"your data is worth €{eur_t:,.2f}/t to the buyer — Taiwan's default "
                     f"is mild and defaults are lawful without limit (IR 2025/2547, "
                     f"docs/15 §8.1); revisit when the default table or the certificate "
                     f"price moves")
    return {
        "id": "mill_epd", "title": "Mill EPD / precursor route",
        "title_zh": "向鋼廠要 EPD（原料路線）",
        "buyer_eur_per_t": eur_t, "buyer_eur_per_yr": eur_yr,
        "ntd_per_yr": None,   # buyer-side money; stated in € to keep sides honest
        "tco2e_per_yr": None,
        "carbon_scope_note": "precursor direct emissions (inside the certificate)",
        "verdict": verdict, "rationale": rationale,
        "provenance": [delta["certificate_price_provenance"]],
    }


def _process_energy_lever(activity: dict) -> dict:
    agg = activity["aggregated"]
    tonnes = sum(p["tonnes"]["value"] for p in agg["production"]) or 1.0
    kwh_per_t = agg["electricity_mwh"]["value"] * 1000.0 / tonnes
    return {
        "id": "process_energy", "title": "Benchmark heat-treatment / plating energy",
        "title_zh": "熱處理／電鍍能耗對標",
        "kwh_per_tonne": round(kwh_per_t, 1),
        "ntd_per_yr": None, "tco2e_per_yr": None,
        "carbon_scope_note": "electricity (indirect) — recorded in the template but NOT "
                             "in the CN 7318 certificate obligation",
        "verdict": "insufficient_data",
        "rationale": (f"your {kwh_per_t:,.0f} kWh/t needs a real peer distribution to "
                      f"call an outlier — {SEED_PROVENANCE}"),
        "provenance": [SEED_PROVENANCE],
    }


def _load_shift_lever(schedule: dict | None) -> dict:
    base = {
        "id": "load_shifting", "title": "Shift flexible loads to cheap/clean hours",
        "title_zh": "彈性負載移峰",
        "carbon_scope_note": "electricity (indirect) — reduces the power bill and the "
                             "recorded indirect line, NOT the CN 7318 certificate",
    }
    if schedule is None:
        return {**base, "ntd_per_yr": None, "tco2e_per_yr": None,
                "verdict": "insufficient_data",
                "rationale": "no schedule available (grid feed offline?) — run "
                             "`carbonpass schedule <firm_dir>`",
                "provenance": []}
    led = schedule["ledger"]
    ntd = led["delta_year_est"]["cost_ntd"]
    tco2e = led["delta_year_est"]["emissions_tco2e"]
    if ntd >= NTD_MATERIALITY_PER_YR:
        verdict, rationale = "worth_it", \
            "real money at current TOU rates — but ranked last: smallest carbon lever " \
            "on this firm's own numbers (the tool says so itself)"
    else:
        verdict, rationale = "not_worth_it_this_year", \
            f"NT${ntd:,.0f}/yr at current tariffs is below materiality for the " \
            f"disruption — revisit if TOU spreads widen (next review ~Oct 2026)"
    return {**base, "ntd_per_yr": ntd, "tco2e_per_yr": tco2e,
            "verdict": verdict, "rationale": rationale,
            "provenance": [schedule["tariff"]["source"],
                           schedule["grid_intensity"]["anchor_source"]]}


def fixlist(activity_path: str | Path, firm_dir: str | Path,
            schedule: dict | None = None) -> dict:
    """Build the ranked fix-list for one firm from the existing three sights."""
    activity = load_activity(activity_path)
    waste = waste_scan(str(activity_path), str(firm_dir))
    waste["drift"] = monthly_series(str(firm_dir), activity)
    delta = cost_delta(activity)

    levers = [
        _yield_lever(waste),
        _epd_lever(delta),
        _process_energy_lever(activity),
        _load_shift_lever(schedule),
    ]
    for rank, lv in enumerate(levers, 1):
        lv["rank"] = rank
    drift_alerts = [a for line in waste["drift"]["lines"] for a in line["alerts"]]
    return {
        "firm": activity["installation"].get("name_en"),
        "period_year": activity["period"]["year"],
        "levers": levers,
        "drift_alerts": drift_alerts,
        "ranking_note": "fixed measured order: yield → mill EPD → process energy → "
                        "load shifting (docs/18 §4) — on the synthetic firm the yield "
                        "lever moved 80× the scheduler",
        "heuristics_note": HEURISTICS_NOTE,
        "disclaimer": "Prepared for verification — nothing here is certified. "
                      "A 'not worth it this year' verdict is a supported answer.",
    }


VERDICT_ICON = {"worth_it": "✅", "not_worth_it_this_year": "⏸", "insufficient_data": "❔"}


def render_fixlist(fl: dict) -> str:
    L = [f"─── Fix-list — {fl['firm']} ({fl['period_year']}) ───"]
    for lv in fl["levers"]:
        icon = VERDICT_ICON[lv["verdict"]]
        head = f"  {lv['rank']}. {icon} {lv['title']}"
        nums = []
        if lv.get("ntd_per_yr"):
            nums.append(f"NT${lv['ntd_per_yr']:,.0f}/yr")
        if lv.get("tco2e_per_yr"):
            nums.append(f"{lv['tco2e_per_yr']:,.0f} tCO2e/yr")
        if lv.get("buyer_eur_per_t") is not None:
            nums.append(f"buyer €{lv['buyer_eur_per_t']:,.2f}/t")
        if nums:
            head += "  [" + " · ".join(nums) + "]"
        L.append(head)
        L.append(f"       {lv['rationale']}")
        L.append(f"       scope: {lv['carbon_scope_note']}")
    for a in fl["drift_alerts"]:
        L.append(f"  {a['message_zh']}")
    L += [f"  ({fl['heuristics_note']})", f"  {fl['disclaimer']}"]
    return "\n".join(L)


def render_fixlist_zh(fl: dict) -> str:
    verdict_zh = {"worth_it": "✅ 值得做", "not_worth_it_this_year": "⏸ 今年先不用",
                  "insufficient_data": "❔ 資料不足"}
    L = [f"🔧 改善清單（{fl['period_year']} 年，依實測影響排序）"]
    for lv in fl["levers"]:
        line = f"{lv['rank']}. {lv['title_zh']}：{verdict_zh[lv['verdict']]}"
        if lv.get("ntd_per_yr"):
            line += f"，約 NT${lv['ntd_per_yr']:,.0f}/年"
        if lv.get("buyer_eur_per_t") is not None:
            line += f"，買家端 €{lv['buyer_eur_per_t']:,.2f}/噸"
        L.append(line)
    if any(lv["verdict"] == "not_worth_it_this_year" for lv in fl["levers"]):
        L.append("（「今年先不用」也是答案——工具能說「不用做」才可信。）")
    for a in fl["drift_alerts"]:
        L.append(a["message_zh"])
    L.append("註：用電相關屬間接排放，記錄於範本但不計入 CN 7318 憑證金額。")
    return "\n".join(L)


def run_fixlist_cli(activity_json: str, firm_dir: str | None) -> int:
    firm_dir = firm_dir or str(
        Path("data/mock_corpus") / Path(activity_json).stem.replace("_activity", "")
        .replace("_novlm", ""))
    schedule = None
    sched_path = Path("out") / f"{Path(firm_dir).name}_schedule.json"
    if sched_path.exists():
        schedule = json.loads(sched_path.read_text(encoding="utf-8"))
    fl = fixlist(activity_json, firm_dir, schedule)
    print(render_fixlist(fl))
    out = Path("out") / f"{Path(activity_json).stem.replace('_activity', '')}_fixlist.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(fl, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nJSON -> {out}")
    return 0
