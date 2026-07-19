#!/usr/bin/env python3
"""
Pull the full MOENV carbon-footprint emission-coefficient table (dataset CFP_P_02
== data.gov.tw #28176) into data/ef/moenv_coefficients.json.

Design notes (see docs/SOURCES.md §4):
  - Calls the canonical MOENV API directly (NOT the Swagger "Try it out" proxy,
    which 500s). Uppercase DataID, api_key as query param, no `language` param.
  - Paginates with offset/limit until all rows are fetched (the default limit is
    1000 — a single call silently truncates).
  - If the API fails (no key / 500 / network) it keeps any existing snapshot and
    exits non-zero with guidance, so a flaky upstream never blocks the build.
  - Stdlib only (urllib) — no third-party deps required.

Usage:
    python scripts/pull_moenv_ef.py                # uses MOENV_API_KEY from .env / env
    python scripts/pull_moenv_ef.py --limit 1000   # page size
"""
from __future__ import annotations
import argparse, json, os, sys, time, urllib.parse, urllib.request
from pathlib import Path

DATASET = "CFP_P_02"
BASE = f"https://data.moenv.gov.tw/api/v2/{DATASET}"
OUT = Path("data/ef/moenv_coefficients.json")


def load_env_key() -> str | None:
    """Return MOENV_API_KEY from the environment or a local .env (no deps)."""
    key = os.environ.get("MOENV_API_KEY")
    if key:
        return key.strip()
    env = Path(".env")
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("MOENV_API_KEY"):
                _, _, val = line.partition("=")
                return val.strip().strip('"').strip("'") or None
    return None


def fetch_page(api_key: str, offset: int, limit: int) -> dict:
    params = {
        "api_key": api_key,
        "limit": str(limit),
        "offset": str(offset),
        "sort": "ImportDate desc",
        "format": "json",
        # NOTE: do NOT send `language` — the CFP endpoints 500 on it.
    }
    url = f"{BASE}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "carbonpass/0.1"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def records_of(payload) -> list:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        return payload.get("records") or payload.get("data") or []
    return []


def total_of(payload) -> int | None:
    """Return the API-reported total row count, or None if not reported.

    NOTE: the CFP endpoints often return a bare list / no total key. In that
    case we must NOT fake a total from the page length — doing so makes the
    pagination loop stop after one page (the bug that left a truncated
    1000-row snapshot). Pagination then relies on short-page detection.
    """
    if isinstance(payload, dict):
        for k in ("total", "count", "__totalCount"):
            v = payload.get(k)
            if isinstance(v, (int, str)) and str(v).isdigit():
                return int(v)
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=1000)
    ap.add_argument("--max-pages", type=int, default=50)
    args = ap.parse_args()

    OUT.parent.mkdir(parents=True, exist_ok=True)
    api_key = load_env_key()

    if not api_key:
        return bail("No MOENV_API_KEY found (env or .env).")

    all_rows, offset, total, total_seen = [], 0, None, False
    try:
        for page in range(args.max_pages):
            payload = fetch_page(api_key, offset, args.limit)
            rows = records_of(payload)
            if not total_seen:
                total = total_of(payload)
                total_seen = True
                print(f"reported total: {total if total is not None else 'not reported (paginate to short page)'}")
            if not rows:
                break
            all_rows.extend(rows)
            print(f"  page {page}: +{len(rows)} (have {len(all_rows)})")
            offset += args.limit
            if (total is not None and len(all_rows) >= total) or len(rows) < args.limit:
                break
            time.sleep(0.3)
    except Exception as e:  # noqa: BLE001
        return bail(f"API error: {e}")

    if not all_rows:
        return bail("API returned 0 rows (dataset may be empty upstream).")

    OUT.write_text(json.dumps(all_rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK: wrote {len(all_rows)} records -> {OUT}")
    if total and len(all_rows) < total:
        print(f"WARNING: fetched {len(all_rows)} < reported total {total}; raise --max-pages")
    return 0


def bail(msg: str) -> int:
    print(f"[pull_moenv_ef] {msg}", file=sys.stderr)
    if OUT.exists():
        try:
            n = len(json.loads(OUT.read_text(encoding="utf-8")))
            print(f"[pull_moenv_ef] keeping existing snapshot: {OUT} ({n} records)", file=sys.stderr)
        except Exception:
            pass
    print(
        "[pull_moenv_ef] Fallback: download the static file manually and save as "
        f"{OUT}:\n"
        "  https://data.moenv.gov.tw/dataset/detail/CFP_P_02  (歷史資料下載 -> JSON)\n"
        "  or the mirror  https://data.gov.tw/dataset/28176",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
