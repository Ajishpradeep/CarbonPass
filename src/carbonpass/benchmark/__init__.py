"""Sight ④ — the anonymised cluster benchmark ("Am I normal?").

First of its kind for the fastener cluster; the sector-scale reduction
multiplier (docs/PROJECT.md §2). Local-first discipline: firm-level rows NEVER leave
the device — only aggregates with n ≥ 5 firms may be exported (k-anonymity
floor, docs/archive/21 §1.4). The schema doubles as the open-data give-back spec.
"""
from carbonpass.benchmark.schema import BenchmarkRow, K_ANONYMITY_FLOOR
from carbonpass.benchmark.percentile import percentile_screen, seed_distribution
from carbonpass.benchmark.export import export_rows

__all__ = ["BenchmarkRow", "K_ANONYMITY_FLOOR", "percentile_screen",
           "seed_distribution", "export_rows"]
