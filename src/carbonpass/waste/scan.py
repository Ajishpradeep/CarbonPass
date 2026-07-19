"""Per-line waste scan: steel in vs product out, carbon and money, gross AND net.

Everything comes from documents the pipeline already extracts: steel e-invoices
(mass AND unit price) + production log. The screen is a by-product of the same
photograph that files the CBAM pack.

The arithmetic that matters is exact and needs no allocation model:

    SEE_direct = own/AL + ratio × SEE_precursor,  ratio = consumed_t / produced_t
    ⇒ ΔSEE     = Δ(ratio) × SEE_precursor

Yield improvement moves the declared SEE 1:1 through the precursor term. Legal
basis (verified in the law, docs/15 §8.1 Gate A): IR 2025/2547 Annex III §F —
activity level = mass of goods LEAVING the process; scrap is excluded from it,
so the scrap's embodied emissions sit inside the declared SEE whether the owner
looks or not.

Wording discipline (docs/20 §6): scrap is SOLD, not thrown away — the gap is
information, not diligence. Gross embodied carbon is "purchased but never
ships", never "avoided". Money is a MoneyLoss: gross and net travel together.
"""
from __future__ import annotations

import glob
import json

from carbonpass.egui.parser import categorize_item, parse_mig_invoice
from carbonpass.ingestion.pipeline import _is_stainless, _precursor_cn
from carbonpass.prices import certificate_price
from carbonpass.rules import defaults
from carbonpass.waste.money import MoneyLoss

TARGET_LOSS = 0.05      # what a well-run shop achieves; the scenario, not a promise

METHOD_NOTE = (
    "Precursor mass counted is the mass entering the process before cutting "
    "(IR 2025/2547 Annex III §F: scrap is excluded from the activity level, so its "
    "embodied emissions stay inside the declared SEE; also Commission Q&A §4.11). "
    "Scrap is resold and remelted: the SEE effect is exact and 1:1; the atmospheric "
    "effect is real but smaller than the gross figure — remelting recovers the iron, "
    "not the energy already spent making the rod. Gross embodied carbon is 'purchased "
    "but never ships', never 'avoided'.")


def is_stainless(name: str, grade: str) -> bool:
    return _is_stainless(f"{name} {grade}")


def correct_precursor_cn(name: str, grade: str) -> str:
    """Single source of truth is the pipeline's own mapping (CN 7213 / CN 7221)."""
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


def scan(activity_path: str, firm_dir: str,
         data_provenance: str = "synthetic corpus (documented 5–15% band) — "
                                "the pilot measurement replaces these rates") -> dict:
    act = json.load(open(activity_path, encoding="utf-8"))
    year = act["period"].get("year") or int(act["period"]["start"][:4])
    country = act["installation"].get("country", "Taiwan")
    if country in ("TW",):
        country = "Taiwan"
    cert = certificate_price()
    prices = unit_prices_ntd_per_t(firm_dir)

    produced = {p["process_name"]: p["tonnes"]["value"] for p in act["aggregated"]["production"]}

    lines, warnings = [], []
    money_total: MoneyLoss | None = None
    for si in act["aggregated"]["steel_inputs"]:
        name, grade = si["name"], si.get("grade", "")
        cn_right = correct_precursor_cn(name, grade)
        cn_used = (si.get("cn_code_precursor") or "").replace(" ", "")
        # resolve() applies the Annex I country fallback — load-bearing here: Taiwan
        # has NO CN 7221 value (legal-text verified, docs/15 §8.1 Gate B), so every
        # stainless line lands on 'Other countries and territories'.
        dv, used_fallback = defaults.resolve(cn_right, country)
        if dv is None or dv.direct is None:
            warnings.append(f"no default for CN {cn_right} ({country}) — {name} skipped")
            continue
        if used_fallback:
            warnings.append(
                f"{name!r}: {country} has NO default for CN {cn_right} — Annex I fallback "
                f"applies ({dv.direct} = the average of the ten highest-intensity exporters). "
                f"Only Taiwan, Thailand and Vietnam have this hole (confirmed in the OJ text).")
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

        kind = "stainless_304" if is_stainless(name, grade) else "carbon_steel"
        for product, consumed_t in si["consumption_t"]["consumed_t"].items():
            out_t = produced.get(product)
            if not out_t:
                continue
            scrap_t = consumed_t - out_t
            ratio_now = consumed_t / out_t
            ratio_target = 1.0 / (1.0 - TARGET_LOSS)
            d_see = max(0.0, ratio_now - ratio_target) * prec_see
            steel_saved_t = max(0.0, ratio_now - ratio_target) * out_t
            money = (MoneyLoss.from_purchase_value(scrap_t * ntd_per_t, kind)
                     if ntd_per_t else None)
            if money is not None:
                money_total = money if money_total is None else money_total + money
            lines.append({
                "product": product,
                "precursor": name,
                "precursor_cn": cn_right,
                "precursor_see_direct_marked_up": round(prec_see, 6),
                "stainless": kind == "stainless_304",
                "consumed_t": consumed_t,
                "produced_t": out_t,
                "scrap_t": round(scrap_t, 2),
                "loss_pct": round(scrap_t / consumed_t * 100, 2),
                "ratio_t_per_t": round(ratio_now, 4),
                "ntd_per_t": ntd_per_t,
                # gross embodied carbon of the scrapped mass — purchased, never ships
                "embodied_tco2e_per_yr_gross": round(scrap_t * prec_see, 1),
                "money_loss": money.as_dict() if money else None,
                # the 5%-scenario levers (scenario, not promise)
                "scenario_target_loss_pct": TARGET_LOSS * 100,
                "scenario_see_reduction_tco2e_per_t": round(d_see, 4),
                "scenario_buyer_saving_eur_per_t": round(d_see * cert.eur_per_tco2e, 2),
                "scenario_buyer_saving_eur_per_yr": round(d_see * cert.eur_per_tco2e * out_t, 0),
                "scenario_steel_not_bought_t_per_yr": round(steel_saved_t, 1),
                "scenario_embodied_reduction_tco2e_per_yr": round(steel_saved_t * prec_see, 1),
                "scenario_ntd_not_spent_per_yr": (round(steel_saved_t * ntd_per_t, 0)
                                                  if ntd_per_t else None),
            })

    return {
        "installation": act["installation"].get("name_en") or act["installation"].get("name_zh"),
        "period_year": year,
        "certificate_quarter": cert.quarter,
        "certificate_price_eur": cert.eur_per_tco2e,
        "certificate_price_provenance": cert.provenance,
        "lines": lines,
        "totals": {
            "embodied_tco2e_per_yr_gross": round(
                sum(l["embodied_tco2e_per_yr_gross"] for l in lines), 1),
            "money_loss": money_total.as_dict() if money_total else None,
            "scenario_embodied_reduction_tco2e_per_yr": round(
                sum(l["scenario_embodied_reduction_tco2e_per_yr"] for l in lines), 1),
            "scenario_ntd_not_spent_per_yr": round(
                sum(l["scenario_ntd_not_spent_per_yr"] or 0 for l in lines), 0),
        },
        "warnings": warnings,
        "method_note": METHOD_NOTE,
        "data_provenance": data_provenance,
    }


