"""Monthly loss drift from dated e-invoices + the production log.

Purpose: turn the annual blindness into a weekly control loop — "Line 2 loss
rose 7%→11% since March; check the die" (docs/21 §1.2). Steel arrives in lumpy
quarterly invoices, so point-in-time monthly ratios are meaningless; the series
uses a trailing window (default 3 months) so every point spans at least one
delivery.

Alert rule (tunable): the latest trailing-window loss exceeds the mean of the
prior points by more than `sigma` standard deviations AND by at least
`min_rise_pp` percentage points (guards against alerting on tiny σ).
"""
from __future__ import annotations

import glob
import json
from collections import defaultdict

from carbonpass.egui.parser import categorize_item, parse_mig_invoice
from carbonpass.ingestion.pipeline import _is_stainless


def _consumed_by_month(firm_dir: str) -> dict[str, dict[str, float]]:
    """Steel mass (t) per invoice description per 'YYYY-MM', from dated e-invoices."""
    out: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    for path in sorted(glob.glob(f"{firm_dir}/invoices/*.xml")):
        try:
            inv = parse_mig_invoice(path)
        except Exception:
            continue
        d = inv.get("date") or ""
        month = f"{d[:4]}-{d[4:6]}" if len(d) >= 6 else None
        if not month:
            continue
        for item in inv["items"]:
            if categorize_item(item) != "steel" or not item.get("quantity"):
                continue
            kg = item["quantity"] if item["unit"] in ("公斤", "kg", "KG") else item["quantity"] * 1000.0
            out[item["description"]][month] += kg / 1000.0
    return {k: dict(v) for k, v in out.items()}


def _produced_by_month(firm_dir: str) -> dict[str, dict[str, float]]:
    """Production tonnes per CN per 'YYYY-MM' from production_log.csv (+ firm.json year)."""
    fj = json.load(open(f"{firm_dir}/firm.json", encoding="utf-8"))
    year = fj["period_year"]
    out: dict[str, dict[str, float]] = defaultdict(dict)
    with open(f"{firm_dir}/production_log.csv", encoding="utf-8") as f:
        lines = f.read().strip().splitlines()
    header = lines[0].split(",")
    cn_cols = [(i, h.removeprefix("cn_").removesuffix("_t"))
               for i, h in enumerate(header) if h.startswith("cn_")]
    for line in lines[1:]:
        vals = line.split(",")
        month = f"{year}-{int(vals[0]):02d}"
        for i, cn in cn_cols:
            out[cn][month] = float(vals[i])
    return {k: dict(v) for k, v in out.items()}


def rolling_loss(consumed: dict[str, float], produced: dict[str, float],
                 window: int = 3) -> list[dict]:
    """Trailing-window loss series over the union of months (sorted 'YYYY-MM')."""
    months = sorted(set(consumed) | set(produced))
    series = []
    for i, m in enumerate(months):
        win = months[max(0, i - window + 1): i + 1]
        c = sum(consumed.get(x, 0.0) for x in win)
        p = sum(produced.get(x, 0.0) for x in win)
        if c <= 0 or p <= 0 or p > c:
            continue                      # no delivery in window / nonsense ratio
        series.append({"month": m, "window_months": len(win),
                       "consumed_t": round(c, 3), "produced_t": round(p, 3),
                       "loss_pct": round((1.0 - p / c) * 100.0, 2)})
    return series


def drift_alerts(series: list[dict], sigma: float = 2.0, min_points: int = 5,
                 min_rise_pp: float = 1.0) -> list[dict]:
    """Alert when the latest loss breaks above the prior mean + sigma·s.d. (and ≥1pp)."""
    if len(series) < min_points:
        return []
    prior = [s["loss_pct"] for s in series[:-1]]
    mean = sum(prior) / len(prior)
    var = sum((x - mean) ** 2 for x in prior) / max(1, len(prior) - 1)
    sd = var ** 0.5
    latest = series[-1]
    rise = latest["loss_pct"] - mean
    if rise > sigma * sd and rise >= min_rise_pp:
        return [{
            "month": latest["month"],
            "loss_pct": latest["loss_pct"],
            "baseline_pct": round(mean, 2),
            "rise_pp": round(rise, 2),
            "rule": f"trailing loss > baseline + {sigma}σ (σ={sd:.2f}pp) and ≥ {min_rise_pp}pp",
            "message_zh": (f"⚠️ 損耗率警示：{latest['month']} 為 {latest['loss_pct']:.1f}%，"
                           f"高於基準 {mean:.1f}%（+{rise:.1f} 個百分點）— 建議檢查模具與設定"),
        }]
    return []


def monthly_series(firm_dir: str, activity: dict, window: int = 3) -> dict:
    """Per-(precursor → product) drift series + alerts for a firm's document folder.

    The invoice mass of a grade is split across its consuming products by the
    owner-declared annual consumption shares (firm.json), the only split that
    exists at document level.
    """
    consumed = _consumed_by_month(firm_dir)
    produced = _produced_by_month(firm_dir)

    lines = []
    for si in activity["aggregated"]["steel_inputs"]:
        grade = si.get("grade", "")
        con_map = (si.get("consumption_t") or {}).get("consumed_t", {})
        total_consumed = sum(con_map.values()) or 1.0
        by_month = consumed.get(grade)
        if by_month is None:      # fuzzy: grade string inside a description
            by_month = next((v for k, v in consumed.items() if grade and grade in k), {})
        prod_cn = {p["process_name"]: p["cn_code"]
                   for p in activity["aggregated"]["production"]}
        for product, annual_t in con_map.items():
            share = annual_t / total_consumed
            cons_m = {m: v * share for m, v in by_month.items()}
            prod_m = produced.get(prod_cn.get(product, ""), {})
            series = rolling_loss(cons_m, prod_m, window=window)
            lines.append({
                "precursor": si["name"], "grade": grade, "product": product,
                "stainless": _is_stainless(f"{si['name']} {grade}"),
                "series": series,
                "alerts": drift_alerts(series),
            })
    return {"window_months": window, "lines": lines,
            "note": "trailing-window loss; every point spans ≥1 steel delivery. "
                    "Synthetic corpus is jitter around a flat rate — a real drift "
                    "(wearing die) shows as a broken baseline."}
