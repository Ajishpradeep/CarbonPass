"""Unit tests: default-value parsing, row-derived mark-ups, MOENV EF table, fallback, prices."""
from __future__ import annotations

import pytest

from carbonpass import prices
from carbonpass.ingestion import pipeline
from carbonpass.rules import defaults, ef
from carbonpass.rules.see import PrecursorInput, ProcessInput, compute_product_see


def test_markup_derived_from_row_steel():
    """Iron & steel rows carry 10/20/30% — derived, never hard-coded."""
    dv = defaults.lookup("73181542", "Taiwan")
    assert dv.derived_markup(2026) == pytest.approx(0.10)
    assert dv.derived_markup(2027) == pytest.approx(0.20)
    assert dv.derived_markup(2028) == pytest.approx(0.30)
    assert dv.derived_markup(2031) == pytest.approx(0.30)  # 2028 onward


def test_markup_derived_from_row_fertiliser_flat_1pct():
    """Fertilisers carry a FLAT 1% in every year (docs/15 §6 defect 2) — the row knows."""
    dv = defaults.lookup("28141000", "Vietnam")
    assert dv.direct == pytest.approx(3.46)
    assert dv.total == pytest.approx(3.61)
    for year in (2026, 2027, 2028):
        assert dv.derived_markup(year) == pytest.approx(0.01)
    # marked-up column is TOTAL-based: 3.61 × 1.01 — NOT 3.46 × 1.10
    assert dv.for_year(2026) == pytest.approx(3.6461)
    assert dv.for_year_direct(2026) == pytest.approx(3.46 * 1.01)
    assert dv.for_year_indirect(2026) == pytest.approx(0.15 * 1.01)


def test_markup_basis_is_total_not_direct_cement():
    """Defect 1's original repro: India clinker 1.551 = total 1.41 × 1.10;
    the DIRECT marked-up figure is 1.35 × 1.10 = 1.485."""
    dv = defaults.lookup("25231000", "India")
    assert dv.for_year(2026) == pytest.approx(1.551)
    assert dv.for_year_direct(2026) == pytest.approx(1.485)
    assert dv.for_year_indirect(2026) == pytest.approx(0.07 * 1.10)


def test_grid_ef_from_config_not_literal():
    """Default = 2025 industrial 0.466 (MOEA 2 Jun 2026). 0.474 is the 2024 figure — history."""
    from carbonpass import config
    from carbonpass.rules.gridef import load_grid_ef

    ef_ = load_grid_ef()
    assert ef_.kgco2e_per_kwh == pytest.approx(0.466)
    assert ef_.year == 2025 and ef_.series == "industrial"
    assert "0.466" in ef_.provenance and "MOEA" in ef_.provenance
    assert load_grid_ef(2024, "overall").kgco2e_per_kwh == pytest.approx(0.474)
    with pytest.raises(KeyError):
        load_grid_ef(2023)          # not in the file — no silent extrapolation
    # the old hard-coded constants must stay dead (docs/21 §7.6)
    assert not hasattr(config, "GRID_EF_KGCO2_PER_KWH")
    assert not hasattr(config, "CERTIFICATE_PRICE_EUR")
    assert not hasattr(config, "markup_for_year")


def test_certificate_price_published_and_refusal():
    """Engine quotes only published quarters; unpublished quarters raise (kill-list)."""
    cert = prices.certificate_price()
    assert cert.quarter == "2026Q2" and cert.eur_per_tco2e == pytest.approx(75.28)
    assert cert.published and cert.provenance
    q1 = prices.certificate_price("2026Q1")
    assert q1.eur_per_tco2e == pytest.approx(75.36)
    with pytest.raises(prices.UnpublishedQuarterError):
        prices.certificate_price("2026Q3")   # lands 5 Oct 2026 — never quote before


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


def test_lookup_short_query_guard():
    """Defect 10: short queries must never silently skip a precursor."""
    # one unambiguous extension -> found (used to be a silent None)
    dv = defaults.lookup("7223", "Taiwan")
    assert dv is not None and dv.cn_code == "722300" and dv.direct is not None
    # several extensions -> loud, with candidates
    with pytest.raises(ValueError, match="ambiguous"):
        defaults.lookup("7318", "Taiwan")
    # no forward row, no extension carrying a value -> None (fallback path stays open)
    assert defaults.lookup("7221", "Taiwan") is None


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
    # share recorded, never capped: defaults are lawful without limit (docs/15 §8.1)
    assert r.share_default_values > 0.9
    assert any("default value used" in n for n in r.needs_attention)
    assert not any("ceiling" in n for n in r.needs_attention)
    line = r.precursor_lines[0]["see_direct_used"]
    assert line["source"] == "default"
