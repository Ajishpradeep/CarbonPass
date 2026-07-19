"""Taipower time-of-use tariff model (高壓電力三段式) — shared by scheduler + corpus.

Stylized from the published rate schedule (taipower.com.tw rate-table hub;
re-verify the current table before submission — flagged in docs/archive/10 §5.2).
Summer = 16 May – 15 Oct (we approximate by month: Jun–Sep in the corpus).

Weekday banding (three-段式):
    peak      16:00–22:00 summer / 15:00–21:00 non-summer (weekdays)
    half-peak 09:00–16:00 + 22:00–24:00 summer; 06:00–15:00 + 21:00–24:00 non-summer
    off-peak  everything else + weekends (Saturday partly half-peak — simplified
              to off-peak here; refine at pilot with the real calendar)
"""
from __future__ import annotations

RATES = {
    "summer": {"peak": 9.39, "half": 5.85, "off": 2.53},
    "nonsummer": {"peak": 8.63, "half": 5.44, "off": 2.32},
    "capacity_ntd_per_kw": 236.2,
}


def season_of_month(month: int) -> str:
    return "summer" if 6 <= month <= 9 else "nonsummer"


def band_of_hour(hour_of_week: int, season: str) -> str:
    """TOU band for an hour index in a Mon-00:00-anchored week."""
    dow, hod = divmod(hour_of_week, 24)
    if dow >= 5:                      # weekend
        return "off"
    if season == "summer":
        if 16 <= hod < 22:
            return "peak"
        if 9 <= hod < 16 or 22 <= hod < 24:
            return "half"
        return "off"
    if 15 <= hod < 21:
        return "peak"
    if 6 <= hod < 15 or 21 <= hod < 24:
        return "half"
    return "off"


def price_curve(hours: int = 168, month: int = 7) -> list[float]:
    """NT$/kWh for each hour of the horizon (week anchored on Monday 00:00)."""
    season = season_of_month(month)
    r = RATES[season]
    return [r[{"peak": "peak", "half": "half", "off": "off"}[band_of_hour(h % 168, season)]]
            for h in range(hours)]
