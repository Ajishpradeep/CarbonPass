"""Benchmark module: k≥5 floor, honest labels, percentile screen."""
from __future__ import annotations

import json

import pytest

from carbonpass.benchmark import (K_ANONYMITY_FLOOR, BenchmarkRow, export_rows,
                                  percentile_screen)
from carbonpass.benchmark.export import KAnonymityError
from carbonpass.benchmark.percentile import seed_row


def _row(n: int) -> BenchmarkRow:
    return BenchmarkRow(
        sector="fasteners", cn_prefix="7318", period="2026", metric="loss_pct",
        n_firms=n,
        percentiles={"p10": 5.5, "p25": 7.0, "p50": 9.0, "p75": 11.5, "p90": 13.5},
        provenance="test", synthetic=True)


def test_k_anonymity_floor_is_hard(tmp_path):
    assert K_ANONYMITY_FLOOR == 5
    with pytest.raises(KAnonymityError, match="fewer than 5"):
        export_rows([_row(5), _row(4)], tmp_path / "rows.json")
    # nothing was written on refusal
    assert not (tmp_path / "rows.json").exists()
    out = export_rows([_row(5), _row(23)], tmp_path / "rows.json")
    payload = json.loads(out.read_text(encoding="utf-8"))
    assert payload["k_anonymity_floor"] == 5
    assert all(r["n_firms"] >= 5 for r in payload["rows"])
    assert payload["spec"] == "schema/benchmark_row.schema.json"


def test_rows_validate_against_public_schema():
    """The give-back spec is a real artifact — our own rows must satisfy it."""
    import jsonschema

    schema = json.loads(open("schema/benchmark_row.schema.json", encoding="utf-8").read())
    jsonschema.validate(_row(7).as_dict(), schema)
    jsonschema.validate(seed_row().as_dict(), schema)
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(_row(3).as_dict(), schema)   # schema itself enforces n>=5


def test_percentile_screen_honestly_labelled():
    s = percentile_screen(9.1, corpus_loss_pcts=[9.1, 9.7, 8.7])
    assert 30 <= s["percentile"] <= 75          # mid-band value sits mid-distribution
    assert s["seed_row"]["synthetic"] is True
    assert "synthetic seed" in s["label"]
    assert "合成種子" in s["message_zh"]         # the label reaches the zh-TW surface
    assert "pilot" in s["seed_row"]["provenance"]
    # band edges = documented 5–15%
    assert s["band"]["low"] == 5.0 and s["band"]["high"] == 15.0
