# MASTER HANDOFF — CarbonPass, complete project state

**Date:** 18 Jul 2026 · **Status:** 🟢 **LIVE — the single entry point to this project.**
**Supersedes:** `docs/12_kickoff_session_handoff.md` (kickoff-era handoff, kept as history).
**Audience:** any fresh agent or engineer. Reading this file end-to-end, then following its pointers,
recovers the full analysis, every fact, every correction, and every artifact in the repo.

---

## 0. The project in one paragraph (current framing — use this one)

**CarbonPass** is a local-first AI copilot that gives a small export factory the operational
self-knowledge a large one gets from enterprise software, starting from a photograph of its own
paperwork. The frame is **"The Factory That Cannot See Itself"**: a 3,000-person factory sees its
carbon, its waste and its energy on a dashboard; a 30-person factory has the same data in a drawer
as paper. One photograph inside LINE (Mandarin/Taiwanese, offline, on-premises — raw documents never
leave the building) returns **four kinds of sight**: the EU CBAM data pack its buyer asks for, a
per-line waste map (gross *and* net), a grid-aware machine schedule, and the first anonymised sector
yield benchmark. Beachhead: the ~1,800-firm fastener cluster of Gangshan–Luzhu ("Kingdom of Screws"),
~2,600 CBAM-exposed Taiwanese SMEs. Entry for the **2026 Presidential Hackathon International Track**
("Digital Inclusion in the AI Era"), submission **31 Jul 2026, 17:00 GMT+8**.

Three sentences of positioning discipline: CBAM is an **assist and a forcing function, not a
catastrophe** (Taiwan's default is mild; compliance data is worth ~€4/t to a carbon-steel maker — we
say so first). The waste is **visible as a pile, invisible as information** (the owner *sells* his
scrap; he cannot attribute, price, carbon-link or benchmark it). The AI **replaces nobody** — in a
30-person firm there is no analyst to replace; it supplies a capability that never existed in the
building.

## 1. Current status (18 Jul 2026)

| Item | State |
|---|---|
| Submission proposal | **Rev 5** — `CarbonPass - Final Submission Proposal (PHIT 2026).pdf` (21 pp) + same-name `.md` at repo root; LaTeX source `docs/17_final_proposal_source.tex`; charts in `proposal_assets/` |
| Claim verification | **Complete** — every load-bearing claim audited by research agents against official sources; register in `docs/19` |
| Engine (Modules 1–3 + waste + atlas) | Working end-to-end; 27/27 tests green; all figures regenerable from committed scripts |
| Pilot / partners | **Targets, not secured** (TIFI member firm; MIRDC / Kaohsiung EPB) — say so honestly everywhere |
| Open before 31 Jul | Demo video · real LINE channel (optional; simulator suffices) · `GRID_EF` update 0.474→0.466 · price re-checks (watch-list §8) · team roster in application form |

## 2. How the thesis evolved (read this to understand *why* the docs disagree)

Each stage killed part of its predecessor. The corrections are the project's credibility exhibit —
never un-kill a dead claim.

| Stage | Thesis | What killed it / what survived | Doc |
|---|---|---|---|
| 1. Compliance saviour | "CBAM's €450–750/t defaults will crush Gangshan; we generate the pack" | **Dead:** our own engine parsed the adopted tables — Taiwan's default is €224/t, among the world's mildest; data worth ~€4/t. Survived: the engine, the pack, the buyer-retention logic | `docs/09` (Rev 2), kill in `docs/12` §4 |
| 2. Provability divide | "CBAM taxes the inability to *prove* carbon; 33/87 book split; 44× reward gap; policy fix" | **Demoted, not dead:** all facts verified and reusable (atlas, accreditation gateway, same-factory-moved) but it's a legislation deck with no person in it — wrong register for this hackathon. Survived: every measurement, as *expansion* evidence | `docs/14` (annex), evidence in `docs/15` |
| 3. Waste thesis | "They throw away 10% of their steel and nobody has ever counted it" | **Corrected:** scrap is *sold*, not trashed; owner knows the tonnage; money was quoted at purchase price not net. Survived (at honest magnitude): the information gap, the 80× yield lever, the stainless finding | `docs/16`, corrections in `docs/18` §2 |
| 4. **Organizational blind spots (LIVE)** | "The factory that cannot see itself — four blind spots, one data spine; sight → reduction" | Current frame. Externally verified end-to-end | `docs/18` (frame), `docs/19` (verification), Rev 5 PDF |

