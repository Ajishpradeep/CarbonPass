"""Taiwan grid electricity emission factor — the single reader for data/ef/grid_ef.yaml.

Rule (docs/21 §2.8): no code may hard-code a factor; select by year+series and
carry the provenance string into every output. The file's `default_selection`
(2025 industrial = 0.466, MOEA announcement 2 Jun 2026) is the engine default —
0.474 is the 2024 figure and is history (docs/19 §5).

Scope note: this is TAIWAN's public-utility factor. It must never be applied to
a non-Taiwanese installation (docs/15 §6 defect 3) — callers guard on country.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import yaml

from carbonpass.config import DATA_DIR

GRID_EF_YAML = DATA_DIR / "ef" / "grid_ef.yaml"


@dataclass(frozen=True)
class GridEF:
    kgco2e_per_kwh: float   # numerically == tCO2e/MWh
    year: int
    series: str             # overall | industrial | residential
    announced: str
    source_url: str

    @property
    def provenance(self) -> str:
        return (f"Taiwan grid EF {self.kgco2e_per_kwh} kgCO2e/kWh "
                f"({self.year} {self.series}, MOEA announced {self.announced})")


@lru_cache(maxsize=8)
def load_grid_ef(year: int | None = None, series: str | None = None) -> GridEF:
    """Factor for a year+series; defaults to the file's `default_selection`."""
    with open(GRID_EF_YAML, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    sel = cfg["default_selection"]
    year = year if year is not None else int(sel["year"])
    series = series if series is not None else str(sel["series"])
    factors = cfg["factors"]
    if year not in factors:
        raise KeyError(f"no grid EF for {year} in {GRID_EF_YAML.name} "
                       f"(have {sorted(factors)}); next update {cfg.get('next_update_expected')}")
    if series not in factors[year]:
        raise KeyError(f"no {series!r} series for {year} in {GRID_EF_YAML.name} "
                       f"(have {sorted(factors[year])})")
    return GridEF(float(factors[year][series]), year, series,
                  str(cfg.get("announced", "")), str(cfg.get("source_url", "")))
