"""Golden tests: reproduce the Commission's screws & nuts answer key.

Inputs and expected outputs transcribed from
data/cbam_official/template_examples/4 CBAM SEE V2.1_Example Steel 3 Screws and
nuts_final.xlsx (see schema/cbam_template_map.yaml for cell coordinates).

The engine must reproduce the workbook's SEE figures. Tolerance: 1e-9 relative —
the chain is deterministic arithmetic; anything looser hides a wrong formula.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from carbonpass.rules.see import PrecursorInput, ProcessInput, compute_installation

GOLDEN = json.loads(
    (Path(__file__).parent / "screws_and_nuts_expected.json").read_text(encoding="utf-8"))
REL_TOL = 1e-9


def build_processes() -> list[ProcessInput]:
    inp = GOLDEN["inputs"]
    precs = {pr["name"]: pr for pr in inp["purchased_precursors"]}
    processes = []
    for proc in inp["production_processes"]:
        p_precs = []
        for pr in precs.values():
            mass = pr["consumed_in_process_t"].get(proc["name"], 0.0)
            if not mass:
                continue
            p_precs.append(PrecursorInput(
                name=pr["name"],
                mass_t=mass,
                cn_code="",                      # answer key uses measured (actual) data
                see_direct=pr["see_direct_tco2e_per_t"],
                spec_electricity_mwh_per_t=pr["spec_electricity_mwh_per_t"],
                electricity_ef=pr["electricity_ef_tco2e_per_mwh"],
            ))
        products = [pp for pp in GOLDEN["expected"]["products"]
                    if pp["product_name"] == proc["name"]]
        processes.append(ProcessInput(
            name=proc["name"],
            cn_code=products[0]["cn_code"],
            production_t=proc["production_level_t"],
            production_unc_rel=0.0,
            direct_emissions_tco2e=proc["direct_attributed_emissions_tco2e"],
            direct_unc_rel=0.0,
            electricity_mwh=proc["electricity_consumption_mwh"],
            electricity_unc_rel=0.0,
            electricity_ef=proc["electricity_ef_tco2_per_mwh"],
            electricity_ef_source=proc["electricity_ef_source"],
            precursors=p_precs,
        ))
    return processes


@pytest.fixture(scope="module")
def results():
    period_year = int(GOLDEN["reporting_period"]["start"][:4])
    return {r.product_name: r for r in compute_installation(build_processes(), period_year)}


@pytest.mark.parametrize("expected", GOLDEN["expected"]["products"],
                         ids=[p["cn_code"] for p in GOLDEN["expected"]["products"]])
def test_product_see(results, expected):
    r = results[expected["product_name"]]
    assert r.cn_code == expected["cn_code"]
    assert r.see_direct.value == pytest.approx(expected["see_direct"], rel=REL_TOL)
    assert r.see_indirect.value == pytest.approx(expected["see_indirect"], rel=REL_TOL)
    assert r.see_total.value == pytest.approx(expected["see_total"], rel=REL_TOL)
    assert r.embedded_electricity_mwh_per_t.value == pytest.approx(
        expected["embedded_electricity_mwh_per_t"], rel=REL_TOL)
    assert r.share_default_values == pytest.approx(expected["share_default_values"], abs=1e-12)


def test_installation_totals():
    """Cross-check the installation-level roll-up (C_Emissions&Energy)."""
    inp = GOLDEN["inputs"]
    exp = GOLDEN["expected"]["installation_totals"]
    ss = inp["source_streams"][0]
    fuel_tj = ss["activity_data_t"] * ss["ncv_gj_per_t"] / 1000.0
    assert fuel_tj == pytest.approx(exp["fuel_input_tj"], rel=REL_TOL)
    assert fuel_tj * ss["ef_tco2_per_tj"] == pytest.approx(
        exp["total_direct_emissions_tco2e"], rel=REL_TOL)
    indirect = sum(p["electricity_consumption_mwh"] * p["electricity_ef_tco2_per_mwh"]
                   for p in inp["production_processes"])
    assert indirect == pytest.approx(exp["total_indirect_emissions_tco2e"], rel=REL_TOL)
    # direct attributed emissions must sum to the installation total
    attributed = sum(p["direct_attributed_emissions_tco2e"] for p in inp["production_processes"])
    assert attributed == pytest.approx(exp["total_direct_emissions_tco2e"], rel=REL_TOL)


def test_indirect_not_in_certificate_flag(results):
    """G7: indirect SEE is recorded but flagged as outside the CN 7318 certificate."""
    for r in results.values():
        assert "NOT in the CN 7318 certificate" in r.see_indirect.note
