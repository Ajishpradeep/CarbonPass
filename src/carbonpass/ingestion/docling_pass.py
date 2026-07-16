"""Docling layout pre-pass: PDF/image -> plain text + tables for VLM cross-checking.

Degrades gracefully: if docling (or its model downloads) are unavailable, returns
None and the VLM runs on the raw image alone.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path


@lru_cache(maxsize=1)
def _converter():
    try:
        from docling.document_converter import DocumentConverter

        return DocumentConverter()
    except Exception as e:  # noqa: BLE001 — any import/model failure -> skip pre-pass
        print(f"[docling] unavailable ({e.__class__.__name__}: {e}) — VLM-only path")
        return None


def layout_text(path: str | Path) -> str | None:
    """Return the document's text in reading order, or None if docling unavailable."""
    conv = _converter()
    if conv is None:
        return None
    try:
        result = conv.convert(str(path))
        return result.document.export_to_markdown()
    except Exception as e:  # noqa: BLE001
        print(f"[docling] convert failed for {path}: {e} — VLM-only path")
        return None
