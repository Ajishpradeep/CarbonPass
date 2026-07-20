# CarbonPass — the factory that cannot see itself

*Last verified: 20 Jul 2026 (Sprint 2 complete — 53/53 tests green).*

Local-first AI that turns a small Taiwanese factory's photographed paperwork
(Taipower bill, steel e-invoices, production log) into **four kinds of sight**
— offline, in Taiwanese, raw documents never leaving the building:

| Sight | The owner's question | Surface | Measured anchor (synthetic corpus) |
|---|---|---|---|
| ① Product carbon | "What carbon is in my product?" | CBAM Communication Template (.xlsx) + ranked fix-list | Commission's own worked examples (screws-and-nuts, cement) reproduced at rel 1e-9; firm_a data worth €4.03/t to its buyer (and the tool says when that's *not* worth chasing) |
| ② Material loss | "What do I lose between buying and shipping?" | Waste map, gross **and** net, monthly drift alert | firm_a: 9.1% loss → 758 tCO₂e/yr embodied carbon purchased-but-never-shipped; NT$7.35M at purchase price / **NT$4.4–5.1M net of scrap resale**; 5%-scenario = 359 t + NT$3.5M ≈ **80×** the scheduler |
| ③ Energy timing | "When should my machines run?" | Grid-aware MILP shift plan (live #8931 feed + TOU) | NT$399,800/yr + ~4 tCO₂e (indirect — recorded, **not** in the CN 7318 certificate) |
| ④ Peer position | "Am I normal?" | Anonymised percentile screen (k≥5 floor) | synthetic seed on the documented 5–15% band — labelled; the pilot populates it |

**Ground rules baked into the code** ([docs/FACTS.md](docs/FACTS.md) §8): one SEE per CN code per
**calendar year**, never per shipment · defaults are lawful without limit (no 80/20 rule, no cap —
verified against IR 2025/2547 itself, [docs/FACTS.md](docs/FACTS.md) §2) · mass counts **before
cutting** (Annex III §F: scrap sits inside the declared SEE — the yield lever's legal basis) ·
electricity is recorded but **not** certificated for iron & steel · money and carbon always gross
**and** net, enforced in types · prices/factors are dated config (`data/prices.yaml`,
`data/ef/grid_ef.yaml`), never literals — the engine **refuses** to quote an unpublished certificate
quarter · the tool prepares verification, never certifies.

Entry point for a fresh session: **[docs/PROJECT.md](docs/PROJECT.md)** (thesis, state, roadmap) →
**[docs/FACTS.md](docs/FACTS.md)** (every verified number + the kill-list) →
**[docs/SOURCES.md](docs/SOURCES.md)** (official sources & data contract). History: `docs/archive/`.
The live submission artifact (Rev 5, externally verified) is in `proposal/`.

---

## 1. Setup

Requires **Python 3.12** (pinned in `.python-version`) and [`uv`](https://docs.astral.sh/uv/).

```bash
uv sync                                  # installs everything incl. docling, OR-Tools, FastAPI
brew install ollama                      # local VLM serving (any OS: https://ollama.com/download)
ollama serve &                           # if not already running as a service
ollama pull qwen3-vl:8b-instruct         # ~6.1 GB, one-time — the default model
ollama pull qwen3-vl:4b-instruct         # ~3.3 GB, optional — matches the 8B on the bake-off, faster
cp .env.example .env                     # see §2 below for what each value does
```

Verify Ollama is reachable before running anything that ingests a photo:

```bash
curl -s http://localhost:11434/api/tags | head -c 200   # should list the pulled models
```

### 1.1 Environment variables (`.env`, gitignored — `.env.example` is the template)

| Variable | Required? | Purpose |
|---|---|---|
| `MOENV_API_KEY` | optional | live refresh of `data/ef/moenv_coefficients.json` via `scripts/pull_moenv_ef.py`; the committed snapshot (1,164 rows) works without it |
| `OLLAMA_HOST` | optional | defaults to `http://localhost:11434` |
| `OLLAMA_MODEL` | optional | defaults to `qwen3-vl:8b-instruct`; set to `qwen3-vl:4b-instruct` for the faster edge-tier model |
| `LINE_CHANNEL_SECRET` / `LINE_CHANNEL_ACCESS_TOKEN` | optional | only needed to wire a **real** LINE channel; leaving both unset runs the webhook in **simulator mode** (§4) |

---

## 2. Run — all four sights on the synthetic corpus (Firm A)

```bash
# 0. generate the synthetic 3-firm corpus (data/mock_corpus/ is gitignored; regenerate at will)
uv run python scripts/make_mock_corpus.py

# 1. documents -> validated activity data (VLM parses the Taipower bills;
#    steel/gas come from MIG 4.0 e-invoice XML; production log from CSV)
uv run python -m carbonpass ingest data/mock_corpus/firm_a -o out/firm_a_activity.json
#    add --no-vlm to skip Ollama entirely (structured parsers only; no electricity data)

# Sight ①: activity data -> filled Communication Template + flags sidecar
uv run python -m carbonpass pack out/firm_a_activity.json

# Sight ② standalone: waste map (gross AND net) + monthly drift series
uv run python scripts/waste_scan.py out/firm_a_activity.json data/mock_corpus/firm_a

# Sight ③: grid-aware shift plan (live Taipower #8931 feed + TOU tariffs)
uv run python -m carbonpass schedule data/mock_corpus/firm_a

# The one screen the demo pivots on — ranked fix-list, each lever able to
# answer "not worth it this year" (replaces the old costdelta screen):
uv run python -m carbonpass fixlist out/firm_a_activity.json --firm-dir data/mock_corpus/firm_a
```

Firms **B** (two product lines sharing one meter — the allocation case; stainless resolves through
the Annex I fallback because Taiwan's CN 7221 row is a hole in the published OJ itself) and **C**
(mill EPD supplied — €60.31/t buyer delta) run identically:

```bash
uv run python -m carbonpass ingest data/mock_corpus/firm_b --no-vlm -o out/firm_b_novlm_activity.json
uv run python -m carbonpass fixlist out/firm_b_novlm_activity.json --firm-dir data/mock_corpus/firm_b
```

---

## 3. Run — the local API server

```bash
uv run python -m carbonpass serve                 # http://127.0.0.1:8787
# or: uv run python -m carbonpass serve --host 0.0.0.0 --port 8080
```

| Method & path | Body / query | What it does |
|---|---|---|
| `GET /health` | — | `{status, version, ollama: bool}` |
| `POST /ingest` | `{firm_dir, use_vlm}` | documents → activity-data JSON, written to `out/` |
| `POST /pack` | `{activity_json, output?}` | Sight ①: filled Communication Template + flags sidecar |
| `GET /fixlist` | `?activity_json=&firm_dir=` | the ranked fix-list (replaces `/costdelta`) |
| `POST /waste` | `{activity_json, firm_dir}` | Sight ②: waste map (gross+net) + drift series |
| `POST /schedule` | `{firm_dir, month?}` | Sight ③: grid-aware shift plan + ledger |
| `POST /line/webhook` | LINE event payload | Module 3 front end (see §4) |

Everything runs on the factory's own machine; only the `.xlsx` pack the owner explicitly sends ever
leaves it.

---

## 4. Run — the LINE flow (simulator needs no LINE channel)

```bash
uv run python -m carbonpass serve &
uv run python scripts/line_simulator.py          # full run incl. the VLM step
uv run python scripts/line_simulator.py --fast   # skips 「產生報告」's VLM pass (minutes -> seconds)
```

The simulator plays one session through **all four sights** from one photo set:

```
👤 (photographs two Taipower bills)
👤 狀態          → what's been received so far
👤 產生報告      → Sight ① CBAM pack + ranked fix-list        (skipped with --fast)
👤 浪費 / 損耗   → Sight ② waste map, gross AND net, + drift alerts
👤 排程 / 省電   → Sight ③ grid-aware shift plan
👤 我正常嗎 / 同業 → Sight ④ percentile vs the (labelled) seed band
```

To wire a **real** LINE channel: create a Messaging API channel in the LINE Developers console, set
`LINE_CHANNEL_SECRET` + `LINE_CHANNEL_ACCESS_TOKEN` in `.env`, and point the webhook URL at
`https://<your-host>/line/webhook`. Nothing else changes — the same handlers serve both modes.

---

## 5. Verification & analysis extras

```bash
uv run pytest                                     # 53 green (see §6)
uv run python scripts/degrade_corpus.py           # phone-photo degradations of the corpus
uv run python scripts/vlm_bakeoff.py --models qwen3-vl:8b-instruct qwen3-vl:4b-instruct
uv run python scripts/verify_workbook_recalc.py   # LibreOffice recompute vs engine sidecar (needs LibreOffice ≥26 installed)
uv run python scripts/atlas_scan.py               # 120-country CBAM default-value atlas -> out/atlas/
python scripts/pull_moenv_ef.py                   # refresh the MOENV coefficient snapshot (needs MOENV_API_KEY)
```

---

## 6. Tests

```bash
uv run pytest -q
```

**53 passed.** Covers: both Commission worked examples (screws-and-nuts, cement) at rel 1e-9 ·
firms A/B/C reconciled end-to-end vs ground truth at rel 1e-6 · the unpublished-certificate-quarter
refusal · `MoneyLoss` gross+net enforcement · the drift-alert rule (fires on a rising series, silent
on a flat one) · the k≥5 benchmark-export refusal · the pinned "not worth it this year" fix-list
verdict · the row-derived mark-up (fertiliser flat 1% vs steel 10/20/30%) · the grid-EF/certificate
config loaders.

---

## 7. Repo map

```
README.md                          this file
docs/PROJECT.md · FACTS.md · SOURCES.md   the three live docs (see top of this file)
docs/archive/                      everything superseded — never a source of claims
proposal/                          the live submission artifact (Rev 5 PDF/MD/TeX + figs/)
schema/
  cbam_template_map.yaml           writer contract: exact cells, input vs formula
  activity_data.schema.json        ingestion output schema
  benchmark_row.schema.json        PUBLIC give-back spec: k>=5 anonymised benchmark rows
src/carbonpass/
  ingestion/    docling pre-pass + qwen3-vl (Ollama) + PP-OCRv4 numeric backstop
  egui/         MIG 4.0 e-invoice XML parser (structured path)
  allocation/   OR-Tools LP + NumPy Monte-Carlo (per-line uncertainty)
  rules/        SEE per IR 2025/2547; defaults + row-derived mark-ups + resolve()
                fallback; grid EF loader (rules/gridef.py); MOENV EFs
  prices.py     dated certificate prices + scrap recovery (refuses unpublished quarters)
  writer/       openpyxl fill of the Commission template + flags sidecar
  waste/        Sight ②: scan (gross+net MoneyLoss), monthly drift + alert
  benchmark/    Sight ④: k>=5 schema, aggregate-only export, percentile screen
  costdelta/    fixlist.py — the ranked fix-list (screen.py feeds it; costdelta CLI/API kept as a deprecated alias)
  scheduler/    Sight ③: live #8931 grid feed, TOU tariffs, MILP, ledger
  api/          FastAPI app (§3)
  line_bot/     LINE webhook, simulator + real-channel modes (§4)
scripts/        corpus generator, LINE simulator, bake-off, recalc verifier, waste CLI, atlas scan
tests/golden/   screws-and-nuts + cement answer keys, firm A/B/C e2e goldens
data/cbam_official/   Commission template, filled examples, default values,
                      legal/ (the five EUR-Lex acts + grep-able .txt)
data/prices.yaml      dated certificate quarters + scrap recovery ranges
data/ef/              grid_ef.yaml (2025 industrial 0.466 default) + MOENV coefficient snapshot
data/mock_corpus/     generated synthetic corpus (gitignored — regenerate with scripts/make_mock_corpus.py)
out/                  generated artifacts (gitignored) — activity JSON, packs, fixlists, waste, schedules
```

---

## 8. Status vs Sprint-2 Definition of Done

| # | Item | Status |
|---|------|--------|
| 1 | All correctness defects closed; cement + firm_b/c goldens; ≥35 tests | ✅ 53 green |
| 2 | `waste/` live: drift+alert, gross/net type, method note, LINE+API | ✅ |
| 3 | Fix-list replaces costdelta; negative answer pinned | ✅ |
| 4 | Benchmark module + public k≥5 schema + percentile screen | ✅ |
| 5 | Simulator plays four sights in one session | ✅ (demo video: yours to record from it) |
| 6 | Engine consumes `prices.yaml` + `grid_ef.yaml`; refusal pinned; provenance everywhere | ✅ |
| 6b | Legal-text gates recorded ([docs/FACTS.md](docs/FACTS.md) §2) | ✅ no estimation cap; CN 7221 hole confirmed in the OJ |
| 7 | Kill-list grep clean; README current | ✅ this file |

**Not yet started** (next in the roadmap, [docs/PROJECT.md](docs/PROJECT.md) §6): the `pilot/` intake
kit (zh-TW checklist, consent one-pager, `carbonpass pilot run <folder>`, yield-measurement protocol,
PII scrub script) and bbox-grounded backstop hardening — both mentorship-window work, not submission
blockers.

Known caveats: openpyxl drops some conditional-formatting extensions of the template on save
(cosmetic); SEE cells in the output workbook are recomputed by Excel/LibreOffice on open — the
engine's numbers are in the `.flags.json` sidecar and `scripts/verify_workbook_recalc.py` proves the
workbook reproduces them (re-verified after the 0.466 grid-EF migration).
