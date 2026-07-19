"""Thin CLI wrapper around carbonpass.waste (the productized module — docs/21 §1.2).

Run:  uv run python scripts/waste_scan.py out/firm_a_activity.json data/mock_corpus/firm_a
Out:  out/waste/<firm>_waste.json (+ drift series) + printed summary
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

from carbonpass.waste import monthly_series, render, scan


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print(__doc__)
        return 2
    activity_path, firm_dir = argv[1], argv[2]
    r = scan(activity_path, firm_dir)
    activity = json.load(open(activity_path, encoding="utf-8"))
    r["drift"] = monthly_series(firm_dir, activity)
    print(render(r))
    for line in r["drift"]["lines"]:
        for a in line["alerts"]:
            print(f"  {a['message_zh']}")
    out = Path("out/waste") / f"{Path(activity_path).stem.replace('_activity', '')}_waste.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nJSON -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
