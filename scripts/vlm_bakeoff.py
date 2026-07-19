#!/usr/bin/env python3
"""Sprint-1 VLM bake-off: {model} × {degradation} × {±docling context} on the corpus.

Measures field-level extraction accuracy vs corpus ground truth on the Taipower
bill task (the pure photo-parse path — invoices have the structured XML route).
Outputs incremental JSON (resumable) + a markdown table for docs/archive/13.

Usage:
    python scripts/vlm_bakeoff.py --models qwen3-vl:8b-instruct,qwen3-vl:4b-instruct \
        --bills 4 --variants clean,rot,blur,dark,jpeg,warp,combo [--with-context both]
Notes:
    * degraded images must exist: run scripts/degrade_corpus.py first
    * each (model, variant, context) cell = N bills; per-cell accuracy = correct/total fields
    * resumable: existing (model,variant,context,bill) results in out/bakeoff/results.json
      are skipped, so the matrix can be extended incrementally
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from carbonpass.ingestion.scoring import BILL_FIELDS, score_fields  # noqa: E402
from carbonpass.ingestion import backstop  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
CORPUS = REPO / "data" / "mock_corpus"
OUT = REPO / "out" / "bakeoff"
RESULTS = OUT / "results.json"


def bill_paths(firm: str, variant: str, n: int) -> list[Path]:
    src = (CORPUS / firm / "bills") if variant == "clean" else (CORPUS / "degraded" / firm / variant)
    # spread across seasons: take every 3rd month first
    all_pngs = sorted(src.glob("taipower_*.png"))
    picked = all_pngs[::max(1, len(all_pngs) // n)][:n]
    return picked


def run_cell(model: str, variant: str, use_context: bool, firm: str, n_bills: int,
             expected_by_month: dict, results: dict) -> None:
    from carbonpass.ingestion.vlm import extract_from_image
    from carbonpass.ingestion.docling_pass import layout_text

    for png in bill_paths(firm, variant, n_bills):
        key = f"{model}|{variant}|{'ctx' if use_context else 'noctx'}|{png.name}"
        if key in results["cells"]:
            continue
        t0 = time.time()
        try:
            context = layout_text(png) if use_context else None
            fields = extract_from_image(png, "taipower_bill", context_text=context, model=model)
            fields.pop("confidence", None)
            month = fields.get("billing_month")
            exp = expected_by_month.get(int(month)) if isinstance(month, (int, float)) else None
            if exp is None:
                # month itself misread — score all fields as wrong vs the file's true month
                true_month = int(png.stem.split("_")[-1])
                exp = expected_by_month[true_month]
            scores = score_fields(fields, exp, BILL_FIELDS)
            bs = backstop.check_fields("taipower_bill", fields, context) if use_context else None
            cell = {
                "ok": sum(scores.values()), "tot": len(scores),
                "wrong": [f for f, v in scores.items() if not v],
                "seconds": round(time.time() - t0, 1),
                "backstop_flags": [m["field"] for m in bs["mismatches"]] if bs else None,
            }
        except Exception as e:  # noqa: BLE001 — a failed call is a scored failure, not a crash
            cell = {"ok": 0, "tot": len(BILL_FIELDS), "wrong": ["<error>"],
                    "seconds": round(time.time() - t0, 1), "error": f"{type(e).__name__}: {e}"}
        results["cells"][key] = cell
        RESULTS.write_text(json.dumps(results, indent=1), encoding="utf-8")
        print(f"  {key}: {cell['ok']}/{cell['tot']} ({cell['seconds']}s)"
              + (f" wrong={cell['wrong']}" if cell["wrong"] else ""), flush=True)


def summarize(results: dict) -> str:
    agg: dict[tuple, list] = {}
    for key, cell in results["cells"].items():
        model, variant, ctx, _ = key.split("|", 3)
        agg.setdefault((model, variant, ctx), []).append(cell)
    lines = ["| model | variant | context | bills | field acc | avg s/doc |",
             "|---|---|---|---|---|---|"]
    for (model, variant, ctx), cells in sorted(agg.items()):
        ok = sum(c["ok"] for c in cells)
        tot = sum(c["tot"] for c in cells)
        secs = sum(c["seconds"] for c in cells) / len(cells)
        lines.append(f"| {model} | {variant} | {ctx} | {len(cells)} | "
                     f"**{ok}/{tot} ({ok / tot:.0%})** | {secs:.0f} |")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default="qwen3-vl:8b-instruct")
    ap.add_argument("--firm", default="firm_a")
    ap.add_argument("--bills", type=int, default=4)
    ap.add_argument("--variants", default="clean,rot,blur,dark,jpeg,warp,combo")
    ap.add_argument("--with-context", choices=["yes", "no", "both"], default="no",
                    help="docling context is slow; default no (pure-photo robustness)")
    args = ap.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    results = json.loads(RESULTS.read_text(encoding="utf-8")) if RESULTS.exists() else {"cells": {}}

    gt = json.loads((CORPUS / "ground_truth.json").read_text(encoding="utf-8"))
    expected_by_month = {b["month"]: b for b in
                         gt["firms"][args.firm]["expected_extractions"]["bills"]}

    ctx_opts = {"yes": [True], "no": [False], "both": [False, True]}[args.with_context]
    for model in args.models.split(","):
        for variant in args.variants.split(","):
            for use_ctx in ctx_opts:
                print(f"=== {model} × {variant} × {'ctx' if use_ctx else 'noctx'} ===", flush=True)
                run_cell(model, variant, use_ctx, args.firm, args.bills,
                         expected_by_month, results)

    md = summarize(results)
    (OUT / "summary.md").write_text(md + "\n", encoding="utf-8")
    print("\n" + md)
    print(f"\nresults: {RESULTS}\nsummary: {OUT / 'summary.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
