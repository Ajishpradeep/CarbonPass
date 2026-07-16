"""Unit tests: default-value parsing, mark-up years, MOENV EF table, default fallback."""
from __future__ import annotations

import pytest

from carbonpass.config import markup_for_year
from carbonpass.rules import defaults, ef
from carbonpass.rules.see import PrecursorInput, ProcessInput, compute_product_see


def test_markup_years():
    assert markup_for_year(2026) == 0.10
    assert markup_for_year(2027) == 0.20
    assert markup_for_year(2028) == 0.30
    assert markup_for_year(2031) == 0.30  # 2028 onward


def test_taiwan_7318_default_row():
    dv = defaults.lookup("73181542", "Taiwan")
    assert dv is not None
    assert dv.cn_code == "731815"
    assert dv.direct == pytest.approx(2.70719)
    assert dv.indirect is None            # N/A — not in the CN 7318 certificate
    assert dv.y2026 == pytest.approx(2.70719 * 1.10)
    assert dv.y2027 == pytest.approx(2.70719 * 1.20)
    assert dv.y2028 == pytest.approx(2.70719 * 1.30)


def test_taiwan_wire_rod_default_rows():
    assert defaults.lookup("7213", "Taiwan").direct == pytest.approx(2.297829146)
    assert defaults.lookup("7227", "Taiwan").direct == pytest.approx(2.17)


def test_moenv_table_loaded_full():
    rows = ef.load_all()
    assert len(rows) > 1000, "coefficient snapshot truncated — rerun scripts/pull_moenv_ef.py"
    hit = ef.best("天然氣")
    assert hit is not None and hit.kgco2e > 0


def test_default_precursor_fallback_and_flags():
    """No EPD -> CBAM default with year mark-up, flagged default + needs-attention."""
    p = ProcessInput(
        name="Carbon steel screws and nuts", cn_code="73181542",
        production_t=1000.0, production_unc_rel=0.0,
        direct_emissions_tco2e=150.0, direct_unc_rel=0.0,
        electricity_mwh=200.0, electricity_unc_rel=0.0, electricity_ef=0.474,
        precursors=[PrecursorInput(name="Carbon steel wire rod", mass_t=1100.0,
                                   cn_code="7213", country="Taiwan")],
    )
    r = compute_product_see(p, period_year=2026)
    expected_prec = 2.297829146 * 1.10
    assert r.see_direct.value == pytest.approx(0.15 + 1.1 * expected_prec, rel=1e-9)
    assert r.share_default_values > 0.9
    assert any("default value used" in n for n in r.needs_attention)
    assert any("20% ceiling" in n for n in r.needs_attention)
    line = r.precursor_lines[0]["see_direct_used"]
    assert line["source"] == "default"
