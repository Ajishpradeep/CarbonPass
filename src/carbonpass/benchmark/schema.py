"""Benchmark row schema — also the open-data give-back spec (docs/archive/21 §1.4).

A published row is an AGGREGATE over n ≥ 5 firms; nothing below that floor is
ever exported (k-anonymity). Firm-level observations exist only on-device.

The JSON Schema twin of this dataclass lives at schema/benchmark_row.schema.json
— written as a public artifact so MOENV/TIFI/MIRDC (or anyone) can publish
compatible rows.
"""
from __future__ import annotations

from dataclasses import dataclass, field

K_ANONYMITY_FLOOR = 5   # publish nothing below this — hard floor, not a default


@dataclass(frozen=True)
class BenchmarkRow:
    """One published aggregate: a sector × CN-prefix × period × metric distribution."""
    sector: str                 # e.g. "fasteners"
    cn_prefix: str              # e.g. "7318"
    period: str                 # e.g. "2026" or "2026H1"
    metric: str                 # "loss_pct" | "kwh_per_tonne"
    n_firms: int                # ≥ K_ANONYMITY_FLOOR to be exportable
    percentiles: dict[str, float]   # {"p10":…, "p25":…, "p50":…, "p75":…, "p90":…}
    provenance: str             # data source + date; "synthetic seed" until the pilot
    synthetic: bool = True      # flips to False only when real pilot rows land
    notes: list[str] = field(default_factory=list)

    def __post_init__(self):
        need = {"p10", "p25", "p50", "p75", "p90"}
        if not need <= set(self.percentiles):
            raise ValueError(f"percentiles must include {sorted(need)}")

    @property
    def exportable(self) -> bool:
        return self.n_firms >= K_ANONYMITY_FLOOR

    def as_dict(self) -> dict:
        return {
            "sector": self.sector, "cn_prefix": self.cn_prefix, "period": self.period,
            "metric": self.metric, "n_firms": self.n_firms,
            "percentiles": dict(self.percentiles),
            "synthetic": self.synthetic, "provenance": self.provenance,
            "notes": list(self.notes),
        }
