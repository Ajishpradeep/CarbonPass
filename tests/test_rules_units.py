"""Unit tests: default-value parsing, mark-up years, MOENV EF table, default fallback."""
from __future__ import annotations

import pytest

from carbonpass.config import markup_for_year
from carbonpass.ingestion import pipeline
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


def test_stainless_wire_rod_is_7221_not_7227():
    """The precursor a stainless fastener maker actually buys.

    CN 7221 = stainless rod, hot-rolled, in irregularly wound coils — the stainless twin
    of CN 7213. CN 7227 is alloy steel *other than stainless*, and Taiwan's 7227 is the
    lowest value assigned to any country on earth: using it for stainless made a stainless
    screw look cleaner than a carbon one.
    """
    assert pipeline._precursor_cn("SUS304 盤元線材 Stainless steel wire rod") == "7221"
    assert pipeline._precursor_cn("SAE1008 盤元線材 Carbon steel wire rod") == "7213"
    assert pipeline._precursor_cn("不鏽鋼線材") == "7221"
    # the trap this guards: 7227 is Taiwan's best-on-earth value, 7221 has no Taiwan value
    assert defaults.lookup("7227", "Taiwan").direct < defaults.lookup("7213", "Taiwan").direct


def test_taiwan_has_no_stainless_rod_value_so_fallback_applies():
    """Q&A p.37 §4.25: not listed -> 'Other countries and territories' table.

    Of the 33 countries with a full steel book, only Taiwan, Thailand and Vietnam have no
    CN 7221 value at all. Taiwan's 7221 row reads "see below" with nothing below it.
    """
    assert defaults.lookup("7221", "Taiwan") is None

    dv, used_fallback = defaults.resolve("7221", "Taiwan")
    assert used_fallback is True
    assert dv.direct == pytest.approx(4.82)
    assert dv.y2026 == pytest.approx(4.82 * 1.10)

    # a country that IS listed must not be routed to the fallback
    dv_cn, fb_cn = defaults.resolve("7221", "China")
    assert fb_cn is False and dv_cn.direct == pytest.approx(5.59)

    # and resolve() must not change the answer where a country value exists
    dv_tw, fb_tw = defaults.resolve("7213", "Taiwan")
    assert fb_tw is False and dv_tw.direct == pytest.approx(2.297829146)


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