**The recurring failure mode, name it to avoid it:** collapsing a nuanced quantity into its gross
upper bound (€450–750 was the fallback, not Taiwan; NT$7.35M was purchase price, not net; 758 t is
embodied, not atmospheric). **Rule: every headline number ships with its net/actual twin in the same
sentence.**

## 3. Document index (read order for a fresh session)

| # | File | Status | What it holds |
|---|---|---|---|
| — | **this file** | 🟢 LIVE | Entry point |
| 21 | `docs/21_sprint2_blueprint_kickoff.md` | 🟢 LIVE | **The build order**: Sprint-2 engineering blueprint + Claude Code kickoff prompt (successor to docs/10+11, which are fully built); correctness-debt closure, waste/benchmark productization, pilot kit, sprint calendar |
| 22 | `docs/22_official_sources_inventory.md` | 🟢 LIVE | **Official docs/datasets/APIs for Sprint 2** (successor to docs/10 §3): what's in-repo, the 5 EUR-Lex legal texts to download (incl. the critical IR 2025/2547 Annex III check), watch-cadence pages, new configs `data/prices.yaml` + `data/ef/grid_ef.yaml`, pilot-only inputs |
| 19 | `docs/19_claim_verification_register.md` | 🟢 LIVE | Claim-by-claim external audit (EU/Taiwan/industry), corrections applied, standing rules, watch-list |
| 18 | `docs/18_claims_audit_and_refined_pitch.md` | 🟢 LIVE | The blind-spots frame, magnitude-honesty audit, reduction theory, winners-study lessons |
| 17 | `docs/17_final_proposal_source.tex` (+ root PDF/MD) | 🟢 LIVE | The submission artifact itself (Rev 5) |
| 16 | `docs/16_waste_extension.md` | 🟡 superseded framing | Waste findings + honest limits §7 (still binding); "trash" framing corrected by 18 |
| 15 | `docs/15_evidence_dossier.md` | 🟢 evidence | Primary-source dossier: CBAM legal quotes, workbook forensics, **kill-list §5**, **engine defects §6**, Commission-file defects §7, unresolved §8 |
| 14 | `docs/14_scope_extension.md` | 🟡 annex | Provability-divide facts (verified): 33/87, 4-doors (now 8 — see 19), 44× table |
| 13 | `docs/13_sprint1_report.md` | ✅ history | Sprint-1 results: VLM bake-off, backstop, scheduler, LINE, LibreOffice recompute |
| 12 | `docs/12_kickoff_session_handoff.md` | ✅ history | Kickoff build record; the €4/€60 finding; template mechanics |
| 11/10/09/00 | setup, PoC blueprint, master proposal Rev 2, first handoff | ✅ history | Deep background; 09 §4 capability audit & references still cited |
| — | `materials/` | reference | **PHIT Winners Study** (what actually wins — read before any pitch work), prior proposal iterations, charts |

## 4. The current frame, operationally

Four blind spots = four product outputs, each with a measured number (all engine-produced, all in `out/`):

