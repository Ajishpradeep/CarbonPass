"""Aggregate-only export with the k ≥ 5 anonymity floor — the give-back path.

Firm-level data never leaves the device (local-first, docs/21 §1.4). What CAN
leave is a list of BenchmarkRow aggregates, and only those with n_firms ≥ 5.
Publishing a row below the floor requires the owner's explicit sign-off AND a
schema change — i.e. it cannot happen here.
"""
from __future__ import annotations

import json
from pathlib import Path

from carbonpass.benchmark.schema import K_ANONYMITY_FLOOR, BenchmarkRow


class KAnonymityError(ValueError):
    """Raised when an export would publish a row aggregating fewer than 5 firms."""


def export_rows(rows: list[BenchmarkRow], out_path: str | Path) -> Path:
    """Write exportable rows as JSON. Raises on ANY row below the floor —
    silently dropping would hide a policy violation; refusing surfaces it."""
    bad = [r for r in rows if not r.exportable]
    if bad:
        raise KAnonymityError(
            f"{len(bad)} row(s) aggregate fewer than {K_ANONYMITY_FLOOR} firms "
            f"(e.g. {bad[0].sector}/{bad[0].cn_prefix} n={bad[0].n_firms}) — "
            f"k-anonymity floor is a hard rule (docs/21 §1.4); collect more firms "
            f"or widen the aggregation bucket")
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "spec": "schema/benchmark_row.schema.json",
        "k_anonymity_floor": K_ANONYMITY_FLOOR,
        "rows": [r.as_dict() for r in rows],
    }
    out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return out_path