def render(r: dict) -> str:
    L = [f"─── Steel in vs product out — {r['installation']} ({r['period_year']}) ───", ""]
    for l in r["lines"]:
        tag = " ⚠ STAINLESS" if l["stainless"] else ""
        money = l["money_loss"]
        L += [f"  {l['product']}{tag}",
              f"    steel in {l['consumed_t']:>8,.0f} t → product out {l['produced_t']:>8,.0f} t"
              f"   → scrap {l['scrap_t']:>6,.0f} t  ({l['loss_pct']:.1f}%)",
              f"    carbon purchased that never ships: {l['embodied_tco2e_per_yr_gross']:>8,.0f} tCO2e/yr (gross embodied)"]
        if money:
            lo, hi = money["net_of_resale_ntd_range"]
            L.append(f"    money: NT${money['purchase_value_ntd']:,.0f} at purchase price "
                     f"/ NT${lo:,.0f}–{hi:,.0f} net of scrap resale")
        L += [f"    → at {l['scenario_target_loss_pct']:.0f}% loss (scenario): "
              f"SEE −{l['scenario_see_reduction_tco2e_per_t']:.3f} tCO2e/t "
              f"(buyer −€{l['scenario_buyer_saving_eur_per_t']:,.2f}/t = "
              f"−€{l['scenario_buyer_saving_eur_per_yr']:,.0f}/yr), "
              f"{l['scenario_steel_not_bought_t_per_yr']:,.0f} t steel never bought,",
              f"      {l['scenario_embodied_reduction_tco2e_per_yr']:,.0f} tCO2e/yr less embodied carbon purchased"
              + (f", NT${l['scenario_ntd_not_spent_per_yr']:,.0f}/yr not spent"
                 if l["scenario_ntd_not_spent_per_yr"] else ""), ""]
    t = r["totals"]
    L.append(f"  TOTAL gross embodied in scrap : {t['embodied_tco2e_per_yr_gross']:,.0f} tCO2e/yr")
    if t["money_loss"]:
        m = t["money_loss"]
        lo, hi = m["net_of_resale_ntd_range"]
        L.append(f"  TOTAL money : NT${m['purchase_value_ntd']:,.0f} gross "
                 f"/ NT${lo:,.0f}–{hi:,.0f} net of resale")
    L += [f"  TOTAL 5%-scenario : {t['scenario_embodied_reduction_tco2e_per_yr']:,.0f} tCO2e/yr "
          f"less purchased · NT${t['scenario_ntd_not_spent_per_yr']:,.0f}/yr not spent", ""]
    for w in r["warnings"]:
        L.append(f"  ⚠ {w}")
    L += ["", f"  {r['method_note']}", f"  Data: {r['data_provenance']}"]
    return "\n".join(L)