| Owner's question | Output | Measured anchor |
|---|---|---|
| "What carbon is in my product?" | CBAM pack in the Commission's template | Commission's own worked example reproduced at rel 1e-9; Taiwan default €224.18/t vs actual €220.15 (firm_a: €4.03/t); mill EPD lever €60.31/t (firm_c) |
| "What do I lose between buying and shipping?" | Waste map, per line, monthly drift | 1.10:1 steel-in/product-out; firm_a 758 tCO₂e gross, NT$7.35M gross / ~NT$4–5M net; 9.1%→5% scenario = 359 t + NT$3.48M = **80×** the scheduler |
| "When should my machines run?" | Grid-aware MILP schedule | NT$399,800/yr + 4.49 tCO₂e (firm_a, live #8931 feed, verified TOU 9.39/5.85/2.53) |
| "Am I normal?" | Anonymised cluster benchmark (open-data give-back) | First of its kind; the sector-scale reduction multiplier |

Reduction levers, ranked honestly (proposal §2.5.1): yield (80×, moves the declared number 1:1) →
mill EPD / precursor route (€60/t; EAF rod fractions of BF in the EU's own tables) → heat-treatment
energy benchmarking → load shifting (ranked last by the tool itself) → cluster benchmark multiplier.
The stainless finding (`docs/16` §4): Taiwan's stainless block is ~2.6× world median, CN 7221 has no
Taiwan row (fallback 5.302 applies), the default under-counts honest stainless ~2× — why a *sight*
tool beats a *filing* tool.

Inclusion proof (the demo, not a slide): qwen3-VL **4B**, 336/336 fields across six phone-photo
degradations, 18–31 s/doc, laptop, offline, no GPU; LINE zh-TW; local-first.

## 5. Engine & repo state

```
src/carbonpass/   ingestion (VLM + docling + PP-OCRv4 backstop) · allocation (OR-Tools LP + 10k MC)
                  rules (SEE, defaults + resolve() fallback, markup) · writer (template fill + flags)
                  scheduler (grid.py #8931 live, tariffs, milp, ledger) · costdelta · api (FastAPI + LINE)
scripts/          make_mock_corpus · degrade_corpus · vlm_bakeoff · atlas_scan · waste_scan
                  verify_workbook_recalc · line_simulator · pull_moenv_ef · inspect_template
data/cbam_official/  default_values.xlsx (Reg 2025/2621) · benchmarks.xlsx (2025/2620) ·
                  communication_template.xlsx + 7 filled Commission examples (Screws-and-nuts = golden)
                  · cbam_qa.pdf (May 2026, LIVE rules) · guidance PDFs (2023, EXPIRED — mechanics only!)
data/ef/          moenv_coefficients.json (1,164 rows; wired into nothing — defect 4)
out/              firm_a/b/c activity, packs, flags, costdelta · waste/ · atlas/ · bakeoff/ · schedule
```

Run: `uv run pytest` (27 green) · `carbonpass {ingest,pack,costdelta,schedule,serve}` · README has
per-artifact commands. Environment: Python 3.12 (uv), Ollama `qwen3-vl:8b-instruct` + `4b-instruct` +
`blaifa/InternVL3_5:8b`, LibreOffice 26.2.4 (installed from `mirror.twds.com.tw` — TDF host resets
long downloads), TC font required for corpus render (`Arial Unicode.ttf`; reportlab's STSong drops
TC glyphs), Ollama `num_ctx` must be ≥8192, 民國-year needs a prompt example.

**Open engine defects** (full detail `docs/15` §6): markup applied to TOTAL not direct + hard-coded
10/20/30 → **cement/fertiliser numbers unpublishable** (steel/alu fine) · `GRID_EF` hard-coded
0.474 → **update to 0.466 industrial (2025, published 2 Jun 2026)** · firm_b/c ground truth drifts
rel ~1e-4 (generator derives GT from intended totals, not emitted rows) · backstop is presence-based
(bbox grounding = upgrade) · certificate price hard-coded {Q1,Q2} · `defaults.lookup()` silent-None
on short CN queries · writer steel-labelled (1-line fix for other sectors).

## 6. Claim discipline (binding — extends `docs/15` §5, `docs/18` §2, `docs/19` §5)

Never: €450–750/t for Taiwan · "80% must be verified actual data" / 20% default cap (repealed-era) ·
"5% variance threshold" (exists nowhere) · "verification costs €5k–50k" (untraceable) · "403
verifiers" (that's EU ETS; CBAM count is zero) · "developing countries get worse defaults" (false by
measurement) · "2,400-page regulation" (say: eleven legislative acts + annexes) · "throwing scrap
away / nobody counts it" (sold; say information gap) · gross waste money without net (recovery
30–40%) · "avoided" for gross embodied carbon · 0.474 as current grid EF · "only four NABs" (eight,
2 Jul 2026, rising) · "top-3 exporter" without "by volume; #4 by value" · a Q3-2026 certificate price
(none until 5 Oct) · ISO 14067 as CBAM by-product (LCA factors not accepted, QA §4.24) · citing the
2023 guidance PDFs as rule source (expired; mechanics only).

