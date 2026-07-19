"""Allocation engine: installation-level energy -> per-process attribution.

Two-step attribution per IR 2025/2547 (docs/archive/10 §2A):
  step 1: installation totals -> production processes (CBAM vs non-CBAM split)
  step 2: process emissions -> CN-code products (here 1:1 process:product)

Method: an OR-Tools linear program finds process shares that (a) conserve the
metered totals, (b) stay within physical bounds, and (c) deviate minimally from
engineering priors (machine kW x run-hours for electricity; production-tonnage
heat demand for fuel). With bill-level data only, the LP collapses to the priors
— the honest state of knowledge (gap G4); sub-meter/AMI constraints tighten it
at the pilot without changing the model.

Uncertainty: NumPy Monte-Carlo over machine hours, production masses and metered
totals -> per-line mean + relative 1-sigma. The uncertainty is a feature
verifiers want, not a bug.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from ortools.linear_solver import pywraplp


@dataclass
class ProcessSpec:
    name: str
    production_t: float
    production_unc_rel: float = 0.01


@dataclass
class MachineSpec:
    name: str
    kw: float
    hours: float
    process: str            # process name or "shared"
    hours_unc_rel: float = 0.10


@dataclass
class AllocationInput:
    processes: list[ProcessSpec]
    machines: list[MachineSpec]
    fuel_co2e_t: float                  # installation-level direct emissions from fuels
    fuel_unc_rel: float
    electricity_mwh: float              # installation-level metered electricity
    electricity_unc_rel: float
    non_cbam_fuel_share: float = 0.0    # C_Emissions&Energy (iii): fuel to non-CBAM goods
    non_cbam_elec_share: float = 0.0


@dataclass
class AllocatedProcess:
    name: str
    direct_emissions_tco2e: float
    direct_unc_rel: float
    electricity_mwh: float
    electricity_unc_rel: float
    fuel_share: float
    elec_share: float


@dataclass
class AllocationResult:
    processes: list[AllocatedProcess]
    n_samples: int
    notes: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
def _prior_shares(processes: list[ProcessSpec], machines: list[MachineSpec],
                  prod_t: dict[str, float]) -> tuple[dict[str, float], dict[str, float]]:
    """Engineering priors: fuel by production tonnage, electricity by kW x hours."""
    total_t = sum(prod_t.values())
    fuel = {p.name: prod_t[p.name] / total_t for p in processes}

    weights = {p.name: 0.0 for p in processes}
    for m in machines:
        e = m.kw * m.hours
        if m.process == "shared":
            for p in processes:
                weights[p.name] += e * prod_t[p.name] / total_t
        else:
            weights[m.process] += e
    wsum = sum(weights.values())
    elec = {k: (v / wsum if wsum else fuel[k]) for k, v in weights.items()}
    return fuel, elec


def _solve_shares(prior: dict[str, float], cbam_total_share: float) -> dict[str, float]:
    """LP: find shares summing to the CBAM share, minimising L1 distance to priors.

    Trivially equals the (scaled) priors today; the LP exists so sub-meter
    readings can be added as hard constraints (share_p * total == meter_p ± tol)
    without restructuring the engine.
    """
    solver = pywraplp.Solver.CreateSolver("GLOP")
    names = list(prior)
    x = {n: solver.NumVar(0.0, 1.0, f"share_{n}") for n in names}
    dev = {n: solver.NumVar(0.0, 1.0, f"dev_{n}") for n in names}
    solver.Add(solver.Sum(x.values()) == cbam_total_share)
    for n in names:
        target = prior[n] * cbam_total_share
        solver.Add(dev[n] >= x[n] - target)
        solver.Add(dev[n] >= target - x[n])
    solver.Minimize(solver.Sum(dev.values()))
    status = solver.Solve()
    if status != pywraplp.Solver.OPTIMAL:
        raise RuntimeError(f"allocation LP infeasible (status={status})")
    return {n: x[n].solution_value() for n in names}


def allocate(inp: AllocationInput, n_samples: int = 10_000, seed: int = 7) -> AllocationResult:
    rng = np.random.default_rng(seed)
    names = [p.name for p in inp.processes]

    # Point estimate (the numbers that go in the template)
    prod_t = {p.name: p.production_t for p in inp.processes}
    fuel_prior, elec_prior = _prior_shares(inp.processes, inp.machines, prod_t)
    fuel_share = _solve_shares(fuel_prior, 1.0 - inp.non_cbam_fuel_share)
    elec_share = _solve_shares(elec_prior, 1.0 - inp.non_cbam_elec_share)

    # Monte-Carlo for uncertainty
    dir_samples = {n: np.empty(n_samples) for n in names}
    elec_samples = {n: np.empty(n_samples) for n in names}
    for i in range(n_samples):
        prod_s = {p.name: p.production_t * (1 + rng.normal(0, p.production_unc_rel))
                  for p in inp.processes}
        machines_s = [
            MachineSpec(m.name, m.kw, m.hours * (1 + rng.normal(0, m.hours_unc_rel)), m.process)
            for m in inp.machines
        ]
        f_prior, e_prior = _prior_shares(inp.processes, machines_s, prod_s)
        fuel_tot = inp.fuel_co2e_t * (1 + rng.normal(0, inp.fuel_unc_rel))
        elec_tot = inp.electricity_mwh * (1 + rng.normal(0, inp.electricity_unc_rel))
        for n in names:
            dir_samples[n][i] = fuel_tot * f_prior[n] * (1.0 - inp.non_cbam_fuel_share)
            elec_samples[n][i] = elec_tot * e_prior[n] * (1.0 - inp.non_cbam_elec_share)

    out = []
    for n in names:
        d_mean = float(inp.fuel_co2e_t * fuel_share[n])
        e_mean = float(inp.electricity_mwh * elec_share[n])
        out.append(AllocatedProcess(
            name=n,
            direct_emissions_tco2e=d_mean,
            direct_unc_rel=float(dir_samples[n].std() / dir_samples[n].mean()) if d_mean else 0.0,
            electricity_mwh=e_mean,
            electricity_unc_rel=float(elec_samples[n].std() / elec_samples[n].mean()) if e_mean else 0.0,
            fuel_share=float(fuel_share[n]),
            elec_share=float(elec_share[n]),
        ))
    notes = [
        "shares from engineering priors (machine kW x run-hours; production-tonnage heat demand)",
        "bill-level data only — no sub-metering constraints active (tighten with 15-min AMI at pilot)",
        f"Monte-Carlo n={n_samples}: machine hours ±10% (1σ), production ±1%, metered totals ± document uncertainty",
    ]
    return AllocationResult(processes=out, n_samples=n_samples, notes=notes)
