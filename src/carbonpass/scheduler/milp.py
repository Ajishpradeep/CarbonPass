"""OR-Tools MILP: shift flexible loads against TOU prices + hourly grid intensity.

Decision: kWh delivered per flexible load per hour over a one-week horizon.
Fixed loads keep the baseline. Constraints: weekly energy conservation per load,
per-load kW rating, operating window (Mon–Sat 06:00–22:00), contract-capacity
cap on total site kW. Objective: α·NT$(TOU) + β·kgCO2e(hourly grid intensity)
— cost-first by default (α=1, β=grid-weight so a tonne trades at ~NT$1,000).

Kept linear (GLOP) — no integrality needed at hourly resolution for the PoC;
CP-SAT with min-run-blocks is the pilot refinement.
"""
from __future__ import annotations

from dataclasses import dataclass

from ortools.linear_solver import pywraplp

from carbonpass.scheduler.loads import Load, baseline_profile


@dataclass
class ScheduleResult:
    hours: int
    baseline_kw: list[float]
    optimized_kw: list[float]
    per_load_kwh: dict[str, list[float]]
    baseline_cost_ntd: float
    optimized_cost_ntd: float
    baseline_co2_kg: float
    optimized_co2_kg: float
    notes: list[str]


def optimize_week(loads: list[Load], price: list[float], intensity: list[float],
                  contract_capacity_kw: float,
                  alpha_cost: float = 1.0, beta_co2_ntd_per_kg: float = 1.0) -> ScheduleResult:
    hours = len(price)
    assert len(intensity) == hours

    flexible = [ld for ld in loads if ld.flexible]
    fixed = [ld for ld in loads if not ld.flexible]
    fixed_profile = baseline_profile(fixed, hours)
    base_profile = baseline_profile(loads, hours)

    def allowed(ld: Load, h: int) -> bool:
        dow, hod = divmod(h % 168, 24)
        if ld.weekdays_only_plus_sat and dow >= 6:
            return False
        lo, hi = ld.window
        return lo <= hod < hi

    solver = pywraplp.Solver.CreateSolver("GLOP")
    x = {}  # kWh of load ld in hour h
    for ld in flexible:
        for h in range(hours):
            ub = ld.kw if allowed(ld, h) else 0.0
            x[ld.name, h] = solver.NumVar(0.0, ub, f"x_{ld.name}_{h}")
        solver.Add(solver.Sum(x[ld.name, h] for h in range(hours)) == ld.weekly_kwh)

    # site capacity cap: fixed + flexible within contract capacity
    for h in range(hours):
        solver.Add(solver.Sum(x[ld.name, h] for ld in flexible)
                   <= max(0.0, contract_capacity_kw - fixed_profile[h]))

    cost_terms = []
    for ld in flexible:
        for h in range(hours):
            unit = alpha_cost * price[h] + beta_co2_ntd_per_kg * intensity[h]
            cost_terms.append(unit * x[ld.name, h])
    solver.Minimize(solver.Sum(cost_terms))

    status = solver.Solve()
    if status not in (pywraplp.Solver.OPTIMAL, pywraplp.Solver.FEASIBLE):
        raise RuntimeError(f"scheduler LP infeasible (status={status}) — "
                           f"check contract capacity vs weekly energy")

    per_load = {ld.name: [x[ld.name, h].solution_value() for h in range(hours)]
                for ld in flexible}
    opt_profile = [fixed_profile[h] + sum(per_load[ld.name][h] for ld in flexible)
                   for h in range(hours)]

    def cost(profile):  # NT$ energy charge for the week
        return sum(profile[h] * price[h] for h in range(hours))

    def co2(profile):   # kg for the week
        return sum(profile[h] * intensity[h] for h in range(hours))

    return ScheduleResult(
        hours=hours,
        baseline_kw=[round(v, 2) for v in base_profile],
        optimized_kw=[round(v, 2) for v in opt_profile],
        per_load_kwh={k: [round(v, 2) for v in vs] for k, vs in per_load.items()},
        baseline_cost_ntd=round(cost(base_profile), 0),
        optimized_cost_ntd=round(cost(opt_profile), 0),
        baseline_co2_kg=round(co2(base_profile), 1),
        optimized_co2_kg=round(co2(opt_profile), 1),
        notes=[
            f"flexible loads: {[ld.name for ld in flexible]}",
            f"fixed loads keep baseline: {[ld.name for ld in fixed]}",
            "operating window Mon-Sat 06:00-22:00; order-deadline windows arrive via LINE at pilot",
            f"objective: NT$ + CO2 at NT${beta_co2_ntd_per_kg:.0f}/kg shadow price",
        ],
    )
