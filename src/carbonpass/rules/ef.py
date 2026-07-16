"""MOENV emission-coefficient lookup (data/ef/moenv_coefficients.json, dataset CFP_P_02).

Records: {name 係數名稱, coe kgCO2e, unit, departmentname, announcementyear}.
Used for Scope-1 fuel/material factors and org-inventory by-products; CBAM
combustion factors may also come from IPCC/template values (rules.see decides).
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache

from carbonpass.config import MOENV_EF_JSON


@dataclass(frozen=True)
class EmissionFactor:
    name: str
    kgco2e: float
    unit: str
    department: str
    year: str


@lru_cache(maxsize=1)
def load_all() -> list[EmissionFactor]:
    rows = json.loads(MOENV_EF_JSON.read_text(encoding="utf-8"))
    out = []
    for r in rows:
        try:
            out.append(EmissionFactor(
                name=r["name"], kgco2e=float(r["coe"]), unit=r["unit"],
                department=r.get("departmentname", ""), year=r.get("announcementyear", ""),
            ))
        except (KeyError, ValueError):
            continue
    return out


def search(keyword: str, limit: int = 10) -> list[EmissionFactor]:
    """Substring search over 係數名稱, newest announcement year first."""
    hits = [ef for ef in load_all() if keyword in ef.name]
    return sorted(hits, key=lambda e: e.year, reverse=True)[:limit]


def best(keyword: str) -> EmissionFactor | None:
    hits = search(keyword, limit=1)
    return hits[0] if hits else None
