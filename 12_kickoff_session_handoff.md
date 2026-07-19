# SESSION HANDOFF — Module 1 Kickoff Build (16 Jul 2026)

> ⚠️ **SUPERSEDED (18 Jul 2026).** This is the kickoff-era handoff, kept as history. The live,
> complete entry point to the project is **`docs/20_master_handoff.md`** — read that first; it
> indexes every doc (including this one), the current framing, the kill-lists, and next steps.

**Purpose:** single self-sufficient document to resume from a fresh session. It records what
was built in the kickoff coding session, what was verified, the one strategic finding that
changes the pitch, and the next steps. Read order for a new session: **this file**, then
`docs/10_poc_blueprint.md` (§2A is load-bearing), `docs/00_session_handoff.md` (kill-list),
`docs/11_setup_kickoff.md` (original plan this session executed), `docs/09_master_proposal.md`
(product concept).

---

## 1. What this project is (one paragraph)

**CarbonPass** = local-first AI for Taiwan's fastener SMEs (CN 7318, Gangshan–Luzhu):
photograph a Taipower bill + steel e-invoices + production log → verifier-ready **EU CBAM
"Communication Template for installations"** (.xlsx, the Commission's own file) with one SEE
(tCO2e/t) per CN code per **calendar year** (never per shipment), every figure flagged
actual/default with per-line uncertainty, plus a default-vs-actual buyer-cost screen.
Entry for the 2026 Presidential Hackathon International Track (submission **31 Jul 2026**).
Module 2 (grid scheduler) and Module 3 (LINE bot) come later.

## 2. State at end of this session — ALL 7 kickoff steps DONE

Repo `/Users/pardeep/code/Personal/CarbonPass`, 8 commits on `main`, `uv run pytest` → 9/9 green.

| Commit | What |
|---|---|
| `badabcf` | scaffold, deps (Python **3.12**, uv), **MOENV pagination bugfix** — table was silently truncated at 1,000 rows; full table = **1,164** |
| `0974de7` | `schema/cbam_template_map.yaml` + golden values from the answer key |
| `81d97cb` | `scripts/make_mock_corpus.py` — 3 firms, 295 files + ground truth |
| `436a185` | allocation (OR-Tools LP + 10k Monte-Carlo) + rules (SEE, defaults, MOENV EF); golden tests pass at **rel 1e-9** |
| `fc3bbb8` | ingestion (docling pre-pass → qwen3-vl via Ollama; MIG 4.0 XML parser); **Firm A e2e: 72/72 bill fields = 100%** |
| `82f2d84` | writer (fills Commission template, formula-overwrite guard, flags sidecar) + costdelta screen |
| `d44fc71` | README (run commands, measured results, DoD table) |
| `e1e13ff` | committed `data/cbam_official/` assets (template, examples, default values) |

**Environment set up this session:** `brew install ollama` (0.32.0), `ollama pull
qwen3-vl:8b-instruct` (Q4_K_M, 5.8 GB) — both done and working. Python pinned 3.12
(docs said 3.10/3.11; 3.12 works with every dep — decision confirmed by owner).
`.env` holds `MOENV_API_KEY` (never commit it; it briefly leaked into git-tracked
`.env.example` and was removed).

**Definition of Done (docs/11 §6): 7/7 met.** Outputs live in `out/` (gitignored):
`firm_a_activity.json`, `firm_a_communication_template.xlsx` (19 sheets, formulas intact),
`.flags.json` sidecar, `firm_a_costdelta.json`.

## 3. How the pipeline works (what a new session needs to know)

```
ingest  data/mock_corpus/firm_X → out/firm_X_activity.json     (schema/activity_data.schema.json)
pack    out/firm_X_activity.json → filled .xlsx + .flags.json  (writer touches INPUT cells only)
costdelta out/firm_X_activity.json → buyer screen
```
Run commands are in README.md. Corpus regenerates with `uv run python scripts/make_mock_corpus.py`.

Key mechanics discovered/verified this session:

- **Template mechanics** (`schema/cbam_template_map.yaml` is the contract):
  the workbook computes SEE itself via hidden `InputOutput` array-formula matrix
  (AK71:AK80 direct / AM71:AM80 indirect / AO71:AO80 embedded electricity). The writer fills
  ~50 input cells; Excel/LibreOffice recomputes on open (openpyxl doesn't evaluate).
  `D_Processes` blocks: header row 11, stride 65; `E_PurchPrec` blocks: header 14, stride 44.
  A runtime guard refuses to overwrite formula cells — it caught 2 map errors already; trust it.
- **The SEE chain** (golden-tested against the Commission's screws & nuts example):
  `SEE_dir(good) = DirEm(p)/AL(p) + Σ m_i/AL(p)·SEE_dir(prec_i)`; indirect analogous via
  spec-electricity × EF. Answer-key targets: CN 73181542 → 2.4135382 total; CN 73181535 →
  4.2312427. Reproduced at rel 1e-9 (`tests/golden/`).
- **Ingestion**: structured-first — steel/gas from MIG 4.0 e-invoice XML (`egui/parser.py`),
  Taipower bill via qwen3-vl photo parse (+docling layout context), production log CSV.
  Firm A: 100% field accuracy (72/72 across 12 bills), aggregate electricity rel err 2e-6.
  Gotchas fixed: ROC year 民國115→2026 needs an explicit example in the prompt; Ollama default
  num_ctx 4096 is too small → client sets 8192.
- **Corpus** (synthetic, deterministic, gitignored): firm_a = default-precursor common case;
  firm_b = carbon+stainless on one meter (allocation case); firm_c = mill-EPD case.
  Traditional Chinese rendering requires `/Library/Fonts/Arial Unicode.ttf` — reportlab's
  built-in `STSong-Light` is Simplified-only and silently drops TC glyphs (電, 灣, 費…).

## 4. THE FINDING — the €450–750/t default claim is dead for Taiwan CN 7318

**Old claim** (docs/09 §3.1, docs/00 §2): actual ≈€150/t vs default **€450–750/t** → savings
€300–600/t ("30–50% of product value"). Basis: industry estimates assuming defaults at the
worst observed intensity worldwide.

**Adopted reality** (`data/cbam_official/default_values.xlsx`, "DVs as adopted v20260204",
machine-readable IR 2025/2621; parsed + unit-tested in `rules/defaults.py`): defaults are
**per-country**. Taiwan sheet, CN 7318 (all 15xx/16xx lines): direct **2.70719 tCO2e/t**,
indirect **N/A** (confirms G7: indirect not in the CN 7318 certificate). With mark-ups and the
€75.28 (Q2 2026) certificate price:

| Year | Default (marked-up) | Buyer cost/t |
|---|---|---|
| 2026 (+10%) | 2.9779 | **€224.18** |
| 2027 (+20%) | 3.2486 | €244.56 |
| 2028+ (+30%)| 3.5193 | €264.94 |

Wire-rod precursor defaults (Taiwan): CN 7213 = 2.297829146, CN 7227 = 2.17 (+ mark-up when used).

**Measured on our corpus (engine output, ground-truth-verified):**

| Firm | Situation | Actual SEE (dir) | Buyer cost | Delta vs default | Per year |
|---|---|---|---|---|---|
| firm_a | no mill EPD (default precursor) | 2.924 | €220.15/t | **€4.03/t** | ~€12k @3,000 t |
| firm_c | mill EPD supplied | 2.177 | €163.87/t | **€60.31/t** | **~€108k @1,800 t** |

**Deviation from our claim: the penalty side was overstated 2–3×; the savings side 5–150×.**

**Confidence:** high — the source is the Commission's adopted file that importers will
actually use, sitting in the repo; mark-up arithmetic matches to the last digit.
Open check (15 min, next session): cross-read the IR 2025/2621 legal text (C4 link in
docs/10 §3) to confirm the xlsx transcription, and re-verify the certificate price quarterly.

**Why the product still works (the pitch shifts, honestly, and gets better):**
1. **The value concentrated into one document.** ~93% of the achievable saving comes from the
   mill EPD for the wire rod (firm_a €4/t → firm_c €60/t). The tool's killer move is telling
   the owner *"request this one EPD from 中鋼; it unlocks ~€108k/yr for your buyer"* — and
   flagging it automatically (`needs-attention` lines do this today).
2. **The penalty ratchets automatically** (+10→30% by 2028) and the certificate price is
   expected to rise: every delta grows without us claiming anything speculative.
3. **Retention, not €/t, was always the binding argument** — the importer keeps the supplier
   whose verifier-ready pack shows up (audit exposure, Scope-3, 50t de-minimis cumulated per
   importer). Unchanged.
4. **Consultant economics now favor us MORE:** nobody hires a per-engagement consultant for a
   €12k/yr problem — but a near-zero-marginal-cost tool clears that bar easily.
5. **New honest feature to build:** verification costs (accredited verifier, thousands €/yr)
   vs data value — the screen can answer "is this worth it for me this year?" per firm.

**KILL-LIST ADDITION (extends docs/00 §4): never reuse "€450–750/t default" or "30–50% of
product value" for Taiwan-origin CN 7318.** Use regulation-derived numbers from
`rules/defaults.py`. (Saved to agent memory as `taiwan-default-value-gap` too.)

### 4b. The competitor inversion (added 17 Jul — now in docs/09 Rev. 2)

Defaults are **per-country**. CN 7318 direct SEE by origin (base, before mark-up):
Taiwan **2.707** · Thailand 2.408 · US 2.580 · Vietnam 2.750 · Japan 2.800 · S. Korea 3.474 ·
fallback "other countries" 4.801 · Türkiye 5.430 · India 5.720 · China **6.375** · Indonesia 8.230.
So the €450–750/t folklore was *true for China/India/Türkiye*, not Taiwan → **CBAM is a tariff
on Taiwan's competitors**: TW no-data €224/t vs China no-data €528/t (2026) = ~€300/t legislated
advantage; ~€364/t with the mill EPD. Wire-rod precursor defaults also favour TW (7213: 2.298 vs
CN 3.169; 7227: 2.17 vs CN 6.12). Benchmarks workbook (Reg 2025/2620, in repo): CN 7318 deduction
1.364 (carbon)/1.154 (stainless) tCO2e/t — additive + identical across default/actual paths →
cuts levels during free-allocation phase-in (to 2034) but **preserves every delta**; exact
phase-in factor still to verify against the legal text. **docs/09 Rev. 2 (17 Jul) rebuilt
§2.3/§3.1/§5.2/§7.x/§8/§9 + refs [32][33][34] on these numbers — the proposal is the
submission-facing artifact; keep it consistent with `rules/defaults.py` output if data updates.

## 5. Known caveats / honest limits

- openpyxl drops some conditional-formatting extensions of the template on save (cosmetic).
- Output workbook SEE cells recompute in Excel/LibreOffice; cross-check numbers live in the
  `.flags.json` sidecar, pinned by golden tests. Not yet opened in real Excel — do once.
- Corpus PNGs are clean renders; no tilt/blur/phone-photo degradation tested yet.
- firm_a/b legitimately breach the 20% default ceiling for complex goods → flagged; that's
  the feature, not a bug.
- VLM accuracy (100%) is on synthetic bills — treat as upper bound until the pilot's real
  consented bills (gap G2/G3 in docs/10 §11).
- Allocation LP currently collapses to engineering priors (bill-level data only — honest per
  G4); sub-meter/AMI constraints attach without restructuring.

> **Update 17 Jul 2026:** Sprint 1 executed — items 1, 3(partly), 4(backstop), 5 and 6(FastAPI/
> LINE + Module 2) below are done; see **docs/13_sprint1_report.md** for results (8B bake-off
> 100% across degradations, PP-OCRv4 backstop catch-rate, NT$399,800/yr firm_a shift plan,
> LINE simulator e2e, workbook-recompute verification).

## 6. Next steps (in order of value)

> ⚠️ **POINTER (17 Jul 2026):** superseded by **`docs/14_scope_extension.md`** §6. The §4 finding below
> still stands and got bigger: the atlas scan shows **33 countries have a CN 7318 15 row and 87 have
> none**, and the "same factory, moved" table prices proving at **€4/t in Taiwan vs €177/t with no
> book**. Item 2 below (verify IR 2025/2621 legal text) is now **critical and unresolved** —
> see `docs/15` §8.1. Kill-list additions: `docs/15` §5.

1. **Sprint-1 bake-off** (docs/10 §6.2): qwen3-vl:8b vs **InternVL3.5-8B**, ±docling,
   ±PaddleOCR-VL backstop, on degraded photos (tilt/blur/low-light augmentation of the corpus).
   Also `ollama pull qwen3-vl:4b-instruct` for the CPU/edge path.
2. **Verify IR 2025/2621 legal text** against the xlsx (15 min) + re-check certificate price.
3. **Verification-cost screen**: add verifier-fee assumption to costdelta ("worth it this
   year?" answer per firm) — the honest differentiator.
4. **Run firms B & C e2e** through the VLM path (only A was run full-pipe); B exercises the
   two-process allocation in the writer (multi-block fill is coded but only dry-run on C).
5. **Open the filled xlsx in Excel/LibreOffice once** — confirm SEE cells recompute to the
   sidecar values.
6. **FastAPI surface + LINE bot** (Module 3) and **Module 2** (grid scheduler, #8931 feed) —
   per docs/10 §8 sprint plan.
7. **Demo video + submission materials** — deadline 31 Jul 2026; use the firm_a→firm_c EPD
   narrative and regulation-derived numbers.
8. Track the **EP plenary vote (Sep 2026)** on the ~180-category downstream extension.

## 7. Sources / files index

- **In-repo data:** `data/cbam_official/` (communication_template.xlsx, template_examples/
  incl. the screws & nuts answer key, default_values.xlsx = C5 "DVs as adopted v20260204",
  benchmarks.xlsx, guidance EN/ZH, Q&A) · `data/ef/moenv_coefficients.json` (1,164 rows,
  refresh: `python scripts/pull_moenv_ef.py`).
- **Regulations (free, URLs in docs/10 §3):** IR 2025/2547 (methodology), IR 2025/2621
  (defaults), IR 2025/2546 (verification). Certificate price page = C13.
- **Prior docs:** `docs/00_session_handoff.md` (verified facts + kill-list),
  `docs/09_master_proposal.md` (concept), `docs/10_poc_blueprint.md` (tech spec; §2A =
  how CBAM actually works), `docs/11_setup_kickoff.md` (the plan this session executed).
- **Taiwan data:** MOENV EF data.gov.tw #28176 (API: data.moenv.gov.tw, key in `.env`);
  Taipower #8931/#37331 (Module 2); e-invoice MIG 4.0 / Turnkey
  (github.com/phidiassj/TaiwanEInvoiceOpenAPI).
- **Stack decisions (locked):** qwen3-vl:8b-instruct on Ollama (local-first), Docling
  pre-pass, OR-Tools + NumPy MC, openpyxl, FastAPI, LINE. Only approved VLM challenger:
  InternVL3.5-8B.
