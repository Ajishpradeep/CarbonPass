"""Numeric backstop tests — including the injected-error catch-rate check."""
from __future__ import annotations

from carbonpass.ingestion.backstop import check_fields, numbers_in_text

OCR_TEXT = """台灣電力股份有限公司 電費通知單
尖峰 11,149 9.39 104,689
半尖峰 18,019 5.85 105,411
離峰 28,408 2.53 71,872
合計 57,576
契約容量: 499 瓩
本期電費總計: 393,838 元"""


def test_numbers_normalized():
    nums = numbers_in_text(OCR_TEXT)
    assert {"11149", "18019", "28408", "57576", "499", "393838"} <= nums
    assert "9.39" in nums and "9" in nums   # decimal + integer part indexed


def test_correct_fields_pass():
    fields = {"kwh_peak": 11149, "kwh_half_peak": 18019, "kwh_off_peak": 28408,
              "kwh_total": 57576, "total_ntd": 393838, "contract_capacity_kw": 499}
    report = check_fields("taipower_bill", fields, OCR_TEXT)
    assert report["passed"] and not report["mismatches"]
    assert len(report["fields_checked"]) == 6


def test_injected_errors_are_caught():
    """3 wrong-digit injections (misread/transposed/hallucinated) must all fire."""
    fields = {"kwh_peak": 11146,        # last digit misread (9->6)
              "kwh_half_peak": 18091,   # transposition (19->91)
              "kwh_off_peak": 28408,    # correct
              "kwh_total": 57576,       # correct
              "total_ntd": 493838,      # leading digit hallucinated (3->4)
              "contract_capacity_kw": 499}
    report = check_fields("taipower_bill", fields, OCR_TEXT)
    caught = {m["field"] for m in report["mismatches"]}
    assert caught == {"kwh_peak", "kwh_half_peak", "total_ntd"}
    assert not report["passed"]


def test_confidence_downgrade_on_mismatch():
    from carbonpass.ingestion.backstop import apply_to_document

    doc = {"type": "taipower_bill",
           "fields": {"kwh_peak": 99999, "kwh_total": 57576},
           "confidence": {"kwh_peak": 0.98},
           "validation": {"passed": True, "checks": []}}
    apply_to_document(doc, OCR_TEXT)
    assert doc["validation"]["backstop"]["passed"] is False
    assert doc["confidence"]["kwh_peak"] <= 0.25
    assert doc["validation"]["passed"] is False


def test_no_ocr_text_is_none():
    assert check_fields("taipower_bill", {"kwh_peak": 1}, None) is None
