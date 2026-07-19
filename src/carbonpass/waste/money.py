"""MoneyLoss — money stated gross AND net, enforced by the type.

The Rev-3 mistake (docs/PROJECT.md §1): NT$7.35M/yr was quoted at purchase price when
scrap is SOLD at ~30–40% recovery — the honest net is NT$4–5M. Rule (docs/archive/20 §2,
docs/FACTS.md §8): every headline number ships with its net twin in the same
sentence. This type makes the gross figure unreachable without the net one:
construction requires a dated recovery range from data/prices.yaml, and every
rendering (str, dict) emits both together.
"""
from __future__ import annotations

from dataclasses import dataclass

from carbonpass.prices import ScrapRecovery, scrap_recovery


@dataclass(frozen=True)
class MoneyLoss:
    """A yearly material-money loss. Never renders gross without net."""
    _purchase_value_ntd: float
    recovery: ScrapRecovery

    @classmethod
    def from_purchase_value(cls, purchase_value_ntd: float, kind: str) -> "MoneyLoss":
        """kind: 'carbon_steel' | 'stainless_304' — resale range comes from prices.yaml."""
        return cls(float(purchase_value_ntd), scrap_recovery(kind))

    @property
    def net_range_ntd(self) -> tuple[float, float]:
        """Net cash loss after resale: gross × (1 − recovery), high recovery → low loss."""
        g = self._purchase_value_ntd
        return (g * (1.0 - self.recovery.pct_high), g * (1.0 - self.recovery.pct_low))

    def as_dict(self) -> dict:
        lo, hi = self.net_range_ntd
        return {
            "purchase_value_ntd": round(self._purchase_value_ntd),
            "net_of_resale_ntd_range": [round(lo), round(hi)],
            "resale_recovery_pct_range": [self.recovery.pct_low, self.recovery.pct_high],
            "recovery_provenance": self.recovery.provenance,
        }

    def __str__(self) -> str:
        lo, hi = self.net_range_ntd
        return (f"NT${self._purchase_value_ntd:,.0f} at purchase price "
                f"→ NT${lo:,.0f}–{hi:,.0f} net of scrap resale "
                f"(recovery {self.recovery.pct_low:.0%}–{self.recovery.pct_high:.0%}, "
                f"as of {self.recovery.asof})")

    def __add__(self, other: "MoneyLoss") -> "MoneyLoss":
        if self.recovery != other.recovery:
            # keep totals honest across mixed materials: widen to the outer range
            merged = ScrapRecovery(
                kind=f"{self.recovery.kind}+{other.recovery.kind}",
                pct_low=min(self.recovery.pct_low, other.recovery.pct_low),
                pct_high=max(self.recovery.pct_high, other.recovery.pct_high),
                asof=min(self.recovery.asof, other.recovery.asof),
                basis="merged ranges of the summed lines",
            )
            return MoneyLoss(self._purchase_value_ntd + other._purchase_value_ntd, merged)
        return MoneyLoss(self._purchase_value_ntd + other._purchase_value_ntd, self.recovery)
