"""Before/after ledger + CLI entry for Module 2.

Output framing is G7-honest by construction (docs/10 §2A): shifting load reduces
the POWER BILL and the indirect-emissions line of the template / the buyer's
Scope-3 figures. It does NOT reduce the CN 7318 CBAM certificate today (only
cement & fertiliser include indirect emissions in the certificate). The ledger
is structured to ISO 14064-2 baseline-and-monitoring LOGIC; certification
remains the act of an accredited verifier.
"""
from __future__ import annotations

import json
from pathlib import Path

from carbonpass.scheduler import grid, tariffs
from carbonpass.scheduler.loads import loads_from_machines
from carbonpass.scheduler.milp import optimize_week

WEEKS_PER_YEAR = 50


def schedule_firm(firm_dir: str | Path, month: int = 7) -> dict:
    firm_dir = Path(firm_dir)
    onboarding = json.loads((firm_dir / "firm.json").read_text(encoding="utf-8"))
    machines = onboarding.get("machines", [])
    capacity = float(onboarding["identity"].get("contract_capacity_kw", 500))

    loads = loads_from_machines(machines)
    curve = grid.hourly_curve(168)
    price = tariffs.price_curve(168, month=month)
    result = optimize_week(loads, price, curve["hourly_kgco2_per_kwh"], capacity)

    ntd_week = result.baseline_cost_ntd - result.optimized_cost_ntd
    co2_week = result.baseline_co2_kg - result.optimized_co2_kg
    return {
        "firm": onboarding["identity"].get("name_en", firm_dir.name),
        "horizon": "one week, hourly (Mon 00:00 anchor)",
        "grid_intensity": {k: curve[k] for k in
                           ("anchor_kgco2_per_kwh", "anchor_source", "anchor_ts",
                            "sanity_vs_official_annual", "note")},
        "tariff": {"month": month, "season": tariffs.season_of_month(month),
                   "rates_ntd_per_kwh": tariffs.RATES[tariffs.season_of_month(month)],
                   "source": "Taipower rate table (re-verify current schedule pre-submission)"},
        "loads": [{"name": ld.name, "kw": ld.kw, "weekly_kwh": round(ld.weekly_kwh, 1),
                   "flexible": ld.flexible} for ld in loads],
        "shift_plan": {
            "per_load_kwh_by_hour": result.per_load_kwh,
            "site_kw_baseline": result.baseline_kw,
            "site_kw_optimized": result.optimized_kw,
        },
        "ledger": {
            "structure": "ISO 14064-2 baseline-and-monitoring logic (structured-to, not certified)",
            "baseline_week": {"cost_ntd": result.baseline_cost_ntd,
                              "emissions_kgco2e": result.baseline_co2_kg},
            "optimized_week": {"cost_ntd": result.optimized_cost_ntd,
                               "emissions_kgco2e": result.optimized_co2_kg},
            "delta_week": {"cost_ntd": round(ntd_week, 0), "emissions_kgco2e": round(co2_week, 1)},
            "delta_year_est": {"cost_ntd": round(ntd_week * WEEKS_PER_YEAR, 0),
                               "emissions_tco2e": round(co2_week * WEEKS_PER_YEAR / 1000, 2)},
        },
        "honesty": [
            "Reduces the electricity bill and the indirect-emissions line (template record / "
            "buyer Scope-3). Does NOT reduce the CN 7318 CBAM certificate today — indirect "
            "emissions are certificate-relevant only for cement and fertiliser (docs/10 G7).",
            "Baseline = flat operation Mon-Sat 06:00-22:00; refine with 15-min AMI data at pilot.",
            "Nothing here is certified; verification is the accredited verifier's act.",
        ],
        "solver_notes": result.notes,
    }


def run_schedule_cli(firm_dir: str, output: str | None, month: int = 7) -> int:
    res = schedule_firm(firm_dir, month=month)
    out = Path(output) if output else Path("out") / f"{Path(firm_dir).name}_schedule.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
    led = res["ledger"]
    print(f"OK: shift plan -> {out}")
    print(f"  grid anchor: {res['grid_intensity']['anchor_kgco2_per_kwh']} kgCO2e/kWh "
          f"({res['grid_intensity']['anchor_source']})")
    print(f"  week: NT${led['baseline_week']['cost_ntd']:,.0f} -> NT${led['optimized_week']['cost_ntd']:,.0f} "
          f"(save NT${led['delta_week']['cost_ntd']:,.0f}); "
          f"CO2 {led['baseline_week']['emissions_kgco2e']:,.0f} -> {led['optimized_week']['emissions_kgco2e']:,.0f} kg")
    print(f"  year est.: save NT${led['delta_year_est']['cost_ntd']:,.0f} + "
          f"{led['delta_year_est']['emissions_tco2e']} tCO2e (Scope-3/indirect line, not the CBAM certificate)")
    return 0
