# CarbonPass — the factory that cannot see itself

Local-first AI that turns a small Taiwanese factory's photographed paperwork
(Taipower bill, steel e-invoices, production log) into **four kinds of sight**
— offline, in Taiwanese, raw documents never leaving the building:

| Sight | The owner's question | Surface | Measured anchor (synthetic corpus) |
|---|---|---|---|
| ① Product carbon | "What carbon is in my product?" | CBAM Communication Template (.xlsx) + ranked fix-list | Commission's own worked example reproduced at rel 1e-9; firm_a data worth €4.03/t to its buyer (and the tool says when that's *not* worth chasing) |
| ② Material loss | "What do I lose between buying and shipping?" | Waste map, gross **and** net, monthly drift alert | firm_a: 9.1% loss → 758 tCO₂e/yr embodied carbon purchased-but-never-shipped; NT$7.35M at purchase price / **NT$4.4–5.1M net of scrap resale**; 5%-scenario = 359 t + NT$3.5M ≈ **80×** the scheduler |
| ③ Energy timing | "When should my machines run?" | Grid-aware MILP shift plan (live #8931 feed + TOU) | NT$399,800/yr + ~4 tCO₂e (indirect — recorded, **not** in the CN 7318 certificate) |
| ④ Peer position | "Am I normal?" | Anonymised percentile screen (k≥5 floor) | synthetic seed on the documented 5–15% band — labelled; the pilot populates it |

**Ground rules baked into the code** (docs/21 §2): one SEE per CN code per
**calendar year**, never per shipment · defaults are lawful without limit (no
80/20 rule, no cap — verified against IR 2025/2547 itself, docs/15 §8.1) · mass
counts **before cutting** (Annex III §F: scrap sits inside the declared SEE —
the yield lever's legal basis) · electricity is recorded but **not**
certificated for iron & steel · money and carbon always gross **and** net,
enforced in types · prices/factors are dated config (`data/prices.yaml`,
`data/ef/grid_ef.yaml`), never literals — the engine **refuses** to quote an
unpublished certificate quarter · the tool prepares verification, never
certifies.

Entry point for a fresh session: **`docs/20_master_handoff.md`** (state, doc
index, kill-list) → **`docs/21_sprint2_blueprint_kickoff.md`** (build order).

## Setup

```bash
uv sync                                  # Python 3.12; installs everything incl. docling
brew install ollama                      # local VLM serving
ollama serve &                           # if not already running as a service
ollama pull qwen3-vl:8b-instruct         # ~6 GB, one-time (4B also supported)
python scripts/pull_moenv_ef.py          # refresh MOENV coefficient table (optional; snapshot committed)
cp .env.example .env                     # fill MOENV_API_KEY only if you want live refreshes
```

## Run (Firm A, all four sights)

```bash
# 0. generate the synthetic 3-firm corpus (data/mock_corpus/ is gitignored)
uv run python scripts/make_mock_corpus.py

# 1. documents -> validated activity data (VLM parses the Taipower bills;
#    steel/gas from MIG 4.0 e-invoice XML; production log from CSV)
uv run python -m carbonpass ingest data/mock_corpus/firm_a -o out/firm_a_activity.json
#    add --no-vlm to skip Ollama (structured parsers only; no electricity data)

# Sight ①: activity data -> filled Communication Template + flags sidecar
uv run python -m carbonpass pack out/firm_a_activity.json

# Sight ② standalone: waste map (gross AND net) + drift series
uv run python scripts/waste_scan.py out/firm_a_activity.json data/mock_corpus/firm_a

# Sight ③: grid-aware shift plan (live Taipower #8931 feed + TOU tariffs)
uv run python -m carbonpass schedule data/mock_corpus/firm_a

# The one screen the demo pivots on — ranked fix-list, each lever able to
# answer "not worth it this year" (replaces the old costdelta screen):
uv run python -m carbonpass fixlist out/firm_a_activity.json

# All four sights through LINE (simulator needs no LINE channel):
uv run python -m carbonpass serve &
uv run python scripts/line_simulator.py          # --fast skips the VLM step
# session: photos -> 狀態 -> 產生報告(①) -> 浪費(②) -> 排程(③) -> 我正常嗎(④)
```

## Verification extras

```bash
uv run python scripts/degrade_corpus.py          # phone-photo degradations of the corpus
uv run python scripts/vlm_bakeoff.py --models qwen3-vl:8b-instruct   # accuracy matrix
uv run python scripts/verify_workbook_recalc.py  # LibreOffice recompute vs engine sidecar
uv run python scripts/atlas_scan.py              # 120-country default-value atlas
```

Firms B (two product lines sharing one meter — the allocation case; stainless
resolves through the Annex I fallback because Taiwan's CN 7221 row is a hole in
the published OJ itself) and C (mill EPD supplied — €60.31/t buyer delta) run
identically and are golden-tested end-to-end.

## Tests

```bash
uv run pytest      # 53 green: Commission screws-and-nuts AND cement examples at
                   # rel 1e-9; firms A/B/C e2e vs ground truth; unpublished-quarter
                   # refusal; MoneyLoss gross+net enforcement; drift alert;
                   # k>=5 export refusal; the pinned "not worth it this year"
```

## Repo map

```
schema/cbam_template_map.yaml      writer contract: exact cells, input vs formula
schema/activity_data.schema.json   ingestion output schema
schema/benchmark_row.schema.json   PUBLIC give-back spec: k>=5 anonymised benchmark rows
src/carbonpass/
  ingestion/   docling pre-pass + qwen3-vl (Ollama) + PP-OCRv4 backstop
  egui/        MIG 4.0 e-invoice XML parser (structured path)
  allocation/  OR-Tools LP + NumPy Monte-Carlo (per-line uncertainty)
  rules/       SEE per IR 2025/2547; defaults + row-derived mark-ups + resolve()
               fallback; grid EF loader (rules/gridef.py); MOENV EFs
  prices.py    dated certificate prices + scrap recovery (refuses unpublished quarters)
  writer/      openpyxl fill of the Commission template + flags sidecar
  waste/       Sight ②: scan (gross+net MoneyLoss), monthly drift + alert
  benchmark/   Sight ④: k>=5 schema, aggregate-only export, percentile screen
  costdelta/   fixlist.py — the ranked fix-list (screen.py feeds it)
  scheduler/   Sight ③: live #8931 grid feed, TOU tariffs, MILP, ledger
  api/ + line_bot/   FastAPI + LINE webhook (simulator mode without a channel)
scripts/       corpus generator, simulator, bake-off, recalc verifier, waste CLI
tests/golden/  screws & nuts AND cement answer keys + firm A/B/C e2e goldens
data/cbam_official/   Commission template, filled examples, default values,
                      legal/ (the five EUR-Lex acts + grep-able .txt)
data/prices.yaml      dated certificate quarters + scrap recovery ranges
data/ef/              grid_ef.yaml (2025 industrial 0.466 default) + MOENV snapshot
data/mock_corpus/     generated synthetic corpus (gitignored)
```

## Status vs Sprint-2 Definition of Done (docs/21 §7)

| # | Item | Status |
|---|------|--------|
| 1 | All §1.1 defects closed; cement + firm_b/c goldens; ≥35 tests | ✅ 53 green |
| 2 | `waste/` live: drift+alert, gross/net type, method note, LINE+API | ✅ |
| 3 | Fix-list replaces costdelta; negative answer pinned | ✅ |
| 4 | Benchmark module + public k≥5 schema + percentile screen | ✅ |
| 5 | Simulator plays four sights in one session | ✅ (video to record) |
| 6 | Engine consumes prices.yaml + grid_ef.yaml; refusal pinned; provenance everywhere | ✅ |
| 6b | Legal-text gates recorded (docs/15 §8.1) | ✅ no estimation cap; CN 7221 hole confirmed in the OJ |
| 7 | Kill-list grep clean; README current | ✅ this file |

Known caveats: openpyxl drops some conditional-formatting extensions of the
template on save (cosmetic); SEE cells in the output workbook are recomputed by
Excel/LibreOffice on open — the engine's numbers are in the `.flags.json`
sidecar and `scripts/verify_workbook_recalc.py` proves the workbook reproduces
them (re-verified after the 0.466 grid-EF migration). Sprint-1 history
(bake-off, backstop, scheduler, LINE): `docs/13_sprint1_report.md`.
