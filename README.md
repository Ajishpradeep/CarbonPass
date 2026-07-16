# CarbonPass — Module 1 PoC

Local-first AI that turns a Taiwanese fastener SME's documents (Taipower bill,
steel wire-rod e-invoices, production log) into a **verifier-ready EU CBAM
"Communication Template for installations"** (`.xlsx`) for CN 7318 goods, plus a
default-vs-actual buyer-cost screen.

**CBAM ground rules baked into the code** (see `docs/10_poc_blueprint.md` §2A):
one SEE (tCO2e/t) per CN code per **calendar year** — never per shipment; output
is the producer→importer **Communication Template**, not the EU Registry
declaration; the dominant input is the **purchased steel precursor**; indirect
(electricity) emissions are recorded but are **not** in the CN 7318 certificate;
every figure carries a source flag (actual/default) + per-line uncertainty; the
tool **prepares** verification — it never certifies.

## Setup

```bash
uv sync                                  # Python 3.12; installs everything incl. docling
brew install ollama                      # local VLM serving
ollama serve &                           # if not already running as a service
ollama pull qwen3-vl:8b-instruct         # ~6 GB, one-time
python scripts/pull_moenv_ef.py          # refresh MOENV coefficient table (optional; snapshot committed)
cp .env.example .env                     # fill MOENV_API_KEY only if you want live refreshes
```

## Run (Firm A end-to-end)

```bash
# 1. generate the synthetic 3-firm corpus (data/mock_corpus/ is gitignored)
uv run python scripts/make_mock_corpus.py

# 2. documents -> validated activity data (VLM parses the 12 Taipower bills;
#    steel/gas come from MIG 4.0 e-invoice XML; production log from CSV)
uv run python -m carbonpass ingest data/mock_corpus/firm_a -o out/firm_a_activity.json
#    add --no-vlm to skip Ollama (structured parsers only; no electricity data)

# 3. activity data -> filled Communication Template + flags sidecar
uv run python -m carbonpass pack out/firm_a_activity.json -o out/firm_a_communication_template.xlsx

# 4. the buyer screen: what your data is worth to the EU importer
uv run python -m carbonpass costdelta out/firm_a_activity.json

# 5. Module 2 — grid-aware shift plan (live Taipower #8931 feed + TOU tariffs)
uv run python -m carbonpass schedule data/mock_corpus/firm_a

# 6. Module 3 — local API + LINE webhook (simulator needs no LINE channel)
uv run python -m carbonpass serve &
uv run python scripts/line_simulator.py --fast
```

## Sprint-1 extras

```bash
uv run python scripts/degrade_corpus.py          # phone-photo degradations of the corpus
uv run python scripts/vlm_bakeoff.py --models qwen3-vl:8b-instruct   # accuracy matrix
uv run python scripts/verify_workbook_recalc.py  # LibreOffice recompute vs engine sidecar
```
Results and findings: `docs/13_sprint1_report.md`.

Firms B (two product lines sharing one meter — the allocation case) and C
(mill EPD supplied — the actual-precursor case) run identically.

## Tests

```bash
uv run pytest            # incl. golden tests reproducing the European Commission's
                         # own worked "screws and nuts" example at 1e-9 relative
```

## Repo map

```
schema/cbam_template_map.yaml      writer contract: exact cells, input vs formula
schema/activity_data.schema.json   ingestion output schema
src/carbonpass/
  ingestion/   docling pre-pass + qwen3-vl (Ollama) + validation pipeline
  egui/        MIG 4.0 e-invoice XML parser (structured path)
  allocation/  OR-Tools LP + NumPy Monte-Carlo (per-line uncertainty)
  rules/       SEE per IR 2025/2547; CBAM default values + 10/20/30% mark-ups; MOENV EFs
  writer/      openpyxl fill of the Commission template + flags sidecar
  costdelta/   default-vs-actual buyer cost screen
scripts/       corpus generator, MOENV fetcher, template inspector
tests/golden/  the screws & nuts answer key, transcribed + reproduced
data/cbam_official/   Commission template, filled examples, default values (committed)
data/ef/              MOENV coefficient snapshot (committed)
data/mock_corpus/     generated synthetic corpus (gitignored)
```

## Status vs Definition of Done (docs/11 §6)

| # | Item | Status |
|---|------|--------|
| 1 | Repo scaffolded, deps install cleanly | ✅ `uv sync` clean on Python 3.12 |
| 2 | `cbam_template_map.yaml` + golden expected outputs | ✅ transcribed from the answer key |
| 3 | Mock corpus (3 firms + ground truth) | ✅ 295 files, hand-computed SEE |
| 4 | Ingestion runs Firm A end-to-end via qwen3-vl | ✅ 72/72 bill fields (100%), electricity rel err 2e-6 |
| 5 | Rules engine reproduces screws & nuts SEE | ✅ rel 1e-9, pytest green |
| 6 | Writer emits filled template with flags | ✅ + `.flags.json` sidecar |
| 7 | README documents run commands | ✅ this file |

Measured on the corpus (period 2026, cert price €75.28): firm_a — default
precursor, SEE 2.92 tCO2e/t direct, buyer delta only €4/t (95% of the number IS
the default → the flag tells the owner to request a mill EPD); firm_c — EPD
supplied, SEE 2.18, delta **€60.31/t ≈ €108k/yr**. The adopted Taiwan CN 7318
default (2.71 +10% → €224/t) is far below the older industry estimates of
€450–750/t — use these regulation-derived numbers in any pitch.

Known caveats: openpyxl drops some conditional-formatting extensions of the
template on save (cosmetic); SEE cells in the output workbook are recomputed by
Excel/LibreOffice on open (openpyxl does not evaluate formulas) — the engine's
numbers, which the golden tests pin to the Commission's example, are in the
`.flags.json` sidecar, and `scripts/verify_workbook_recalc.py` proves the
workbook independently recomputes them. Sprint-1 status (bake-off, PP-OCRv4
numeric backstop, Module 2 scheduler, Module 3 LINE surface):
`docs/13_sprint1_report.md`.
