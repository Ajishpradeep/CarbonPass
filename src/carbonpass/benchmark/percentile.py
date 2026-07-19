"""Percentile screen: where does this firm sit against the modelled band?

Seed = the 3 synthetic corpus firms + the DOCUMENTED whole-chain loss band of
5–15% (docs/FACTS.md §8: defensible synthesis; cold forming runs 85–95% material
utilization). Every output says "synthetic seed — pilot populates" until real
rows replace it (docs/FACTS.md §8: provisional numbers stay labelled provisional).
"""
from __future__ import annotations

import bisect
import statistics

from carbonpass.benchmark.schema import BenchmarkRow

SEED_PROVENANCE = ("synthetic seed — 3 corpus firms + documented 5–15% whole-chain "
                   "loss band (docs/FACTS.md §8); the pilot benchmark replaces this")

# The modelled loss distribution behind the seed screen: the documented band as a
# triangular-ish spread. NOT survey data — labelled synthetic everywhere.
_SEED_LOSS_BAND = [5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 15.0]


def seed_distribution(corpus_loss_pcts: list[float] | None = None) -> list[float]:
    """Modelled band + whatever synthetic firms exist. Sorted."""
    vals = sorted(_SEED_LOSS_BAND + list(corpus_loss_pcts or []))
    return vals


def _percentiles(values: list[float]) -> dict[str, float]:
    qs = statistics.quantiles(sorted(values), n=100, method="inclusive")
    pick = lambda p: round(qs[p - 1], 2)
    return {"p10": pick(10), "p25": pick(25), "p50": pick(50),
            "p75": pick(75), "p90": pick(90)}


def seed_row(metric: str = "loss_pct",
             corpus_loss_pcts: list[float] | None = None) -> BenchmarkRow:
    dist = seed_distribution(corpus_loss_pcts)
    return BenchmarkRow(
        sector="fasteners", cn_prefix="7318", period="2026",
        metric=metric, n_firms=len(dist),
        percentiles=_percentiles(dist),
        provenance=SEED_PROVENANCE, synthetic=True,
        notes=["Percentile positions on this seed are ILLUSTRATIVE — the modelled "
               "band, not a measured population. A pilot row (n small, labelled) "
               "replaces it during mentorship."],
    )


def percentile_screen(loss_pct: float,
                      corpus_loss_pcts: list[float] | None = None) -> dict:
    """The 「我正常嗎」 answer for one firm's loss rate, honestly labelled."""
    dist = seed_distribution(corpus_loss_pcts)
    rank = bisect.bisect_left(dist, loss_pct)
    pctile = round(100.0 * rank / len(dist))
    row = seed_row(corpus_loss_pcts=corpus_loss_pcts)
    return {
        "metric": "loss_pct",
        "your_value": round(loss_pct, 2),
        "percentile": pctile,
        "band": {"low": dist[0], "high": dist[-1]},
        "seed_row": row.as_dict(),
        "label": SEED_PROVENANCE,
        "message_zh": (f"你的物料損耗率 {loss_pct:.1f}%，落在示意分布的第 {pctile} 百分位"
                       f"（5–15% 文獻區間，合成種子）。試點量測後會換成真實同業分布。"),
    }
