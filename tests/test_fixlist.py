"""Fix-list: fixed measured order, and the negative answer pinned as a feature."""
from __future__ import annotations

import pytest

from carbonpass.config import MOCK_CORPUS_DIR
from carbonpass.costdelta.fixlist import fixlist, render_fixlist, render_fixlist_zh


@pytest.fixture(scope="module")
def firm_a_fixlist():
    corpus = MOCK_CORPUS_DIR / "firm_a"
    if not corpus.exists():
        pytest.skip("corpus not present")
    # schedule=None -> load-shifting must degrade honestly, not crash offline
    return fixlist("out/firm_a_activity.json", str(corpus), schedule=None)


def test_levers_in_measured_order(firm_a_fixlist):
    ids = [lv["id"] for lv in firm_a_fixlist["levers"]]
    assert ids == ["yield", "mill_epd", "process_energy", "load_shifting"]
    assert [lv["rank"] for lv in firm_a_fixlist["levers"]] == [1, 2, 3, 4]


def test_negative_answer_is_pinned(firm_a_fixlist):
    """The Thailand-row discipline (docs/21 §1.3): firm_a's data is worth €4/t —
    the tool must say 'not worth it this year', and say why."""
    epd = next(lv for lv in firm_a_fixlist["levers"] if lv["id"] == "mill_epd")
    assert epd["verdict"] == "not_worth_it_this_year"
    assert epd["buyer_eur_per_t"] == pytest.approx(4.03, abs=0.15)
    assert "defaults are lawful" in epd["rationale"]
    # and the negative verdict reaches both rendered surfaces
    assert "⏸" in render_fixlist(firm_a_fixlist)
    assert "今年先不用" in render_fixlist_zh(firm_a_fixlist)


def test_yield_lever_is_the_headline(firm_a_fixlist):
    y = firm_a_fixlist["levers"][0]
    assert y["verdict"] == "worth_it"
    assert y["ntd_per_yr"] > 3_000_000            # the 80×-numerator money
    assert y["tco2e_per_yr"] == pytest.approx(359, abs=10)
    assert "Annex III" in y["rationale"]          # legal basis travels with the number
    assert y["money_loss_context"] is not None    # gross+net context attached


def test_every_lever_can_answer_and_is_scoped(firm_a_fixlist):
    for lv in firm_a_fixlist["levers"]:
        assert lv["verdict"] in ("worth_it", "not_worth_it_this_year", "insufficient_data")
        assert lv["rationale"]
        assert lv["carbon_scope_note"]
    # electricity levers carry the not-certificated label (docs/21 §2.2)
    for lid in ("process_energy", "load_shifting"):
        lv = next(x for x in firm_a_fixlist["levers"] if x["id"] == lid)
        assert "NOT" in lv["carbon_scope_note"]
    assert "NOT regulatory" in firm_a_fixlist["heuristics_note"]


def test_small_load_shift_gets_a_no():
    """A firm whose shiftable value is small must hear 'not this year', not a pitch."""
    from carbonpass.costdelta.fixlist import _load_shift_lever

    tiny = {"ledger": {"delta_year_est": {"cost_ntd": 42_000, "emissions_tco2e": 0.5}},
            "tariff": {"source": "test"}, "grid_intensity": {"anchor_source": "test"}}
    lv = _load_shift_lever(tiny)
    assert lv["verdict"] == "not_worth_it_this_year"
    assert "below materiality" in lv["rationale"]
