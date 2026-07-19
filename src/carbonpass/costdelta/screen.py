"""Buyer cost-delta screen: what the EU importer pays WITH vs WITHOUT your data.

Honest magnitude (docs/FACTS.md): Taiwan's default for CN 7318 is mild — data is worth
~€4/t to a carbon-steel maker, and we say so first. The delta is real money at
volume, not a catastrophe averted.

Certificate scope is sector-aware (config.indirect_in_certificate): for iron &
steel (CN 7318) only DIRECT embedded emissions are certificated — indirect is
recorded in the template but not charged (G7). Cement/fertiliser include
indirect. Both sides of the comparison use the same scope:
    actual : SEE_in_scope(engine)                 × certificate price
    default: default value (row-derived mark-up)  × certificate price
"""
from __future__ import annotations

import json
from pathlib import Path

from carbonpass.config import indirect_in_certificate
from carbonpass.pack import load_activity, run_allocation, run_rules
from carbonpass.prices import certificate_price
from carbonpass.rules import defaults


def cost_delta(activity: dict) -> dict:
    alloc = run_allocation(activity)
    results = run_rules(activity, alloc)
    period_year = activity["period"].get("year") or int(activity["period"]["start"][:4])
    cert = certificate_price()
    quarter, price = cert.quarter, cert.eur_per_tco2e
    country = "Taiwan" if activity["installation"]["country"] in ("Taiwan", "TW") else \
        activity["installation"]["country"]

    prod_by_name = {p["process_name"]: p for p in activity["aggregated"]["production"]}
    products = []
    for r in results:
        dv = defaults.lookup(r.cn_code, country)
        in_scope_indirect = indirect_in_certificate(r.cn_code)
        default_see = None
        if dv:
            default_see = (dv.for_year(period_year) if in_scope_indirect
                           else dv.for_year_direct(period_year))
        see_actual_in_scope = r.see_direct.value + (
            r.see_indirect.value if in_scope_indirect else 0.0)
        tonnes = prod_by_name[r.product_name]["tonnes"]["value"]
        actual_cost_t = see_actual_in_scope * price
        default_cost_t = default_see * price if default_see else None
        products.append({
            "product_name": r.product_name,
            "cn_code": r.cn_code,
            "period_year": period_year,
            "annual_production_t": tonnes,
            "see_direct_actual": round(r.see_direct.value, 6),
            "see_direct_uncertainty_rel": round(r.see_direct.uncertainty_rel, 4),
            "indirect_in_certificate": in_scope_indirect,
            "see_in_certificate_scope": round(see_actual_in_scope, 6),
            "default_value_marked_up": default_see,
            "markup": dv.derived_markup(period_year) if dv else None,
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
            "certificate_price_provenance": cert.provenance,
            "disclaimer": "Prepared for verification — figures are not certified. "
                          "Default comparison uses IR 2025/2621 values incl. the period's "
                          "row-derived mark-up."}


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
