"""Golden test: reproduce the Commission's CEMENT answer key (the non-steel golden).

Inputs and expected outputs transcribed from
data/cbam_official/template_examples/1 CBAM SEE V2.1_Example Cement_final.xlsx
(docs/archive/21 §1.1.2 — this workbook sat unused while defects 1–2 lived; a non-steel
golden would have caught them a sprint earlier).

What it exercises beyond screws & nuts:
  * a sector where INDIRECT emissions are inside the certificate obligation
  * process emissions (raw meal) + a biomass-share fuel in the source streams
  * the sector-aware indirect note (not the CN 7318 wording)

Tolerance 1e-9 relative — deterministic arithmetic; the workbook wins disputes.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from carbonpass.config import indirect_in_certificate
from carbonpass.rules.see import ProcessInput, compute_installation

GOLDEN = json.loads(
    (Path(__file__).parent / "cement_expected.json").read_text(encoding="utf-8"))
REL_TOL = 1e-9


@pytest.fixture(scope="module")
def results():
    inp = GOLDEN["inputs"]
    processes = [ProcessInput(
        name=proc["name"],
        cn_code=GOLDEN["expected"]["products"][0]["cn_code"],
        production_t=proc["production_level_t"],
        production_unc_rel=0.0,
        direct_emissions_tco2e=proc["direct_attributed_emissions_tco2e"],
        direct_unc_rel=0.0,
        electricity_mwh=proc["electricity_consumption_mwh"],
        electricity_unc_rel=0.0,
        electricity_ef=proc["electricity_ef_tco2_per_mwh"],
        electricity_ef_source=proc["electricity_ef_source"],
        precursors=[],
    ) for proc in inp["production_processes"]]
    period_year = int(GOLDEN["reporting_period"]["start"][:4])
    return {r.product_name: r for r in compute_installation(processes, period_year)}


def test_cement_see(results):
    exp = GOLDEN["expected"]["products"][0]
    r = results[exp["product_name"]]
    assert r.cn_code == exp["cn_code"]
    assert r.see_direct.value == pytest.approx(exp["see_direct"], rel=REL_TOL)
    assert r.see_indirect.value == pytest.approx(exp["see_indirect"], rel=REL_TOL)
    assert r.see_total.value == pytest.approx(exp["see_total"], rel=REL_TOL)
    assert r.embedded_electricity_mwh_per_t.value == pytest.approx(
        exp["embedded_electricity_mwh_per_t"], rel=REL_TOL)
    assert r.share_default_values == pytest.approx(exp["share_default_values"], abs=1e-12)


def test_cement_source_streams_reproduce_direm():
    """Process emissions + combustion (with biomass zero-rating) roll up to DirEm."""
    total = 0.0
    for ss in GOLDEN["inputs"]["source_streams"]:
        fossil = 1.0 - ss["biomass_pct"] / 100.0
        if ss["method"] == "Process emissions":
            total += ss["activity_data_t"] * ss["ef_tco2_per_t"] * fossil
        else:
            total += ss["activity_data_t"] * ss["ncv_gj_per_t"] / 1000.0 \
                * ss["ef_tco2_per_tj"] * fossil
    assert total == pytest.approx(
        GOLDEN["expected"]["installation_totals"]["total_direct_emissions_tco2e"], rel=REL_TOL)


def test_cement_indirect_is_in_certificate(results):
    """G7: cement's indirect IS certificated — the note must say so (sector-aware)."""
    assert indirect_in_certificate("25232900") is True
    r = results["Cement Bubble"]
    assert "part of the certificate obligation" in r.see_indirect.note
    assert "NOT in the CN" not in r.see_indirect.note
