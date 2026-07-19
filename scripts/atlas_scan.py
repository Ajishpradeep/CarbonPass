"""Provability Atlas — scan the adopted CBAM default tables across every country.

Produces the evidence for docs/14 §5 (ASEAN + South Asia) and the "who is in the
book" coverage map (docs/14 §2, claim 9), using the existing rules engine with no
modifications:

    load_country()  -> parses one country sheet (IR 2025/2621, "DVs as adopted")
    lookup()        -> longest-prefix CN match within a country

Two things this script deliberately does NOT do:
  * it reports STEEL and ALUMINIUM only, because the engine's mark-up handling is
    wrong for cement/fertiliser (docs/15 §6 bugs 1-2: the workbook's marked-up
    column is TOTAL-based, and fertiliser carries a flat 1% not 10/20/30);
  * it never claims a country is "unlisted" from a missing VALUE — only from a
    missing ROW, which is how the fallback is actually reached.

Run:  uv run python scripts/atlas_scan.py
Out:  out/atlas/{coverage.json,asean_south_asia.json,summary.md}
"""
from __future__ import annotations

import json
import statistics
from pathlib import Path

import openpyxl

from carbonpass.config import DEFAULT_VALUES_XLSX
from carbonpass.prices import certificate_price
from carbonpass.rules import defaults

FALLBACK_SHEET = "_Other Countries and Territorie"

# Owner decision (docs/14 §1): ASEAN + South Asia foreground — New Southbound.
# Taiwan included as the origin/lab; fallback included as the floor everyone
# without a book falls to.
FOCUS = [
    "Taiwan",
    # ASEAN
    "Vietnam", "Thailand", "Philippines", "Indonesia", "Malaysia",
    "Singapore", "Cambodia", "Myanmar_Burma", "Laos", "Brunei",
    # South Asia
    "India", "Pakistan", "Bangladesh", "Sri Lanka", "Nepal",
]

# Steel + aluminium only (see module docstring).
GOODS = [
    ("73181500", "Screws/bolts, threaded (fasteners)"),
    ("72131000", "Wire rod (fastener precursor)"),
    ("72279000", "Alloy steel bars/rods"),
    ("76041010", "Aluminium bars/rods, non-alloy"),
    ("76061190", "Aluminium plates/sheets"),
]


def sheet_names() -> list[str]:
    wb = openpyxl.load_workbook(DEFAULT_VALUES_XLSX, data_only=True, read_only=True)
    names = wb.sheetnames
    wb.close()
    return names


def scan_coverage(countries: list[str]) -> dict:
    """How deep is each country's book? Coverage = rows carrying a direct value."""
    rows = []
    for c in countries:
        try:
            dvs = defaults.load_country(c)
        except KeyError:
            continue
        numeric = [d for d in dvs if d.direct is not None]
        has_fastener = any(d.cn_code.startswith("731815") for d in dvs if d.direct is not None)
        rows.append({
            "country": c,
            "rows": len(dvs),
            "numeric": len(numeric),
            "has_cn_731815": has_fastener,
        })
    rows.sort(key=lambda r: -r["numeric"])
    numeric_counts = [r["numeric"] for r in rows]
    return {
        "countries_scanned": len(rows),
        "full_book_ge_200": sum(1 for n in numeric_counts if n >= 200),
        "thin_book_lt_50": sum(1 for n in numeric_counts if n < 50),
        "with_cn_731815": sum(1 for r in rows if r["has_cn_731815"]),
        "without_cn_731815": sum(1 for r in rows if not r["has_cn_731815"]),
        "median_numeric": statistics.median(numeric_counts) if numeric_counts else None,
        "per_country": rows,
    }


def scan_goods(countries: list[str], year: int, price: float) -> dict:
    """Ranked default value + buyer certificate cost per good, per country."""
    out = {}
    for cn, label in GOODS:
        listed, absent = [], []
        for c in countries:
            try:
                dv = defaults.lookup(cn, c)
            except KeyError:
                continue
            if dv is None or dv.direct is None:
                absent.append(c)
                continue
            marked = dv.for_year(year)
            listed.append({
                "country": c,
                "direct": dv.direct,
                "marked_up": marked,
                "buyer_cost_eur_per_t": round(marked * price, 2) if marked else None,
                "route": dv.route,
            })
        listed.sort(key=lambda r: r["direct"])
        out[cn] = {"label": label, "listed": listed, "absent": absent}
    return out


# firm_a's measured actual SEE (direct), engine output pinned by ground truth
# (data/mock_corpus/ground_truth.json: 2.924363267; engine 2.924363986).
FIRM_A_SEE_DIRECT = 2.924363986610001


