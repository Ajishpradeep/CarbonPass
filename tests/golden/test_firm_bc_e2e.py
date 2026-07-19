"""E2E goldens for firms B & C: corpus documents -> engine SEE == ground truth.

Ground truth is computed by scripts/make_mock_corpus.py from the rows the
documents actually carry (rounded monthly production, integer gas m3 / bill kWh
— docs/archive/15 §6 defect 11), independently of the engine's allocation/rules code.
This was blocked while GT came from intended totals: firm_b drifted rel ~7.5e-5,
firm_c ~1.1e-4. Now the reconciliation must be tight.

The no-VLM ingest skips Taipower-bill photos, so electricity is injected from
the ground truth's expected bill extractions (the perfect-VLM assumption): the
test pins the ALLOCATION + RULES math end-to-end; VLM extraction accuracy is
pinned separately by the bake-off (docs/archive/13).
"""
from __future__ import annotations

import json

import pytest

from carbonpass.config import MOCK_CORPUS_DIR
from carbonpass.ingestion.pipeline import ingest_firm
from carbonpass.pack import run_allocation, run_rules

TOL = 1e-6   # engine aggregation rounds to 6 decimals; firm_a historically 2.5e-7


def _ground_truth() -> dict:
    path = MOCK_CORPUS_DIR / "ground_truth.json"
    if not path.exists():
        pytest.skip("mock corpus not generated — run scripts/make_mock_corpus.py")
    return json.loads(path.read_text(encoding="utf-8"))


@pytest.mark.parametrize("firm_key", ["firm_a", "firm_b", "firm_c"])
def test_engine_reproduces_ground_truth(firm_key: str):
    gt_all = _ground_truth()
    gt = gt_all["firms"][firm_key]

    activity = ingest_firm(MOCK_CORPUS_DIR / firm_key, use_vlm=False)
    bills = gt["expected_extractions"]["bills"]
    kwh_by_month = {b["month"]: float(b["kwh_total"]) for b in bills}
    activity["aggregated"]["electricity_mwh"]["value"] = round(
        sum(kwh_by_month.values()) / 1000.0, 6)
    activity["aggregated"]["electricity_kwh_by_month"] = [
        kwh_by_month.get(m, 0.0) for m in range(1, 13)]

    alloc = run_allocation(activity)
    results = {r.cn_code: r for r in run_rules(activity, alloc)}

    assert len(results) == len(gt["products"])
    for p in gt["products"]:
        r = results[p["cn_code"]]
        assert r.see_direct.value == pytest.approx(p["see_direct"], rel=TOL), \
            f"{firm_key} CN {p['cn_code']} direct"
        assert r.see_indirect.value == pytest.approx(p["see_indirect"], rel=TOL), \
            f"{firm_key} CN {p['cn_code']} indirect"
        assert r.see_total.value == pytest.approx(p["see_total"], rel=TOL), \
            f"{firm_key} CN {p['cn_code']} total"
        assert r.share_default_values == pytest.approx(p["share_default_values"], abs=1e-4)
