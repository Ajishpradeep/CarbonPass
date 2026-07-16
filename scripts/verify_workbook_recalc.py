#!/usr/bin/env python3
"""Caveat closure: prove the filled Communication Template recomputes correctly.

openpyxl writes formulas WITHOUT cached values, so any spreadsheet engine that
exports our filled workbook to CSV is forced to actually EVALUATE the template's
formula chain (including the hidden InputOutput array-formula matrix). We export
Summary_Products headlessly via LibreOffice and diff the SEE columns against the
engine's numbers in the .flags.json sidecar.

Pass = the Commission's workbook, filled by our writer, independently computes
the same SEE as our rules engine (which is itself golden-tested against the
Commission's worked example).

Usage:
    python scripts/verify_workbook_recalc.py [out/firm_a_communication_template.xlsx]
Exit 0 on match (rel tol 1e-6), 1 on mismatch/failure.
"""
from __future__ import annotations

import csv
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REL_TOL = 1e-6
SOFFICE_CANDIDATES = [
    "soffice",
    "/Applications/LibreOffice.app/Contents/MacOS/soffice",
]


def find_soffice() -> str | None:
    for cand in SOFFICE_CANDIDATES:
        if shutil.which(cand) or Path(cand).exists():
            return cand
    return None


def export_sheet_csv(soffice: str, xlsx: Path, sheet_index_1based: int, outdir: Path) -> Path:
    """Export one sheet to CSV. Token 5 of the CSV filter = sheet number (1-based)."""
    filter_opts = f'44,34,76,1,,0,false,true,true,false,false,{sheet_index_1based}'
    cmd = [soffice, "--headless", "--norestore",
           "--convert-to", f"csv:Text - txt - csv (StarCalc):{filter_opts}",
           "--outdir", str(outdir), str(xlsx)]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    out = outdir / (xlsx.stem + ".csv")
    if not out.exists():
        raise RuntimeError(f"soffice export failed: {r.stdout}\n{r.stderr}")
    return out


def main() -> int:
    xlsx = Path(sys.argv[1] if len(sys.argv) > 1 else "out/firm_a_communication_template.xlsx")
    sidecar = xlsx.with_suffix(".flags.json")
    if not xlsx.exists() or not sidecar.exists():
        print(f"[recalc] missing {xlsx} or sidecar — run `carbonpass pack` first", file=sys.stderr)
        return 1
    soffice = find_soffice()
    if soffice is None:
        print("[recalc] LibreOffice (soffice) not found — install with "
              "`brew install --cask libreoffice`", file=sys.stderr)
        return 1

    expected = json.loads(sidecar.read_text(encoding="utf-8"))["products"]

    # Sheet order is fixed by the template: Summary_Products is sheet 13 (1-based).
    import openpyxl
    wb = openpyxl.load_workbook(xlsx, read_only=True)
    sheet_no = wb.sheetnames.index("Summary_Products") + 1
    n_sheets = len(wb.sheetnames)
    wb.close()

    with tempfile.TemporaryDirectory() as td:
        csv_path = export_sheet_csv(soffice, xlsx, sheet_no, Path(td))
        rows = list(csv.reader(csv_path.open(encoding="utf-8")))

    # Row 10 in the workbook == rows[9]; columns: D=3 name, F=5 CN, I=8 dir, J=9 ind,
    # K=10 total, O=14 embedded electricity (0-based CSV indices).
    def num(row, col):
        try:
            return float(rows[row][col])
        except (ValueError, IndexError):
            return None

    print(f"[recalc] {xlsx.name}: {n_sheets} sheets; Summary_Products exported via LibreOffice")
    failures = 0
    for i, prod in enumerate(expected):
        r = 9 + i
        got = {
            "product": rows[r][3] if len(rows[r]) > 3 else "",
            "cn": rows[r][5] if len(rows[r]) > 5 else "",
            "see_direct": num(r, 8),
            "see_indirect": num(r, 9),
            "see_total": num(r, 10),
            "embedded_elec": num(r, 14),
        }
        want = {
            "see_direct": prod["see_direct"]["value"],
            "see_indirect": prod["see_indirect"]["value"],
            "see_total": prod["see_total"]["value"],
            "embedded_elec": prod["embedded_electricity_mwh_per_t"]["value"],
        }
        print(f"  row {10 + i}: {got['product']!r} CN {got['cn']}")
        for k, w in want.items():
            g = got[k]
            ok = g is not None and (abs(g - w) <= REL_TOL * max(abs(w), 1e-12))
            status = "OK " if ok else "FAIL"
            print(f"    {status} {k:14} workbook={g!r:<24} engine={w!r}")
            failures += 0 if ok else 1

    if failures:
        print(f"[recalc] MISMATCH: {failures} value(s) differ — writer or engine bug", file=sys.stderr)
        return 1
    print("[recalc] PASS: workbook formulas independently reproduce the engine's SEE "
          f"(rel tol {REL_TOL}). Caveat closed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
