"""Hourly Taiwan grid carbon intensity from Taipower's open generation feed.

Source: 各機組發電量 (generation by unit, 10-minute) — data.gov.tw #8931; the
underlying JSON lives on Taipower's open-data host. We aggregate unit-level MW
by fuel type and convert to gCO2e/kWh with per-fuel emission factors, yielding
the hourly intensity curve Module 2 schedules against.

Per-fuel generation EFs (kgCO2e/kWh, lifecycle-light/combustion-focused —
documented sources; refine with MOENV data at pilot):
    coal 0.912 / gas 0.389 / oil 0.750 / diesel 0.700  (typical thermal plant
    combustion factors, consistent with Taipower's published fleet averages)
    nuclear, hydro, wind, solar, geothermal, storage ~ 0 (combustion basis)
    co-gen 0.60 (mixed fuels)  / IPP coal & gas same as fuel class
Sanity anchor: the demand-weighted mean of our curve must land in the same
range as the official annual average grid EF (data/ef/grid_ef.yaml; 2025 overall 0.467).

Offline-safe: every successful fetch is cached to data/grid/; tests and offline
runs read the cache (or the committed fixture in tests/fixtures/).
"""
from __future__ import annotations

import json
import re
import time
from pathlib import Path

import httpx

from carbonpass.config import DATA_DIR

GRID_CACHE = DATA_DIR / "grid"

# Known layouts of the Taipower "genary" open-data file (checked at runtime).
FEED_URLS = [
    "https://service.taipower.com.tw/data/opendata/apply/file/d006001/001.json",
    "https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/genary.json",
]

FUEL_EF = {  # kgCO2e/kWh by fuel bucket
    "coal": 0.912, "ipp-coal": 0.912, "gas": 0.389, "ipp-gas": 0.389,
    "oil": 0.750, "diesel": 0.700, "cogen": 0.600,
    "nuclear": 0.0, "hydro": 0.0, "wind": 0.0, "solar": 0.0,
    "geothermal": 0.0, "storage": 0.0, "othergreen": 0.0, "pumped": 0.0,
}

# zh-TW fuel labels in the feed -> our buckets
FUEL_MAP = {
    "燃煤": "coal", "汽電共生": "cogen", "民營電廠-燃煤": "ipp-coal",
    "燃氣": "gas", "民營電廠-燃氣": "ipp-gas", "燃油": "oil", "輕油": "diesel",
    "核能": "nuclear", "水力": "hydro", "風力": "wind", "太陽能": "solar",
    "地熱": "geothermal", "儲能": "storage", "其它再生能源": "othergreen",
    "抽蓄發電": "pumped", "抽蓄負載": "storage", "曾文水庫": "hydro",
}


def _bucket(fuel_label: str) -> str | None:
    for key, bucket in FUEL_MAP.items():
        if key in fuel_label:
            return bucket
    return None


def fetch_snapshot(timeout: float = 20.0) -> dict | None:
    """One live 10-min snapshot {bucket: MW}. None if offline/unreachable."""
    for url in FEED_URLS:
        try:
            r = httpx.get(url, timeout=timeout, follow_redirects=True,
                          headers={"User-Agent": "carbonpass/0.1"})
            if r.status_code != 200:
                continue
            data = json.loads(r.content.decode("utf-8-sig"))  # feed ships a BOM
            rows = data.get("aaData") or data.get("data") or []
            feed_ts = data.get("DateTime")
            mw_by_bucket: dict[str, float] = {}
            for row in rows:
                if isinstance(row, dict):
                    # d006001 layout: {機組類型, 機組名稱, 裝置容量(MW), 淨發電量(MW), ...}
                    label = re.sub(r"<[^>]+>", "", str(row.get("機組類型", "")))
                    raw_mw = row.get("淨發電量(MW)", "")
                else:
                    # legacy genary layout: [fuel_label(html), unit, capacity, net_MW, ...]
                    label = re.sub(r"<[^>]+>", "", str(row[0]))
                    raw_mw = row[3] if len(row) > 3 else ""
                bucket = _bucket(label)
                if bucket is None:
                    continue
                try:
                    mw = float(str(raw_mw).replace(",", ""))
                except ValueError:
                    continue
                if mw > 0:
                    mw_by_bucket[bucket] = mw_by_bucket.get(bucket, 0.0) + mw
            if mw_by_bucket:
                snap = {"ts": feed_ts or time.strftime("%Y-%m-%dT%H:%M:%S"),
                        "source": url, "mw_by_fuel": mw_by_bucket}
                GRID_CACHE.mkdir(parents=True, exist_ok=True)
                (GRID_CACHE / "latest_snapshot.json").write_text(
                    json.dumps(snap, ensure_ascii=False, indent=1), encoding="utf-8")
                return snap
        except Exception:  # noqa: BLE001 — offline-safe by design
            continue
    return None


def _official_annual_ef() -> "GridEF":
    """Offline fallback / sanity comparator: the official annual OVERALL factor
    (the generation-mix comparator; the industrial split is for factory Scope-2)."""
    from carbonpass.rules.gridef import load_grid_ef
    sel = load_grid_ef()          # default year from config
    return load_grid_ef(sel.year, "overall")


def intensity_of(mw_by_fuel: dict[str, float]) -> float:
    """kgCO2e/kWh of a generation mix."""
    total = sum(mw_by_fuel.values())
    if total <= 0:
        return _official_annual_ef().kgco2e_per_kwh
    return sum(mw * FUEL_EF.get(b, 0.5) for b, mw in mw_by_fuel.items()) / total


# A typical Taiwan diurnal intensity SHAPE (relative to daily mean), used to
# expand a single live snapshot (or the offline fallback) into an hourly curve:
# solar depresses midday intensity; evening peak leans on gas/coal.
DIURNAL_SHAPE = [1.06, 1.07, 1.07, 1.07, 1.06, 1.04, 1.00, 0.94, 0.88, 0.83,
                 0.80, 0.79, 0.79, 0.80, 0.83, 0.88, 0.95, 1.03, 1.09, 1.11,
                 1.10, 1.09, 1.08, 1.07]


def hourly_curve(hours: int = 168) -> dict:
    """Hourly intensity curve (kgCO2e/kWh) for the scheduling horizon.

    Anchor = live snapshot intensity if reachable, else cached, else the official
    annual overall EF from data/ef/grid_ef.yaml; shaped by the diurnal profile.
    At pilot this is replaced by a curve integrated from continuously logged
    10-min feeds (#37331 backfill).
    """
    snap = fetch_snapshot()
    if snap is None:
        cache = GRID_CACHE / "latest_snapshot.json"
        if cache.exists():
            snap = json.loads(cache.read_text(encoding="utf-8"))
    official = _official_annual_ef()
    anchor = intensity_of(snap["mw_by_fuel"]) if snap else official.kgco2e_per_kwh
    mean_shape = sum(DIURNAL_SHAPE) / 24
    curve = [round(anchor * DIURNAL_SHAPE[h % 24] / mean_shape, 4) for h in range(hours)]
    return {
        "anchor_kgco2_per_kwh": round(anchor, 4),
        "anchor_source": (snap or {}).get("source", f"offline fallback: {official.provenance}"),
        "anchor_ts": (snap or {}).get("ts"),
        "hourly_kgco2_per_kwh": curve,
        "note": "single-snapshot anchor × diurnal shape; pilot upgrade = integrate "
                "logged 10-min feed (#8931/#37331) into a true historical curve",
        "sanity_vs_official_annual": {"ratio": round(anchor / official.kgco2e_per_kwh, 3),
                                      "reference": official.provenance},
    }
