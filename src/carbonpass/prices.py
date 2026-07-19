"""Dated market/regulatory prices — the single reader for data/prices.yaml.

Rule (docs/FACTS.md §8, kill-list): no undated price anywhere; the engine REFUSES to
quote a certificate quarter whose publication date is not recorded in the file.
Q3 2026 does not exist until 5 Oct 2026 — asking for it raises, it never
extrapolates.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import yaml

from carbonpass.config import DATA_DIR

PRICES_YAML = DATA_DIR / "prices.yaml"


class UnpublishedQuarterError(LookupError):
    """Raised when a certificate price is requested for an unpublished quarter."""


@dataclass(frozen=True)
class CertificatePrice:
    quarter: str            # e.g. "2026Q2"
    eur_per_tco2e: float
    published: str          # ISO date of the Commission publication
    source: str

    @property
    def provenance(self) -> str:
        return (f"CBAM certificate price {self.quarter}: €{self.eur_per_tco2e}/tCO2e "
                f"({self.source}, published {self.published})")


@dataclass(frozen=True)
class ScrapRecovery:
    kind: str               # carbon_steel | stainless_304
    pct_low: float
    pct_high: float
    asof: str
    basis: str

    @property
    def provenance(self) -> str:
        return (f"scrap resale recovery ({self.kind}): {self.pct_low:.0%}–{self.pct_high:.0%} "
                f"of purchase value (as of {self.asof}; {self.basis})")


@lru_cache(maxsize=1)
def _load() -> dict:
    with open(PRICES_YAML, encoding="utf-8") as f:
        return yaml.safe_load(f)


def certificate_price(quarter: str | None = None) -> CertificatePrice:
    """Latest PUBLISHED quarter (or a specific one). Refuses unpublished quarters.

    A quarter qualifies only if data/prices.yaml records it with a `published:`
    date — the file is the sole authority on what exists.
    """
    table = _load()["cbam_certificate_eur_per_tco2e"]
    published = {q: row for q, row in table.items()
                 if isinstance(row, dict) and row.get("published") and row.get("price")}
    if quarter is not None:
        if quarter not in published:
            raise UnpublishedQuarterError(
                f"no published CBAM certificate price for {quarter} in data/prices.yaml — "
                f"published quarters: {sorted(published)}. Never quote an unpublished "
                f"quarter (docs/FACTS.md §7 kill-list kill-list; Q3 2026 lands 5 Oct 2026).")
        row = published[quarter]
        return CertificatePrice(quarter, float(row["price"]), str(row["published"]),
                                str(row.get("source", "")))
    q = sorted(published)[-1]
    return certificate_price(q)


def scrap_recovery(kind: str) -> ScrapRecovery:
    """Dated scrap-resale recovery range (fraction of purchase value)."""
    table = _load()["scrap_resale_recovery"]
    if kind not in table:
        raise KeyError(f"no scrap recovery entry {kind!r} in data/prices.yaml "
                       f"(have: {sorted(table)})")
    row = table[kind]
    lo, hi = row["pct_range"]
    return ScrapRecovery(kind, float(lo), float(hi), str(row["asof"]), str(row["basis"]))
