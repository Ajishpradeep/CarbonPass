# CarbonPass — Sprint-2 Engineering Blueprint & Claude Code Kickoff

## From validated PoC to pilot-ready product: the Four Sights build

**Date:** 19 Jul 2026 · **Status:** 🟢 LIVE build order.
**This is the successor to `docs/10` (PoC blueprint) + `docs/11` (setup & kickoff prompt) — everything
in those two documents is BUILT and verified.** Do not re-execute them; they are history and reference.
**Read with:** `docs/20_master_handoff.md` (entry point: framing, doc index, kill-lists, watch-list) ·
`docs/19` (verified-claims register — the numbers the code must match) · `docs/18` (the frame) ·
`docs/15` §6 (engine defects this sprint closes) · **`docs/22_official_sources_inventory.md`
(official docs/datasets/APIs for this sprint — what's in-repo, what a human downloads, watch cadence).**

**Already seeded (19 Jul — consume, do not recreate):** `data/prices.yaml` (certificate quarters with
refuse-unpublished rule; scrap recovery ranges; wire-rod reference) · `data/ef/grid_ef.yaml` (2024/2025
factors incl. the 0.466 industrial split; select-by-year rule) · `data/official_refs/moea_grid_ef_2025.md`
(dated provenance snapshot) · empty `data/cbam_official/legal/` and `data/grid/history/` awaiting the
human downloads in docs/22 §B/§D.

Repo root: `/Users/pardeep/code/Personal/CarbonPass` · Deadline anchors: **submission 31 Jul 17:00** ·
mentorship pilot mid-Sep–mid-Oct · finals late Oct.

---

## 0. Where the project stands (everything below is DONE — do not rebuild)

- **Module 1 end-to-end:** photo/XML/CSV → VLM ingestion (qwen3-vl 8B + 4B, 100% on degraded corpus;
  PP-OCRv4 numeric backstop) → OR-Tools allocation + 10k Monte-Carlo → SEE rules engine (Commission
  screws-and-nuts example at rel 1e-9; 120 country sheets, 12,532 default rows, `resolve()` fallback)
  → filled 19-sheet Communication Template (LibreOffice-recompute-verified) → costdelta screen.
- **Waste scan (script-level):** `scripts/waste_scan.py` → per-line yield, gross carbon & purchase-value
  money (firm_a / firm_b outputs in `out/waste/`).
- **Module 2:** live #8931 grid feed → MILP schedule → NT$399,800/yr + 4.49 t ledger (TOU verified).
- **Module 3:** FastAPI + LINE webhook + credential-free simulator, zh-TW flow.
- **Corpus:** 3 synthetic firms + 6 photo degradations; ground truth (firm_a exact; b/c drift ~1e-4 —
  defect 11, fixed this sprint).
- **Atlas:** `scripts/atlas_scan.py` → 33/87 coverage, same-factory-moved table.
- 27/27 tests green. Proposal Rev 5 (root PDF/MD) externally verified (`docs/19`).

**The strategic shift this sprint serves** (`docs/18`): the product is no longer "a CBAM filing tool
with extras" — it is **four sights from one photograph**: ① product carbon (pack) · ② material loss
(waste map) · ③ energy timing (scheduler) · ④ peer position (benchmark). Code must catch up with the
frame: the waste map is a script, not a module; the benchmark does not exist; the fix-list ranking is
still a cost-delta screen; and several correctness debts would embarrass us under expert
cross-examination at finals.

---

## 1. The build, in order, with rationale

| # | Work item | Why this order |
|---|---|---|
| 1 | **Correctness debt** (defects from `docs/15` §6) | Cheap, protects everything downstream; a judge's expert WILL recompute our numbers |
| 2 | **Waste module productization** (script → `src/carbonpass/waste/` + monthly drift + net-of-resale) | The headline of the proposal must be a product surface, not a script |
| 3 | **Fix-list screen** (costdelta → ranked honest levers incl. "not worth it this year") | Converts three outputs into the one screen the demo pivots on |
| 4 | **Benchmark module** (Sight 4 — schema + percentile screen + open-data spec) | New capability; needed in demo at least on synthetic seed |
| 5 | **Demo video + submission assets** (by 29 Jul) | Deadline-bound; needs 2–4 done first so the demo shows four sights |
| 6 | **Pilot kit** (real-world data readiness) | Mentorship-critical; the pilot measures the one number that hasn't touched reality (the loss rate) |
| 7 | **Ingestion hardening** (bbox-grounded backstop; real-bill variance) | Real bills are the decisive VLM test — G2/G3 from docs/10 §11, still open |

### 1.1 Correctness debt (close ALL of these)

1. **Mark-up basis + per-row derivation** (`rules/see.py`): the workbook's marked-up column applies to
   TOTAL, not direct, and fertilisers carry flat 1% — derive the mark-up from the row
   (`DefaultValue.for_year()`), never hard-code 10/20/30. Add `for_year_direct()`. *(Defects 1–2.)*
2. **Non-steel golden test:** transcribe ONE unused Commission example (recommend cement — simplest,
   exercises indirect) from `data/cbam_official/template_examples/` into `tests/golden/`. This would
   have caught defects 1–2 a sprint earlier. *(Defect 6.)*
3. **Grid EF is stale and hard-coded:** replace `GRID_EF_KGCO2_PER_KWH = 0.474` with a loader for
   the **already-seeded** `data/ef/grid_ef.yaml` (2024: 0.474 · 2025: 0.467 overall / **0.466
   industrial** / 0.471 residential; provenance snapshot in `data/official_refs/moea_grid_ef_2025.md`).
   Default = `default_selection` from the file (2025 industrial); provenance string in every output.
   *(Defect 3 + `docs/19` correction; source docs/22 §D.)*
4. **firm_b/c ground truth:** derive GT from the rows the generator actually emits, not intended
   totals; then run firms B & C e2e as goldens. *(Defect 11.)*
5. **`defaults.lookup()` prefix guard:** short-query returns None silently — raise or fuzzy-match.
   *(Defect 10.)*
6. **Writer sector-label map:** replace 3 hard-coded `"Iron or steel products"` strings. *(Defect 5.)*
7. **Certificate price config:** wire the engine to the **already-seeded** `data/prices.yaml`
   (quarters carry explicit `published:` dates); engine must REFUSE to quote an unpublished quarter
   (Q3 2026 lands 5 Oct — kill-list). The same file feeds the waste module's scrap-recovery ranges
   (item 1.2). *(Defect 7; source docs/22 §C/§D.)*
8. **Legal-text gates** (as soon as a human completes docs/22 §B — the five EUR-Lex PDFs into
   `data/cbam_official/legal/`): (a) read **IR 2025/2547 Annex III** and record the estimation-cap
   verdict in `docs/15` §8.1 — this closes kill-list #2 in one direction or the other; (b) read
   **IR 2025/2621 Annex I at CN 7221** and confirm/refute the TW/TH/VN "hole" — this GATES the
   proposal's "hole in the book" line and the stainless-fallback logic in `defaults.resolve()`.
   Extract a grep-able `.txt` beside each PDF. Record both verdicts in the docs before touching code
   that depends on them.

### 1.2 Waste module (`src/carbonpass/waste/`)

- Port `scripts/waste_scan.py` logic into the package; script becomes a thin CLI wrapper.
- **Monthly drift series:** e-invoices are dated → loss% per line per month; alert rule = trailing
  3-month mean exceeds baseline by >2 s.d. (tunable) → `needs-attention` in LINE ("Line 2 loss rose
  7%→11% since March — check the die").
- **Gross AND net, enforced in the type:** `MoneyLoss{purchase_value, resale_recovery_pct, net}` —
  resale from `data/prices.yaml` (carbon ~30–40%, stainless ~35–45%, both dated; `docs/19` B9). It
  must be impossible to render money without both figures.
- **Method note in every JSON** (already in the script — keep): mass-before-cutting basis; remelt
  caveat; never "avoided".
- LINE command 「浪費」/「損耗」 and `/waste` API route; walk into the simulator flow.

### 1.3 Fix-list screen (`costdelta/` → `fixlist.py`)

One ranked screen per firm, levers in measured order: **yield → mill EPD → process energy → load
shifting**, each with NT$ and tCO₂e (gross/net where applicable), each able to answer **"not worth
it this year"** (the Thailand-row discipline — a negative answer is a feature, pinned by a test).
The EPD lever reuses firm_c logic ("one document from 中鋼 unlocks ~€60/t for your buyer").

### 1.4 Benchmark module (`src/carbonpass/benchmark/`)

- **Schema first** (this is also the open-data give-back spec): `{sector, cn_prefix, period,
  loss_pct, kwh_per_tonne, n_firms, percentiles}` — k-anonymity floor `n ≥ 5` before any figure is
  published; firm-level data never leaves the device (consistent with local-first).
- Seed with the 3 synthetic firms + published band (5–15%) so the demo can show a percentile screen
  honestly labelled "synthetic seed — pilot populates".
- LINE command 「我正常嗎」→ "Your carbon-screw loss 9.1% sits at the 55th percentile of the modelled
  band; the pilot benchmark will replace this."

### 1.5 Demo video + submission assets (hard gate: 29 Jul)

Script the LINE-simulator walkthrough as FOUR questions answered from one photo set: the pack, the
waste map (gross+net), the schedule, the percentile. Record via `scripts/line_simulator.py`; keep
under 3 minutes; zh-TW UI with English captions. Export application-form field answers from Rev 5.

### 1.6 Pilot kit (`pilot/` — new top-level dir, mentorship-critical)

Real-world data work the PoC never needed:

1. **Intake checklist (zh-TW + EN):** 12 months Taipower bills (photos OK) · e-GUI export of steel/
   gas/chemicals invoices (XML preferred; the e-GUI consent path already exists in Module 3) ·
   production log (any format; we provide a one-page template) · machine list (nameplate kW, hours) ·
   scrap sale receipts (for the NET number — new requirement, closes the resale loop with real data).
2. **Consent + data-handling one-pager:** local-first stated as practice: processing on our laptop
   on-site or the firm's machine; raw files never uploaded; only the pack the owner approves leaves.
3. **`carbonpass pilot run <folder>`:** one command over a real intake folder → all four sights +
   a gap report (what's missing, what fell back to defaults) — the mentorship demo IS this command.
4. **Yield measurement protocol:** the pilot's #1 scientific job is replacing the synthetic 9.1%
   with a measured value (invoiced steel mass in vs shipped tonnes out vs scrap receipts — three-way
   reconciliation). Pre-register the protocol in the repo BEFORE the pilot so the measured number,
   whatever it is, is credible. **If real loss is 4% not 9%, we say so at finals — the control-loop
   value survives; the headline shrinks honestly.**
5. **PII scrub:** `scripts/scrub_pilot_data.py` — hash 統編/names/addresses before anything is
   committed or shared; verify against `.gitignore`.

### 1.7 Ingestion hardening (parallel, as time allows)

bbox-grounded numeric matching (qwen3-VL grounding output ↔ PP-OCRv4 boxes) replacing presence-based
backstop (W1) · run firms B & C through the full VLM path · real-bill layout variants (老式帳單,
handwritten meter cards) added to the degradation matrix · optional: InternVL official weights on a
GPU box before finals if anyone challenges the bake-off.

---

## 2. Non-negotiable domain rules (Sprint-2 edition — supersedes docs/10 §2A where they differ)

1. **Per-product-per-YEAR, never per-shipment.** One SEE per CN code per calendar year. Unchanged.
2. **Electricity/indirect is recorded but NOT certificated for iron & steel.** The scheduler's carbon
   never touches CBAM money for CN 7318. Every scheduler output must carry this label (already
   enforced in the ledger — keep it that way in new surfaces).
3. **Mass counts BEFORE cutting** (Q&A §4.11) — the legal basis of the yield lever: scrap sits inside
   the declared SEE. This is why waste is a compliance feature, not a bolt-on.
4. **Defaults are lawful, unlimited, forever** (Q&A §4.25/§5.10). No 80/20 rule, no 20% cap, no 5%
   threshold — kill-list. The tool's job is to make actuals *worth it*, and to say when they aren't.
5. **Gross AND net, everywhere money or carbon appears.** Purchase value + net-of-resale;
   embodied-gross + remelt caveat. Enforced in types, not in prose.
6. **Provisional numbers stay labelled provisional.** 9.1% is synthetic mid-range in a 5–15% band
   until the pilot measures it. The UI says so.
7. **The tool prepares verification; it never certifies.** Zero CBAM verifiers exist yet (first
   accreditations ~Sept 2026; 8 NABs open — re-check, it moves).
8. **Prices and factors are dated config, never literals** — certificate €/t, grid EF, scrap
   recovery, TOU. Refuse to output an undated figure.
9. **Kill-list compliance** (`docs/20` §6 consolidates all): grep the diff before every commit —
   no €450–750, no "2,400 pages", no "throwing away", no 0.474-as-current, no "only four NABs".

---

## 3. New data & assets needed (what exists vs. what to create)

> **See `docs/22_official_sources_inventory.md`** for the full official-sources inventory (exact
> EUR-Lex URLs, watch-cadence pages, and the 30-minute human download list). `data/prices.yaml` and
> `data/ef/grid_ef.yaml` are already seeded (19 Jul) — the code items below consume them.

| Asset | Status | Action |
|---|---|---|
| `data/prices.yaml` (cert quarters w/ published dates, scrap resale %, wire-rod ref) | ✅ **seeded 19 Jul** | Consume in items 1.1.7 / 1.2; update per docs/20 §8 watch-list |
| `data/ef/grid_ef.yaml` (2024 + 2025 overall/industrial/residential) + provenance snapshot | ✅ **seeded 19 Jul** | Consume in item 1.1.3 |
| EU legal texts (5 EUR-Lex PDFs → `data/cbam_official/legal/`) | ⬇️ **human, 30 min** | docs/22 §B exact URLs; then run the legal-text gates (item 1.1.8) — **IR 2025/2547 Annex III** and **IR 2025/2621 CN 7221** are load-bearing |
| Accreditation state-of-play PDF + EA NAB list (dated snapshots → `data/official_refs/`) | ⬇️ + 👀 monthly | docs/22 §C; NAB count moves (4→8 already) — cite by retrieval date |
| Taipower TOU official rate PDF · MOF MIG 4.0 spec | ⬇️ small | docs/22 §D → `data/official_refs/`; TOU verified current (9.39/5.85/2.53, eff. 1 Oct 2025) |
| Logged #8931 history → real diurnal curve | 🟡 snapshot only | Cron-append `scripts/log_grid_feed.py`; seed `data/grid/history/` from #37331 (docs/22 §D) |
| Real AMI 15-min CSV import | ❌ | Parser + synthetic AMI fixture now; real file at pilot |
| Scrap sale receipts (real resale prices → replaces the 30–40% estimate) | 🏭 pilot | Pilot intake item — closes the net-money loop |
| Benchmark schema + seed | ❌ | Item 1.4 |
| Pilot consent/checklist docs (zh-TW) | ❌ | Item 1.6 |
| Commission cement example as golden | ✅ in repo, unused | Item 1.1.2 |
| LINE production channel (2 env vars) | 🟡 optional | Simulator suffices for submission; channel before finals |

---

## 4. Repo delta (target state after Sprint 2)

```
src/carbonpass/
├─ waste/          [NEW: scan.py, drift.py, money.py (gross+net types)]
├─ benchmark/      [NEW: schema.py, percentile.py, export.py (k>=5 anonymized)]
├─ costdelta/      [fixlist.py NEW — ranked levers, "not-yet" answers]
├─ rules/          [see.py markup fix; defaults.py guard; config-driven EF/prices]
├─ scheduler/      [ami.py NEW — 15-min CSV import; grid.py logged-history curve]
└─ (ingestion/allocation/writer/api unchanged in shape)
pilot/             [NEW: intake_checklist_zh.md, consent_zh.md, yield_protocol.md]
scripts/           [+ log_grid_feed.py, scrub_pilot_data.py; waste_scan.py → thin wrapper]
data/              [+ prices.yaml, ef/grid_ef.yaml]
tests/golden/      [+ cement example; firm_b/c e2e goldens after GT fix]
```

---

## 5. Sprint calendar

| Window | Sprint | Definition of Done |
|---|---|---|
| **Now → 29 Jul** | Sprint 2 (this doc) | §1 items 1–5: all defects closed, tests ≥ 35 green incl. cement golden + firm_b/c goldens + negative-fixlist test; waste & benchmark modules live in LINE simulator; demo video recorded; grep-clean vs kill-list |
| 29–31 Jul | Submission | Form filled from Rev 5; video linked; watch-list pass (`docs/20` §8) |
| Aug | Buffer / hardening | Item 1.7; pilot-kit docs translated; GPU bake-off if available |
| Mid-Sep → mid-Oct | Sprint 3 (pilot) | `carbonpass pilot run` on ONE real firm; measured yield replaces 9.1% everywhere (whatever it is); pack reviewed by a TW verification body; one load actually shifted with before/after ledger; benchmark seeded with real rows (n small, labelled) |
| Late Oct | Finals | Live demo + pilot deltas documented weekly; EP-vote and accreditation outcomes on the market slide |

---

## 6. The Claude Code kickoff prompt (paste this, inside the repo)

```
You are the lead engineer on CarbonPass, taking the project from validated PoC to pilot-ready
product. The PoC is COMPLETE — do not rebuild it. Before writing code, read, in this order, and
treat as source of truth:
  - docs/20_master_handoff.md   (project state, doc index, KILL-LIST §6 — binding on every commit)
  - docs/21_sprint2_blueprint_kickoff.md  (this build order — §1 is your work queue, §2 the rules)
  - docs/19_claim_verification_register.md (externally verified numbers the code must match)
  - docs/15_evidence_dossier.md §6        (the exact engine defects you are closing)
  - docs/18_claims_audit_and_refined_pitch.md (the Four Sights frame the code must serve)
  - docs/22_official_sources_inventory.md (official sources: what's in-repo, what's pending
                                           human download, watch cadence — your data contract)

PROJECT IN ONE LINE: a local-first AI that turns a small factory's photographed paperwork into
four kinds of sight — its EU CBAM data pack, its per-line material-waste map (gross AND net), its
grid-aware machine schedule, and its position against sector peers — offline, in Taiwanese, with
raw documents never leaving the building.

CURRENT STATE: Module 1 (pack), waste SCRIPT, Module 2 (scheduler), Module 3 (LINE) all work;
27/27 tests green; proposal Rev 5 verified. DATA CONTRACT (docs/22): data/prices.yaml and
data/ef/grid_ef.yaml are ALREADY SEEDED with dated, sourced values — consume them, never
recreate or override them with literals; data/official_refs/ holds dated provenance snapshots
(add new ones with dated filenames); data/cbam_official/legal/ and data/grid/history/ may still
be empty — they are filled by a human per docs/22 §B/§D, not by you fetching the web.

Your job is §1 of docs/21, IN ORDER:
  0. Preflight the data contract: assert prices.yaml + grid_ef.yaml parse and contain 2026Q2 and
     2025-industrial respectively; if data/cbam_official/legal/ is populated, FIRST run the two
     legal-text gates (docs/21 §1.1.8): record the IR 2025/2547 Annex III estimation-cap verdict
     in docs/15 §8.1, and the IR 2025/2621 CN 7221 verdict (it gates the "hole in the book"
     claim and the stainless fallback in defaults.resolve()). If legal/ is empty, print the
     docs/22 §B download list as a blocker note and continue — do not fetch it yourself.
  1. Close ALL correctness defects (docs/21 §1.1, items 1–8). Non-negotiables: derive mark-ups
     from the workbook row (fertilisers are flat 1% — hard-coded 10/20/30 is a BUG); wire the
     grid EF to data/ef/grid_ef.yaml (default = 2025 industrial 0.466 — 0.474 is stale) and
     certificate prices to data/prices.yaml with a hard REFUSAL to quote an unpublished quarter;
     fix firm_b/c ground truth by deriving it from emitted rows; add ONE non-steel golden test
     from the unused Commission cement example workbook (data/cbam_official/template_examples/).
  2. Productize waste: scripts/waste_scan.py → src/carbonpass/waste/ with (a) monthly drift
     series from dated e-invoices + an alert rule, (b) a MoneyLoss type that makes it IMPOSSIBLE
     to render purchase value without net-of-resale (rates from the seeded data/prices.yaml),
     (c) the method-note (mass-before-cutting; remelt caveat; never "avoided") in every output,
     (d) LINE command + /waste API route wired into the simulator.
  3. Replace the costdelta screen with a ranked fix-list (yield → mill-EPD → process energy →
     load shifting), every lever able to answer "not worth it this year" — pin that negative
     answer with a test (the Thailand-row discipline).
  4. Create src/carbonpass/benchmark/: anonymized schema (k>=5 floor, firm data never leaves
     device), percentile screen seeded from the 3 synthetic firms + the documented 5–15% band,
     honestly labelled "synthetic seed — pilot populates". This schema doubles as our open-data
     give-back spec — write it like a public artifact.
  5. Demo assets: make the LINE simulator run all four sights from one photo set in sequence;
     I will record the video from it.
Then, if time remains before 31 Jul: docs/21 §1.6 pilot kit (intake checklist zh-TW, consent
one-pager, `carbonpass pilot run <folder>`, yield-measurement protocol, PII scrub script) and
§1.7 ingestion hardening (bbox-grounded backstop).

RULES THAT OVERRIDE EVERYTHING (docs/21 §2): per-product-per-YEAR never per-shipment; electricity
is recorded but NOT certificated for iron & steel (label it in every new surface); mass counts
BEFORE cutting (the yield lever's legal basis); defaults are lawful forever (no 80/20, no 20% cap,
no 5% threshold); gross AND net together, enforced in types; provisional numbers labelled
provisional (9.1% is synthetic until the pilot); the tool prepares verification, never certifies;
no undated price or factor anywhere; grep every diff against docs/20 §6 kill-list before commit.

STACK (unchanged — don't re-litigate): Python 3.12/uv; Ollama qwen3-vl 8B/4B; docling + PP-OCRv4
backstop; OR-Tools + NumPy MC; openpyxl; FastAPI + LINE. Env facts: Ollama num_ctx >= 8192;
LibreOffice 26.2.4 for recompute checks; TC font for corpus rendering; 民國-year prompt example.

Ask me before: changing model/stack, paid dependencies, anything implying per-shipment logic,
publishing any benchmark row with n<5, or any claim touching the kill-list. Otherwise proceed
autonomously; small commits; run `uv run pytest` before each; report against docs/21 §7 at the end.
```

---

## 7. Definition of Done (Sprint 2)

1. All seven §1.1 defects closed; cement golden + firm_b/c e2e goldens green; ≥35 tests total.
2. `src/carbonpass/waste/` live: drift series + alert, gross/net MoneyLoss type, method note,
   LINE + API surfaces; `out/waste/` regenerated and matching (net figures now present).
3. Fix-list screen replaces costdelta in LINE/API; negative-answer test pinned.
4. Benchmark module with k≥5 schema doc (`docs/` or `schema/`), percentile screen on synthetic seed.
5. Simulator plays all four sights in one session; demo video recorded (≤3 min).
6. Engine consumes `data/prices.yaml` + `data/ef/grid_ef.yaml` (both pre-seeded); zero hard-coded
   prices/factors remain (grep `75.28|75.36|0.474|0.466` finds only config and tests); every output
   carries a provenance string; unpublished-quarter refusal pinned by a test.
6b. Legal-text gates: if `data/cbam_official/legal/` was populated during the sprint, both verdicts
   (2547 Annex III estimation cap; 2621 CN 7221 hole) are recorded in `docs/15` §8.1 and reflected
   in code/proposal; if not, the blocker is called out in the status report.
7. Kill-list grep clean; README updated; status report vs this section with blockers.

## 8. Pre-flight checklist (before pasting §6)

- [x] Everything in docs/10 + docs/11 (verified done — see §0)
- [x] `data/prices.yaml` + `data/ef/grid_ef.yaml` + `data/official_refs/moea_grid_ef_2025.md` seeded (19 Jul)
- [ ] **The 30-minute human download list (docs/22 §B/§D):** 5 EUR-Lex legal PDFs → `data/cbam_official/legal/` · accreditation state-of-play + EA NAB list (dated) → `data/official_refs/` · Taipower TOU PDF · MOF MIG 4.0 spec · first #37331 pull → `data/grid/history/` — *the legal PDFs unblock kickoff step 0's gates; the rest can land during the sprint*
- [ ] `git status` clean; branch for the sprint
- [ ] `uv run pytest` → 27/27 green (baseline)
- [ ] Ollama serving `qwen3-vl:8b-instruct` + `4b-instruct` (`ollama list`)
- [ ] Read docs/20 §6 kill-list once yourself — you are the last reviewer
- [ ] (Optional, before finals) LINE channel credentials in `.env`; GPU box for InternVL re-run
```
