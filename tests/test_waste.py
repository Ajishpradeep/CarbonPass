"""Waste module: MoneyLoss gross+net enforcement, drift alerts, corpus scan."""
from __future__ import annotations

import json

import pytest

from carbonpass.config import MOCK_CORPUS_DIR
from carbonpass.waste import MoneyLoss, drift_alerts, monthly_series, scan
from carbonpass.waste.drift import rolling_loss


def test_moneyloss_never_renders_gross_alone():
    """docs/21 §2.5: gross AND net together, enforced in the type."""
    m = MoneyLoss.from_purchase_value(7_350_000, "carbon_steel")
    s = str(m)
    assert "7,350,000" in s and "net of scrap resale" in s
    d = m.as_dict()
    assert d["purchase_value_ntd"] == 7_350_000
    lo, hi = d["net_of_resale_ntd_range"]
    # recovery 30–40% -> net loss 60–70% of gross
    assert lo == pytest.approx(7_350_000 * 0.60, rel=1e-6)
    assert hi == pytest.approx(7_350_000 * 0.70, rel=1e-6)
    assert "asof" not in d["recovery_provenance"] or d["recovery_provenance"]
    # construction without a recovery kind is impossible
    with pytest.raises(KeyError):
        MoneyLoss.from_purchase_value(1000, "unobtainium")


def test_moneyloss_sum_merges_ranges():
    a = MoneyLoss.from_purchase_value(1_000_000, "carbon_steel")
    b = MoneyLoss.from_purchase_value(2_000_000, "stainless_304")
    total = (a + b).as_dict()
    assert total["purchase_value_ntd"] == 3_000_000
    lo_r, hi_r = total["resale_recovery_pct_range"]
    assert lo_r == 0.30 and hi_r == 0.45   # outer envelope of the two dated ranges


def _series(losses: list[float]) -> list[dict]:
    return [{"month": f"2026-{i+1:02d}", "window_months": 3,
             "consumed_t": 100.0, "produced_t": 100.0 * (1 - x / 100),
             "loss_pct": x} for i, x in enumerate(losses)]


def test_drift_alert_fires_on_rising_series_and_stays_quiet_on_flat():
    flat = _series([9.0, 9.2, 8.9, 9.1, 9.0, 9.1])
    assert drift_alerts(flat) == []
    rising = _series([7.0, 7.1, 6.9, 7.0, 7.2, 11.0])
    alerts = drift_alerts(rising)
    assert len(alerts) == 1
    a = alerts[0]
    assert a["loss_pct"] == 11.0 and a["rise_pp"] > 3.5
    assert "損耗率警示" in a["message_zh"]
    # too few points -> no verdict either way
    assert drift_alerts(_series([7.0, 12.0])) == []


def test_rolling_loss_skips_windows_without_delivery():
    consumed = {"2026-02": 300.0, "2026-05": 300.0}   # quarterly deliveries
    produced = {f"2026-{m:02d}": 90.0 for m in range(1, 7)}
    series = rolling_loss(consumed, produced, window=3)
    months = [s["month"] for s in series]
    # windows ending in months whose 3-month span holds a delivery
    assert "2026-02" in months and "2026-04" in months
    for s in series:
        assert 0 <= s["loss_pct"] < 100


@pytest.fixture(scope="module")
def firm_a_scan():
    corpus = MOCK_CORPUS_DIR / "firm_a"
    activity_path = "out/firm_a_activity.json"
    if not corpus.exists() or not json.load(open(activity_path)) :
        pytest.skip("corpus/activity not present")
    return scan(activity_path, str(corpus))


def test_scan_output_discipline(firm_a_scan):
    r = firm_a_scan
    # method note in every output: mass-before-cutting + remelt caveat, never 'avoided'
    assert "before cutting" in r["method_note"]
    assert "remelting recovers the iron" in r["method_note"]
    assert "never 'avoided'" in r["method_note"]
    assert "avoided" not in json.dumps([k for l in r["lines"] for k in l])  # no avoided_* keys
    # money always gross+net
    for l in r["lines"]:
        if l["money_loss"]:
            assert set(l["money_loss"]) >= {"purchase_value_ntd", "net_of_resale_ntd_range",
                                            "resale_recovery_pct_range"}
    assert r["totals"]["money_loss"] is not None
    # dated certificate price with provenance
    assert "published" in r["certificate_price_provenance"]
    # provisional label
    assert "pilot" in r["data_provenance"]


def test_scan_firm_a_magnitudes(firm_a_scan):
    """The verified magnitudes (docs/19, docs/20 §4): ~9.1% loss, ~758 t gross embodied."""
    r = firm_a_scan
    line = r["lines"][0]
    assert line["loss_pct"] == pytest.approx(9.1, abs=0.3)
    assert r["totals"]["embodied_tco2e_per_yr_gross"] == pytest.approx(758, abs=15)
    gross = r["totals"]["money_loss"]["purchase_value_ntd"]
    lo, hi = r["totals"]["money_loss"]["net_of_resale_ntd_range"]
    assert gross == pytest.approx(7_350_000, rel=0.05)
    assert 3_800_000 < lo < hi < 5_500_000    # the honest NT$4–5M band


def test_corpus_drift_series_exists_and_is_quiet():
    """Synthetic corpus is flat jitter — the alert must NOT fire (no false alarms)."""
    corpus = MOCK_CORPUS_DIR / "firm_a"
    if not corpus.exists():
        pytest.skip("corpus not present")
    activity = json.load(open("out/firm_a_activity.json", encoding="utf-8"))
    d = monthly_series(str(corpus), activity)
    assert d["lines"], "no drift lines built"
    for line in d["lines"]:
        assert line["series"], f"empty series for {line['product']}"
        assert line["alerts"] == []
