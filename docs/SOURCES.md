# CarbonPass — Official Sources & Data Contract

**Date:** 20 Jul 2026 · **Status:** 🟢 LIVE — what data the engine runs on, where each piece came
from, what is watched on a cadence, and what only the pilot can provide.
**Legend:** ✅ in-repo · 👀 watch cadence · 🏭 pilot-only.

---

## 1. The data contract (binding on all code)

- **No literals.** Prices and factors live in dated config; code reads them through one loader each
  and carries the provenance string into every output:
  - `data/prices.yaml` → `carbonpass/prices.py` — CBAM certificate quarters (each with a
    `published:` date; **requesting an unpublished quarter raises `UnpublishedQuarterError`** —
    never extrapolate, Q3 2026 lands 5 Oct) · scrap-resale recovery ranges (carbon 30–40%,
    stainless 35–45%, dated) · wire-rod reference price.
  - `data/ef/grid_ef.yaml` → `carbonpass/rules/gridef.py` — Taiwan grid EF by year+series;
    `default_selection` = **2025 industrial 0.466** (MOEA, announced 2 Jun 2026; next ~Jun 2027).
    Taiwan-only: `run_rules` refuses to apply it to a non-Taiwanese installation.
- **Default values and mark-ups come from the workbook row itself**
  (`DefaultValue.derived_markup()`), never from constants — fertilisers are flat 1%.
- `data/official_refs/` holds **dated provenance snapshots** (add new ones with dated filenames).
- Update duties: FACTS §9 watch-list, before 31 Jul and before finals.

## 2. EU CBAM — in-repo (✅ all)

| Asset | Path | Note |
|---|---|---|
| Default values workbook (IR 2025/2621, "DVs as adopted v20260204") | `data/cbam_official/default_values.xlsx` | primary source for all default figures |
| Benchmarks workbook (IR 2025/2620) | `data/cbam_official/benchmarks.xlsx` | 73181100→1.364 / 73181210→1.154 byte-verified |
| Communication template v2.1 (blank, 19 sheets) | `data/cbam_official/communication_template.xlsx` | the writer's target |
| 7 filled Commission examples | `data/cbam_official/template_examples/` | screws-and-nuts and cement are golden-tested; blast furnace / EAF alloys / fertiliser / aluminium / hydrogen still unused |
| CBAM Q&A (27–28 May 2026) | `data/cbam_official/cbam_qa.pdf` | the LIVE rules source — check for newer versions before submission & finals |
| **The five legal acts + grep-able `.txt` beside each** | `data/cbam_official/legal/` | IR 2025/2547 (methodology — **no estimation cap**, Annex III §F mass rule, 6-yr retention) · IR 2025/2621 (defaults — the `#VALUE!` CN 7221 rows) · IR 2025/2546 (verification/accreditation) · Reg 2023/956 (base; Art. 31 phase-in lives here, in neither workbook) · Reg 2025/2083 (omnibus, 50 t) |
| Transitional guidance EN/ZH (Dec 2023) | `data/cbam_official/guidance_*.pdf` | ⚠️ EXPIRED rules — mechanics/worked examples only (FACTS §7) |

## 3. EU CBAM — living pages (👀 save dated snapshots to `data/official_refs/`)

| Page | Cadence | Why |
|---|---|---|
| DG TAXUD CBAM hub + certificate-price publications — `taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism_en` | quarterly (Q3 price **5 Oct 2026**) | feeds `data/prices.yaml` |
| "State-of-play CBAM accreditation" PDF (DG TAXUD verification page) | monthly + before finals | NAB count moves (4→8 already); EC vs EA disagree — keep both, cite retrieval date |
| EA CBAM NAB list — `european-accreditation.org` | monthly | the "8 NABs" source (2 Jul 2026) |
| CBAM Q&A page | before submission + finals | newer versions supersede May 2026 |

## 4. Taiwan — datasets & APIs

| Asset | Status | Detail |
|---|---|---|
| MOENV emission coefficients (data.gov.tw #28176, OpenAPI) | ✅ | `data/ef/moenv_coefficients.json` (1,164 rows) via `scripts/pull_moenv_ef.py` (`MOENV_API_KEY` in `.env`); refresh before pilot. Contains the government's own fastener footprint 3.41 tCO₂e/t (FACTS §3) |
| Taipower generation-by-unit 10-min live (#8931) | ✅ wired | `service.taipower.com.tw/data/opendata/apply/file/d006001/001.json` — dict rows, UTF-8-BOM |
| Taipower historical generation (#37331) | ✅ seeded · 👀 | `data/grid/history/` — append monthly for the true diurnal curve (replaces the single-snapshot anchor at pilot) |
| 2025 grid EF (0.467 / 0.466 industrial / 0.471 residential) | ✅ | config `data/ef/grid_ef.yaml` + snapshot `data/official_refs/moea_grid_ef_2025.md` |
| Taipower TOU rate schedule (HV 3-tier summer 9.39/5.85/2.53, eff. 1 Oct 2025) | ✅ | `data/official_refs/taipower_tou_2025-10.pdf`; next review ~Oct 2026 |
| e-invoice MIG 4.0 specification | ✅ | `data/official_refs/mig40_spec.pdf`; parser built on the open Turnkey format (`github.com/phidiassj/TaiwanEInvoiceOpenAPI`) |
| CBAM certificate prices (2026 Q1/Q2) | ✅ · 👀 | `data/prices.yaml` (dated, refuse-unpublished rule) |
| Scrap / steel reference prices | ✅ · 👀 weekly | `data/prices.yaml`. Sources: Feng Hsin (豐興) weekly steel/scrap; `metaltrade.tw` stainless; LME/Argus scrap CFR Taiwan |
| MOENV product carbon-footprint registry (#8992) | ✅ referenced | sanity checks only; no build dependency |

## 5. Accounts / credentials (owner action)

| Item | Needed by | Note |
|---|---|---|
| LINE Messaging API channel (`LINE_CHANNEL_SECRET`, access token → `.env`) | before finals (simulator suffices for 31 Jul) | free; console → webhook at `/line/webhook` |
| MOENV API key | ✅ in `.env` | working |
| GPU box (optional) | before finals | only to re-run InternVL official weights if the bake-off is challenged |

## 6. Pilot-only inputs (🏭 — cannot be downloaded; the `pilot/` intake kit collects them)

12 months of real Taipower bills (photos OK) · e-GUI invoice export (XML preferred; consent path
exists in the LINE flow) · production log (any format; we provide a one-page template) · machine
nameplate list (kW, hours) · **scrap sale receipts** (closes the net-money loop with real resale
prices — replaces the 30–40% estimate) · AMI 15-min CSV (owner-exported, consent-based) · a signed
consent one-pager. The pilot's #1 scientific job: replace the synthetic 9.1% with a measured value
via three-way reconciliation (steel in vs shipped out vs scrap receipts) — protocol pre-registered
in `pilot/` before the pilot starts.
