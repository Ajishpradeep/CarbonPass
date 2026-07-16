"""CBAM default values (IR 2025/2621) — parser for data/cbam_official/default_values.xlsx.

One sheet per country; columns:
    A CN code | B description | C direct | D indirect | E total
    F 2026 (+10%) | G 2027 (+20%) | H 2028+ (+30%) | I production route

Indirect for iron & steel goods is 'N/A' — consistent with G7: indirect emissions
are not part of the CN 7318 certificate obligation.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from functools import lru_cache

import openpyxl

from carbonpass.config import DEFAULT_VALUES_XLSX


@dataclass(frozen=True)
class DefaultValue:
    cn_code: str            # normalized, no spaces (may be 4..8 digits)
    description: str
    direct: float | None
    indirect: float | None  # None == N/A (not in certificate for this sector)
    total: float | None
    y2026: float | None     # incl. +10% mark-up
    y2027: float | None     # incl. +20%
    y2028: float | None     # incl. +30% (2028 onward)
    route: str

    def for_year(self, year: int) -> float | None:
        """Marked-up default value applicable to a determination period."""
        if year <= 2026:
            return self.y2026
        if year == 2027:
            return self.y2027
        return self.y2028


def _num(v) -> float | None:
    if isinstance(v, (int, float)):
        return float(v)
    return None


@lru_cache(maxsize=8)
def load_country(country: str = "Taiwan") -> list[DefaultValue]:
    wb = openpyxl.load_workbook(DEFAULT_VALUES_XLSX, data_only=True, read_only=True)
    if country not in wb.sheetnames:
        raise KeyError(f"no sheet {country!r} in default_values.xlsx")
    out = []
    for row in wb[country].iter_rows(min_row=3):
        code_raw = str(row[0].value or "").strip()
        if not re.fullmatch(r"[0-9 ]{4,12}", code_raw):
            continue  # section headers etc.
        out.append(DefaultValue(
            cn_code=code_raw.replace(" ", ""),
            description=str(row[1].value or "").strip(),
            direct=_num(row[2].value),
            indirect=_num(row[3].value),
            total=_num(row[4].value),
            y2026=_num(row[5].value),
            y2027=_num(row[6].value),
            y2028=_num(row[7].value),
            route=str(row[8].value or "").strip(),
        ))
    wb.close()
    return out


def lookup(cn_code: str, country: str = "Taiwan") -> DefaultValue | None:
    """Longest-prefix match: '73181542' -> row '731815' if no exact row exists."""
    cn = cn_code.replace(" ", "")
    rows = load_country(country)
    best: DefaultValue | None = None
    for r in rows:
        if cn.startswith(r.cn_code) and r.direct is not None:
            if best is None or len(r.cn_code) > len(best.cn_code):
                best = r
    return best
