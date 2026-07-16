"""MIG 4.0 e-invoice (電子發票) XML parser — the structured ingestion path.

Per docs/10 §2A / G11: e-GUI is universal since 2021, so the highest-value inputs
(steel & fuel purchases) can be pulled as clean XML with owner consent instead of
OCR. This parser reads F0401-style B2B exchange XML. The VLM path stays for the
rendered 證明聯 (and for firms that only keep paper).
"""
from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path


def _local(tag: str) -> str:
    """Strip XML namespace."""
    return tag.rsplit("}", 1)[-1]


def _find_text(el: ET.Element, path: list[str]) -> str | None:
    cur = el
    for name in path:
        nxt = None
        for child in cur:
            if _local(child.tag) == name:
                nxt = child
                break
        if nxt is None:
            return None
        cur = nxt
    return (cur.text or "").strip() or None


def parse_mig_invoice(path: str | Path) -> dict:
    """Parse one MIG F0401 invoice XML into a flat dict with line items."""
    root = ET.parse(str(path)).getroot()
    main = next((c for c in root if _local(c.tag) == "Main"), None)
    details = next((c for c in root if _local(c.tag) == "Details"), None)
    amount = next((c for c in root if _local(c.tag) == "Amount"), None)
    if main is None:
        raise ValueError(f"{path}: no <Main> element — not a MIG invoice?")

    items = []
    if details is not None:
        for item in details:
            if _local(item.tag) != "ProductItem":
                continue
            items.append({
                "description": _find_text(item, ["Description"]) or "",
                "quantity": _num(_find_text(item, ["Quantity"])),
                "unit": _find_text(item, ["Unit"]) or "",
                "unit_price": _num(_find_text(item, ["UnitPrice"])),
                "amount": _num(_find_text(item, ["Amount"])),
            })

    return {
        "number": _find_text(main, ["InvoiceNumber"]),
        "date": _find_text(main, ["InvoiceDate"]),
        "seller_name": _find_text(main, ["Seller", "Name"]),
        "seller_ban": _find_text(main, ["Seller", "Identifier"]),
        "buyer_name": _find_text(main, ["Buyer", "Name"]),
        "buyer_ban": _find_text(main, ["Buyer", "Identifier"]),
        "items": items,
        "sales_amount": _num(_find_text(amount, ["SalesAmount"])) if amount is not None else None,
        "tax_amount": _num(_find_text(amount, ["TaxAmount"])) if amount is not None else None,
        "total_amount": _num(_find_text(amount, ["TotalAmount"])) if amount is not None else None,
    }


# Categorisation of line items into activity-data buckets ---------------------
STEEL_PAT = re.compile(r"盤元|線材|wire\s*rod|鋼", re.I)
GAS_PAT = re.compile(r"天然氣|瓦斯|natural\s*gas|LNG|LPG|液化石油氣", re.I)
KG_UNITS = {"公斤", "kg", "KG", "Kg"}
M3_UNITS = {"立方公尺", "m3", "M3", "立方米", "度"}


def categorize_item(item: dict) -> str:
    desc = item.get("description") or ""
    if GAS_PAT.search(desc):
        return "gas"
    if STEEL_PAT.search(desc):
        return "steel"
    return "other"


def classify_validate(inv: dict) -> dict:
    """Cross-field sanity checks a verifier would run first."""
    checks, ok = [], True
    if inv["items"] and inv["sales_amount"] is not None:
        s = sum(i["amount"] or 0 for i in inv["items"])
        good = abs(s - inv["sales_amount"]) <= max(1.0, 0.005 * inv["sales_amount"])
        checks.append(f"sum(items)={s} vs SalesAmount={inv['sales_amount']}: {'OK' if good else 'MISMATCH'}")
        ok &= good
    if inv["sales_amount"] is not None and inv["total_amount"] is not None:
        expected = inv["sales_amount"] + (inv["tax_amount"] or 0)
        good = abs(expected - inv["total_amount"]) <= 1.0
        checks.append(f"sales+tax={expected} vs TotalAmount={inv['total_amount']}: {'OK' if good else 'MISMATCH'}")
        ok &= good
    return {"passed": bool(ok), "checks": checks}


def _num(s: str | None) -> float | None:
    if s is None:
        return None
    try:
        return float(s.replace(",", ""))
    except ValueError:
        return None
