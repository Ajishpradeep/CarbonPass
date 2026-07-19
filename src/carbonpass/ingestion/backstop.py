"""Numeric backstop: cross-check VLM-extracted numbers against layout-OCR text.

Defense-in-depth on the figures a verifier scrutinizes (docs/archive/10 §6.1): the VLM
reads the document as an image; independently, docling's OCR stage (PaddleOCR
PP-OCRv4 recognition models served via RapidOCR/ONNX) reads it as text. A number
the VLM returns that appears NOWHERE in the OCR text is suspect — hallucinated,
misread, or transposed — and gets flagged for human/verifier attention instead
of flowing silently into the pack.

(The full PaddleOCR-VL model is the blueprint's eventual backstop; it needs a
GPU environment. Same model family, same role — documented in docs/archive/13.)
"""
from __future__ import annotations

import re

# fields we cross-check per document type (numeric, verifier-relevant)
NUMERIC_FIELDS = {
    "taipower_bill": ["kwh_peak", "kwh_half_peak", "kwh_off_peak", "kwh_total",
                      "total_ntd", "contract_capacity_kw"],
    "egui_invoice": ["sales_amount", "tax_amount", "total_amount"],
}

_NUM_PAT = re.compile(r"\d[\d,，.]*\d|\d")


def numbers_in_text(text: str) -> set[str]:
    """All numbers in OCR text, normalized to plain digit strings (no separators)."""
    out = set()
    for m in _NUM_PAT.findall(text):
        norm = m.replace(",", "").replace("，", "")
        out.add(norm)
        # OCR text often keeps decimals; index the integer part too
        if "." in norm:
            out.add(norm.split(".", 1)[0])
    return out


def check_fields(doc_type: str, fields: dict, ocr_text: str | None) -> dict | None:
    """Cross-check numeric fields against OCR text. None if no OCR available."""
    if not ocr_text:
        return None
    ocr_numbers = numbers_in_text(ocr_text)
    checked, mismatched = [], []
    for name in NUMERIC_FIELDS.get(doc_type, []):
        v = fields.get(name)
        if not isinstance(v, (int, float)):
            continue
        forms = {str(int(v)) if float(v).is_integer() else str(v)}
        if float(v).is_integer():
            forms.add(f"{int(v)}")
        found = any(f in ocr_numbers for f in forms)
        checked.append(name)
        if not found:
            mismatched.append({"field": name, "vlm_value": v,
                               "note": "value not present in layout-OCR text"})
    return {
        "engine": "PP-OCRv4 (PaddleOCR rec models via docling/RapidOCR)",
        "fields_checked": checked,
        "mismatches": mismatched,
        "passed": not mismatched,
    }


def apply_to_document(doc: dict, ocr_text: str | None) -> None:
    """Attach a backstop report to a pipeline document dict and downgrade
    confidence on mismatched fields (0.25 cap => quantity uncertainty widens)."""
    report = check_fields(doc["type"], doc["fields"], ocr_text)
    if report is None:
        return
    doc.setdefault("validation", {})["backstop"] = report
    if not report["passed"]:
        doc["validation"]["passed"] = False
        conf = doc.setdefault("confidence", {})
        for mm in report["mismatches"]:
            conf[mm["field"]] = min(conf.get(mm["field"], 1.0), 0.25)