Always: certificates = obligation 2026, sales Feb 2027, surrender 30 Sep 2027 · electricity/indirect
is **recorded but not certificated for iron & steel** (scheduler carbon ≠ CBAM money) · mass counts
**before cutting** (scrap sits inside declared SEE — the yield lever's legal basis) · 54% of SME
plants on paper/spreadsheets (IoT Analytics 2025) · cost of poor quality 10–20% of revenue (ASQ) ·
5–15% loss band, 9.1% is synthetic mid-range, pilot calibrates · pilot partners are targets.

## 7. Competition facts & strategy (from Handbook + `materials/` winners study)

Dates: submission **31 Jul 17:00** · preliminary 6–16 Aug (Feasibility 40 / Innovation 30 / Social
Impact 30) · mentorship mid-Sep–mid-Oct · finals late Oct (+ Implementation & Verification 30%,
scored on **delta since submission**; demo or code description required) · awards Dec. Team 3–10,
≥1 non-ROC national, 2 contacts, all English.

Winners-study lessons (2019–2025, 14 Teams of Excellence): theme-lock absolute — 2023–25 winners are
all *AI + named beneficiary population*, so Mr. Lin stays the protagonist and inclusion must be **in
the demo** (LINE, offline 4B) · feasibility beats innovation — bring the working thing · exportable
diplomatic story scores (New Southbound; 44× divide as expansion register) · **winning ≠ surviving:
every winner with an afterlife had an institution — MOENV/SMESA/TIFI/MIRDC integration is the
sustainability plan**.

Scheduled natural experiments inside the mentorship window: EP plenary vote on the ~180-category
downstream extension (Sept 2026; committee passed 6 Jul) · first CBAM verifier accreditations
(~Sept 2026; 8 NABs open).

## 8. Watch-list — moving numbers, re-verify before 31 Jul and again before finals

| Number | Current (18 Jul 2026) | Moves |
|---|---|---|
| CBAM certificate price | €75.28 (Q2) | Q3 published 5 Oct |
| Grid EF | 0.467 / 0.466 industrial (2025) | annually (~Jun) |
| NABs accepting third-country verifiers | 8 (EA list 2 Jul) | rising; EC vs EA lists disagree — cite retrieval date |
| Scrap CFR Taiwan | ~US$325/t | weekly |
| Wire rod (domestic) | ~NT$27,350/t (Apr) | monthly (waste figures at NT$24.5k are conservative) |
| TOU tariff | 9.39/5.85/2.53 confirmed (eff. 1 Oct 2025) | next review ~Oct 2026 |
| EP plenary vote | expected Sept | update market slide with outcome before finals |
| MOENV CBAM platform / verifier-subsidy news | platform live Apr 2026; no subsidy announced | any week |

## 9. Next steps, in order of value

> **Execution note (19 Jul):** items 1 and 3 below are now specified as a concrete build order with a
> paste-able Claude Code kickoff prompt in **`docs/21_sprint2_blueprint_kickoff.md`** — start there.

1. **Submission (by 31 Jul):** demo video (simulator is recordable today: `scripts/line_simulator.py`) ·
   application form filled field-by-field from Rev 5 · `GRID_EF`→0.466 (+ test) · final watch-list pass ·
   team roster + ≥1 non-ROC national confirmed.
2. **Mentorship (Sep–Oct):** ONE real pilot firm (real consented bills → real pack + waste map;
   yield magnitude measured — the decisive test of the 9.1% placeholder) · pack structure reviewed by
   a Taiwanese GHG-verification body · one flexible load actually shifted, before/after ledger ·
   track the two September events (§7) and update the deck with outcomes.
3. **Engineering (as time allows):** fix markup-basis defects (unlocks cement/fertiliser + a non-steel
   golden test from the unused Commission examples) · firm_b/c ground-truth fix · bbox-grounded
   backstop · real AMI CSV import · wire MOENV coefficients (`rules/ef.py`) into the org-inventory path.
4. **Finals (late Oct):** live demo + measured pilot deltas, documented weekly — Implementation &
   Verification is the 30% that did not exist at preliminaries; it is won during mentorship, not on
   stage.
