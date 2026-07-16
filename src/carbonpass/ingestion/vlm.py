"""Ollama VLM client — qwen3-vl document extraction with per-field confidence.

Local-first: images never leave the machine; Ollama serves the model on-prem.
Each document type gets a targeted prompt that requests our JSON structure.
"""
from __future__ import annotations

import base64
import json
from pathlib import Path

import httpx

from carbonpass.config import OLLAMA_HOST, OLLAMA_MODEL

TIMEOUT = httpx.Timeout(600.0, connect=10.0)

BILL_PROMPT = """\
You are reading a Taiwanese Taipower electricity bill (電費通知單, Traditional Chinese).
Extract these fields and return ONLY a JSON object (no prose):
{
 "electricity_no": "電號 exactly as printed",
 "billing_year": <western year. 計費年月 prints the ROC (民國) year: ADD 1911. Example: 計費年月 115年07月 -> billing_year 2026, billing_month 7>,
 "billing_month": <1-12>,
 "contract_capacity_kw": <契約容量 in 瓩/kW>,
 "kwh_peak": <尖峰 度數>,
 "kwh_half_peak": <半尖峰 度數>,
 "kwh_off_peak": <離峰 度數>,
 "kwh_total": <合計 度數>,
 "total_ntd": <本期電費總計 in 元>,
 "confidence": {"<field>": <0..1 confidence for every field above>}
}
Numbers must be plain numbers without commas. If a field is absent use null.
"""

INVOICE_PROMPT = """\
You are reading a Taiwanese electronic invoice certificate (電子發票證明聯, Traditional Chinese).
Extract and return ONLY a JSON object:
{
 "number": "invoice number, e.g. AB12345678",
 "date": "YYYYMMDD",
 "seller_name": "...", "seller_ban": "8-digit 統一編號",
 "buyer_name": "...", "buyer_ban": "8-digit 統一編號",
 "items": [{"description": "...", "quantity": <n>, "unit": "...", "unit_price": <n>, "amount": <n>}],
 "sales_amount": <銷售額合計>, "tax_amount": <營業稅>, "total_amount": <總計>,
 "confidence": {"<field>": <0..1>}
}
Numbers plain, no commas. Missing -> null.
"""

PRODLOG_PROMPT = """\
You are reading a factory production log summary (生產日誌彙總, Traditional Chinese).
It lists monthly production tonnes per CN product code, and a machine table
(機台 / 額定功率 kW / 年運轉時數 h / 所屬產線).
Return ONLY a JSON object:
{
 "monthly_production": [{"month": <1-12>, "<cn_code>": <tonnes>, ...}, ...],
 "totals_by_cn": {"<cn_code>": <tonnes>},
 "machines": [{"name": "...", "kw": <n>, "hours": <n>, "process": "...|shared"}],
 "confidence": {"monthly_production": <0..1>, "machines": <0..1>}
}
"""

PROMPTS = {
    "taipower_bill": BILL_PROMPT,
    "egui_invoice": INVOICE_PROMPT,
    "production_log": PRODLOG_PROMPT,
}


def ollama_available(host: str | None = None) -> bool:
    try:
        r = httpx.get(f"{host or OLLAMA_HOST}/api/version", timeout=3.0)
        return r.status_code == 200
    except Exception:
        return False


def _b64(image_path: Path) -> str:
    return base64.b64encode(image_path.read_bytes()).decode()


def extract_from_image(image_path: str | Path, doc_type: str,
                       context_text: str | None = None,
                       model: str | None = None) -> dict:
    """One image -> extracted JSON dict (validated json, not schema-validated yet)."""
    image_path = Path(image_path)
    prompt = PROMPTS[doc_type]
    if context_text:
        prompt += ("\nFor cross-checking, a layout pre-pass read this text on the page "
                   "(may contain OCR errors):\n" + context_text[:4000])
    payload = {
        "model": model or OLLAMA_MODEL,
        "messages": [{"role": "user", "content": prompt, "images": [_b64(image_path)]}],
        "format": "json",
        "stream": False,
        # num_ctx: instructions + docling context (~1k tokens) + image tokens
        # overflow Ollama's 4096 default; 8192 keeps the whole prompt visible.
        "options": {"temperature": 0, "num_ctx": 8192},
    }
    r = httpx.post(f"{OLLAMA_HOST}/api/chat", json=payload, timeout=TIMEOUT)
    r.raise_for_status()
    content = r.json()["message"]["content"]
    return json.loads(content)
