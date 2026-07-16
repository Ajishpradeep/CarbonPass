"""Field-level scoring of extracted document fields vs corpus ground truth.

Shared by the ingestion accuracy report and the Sprint-1 VLM bake-off.
"""
from __future__ import annotations

BILL_FIELDS = ["kwh_peak", "kwh_half_peak", "kwh_off_peak", "kwh_total",
               "total_ntd", "contract_capacity_kw"]
INVOICE_FIELDS = ["sales_amount", "tax_amount", "total_amount", "number", "seller_ban"]


def field_ok(got, want, rel: float = 0.002) -> bool:
    if want is None:
        return got is None
    if isinstance(want, (int, float)):
        return isinstance(got, (int, float)) and abs(got - want) <= max(1.0, rel * abs(want))
    return str(got).strip() == str(want).strip()


def score_fields(fields: dict, expected: dict, names: list[str]) -> dict:
    """Return {field: bool} for fields present in expected."""
    out = {}
    for name in names:
        if name in expected and expected[name] is not None:
            out[name] = field_ok(fields.get(name), expected[name])
    return out
