"""Waste scan — the carbon a factory buys and throws away, from documents it already has.

The premise (docs/16): a fastener plant buys ~1.10 t of steel per 1 t of product. The
other ~0.10 t leaves as scrap, carrying the wire rod's full embedded emissions with it.
Nobody measures it, because measuring it means reconciling a year of steel e-invoices
against a production log — an ERP job, and a 12-person shop has a spreadsheet.

Everything here comes from data the pipeline ALREADY extracts:
  * steel in  -> MIG 4.0 e-invoice XML (mass AND unit price)
  * product out -> production log
so the screen is a by-product of the same photograph that files the CBAM pack.

The arithmetic that matters is exact and needs no allocation model:

    SEE_direct = own/AL + ratio x SEE_precursor        where ratio = consumed_t / produced_t
    => dSEE     = d(ratio) x SEE_precursor

i.e. yield improvement moves SEE 1:1 through the precursor term. Under CBAM the precursor
mass counted is the mass ENTERING the process, before cutting (Commission Q&A p.32 §4.11) —
so the scrap is in your number whether you look at it or not.

Run:  uv run python scripts/waste_scan.py out/firm_a_activity.json data/mock_corpus/firm_a
Out:  out/waste/<firm>_waste.json + printed summary
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

from carbonpass.egui.parser import categorize_item, parse_mig_invoice
from carbonpass.prices import certificate_price
from carbonpass.ingestion.pipeline import _is_stainless, _precursor_cn
from carbonpass.rules import defaults

TARGET_LOSS = 0.05      # what a well-run shop achieves; the scenario, not a promise


def is_stainless(name: str, grade: str) -> bool:
    return _is_stainless(f"{name} {grade}")


def correct_precursor_cn(name: str, grade: str) -> str:
    """Single source of truth is the pipeline's own mapping (CN 7213 / CN 7221).

    This used to re-derive the CN here because the pipeline's mapping was wrong
    (stainless -> 7227). That is fixed, so we defer to it and keep the mismatch check
    below purely as a guard against regression.
    """
    return _precursor_cn(f"{name} {grade}")


def unit_prices_ntd_per_t(firm_dir: str) -> dict[str, float]:
    """NT$/t per invoice description, straight from the e-invoices (no assumptions)."""
    out: dict[str, list[float]] = {}
    for path in sorted(glob.glob(f"{firm_dir}/invoices/*.xml")) + sorted(glob.glob(f"{firm_dir}/*.xml")):
        try:
            inv = parse_mig_invoice(path)
        except Exception:
            continue
        for item in inv["items"]:
            if categorize_item(item) != "steel":
                continue
            up, qty = item.get("unit_price"), item.get("quantity")
            if not up or not qty:
                continue
            # e-invoices are priced per kg; mass in the pipeline is tonnes
            out.setdefault(item["description"], []).append(up * 1000.0)
    return {k: sum(v) / len(v) for k, v in out.items()}


def scan(activity_path: str, firm_dir: str) -> dict:
    act = json.load(open(activity_path, encoding="utf-8"))
    year = act["period"].get("year") or int(act["period"]["start"][:4])
    country = act["installation"].get("country", "Taiwan")
    if country in ("TW",):
        country = "Taiwan"
    cert = certificate_price()
    quarter, price_eur = cert.quarter, cert.eur_per_tco2e
    prices = unit_prices_ntd_per_t(firm_dir)

    produced = {p["process_name"]: p["tonnes"]["value"] for p in act["aggregated"]["production"]}

    lines, warnings = [], []
    for si in act["aggregated"]["steel_inputs"]:
        name, grade = si["name"], si.get("grade", "")
        cn_right = correct_precursor_cn(name, grade)
        cn_used = (si.get("cn_code_precursor") or "").replace(" ", "")
        # resolve() applies the Annex I country fallback (Q&A p.37) — load-bearing here:
        # Taiwan has NO CN 7221 value, so every stainless line lands on 'Other countries'.
        dv, used_fallback = defaults.resolve(cn_right, country)
        if dv is None or dv.direct is None:
            warnings.append(f"no default for CN {cn_right} ({country}) — {name} skipped")
            continue
        if used_fallback:
            warnings.append(
                f"{name!r}: {country} has NO default for CN {cn_right} — Annex I fallback "
                f"applies ({dv.direct} = the average of the ten highest-intensity exporters, "
                f"Q&A p.37). Only Taiwan, Thailand and Vietnam have this hole.")
        # Row-derived mark-up on the DIRECT figure (docs/15 §6 defects 1–2). For steel
        # direct == total (indirect N/A) so this equals the workbook's marked-up column.
        prec_see = dv.for_year_direct(year)

        if cn_used and cn_used != cn_right:
            wrong = defaults.lookup(cn_used, country)
            if wrong and wrong.direct is not None:
                warnings.append(
                    f"PRECURSOR CN MISMATCH for {name!r}: pipeline used CN {cn_used} "
                    f"({wrong.direct:.3f} tCO2e/t) but the grade is CN {cn_right} "
                    f"({dv.direct:.3f}) -> understated {dv.direct / wrong.direct:.2f}x")

        ntd_per_t = next((v for k, v in prices.items() if k == grade), None)
        if ntd_per_t is None:
            ntd_per_t = next((v for k, v in prices.items() if name.lower()[:12] in k.lower()), None)

        for product, consumed_t in si["consumption_t"]["consumed_t"].items():
            out_t = produced.get(product)
            if not out_t:
                continue
            scrap_t = consumed_t - out_t
            ratio_now = consumed_t / out_t
            ratio_target = 1.0 / (1.0 - TARGET_LOSS)
            d_see = max(0.0, ratio_now - ratio_target) * prec_see
            steel_saved_t = max(0.0, ratio_now - ratio_target) * out_t
            lines.append({
                "product": product,
                "precursor": name,
                "precursor_cn_correct": cn_right,
                "precursor_cn_pipeline": cn_used or None,
                "precursor_see_marked_up": round(prec_see, 6),
                "stainless": is_stainless(name, grade),
                "consumed_t": consumed_t,
                "produced_t": out_t,
                "scrap_t": round(scrap_t, 2),
                "loss_pct": round(scrap_t / consumed_t * 100, 2),
                "ratio_t_per_t": round(ratio_now, 4),
                "ntd_per_t": ntd_per_t,
                "wasted_tco2e_per_yr": round(scrap_t * prec_see, 1),
                "wasted_ntd_per_yr": round(scrap_t * ntd_per_t, 0) if ntd_per_t else None,
                "scenario_target_loss_pct": TARGET_LOSS * 100,
                "see_reduction_tco2e_per_t": round(d_see, 4),
                "buyer_saving_eur_per_t": round(d_see * price_eur, 2),
                "buyer_saving_eur_per_yr": round(d_see * price_eur * out_t, 0),
                "steel_not_bought_t_per_yr": round(steel_saved_t, 1),
                "co2e_avoided_tco2e_per_yr": round(steel_saved_t * prec_see, 1),
                "ntd_saved_per_yr": round(steel_saved_t * ntd_per_t, 0) if ntd_per_t else None,
            })

    return {
        "installation": act["installation"].get("name_en") or act["installation"].get("name_zh"),
        "period_year": year,
        "certificate_quarter": quarter,
        "certificate_price_eur": price_eur,
        "certificate_price_provenance": cert.provenance,
        "lines": lines,
        "totals": {
            "wasted_tco2e_per_yr": round(sum(l["wasted_tco2e_per_yr"] for l in lines), 1),
            "wasted_ntd_per_yr": round(sum(l["wasted_ntd_per_yr"] or 0 for l in lines), 0),
            "co2e_avoided_tco2e_per_yr": round(sum(l["co2e_avoided_tco2e_per_yr"] for l in lines), 1),
            "ntd_saved_per_yr": round(sum(l["ntd_saved_per_yr"] or 0 for l in lines), 0),
        },
        "warnings": warnings,
        "method_note": "Precursor mass counted is the mass entering the process before cutting "
                       "(Commission Q&A p.32 §4.11), so scrap is inside the declared SEE. "
                       "Scrap is resold and remelted: the SEE effect is exact and 1:1, the "
                       "atmospheric effect is real but smaller than the gross figure — "
                       "remelting recovers the iron, not the energy already spent making the rod.",
    }


def render(r: dict) -> str:
    L = [f"─── What you bought and threw away — {r['installation']} ({r['period_year']}) ───", ""]
    for l in r["lines"]:
        tag = " ⚠ STAINLESS" if l["stainless"] else ""
        L += [f"  {l['product']}{tag}",
              f"    steel in {l['consumed_t']:>8,.0f} t → product out {l['produced_t']:>8,.0f} t"
              f"   → scrap {l['scrap_t']:>6,.0f} t  ({l['loss_pct']:.1f}%)",
              f"    that scrap carries {l['wasted_tco2e_per_yr']:>8,.0f} tCO2e/yr"
              + (f"  and cost you NT${l['wasted_ntd_per_yr']:>12,.0f}/yr" if l["wasted_ntd_per_yr"] else ""),
              f"    → at {l['scenario_target_loss_pct']:.0f}% loss: SEE −{l['see_reduction_tco2e_per_t']:.3f} tCO2e/t "
              f"(buyer −€{l['buyer_saving_eur_per_t']:,.2f}/t = −€{l['buyer_saving_eur_per_yr']:,.0f}/yr), "
              f"{l['steel_not_bought_t_per_yr']:,.0f} t steel never bought,",
              f"      {l['co2e_avoided_tco2e_per_yr']:,.0f} tCO2e/yr avoided"
              + (f", NT${l['ntd_saved_per_yr']:,.0f}/yr saved" if l["ntd_saved_per_yr"] else ""), ""]
    t = r["totals"]
    L += [f"  TOTAL thrown away : {t['wasted_tco2e_per_yr']:,.0f} tCO2e/yr"
          + (f" · NT${t['wasted_ntd_per_yr']:,.0f}/yr" if t["wasted_ntd_per_yr"] else ""),
          f"  TOTAL recoverable : {t['co2e_avoided_tco2e_per_yr']:,.0f} tCO2e/yr"
          + (f" · NT${t['ntd_saved_per_yr']:,.0f}/yr" if t["ntd_saved_per_yr"] else ""), ""]
    for w in r["warnings"]:
        L.append(f"  ⚠ {w}")
    L += ["", f"  {r['method_note']}"]
    return "\n".join(L)


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print(__doc__)
        return 2
    r = scan(argv[1], argv[2])
    print(render(r))
    out = Path("out/waste") / f"{Path(argv[1]).stem.replace('_activity', '')}_waste.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nJSON -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