def identical_factory(year: int, price: float) -> dict:
    """The same factory, moved.

    Hold the physics fixed at firm_a's measured SEE and vary ONLY the country of
    origin. What changes is not the carbon — it is whether the EU has a book for
    your country. That difference IS the provability divide, in euros.
    """
    actual_cost = FIRM_A_SEE_DIRECT * price
    rows = []
    for c in ("Taiwan", "Vietnam", "Thailand", "India", "Indonesia", FALLBACK_SHEET):
        dv = defaults.lookup("73181500", c)
        if dv is None or dv.direct is None:
            continue
        marked = dv.for_year(year)
        default_cost = marked * price
        rows.append({
            "origin": c,
            "default_marked_up": marked,
            "buyer_cost_default_eur_per_t": round(default_cost, 2),
            "buyer_cost_actual_eur_per_t": round(actual_cost, 2),
            "reward_for_proving_eur_per_t": round(default_cost - actual_cost, 2),
            "reward_at_1800t_eur_per_yr": round((default_cost - actual_cost) * 1800, 0),
        })
    rows.sort(key=lambda r: r["reward_for_proving_eur_per_t"])
    return {
        "premise": "identical factory, identical process, identical measured SEE "
                   f"({FIRM_A_SEE_DIRECT:.6f} tCO2e/t direct, firm_a engine output); "
                   "only the country of origin changes",
        "note_fallback": "countries with no CN 7318 15 row fall to _Other Countries, "
                         "which the Commission Q&A (p.37) defines as the average of the "
                         "ten exporting countries with the highest emission intensities",
        "rows": rows,
    }


def main() -> int:
    cert = certificate_price()
    quarter, price = cert.quarter, cert.eur_per_tco2e
    year = 2026

    names = sheet_names()
    countries = [n for n in names if n not in ("Overview", "Version History")]
    print(f"sheets: {len(names)} · country-like: {len(countries)}")

    coverage = scan_coverage(countries)
    print(f"coverage: {coverage['countries_scanned']} scanned · "
          f"full(>=200)={coverage['full_book_ge_200']} · thin(<50)={coverage['thin_book_lt_50']} · "
          f"with CN731815={coverage['with_cn_731815']} · without={coverage['without_cn_731815']}")

    focus = [c for c in FOCUS if c in names] + [FALLBACK_SHEET]
    missing_focus = [c for c in FOCUS if c not in names]
    goods = scan_goods(focus, year, price)
    moved = identical_factory(year, price)

    outdir = Path("out/atlas")
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "coverage.json").write_text(
        json.dumps(coverage, ensure_ascii=False, indent=2), encoding="utf-8")
    (outdir / "asean_south_asia.json").write_text(
        json.dumps({"period_year": year, "certificate_quarter": quarter,
                    "certificate_price_eur": price,
                    "focus_not_in_workbook": missing_focus,
                    "goods": goods,
                    "identical_factory": moved}, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [f"# Provability Atlas — scan ({year}, certificate {quarter} €{price}/tCO2e)", ""]
    lines += [f"- sheets in workbook: **{len(names)}** · country sheets scanned: "
              f"**{coverage['countries_scanned']}**",
              f"- full book (>=200 goods with a direct value): **{coverage['full_book_ge_200']}**",
              f"- thin book (<50): **{coverage['thin_book_lt_50']}** · median goods/country: "
              f"**{coverage['median_numeric']}**",
              f"- carry a CN 7318 15 row: **{coverage['with_cn_731815']}** · "
              f"**no row at all: {coverage['without_cn_731815']}**", ""]
    if missing_focus:
        lines += [f"> Focus countries with **no sheet in the workbook at all**: "
                  f"{', '.join(missing_focus)}", ""]
    for cn, blk in goods.items():
        lines += [f"## CN {cn} — {blk['label']}", "",
                  "| Country | direct | 2026 marked-up | buyer €/t | route |",
                  "|---|---|---|---|---|"]
        for r in blk["listed"]:
            name = "**_Other Countries (fallback)_**" if r["country"] == FALLBACK_SHEET else r["country"]
            lines.append(f"| {name} | {r['direct']} | {r['marked_up']} | "
                         f"€{r['buyer_cost_eur_per_t']:,.2f} | {r['route']} |")
        if blk["absent"]:
            lines += ["", f"**No row → falls to the fallback:** {', '.join(blk['absent'])}"]
        lines.append("")

    lines += ["## The same factory, moved", "", moved["premise"], "",
              "| Origin | default (2026) | buyer WITHOUT data | buyer WITH data | "
              "reward for proving | at 1,800 t/yr |", "|---|---|---|---|---|---|"]
    for r in moved["rows"]:
        name = "**_no book → fallback_**" if r["origin"] == FALLBACK_SHEET else r["origin"]
        lines.append(
            f"| {name} | {r['default_marked_up']:.4f} | "
            f"€{r['buyer_cost_default_eur_per_t']:,.2f} | €{r['buyer_cost_actual_eur_per_t']:,.2f} | "
            f"**€{r['reward_for_proving_eur_per_t']:,.2f}/t** | "
            f"€{r['reward_at_1800t_eur_per_yr']:,.0f} |")
    lines += ["", f"> {moved['note_fallback']}", ""]
    (outdir / "summary.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"\n-> {outdir}/summary.md")
    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
