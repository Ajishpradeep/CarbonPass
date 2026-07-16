"""Orchestration: activity_data JSON -> allocation -> SEE results.

Shared by the writer (template fill), the cost-delta screen and future API/LINE
surfaces. One call = one determination period = one installation.
"""
from __future__ import annotations

import json
from pathlib import Path

from carbonpass.allocation.engine import (AllocationInput, AllocationResult,
                                          MachineSpec, ProcessSpec, allocate)
from carbonpass.config import GRID_EF_KGCO2_PER_KWH
from carbonpass.rules.see import (PrecursorInput, ProcessInput, ProductSEE,
                                  compute_installation)


def load_activity(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def fuel_emissions_tco2e(aggregated: dict) -> tuple[float, float]:
    """Installation-level direct emissions from fuel source streams (+ rel unc)."""
    total, var = 0.0, 0.0
    for f in aggregated.get("fuels", []):
        amount = f["amount"]["value"]
        tj = amount * f["ncv_gj_per_unit"] / 1000.0
        co2 = tj * f["ef_tco2_per_tj"]
        total += co2
        var += (co2 * f["amount"].get("uncertainty_rel", 0.0)) ** 2
    return total, (var ** 0.5 / total if total else 0.0)


def run_allocation(activity: dict) -> AllocationResult:
    agg = activity["aggregated"]
    fuel_co2, fuel_unc = fuel_emissions_tco2e(agg)
    processes = [
        ProcessSpec(name=p["process_name"], production_t=p["tonnes"]["value"],
                    production_unc_rel=p["tonnes"].get("uncertainty_rel", 0.01))
        for p in agg["production"]
    ]
    machines = [
        MachineSpec(name=m["name"], kw=m["kw"], hours=m["hours"],
                    process=m.get("process", "shared"))
        for m in agg.get("machines", [])
    ]
    return allocate(AllocationInput(
        processes=processes,
        machines=machines,
        fuel_co2e_t=fuel_co2,
        fuel_unc_rel=fuel_unc,
        electricity_mwh=agg["electricity_mwh"]["value"],
        electricity_unc_rel=agg["electricity_mwh"].get("uncertainty_rel", 0.0),
    ))


def run_rules(activity: dict, alloc: AllocationResult) -> list[ProductSEE]:
    agg = activity["aggregated"]
    period_year = activity["period"].get("year") or int(activity["period"]["start"][:4])
    alloc_by_name = {a.name: a for a in alloc.processes}

    # Distribute purchased steel to processes: explicit onboarding consumption if
    # present, else all mass to the (single) matching process.
    process_inputs = []
    for p in agg["production"]:
        name = p["process_name"]
        a = alloc_by_name[name]
        precursors = []
        for s in agg.get("steel_inputs", []):
            consumed = None
            if s.get("consumption_t"):
                consumed = s["consumption_t"]["consumed_t"].get(name)
            elif len(agg["production"]) == 1:
                consumed = s["mass_t"]["value"]
            if not consumed:
                continue
            epd = s.get("epd")
            precursors.append(PrecursorInput(
                name=s["name"],
                mass_t=float(consumed),
                mass_unc_rel=s["mass_t"].get("uncertainty_rel", 0.005),
                cn_code=s.get("cn_code_precursor", ""),
                country="Taiwan" if s.get("country") in ("TW", "Taiwan") else s.get("country", "Taiwan"),
                see_direct=epd["see_direct"] if epd else None,
                spec_electricity_mwh_per_t=epd.get("spec_electricity_mwh_per_t", 0.0) if epd else 0.0,
                electricity_ef=epd.get("electricity_ef", 0.0) if epd else 0.0,
                epd_document=epd.get("document", "") if epd else "",
            ))
        process_inputs.append(ProcessInput(
            name=name,
            cn_code=p["cn_code"],
            invoice_name=p.get("invoice_name", ""),
            production_t=p["tonnes"]["value"],
            production_unc_rel=p["tonnes"].get("uncertainty_rel", 0.01),
            direct_emissions_tco2e=a.direct_emissions_tco2e,
            direct_unc_rel=a.direct_unc_rel,
            electricity_mwh=a.electricity_mwh,
            electricity_unc_rel=a.electricity_unc_rel,
            electricity_ef=GRID_EF_KGCO2_PER_KWH,   # tCO2/MWh == kg/kWh
            electricity_ef_source="D.4(b)",
            precursors=precursors,
        ))
    return compute_installation(process_inputs, period_year)
