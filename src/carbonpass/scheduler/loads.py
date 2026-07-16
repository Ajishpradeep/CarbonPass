"""Factory load model: which machines can shift, and the baseline week.

Built from the firm's onboarding machine list (firm.json / activity JSON).
Flexible = batch processes whose completion, not timing, is contractual:
heat-treatment furnaces (thermal inertia + batch queues) and compressors
(with buffer tanks) — plating lines are semi-flexible but kept FIXED here
(chemistry stability), formers/rollers/drawers are production-paced = FIXED.
The owner's real constraints (order deadlines) arrive via LINE at pilot;
the PoC uses Mon–Sat around the clock (fastener heat-treatment genuinely runs
nights — ~5,800 h/yr — which is precisely what makes it shiftable into
off-peak hours).
"""
from __future__ import annotations

from dataclasses import dataclass

FLEXIBLE_PAT = ("熱處理", "furnace", "壓縮", "compressor", "空壓")


@dataclass
class Load:
    name: str
    kw: float
    weekly_kwh: float          # energy that must be delivered per week
    flexible: bool
    window: tuple[int, int] = (0, 24)   # allowed hours-of-day for flexible loads
    weekdays_only_plus_sat: bool = True # Sunday off (maintenance/labor)


def loads_from_machines(machines: list[dict], weeks_per_year: float = 50.0) -> list[Load]:
    out = []
    for m in machines:
        name = m.get("name") or m.get("name_en") or m.get("name_zh", "machine")
        zh = m.get("name_zh", "") or ""
        flexible = any(p.lower() in (name + zh).lower() for p in FLEXIBLE_PAT)
        weekly_kwh = m["kw"] * m["hours"] / weeks_per_year
        out.append(Load(name=name, kw=float(m["kw"]), weekly_kwh=weekly_kwh,
                        flexible=flexible))
    return out


def baseline_profile(loads: list[Load], hours: int = 168) -> list[float]:
    """Status-quo weekly kW profile: everything runs flat Mon–Sat around the
    clock (how un-scheduled multi-shift factories actually operate) — i.e.
    price- and carbon-blind."""
    profile = [0.0] * hours
    work_hours = [h for h in range(hours) if (h // 24) < 6]
    for load in loads:
        per_hour = load.weekly_kwh / len(work_hours)
        for h in work_hours:
            profile[h] += per_hour
    return profile
