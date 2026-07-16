"""Module 2 scheduler tests — no network: synthetic intensity + tariff fixtures."""
from __future__ import annotations

import pytest

from carbonpass.scheduler.loads import Load, baseline_profile, loads_from_machines
from carbonpass.scheduler.milp import optimize_week
from carbonpass.scheduler.tariffs import band_of_hour, price_curve

MACHINES = [
    {"name": "Cold former", "kw": 90, "hours": 4400, "process": "P1"},
    {"name": "Heat-treatment furnace", "name_zh": "熱處理爐", "kw": 65, "hours": 5800, "process": "P1"},
    {"name": "Air compressor", "name_zh": "空壓機", "kw": 30, "hours": 6000, "process": "shared"},
]


def synth_intensity(hours=168):
    # midday-low / evening-high synthetic curve around 0.474
    return [0.474 * (1.15 if (h % 24) in (18, 19, 20) else 0.85 if 10 <= h % 24 <= 14 else 1.0)
            for h in range(hours)]


def test_flexibility_classification():
    loads = loads_from_machines(MACHINES)
    flex = {ld.name for ld in loads if ld.flexible}
    assert flex == {"Heat-treatment furnace", "Air compressor"}


def test_energy_conservation_and_capacity():
    loads = loads_from_machines(MACHINES)
    price = price_curve(168, month=7)
    res = optimize_week(loads, price, synth_intensity(), contract_capacity_kw=499)
    for ld in loads:
        if ld.flexible:
            assert sum(res.per_load_kwh[ld.name]) == pytest.approx(ld.weekly_kwh, rel=1e-6)
    assert max(res.optimized_kw) <= 499 + 1e-6
    # weekly totals conserved overall (profiles are rounded to 2 dp for output)
    assert sum(res.optimized_kw) == pytest.approx(sum(res.baseline_kw), abs=1.0)


def test_optimizer_never_worse_than_baseline():
    loads = loads_from_machines(MACHINES)
    price = price_curve(168, month=7)
    res = optimize_week(loads, price, synth_intensity(), contract_capacity_kw=499,
                        beta_co2_ntd_per_kg=0.0)   # pure cost objective
    assert res.optimized_cost_ntd <= res.baseline_cost_ntd
    # with TOU spreads and a flat baseline, savings should be strictly positive
    assert res.optimized_cost_ntd < res.baseline_cost_ntd


def test_tou_banding_summer_weekday_and_weekend():
    assert band_of_hour(17, "summer") == "peak"       # Monday 17:00
    assert band_of_hour(10, "summer") == "half"       # Monday 10:00
    assert band_of_hour(3, "summer") == "off"         # Monday 03:00
    assert band_of_hour(6 * 24 + 12, "summer") == "off"   # Sunday noon


def test_baseline_profile_energy():
    loads = loads_from_machines(MACHINES)
    prof = baseline_profile(loads)
    assert sum(prof) == pytest.approx(sum(ld.weekly_kwh for ld in loads), rel=1e-9)
