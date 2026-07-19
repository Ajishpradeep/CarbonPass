"""Sight ② — the material-waste map (docs/18 §3).

The pile is visible; the information is not. This package turns the same
documents that file the CBAM pack (steel e-invoices + production log) into
per-line yield, monthly drift, and money stated gross AND net — enforced in
types, not in prose (docs/21 §2.5).
"""
from carbonpass.waste.money import MoneyLoss
from carbonpass.waste.scan import render, scan
from carbonpass.waste.drift import drift_alerts, monthly_series

__all__ = ["MoneyLoss", "scan", "render", "monthly_series", "drift_alerts"]
