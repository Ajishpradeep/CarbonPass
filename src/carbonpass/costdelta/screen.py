"""Buyer cost-delta screen: what the EU importer pays WITH vs WITHOUT your data.

The killer demo number (docs/09 §5.2): "with your data your buyer surrenders
≈€150/t; without it €450-750/t and rising."

Certificate scope for CN 7318 (iron & steel) = DIRECT embedded emissions only —
indirect is recorded in the template but not certificated (G7). Both sides of
the comparison therefore use direct SEE:
    actual : SEE_direct(engine)              × certificate price
    default: default value (with year mark-up) × certificate price
"""
from __future__ import annotations

import json
from pathlib import Path

from carbonpass.config import CERTIFICATE_PRICE_EUR, markup_for_year
from carbonpass.pack import load_activity, run_allocation, run_rules
from carbonpass.rules import defaults


def latest_certificate_price() -> tuple[str, float]:
    quarter = sorted(CERTIFICATE_PRICE_EUR)[-1]
    return quarter, CERTIFICATE_PRICE_EUR[quarter]


def cost_delta(activity: dict) -> dict:
    alloc = run_allocation(activity)
    results = run_rules(activity, alloc)
    period_year = activity["period"].get("year") or int(activity["period"]["start"][:4])
    quarter, price = latest_certificate_price()
    country = "Taiwan" if activity["installation"]["country"] in ("Taiwan", "TW") else \
        activity["installation"]["country"]

    prod_by_name = {p["process_name"]: p for p in activity["aggregated"]["production"]}
    products = []
    for r in results:
        dv = defaults.lookup(r.cn_code, country)
        default_see = dv.for_year(period_year) if dv else None
        tonnes = prod_by_name[r.product_name]["tonnes"]["value"]
        actual_cost_t = r.see_direct.value * price
        default_cost_t = default_see * price if default_see else None
        products.append({
            "product_name": r.product_name,
            "cn_code": r.cn_code,
            "period_year": period_year,
            "annual_production_t": tonnes,
            "see_direct_actual": round(r.see_direct.value, 6),
            "see_direct_uncertainty_rel": round(r.see_direct.uncertainty_rel, 4),
            "default_value_marked_up": default_see,
            "markup": markup_for_year(period_year),
            "certificate_price_eur": price,
            "certificate_quarter": quarter,
            "buyer_cost_actual_eur_per_t": round(actual_cost_t, 2),
            "buyer_cost_default_eur_per_t": round(default_cost_t, 2) if default_cost_t else None,
            "delta_eur_per_t": round(default_cost_t - actual_cost_t, 2) if default_cost_t else None,
            "delta_eur_per_year_at_full_volume": (
                round((default_cost_t - actual_cost_t) * tonnes, 0) if default_cost_t else None),
            "note_indirect": "indirect SEE recorded in the template but NOT certificated for CN 7318",
        })
    return {"products": products,
            "disclaimer": "Prepared for verification — figures are not certified. "
                          "Default comparison uses IR 2025/2621 values incl. the period mark-up."}


def render_text(delta: dict) -> str:
    lines = []
    for p in delta["products"]:
        lines += [
            f"─── {p['product_name']} (CN {p['cn_code']}, {p['period_year']}) ───",
            f"  your verified SEE (direct):    {p['see_direct_actual']:.3f} tCO2e/t  "
            f"(±{p['see_direct_uncertainty_rel']:.1%})",
            f"  WITH your data   → buyer pays  €{p['buyer_cost_actual_eur_per_t']:>8,.2f} /t",
        ]
        if p["buyer_cost_default_eur_per_t"]:
            lines += [
                f"  WITHOUT it (default +{p['markup']:.0%})   €{p['buyer_cost_default_eur_per_t']:>8,.2f} /t",
                f"  YOUR DATA IS WORTH             €{p['delta_eur_per_t']:>8,.2f} /t  "
                f"≈ €{p['delta_eur_per_year_at_full_volume']:>10,.0f} /yr at {p['annual_production_t']:,.0f} t",
            ]
        lines.append(f"  (certificate price {p['certificate_quarter']}: €{p['certificate_price_eur']}/tCO2e)")
    lines.append(delta["disclaimer"])
    return "\n".join(lines)


def run_costdelta_cli(activity_json: str) -> int:
    activity = load_activity(activity_json)
    delta = cost_delta(activity)
    print(render_text(delta))
    out = Path("out") / f"{Path(activity_json).stem.replace('_activity', '')}_costdelta.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(delta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nJSON -> {out}")
    return 0
