# Official Sources Inventory — Sprint 2 / pilot edition

**Date:** 19 Jul 2026 · **Status:** 🟢 LIVE · **Successor to `docs/10` §3** (the original download
inventory — everything there is downloaded and in-repo). This lists what the CURRENT plan
(`docs/21`) needs: what is in place, what was just placed, what a human must download (exact URLs —
our sandbox fetcher is blocked on some official sites), what is watched on a cadence, and what only
the pilot can provide. **Legend:** ✅ in-repo · 🆕 placed 19 Jul · ⬇️ download needed (exact URL
given) · 👀 watch cadence · 🏭 pilot-only.

---

## A. EU CBAM — machine-readable assets (✅ all in-repo, unchanged)

| Asset | Path | Note |
|---|---|---|
| Default values workbook ("DVs as adopted v20260204", IR 2025/2621) | `data/cbam_official/default_values.xlsx` | Primary source for all default figures |
| Benchmarks workbook (IR 2025/2620) | `data/cbam_official/benchmarks.xlsx` | 73181100→1.364 / 73181210→1.154 byte-verified |
| Communication template v2.1 (blank) | `data/cbam_official/communication_template.xlsx` | 19 sheets |
| 7 filled Commission examples (incl. **Screws & nuts = golden**, **Cement = next golden**, docs/21 §1.1.2) | `data/cbam_official/template_examples/` | 6 of 7 still unused — cement first |
| CBAM Q&A (27–28 May 2026) | `data/cbam_official/cbam_qa.pdf` | The LIVE rules source |
| Transitional guidance EN/ZH (Dec 2023) | `data/cbam_official/guidance_*.pdf` | ⚠️ EXPIRED rules — mechanics/worked examples only (kill-list #5) |

## B. EU CBAM — legal texts (⬇️ **the one real gap**; EUR-Lex blocks our fetcher — download in a browser to `data/cbam_official/legal/`)

| Regulation | CELEX | Why we need the text itself | URL |
|---|---|---|---|
| **IR (EU) 2025/2547 — definitive-period methodology** | 32025R2547 | 🔴 CRITICAL (`docs/15` §8.1): close the Annex III estimation-cap question (kill-list #2 is "unanswerable from this repo" until read); also the mass-before-cutting rule in legal form | `https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32025R2547` |
| **IR (EU) 2025/2621 — default values** | 32025R2621 | Verify the workbook against the law — esp. **the CN 7221 "see below" hole** for TW/TH/VN before we publish "hole in the book" (docs/16 §7.6) | `https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32025R2621` |
| IR (EU) 2025/2546 — verification & accreditation | 32025R2546 | Pilot verifier-review prep; verification-dossier roadmap item | `https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32025R2546` |
| Reg (EU) 2023/956 — base CBAM regulation | 32023R0956 | Annex I scope; free-allocation phase-in (Art. 31) — the phase-in factors are in NEITHER workbook (`docs/15` §2.8) | `https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32023R0956` |
| Reg (EU) 2025/2083 — omnibus (50 t de minimis) | 32025R2083 | De-minimis mechanics cited in proposal | `https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32025R2083` |

*(HTML alternative for grep-able text: replace `/TXT/PDF/` with `/TXT/HTML/`. After download, run a
text extraction into `.txt` beside each PDF so the rules engine and future audits can grep the law.)*

## C. EU CBAM — living pages (👀 re-fetch on cadence; save dated snapshots to `data/official_refs/`)

| Page | Cadence | Why |
|---|---|---|
| DG TAXUD CBAM hub + **certificate price publications** — `https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism_en` | Quarterly (Q3 price lands **5 Oct 2026**) | Feeds `data/prices.yaml`; engine refuses unpublished quarters |
| **"State-of-play CBAM accreditation" PDF** (linked from the DG TAXUD verification page) | Monthly + before finals | NAB count moves (4 → 8 already); cite by retrieval date; EC vs EA lists disagree — keep both |
| **EA (European Accreditation) CBAM NAB list** — `https://european-accreditation.org` | Monthly | The "8 NABs" source (2 Jul 2026) |
| CBAM Q&A page (new versions supersede May 2026) | Before submission + before finals | Our live-rules source must stay current |

## D. Taiwan — datasets & APIs

| Asset | Status | Detail |
|---|---|---|
| MOENV emission coefficients (data.gov.tw **#28176**, OpenAPI) | ✅ wired | `data/ef/moenv_coefficients.json` (1,164 rows) via `scripts/pull_moenv_ef.py` (`MOENV_API_KEY` in `.env`); refresh before pilot; **still unwired in engine** — docs/21 item (rules/ef.py) |
| Taipower generation-by-unit 10-min live (**#8931**) | ✅ wired | `service.taipower.com.tw/data/opendata/apply/file/d006001/001.json` (dict rows, UTF-8-BOM) |
| Taipower historical generation (**#37331**) | ⬇️ | Download monthly CSVs → `data/grid/history/` for the true diurnal curve (docs/21 §3); deep archive may need a Taipower request — start with what the portal serves: `https://data.gov.tw/dataset/37331` |
| **2025 grid EF (0.467 / 0.466 industrial / 0.471 residential; national 0.456 est.)** | 🆕 | Snapshot `data/official_refs/moea_grid_ef_2025.md` + config `data/ef/grid_ef.yaml` — announced 2 Jun 2026; next update ~Jun 2027 |
| Taipower TOU rate schedule (HV 3-tier summer 9.39/5.85/2.53, eff. 1 Oct 2025) | ⬇️ small | Verified current (`docs/19` B5). Save the official rate-table PDF from `https://www.taipower.com.tw/2764/2765/2801/` → `data/official_refs/taipower_tou_2025-10.pdf`; next review ~Oct 2026 |
| e-invoice **MIG 4.0 specification** | ⬇️ | Our parser is built on the open Turnkey format (`github.com/phidiassj/TaiwanEInvoiceOpenAPI`); for the pilot, put the official MOF spec in-repo: 財政部電子發票整合服務平台 → 資源下載 → MIG 4.0 → `data/official_refs/mig40_spec.pdf` |
| **CBAM certificate prices** (Q1/Q2 2026) | 🆕 | `data/prices.yaml` (dated, refuse-unpublished rule) |
| **Scrap/steel reference prices** | 🆕 + 👀 | `data/prices.yaml` seeded (recovery 30–40% carbon / 35–45% stainless, asof 18 Jul). Weekly update sources: Feng Hsin (豐興) published weekly steel/scrap prices (industry reference); `metaltrade.tw` stainless; LME/Argus scrap CFR Taiwan |
| MOENV product carbon-footprint registry (#8992) | ✅ referenced | Benchmarks/sanity only; no build dependency |

## E. Accounts / credentials (owner action, not downloads)

| Item | Needed by | Note |
|---|---|---|
| LINE Messaging API channel (2 values → `.env`: `LINE_CHANNEL_SECRET`, access token) | Before finals (simulator suffices for 31 Jul) | Free; console → point webhook at `/line/webhook` |
| MOENV API key | ✅ in `.env` | Already working |
| GPU box (optional) | Before finals | Only to re-run InternVL official weights if the bake-off is challenged |

## F. Pilot-only inputs (🏭 — cannot be downloaded; the intake checklist in `pilot/` collects them)

12 months of real Taipower bills (photos) · e-GUI invoice export (XML) · production log (any format)
· machine nameplate list · **scrap sale receipts** (closes the net-money loop with real resale prices)
· AMI 15-min CSV (owner-exported from the Taipower app, consent-based) · a signed consent one-pager.

---

## The 30-minute human to-do (everything ⬇️ above, in order)

1. Browser-download the 5 EUR-Lex PDFs (§B) → `data/cbam_official/legal/` (+ extract `.txt` beside each).
2. Read IR 2025/2547 Annex III → close kill-list #2 (estimation cap: exists or not — record verdict in `docs/15` §8.1).
3. Read IR 2025/2621 Annex I at CN 7221 → confirm or refute the "hole" for TW/TH/VN — gate on the proposal's "hole in the book" line.
4. Save the Taipower TOU PDF and the MIG 4.0 spec (§D) → `data/official_refs/`.
5. Pull the current accreditation state-of-play PDF + EA list (§C) → `data/official_refs/` (dated filenames).
6. Start `data/grid/history/` with whatever #37331 serves today.

After step 6, every factual claim in the proposal and every config the Sprint-2 code needs is backed
by a primary document inside the repo — nothing load-bearing lives only in a URL or a memory.
