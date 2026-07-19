# CarbonPass — Project Book

**Date:** 19 Jul 2026 · **Status:** 🟢 LIVE — the single entry point to this project.
**The live doc set is exactly four files:** [`README.md`](../README.md) (run the code) · **this file**
(what the project is, where it stands, what happens next) · [`FACTS.md`](FACTS.md) (every verified
number and the claim discipline — the only place a pitch may take a fact from) ·
[`SOURCES.md`](SOURCES.md) (official data sources and the data contract). Everything older lives in
[`archive/`](archive/) and is history, not guidance.

---

## 1. The project in one paragraph

**CarbonPass** is a local-first AI copilot that gives a small export factory the operational
self-knowledge a large one gets from enterprise software, starting from a photograph of its own
paperwork. The frame is **"The Factory That Cannot See Itself"**: a 3,000-person factory sees its
carbon, its waste and its energy on a dashboard; a 30-person factory has the same data in a drawer as
paper. One photograph inside LINE (Mandarin/Taiwanese, offline, on-premises — raw documents never
leave the building) returns **four kinds of sight**: the EU CBAM data pack its buyer asks for, a
per-line waste map (gross *and* net), a grid-aware machine schedule, and the first anonymised sector
yield benchmark. Beachhead: the ~1,800-firm fastener cluster of Gangshan–Luzhu ("Kingdom of Screws"),
~2,600 CBAM-exposed Taiwanese SMEs. Entry for the **2026 Presidential Hackathon International Track**
("Digital Inclusion in the AI Era"), submission **31 Jul 2026, 17:00 GMT+8**.

Positioning discipline, three sentences: CBAM is an **assist and a forcing function, not a
catastrophe** (Taiwan's default is mild; compliance data is worth ~€4/t to a carbon-steel maker — we
say so first). The waste is **visible as a pile, invisible as information** (the owner *sells* his
scrap; he cannot attribute, price, carbon-link or benchmark it). The AI **replaces nobody** — in a
30-person firm there is no analyst to replace; it supplies a capability that never existed in the
building.

**The one rule that guards against our own recurring failure mode:** we have twice inflated a claim
by collapsing a nuanced quantity into its gross upper bound (€450–750 was the fallback, not Taiwan;
NT$7.35M was purchase price, not net; 758 t is embodied, not atmospheric). **Every headline number
ships with its net/actual twin in the same sentence.** The engine now enforces this in types
(`MoneyLoss` cannot render gross without net).

## 2. The four sights (all built, all measured)

| Owner's question | Output | Measured anchor (synthetic corpus — pilot calibrates) |
|---|---|---|
| "What carbon is in my product?" | CBAM pack in the Commission's template + ranked fix-list | Commission's own worked examples (screws-and-nuts AND cement) reproduced at rel 1e-9; Taiwan default €224.18/t vs firm_a actual €220.15 → data worth €4.03/t (and the tool says when that's *not* worth chasing); firm_c mill-EPD lever €60.31/t |
| "What do I lose between buying and shipping?" | Waste map per line, monthly drift alert, gross AND net | 1.10:1 steel-in/product-out; firm_a 9.1% loss = 758 tCO₂e/yr embodied carbon purchased-but-never-shipped, NT$7.35M at purchase price / **NT$4.4–5.1M net of scrap resale**; 5%-scenario = 359 t + NT$3.48M = **80× the scheduler** |
| "When should my machines run?" | Grid-aware MILP schedule (live #8931 feed) | NT$399,800/yr + ~4 tCO₂e — labelled: indirect, recorded but NOT in the CN 7318 certificate |
| "Am I normal?" | Anonymised cluster benchmark (k≥5 floor; open-data give-back spec) | Synthetic seed on the documented 5–15% band, labelled as such; the sector-scale reduction multiplier |

**Reduction levers, ranked honestly** (the fix-list screen keeps this fixed order and each lever can
answer "not worth it this year" — a tool that can say *no* is a compliance instrument, not a
brochure): ① **yield** (80×, moves the declared SEE 1:1 — legal basis IR 2025/2547 Annex III §F,
mass counted before cutting) → ② **mill EPD / precursor route** (€60/t measured; EAF rod is
fractions of BF in the EU's own tables) → ③ **process-energy benchmarking** (needs the pilot's peer
data — the tool says so) → ④ **load shifting** (real money, smallest carbon — ranked last by the
tool itself) → ⑤ the **cluster benchmark** as the multiplier across ~1,800 firms.

**The stainless finding** (our strongest systemic result): Taiwan's stainless block sits ~2.6× the
world median in the adopted tables; CN 7221 (the rod a stainless fastener maker actually buys) has
**no Taiwan value at all — the published Official Journal row literally reads
`see below … #VALUE! #VALUE! #VALUE!`** (a spreadsheet error enacted into law, verified 20 Jul); the
Annex I fallback applies (4.82 → 5.302 in 2026); and the flat default under-counts an honest
stainless maker ~2× — reporting honestly would cost his buyer ~€228/t, so nobody reports, and
Taiwan's real carbon problem stays legally invisible. **This is why a *sight* tool beats a *filing*
tool.** Full numbers: [`FACTS.md`](FACTS.md) §3.

**Inclusion proof (in the demo, not on a slide):** qwen3-VL **4B**, 336/336 fields across six
phone-photo degradations, 18–31 s/doc, laptop, offline, no GPU; LINE zh-TW; local-first.

## 3. How the thesis evolved (the credibility exhibit — never un-kill a dead claim)

| Stage | Thesis | What killed it / what survived |
|---|---|---|
| 1. Compliance saviour | "€450–750/t defaults will crush Gangshan" | Dead: our own engine parsed the adopted tables — Taiwan ≈ €224/t, data worth ~€4/t. Survived: the engine, the pack |
| 2. Provability divide | "CBAM taxes the inability to *prove*; policy fix" | Demoted: facts verified and reusable (atlas, 44×, accreditation gateway) but a legislation deck with no person in it. Survived: every measurement, as expansion evidence |
| 3. Waste thesis | "They throw away 10% of their steel; nobody counts it" | Corrected: scrap is *sold*; the owner knows the tonnage; money was gross not net. Survived at honest magnitude: the information gap, the 80× lever, the stainless finding |
| 4. **Four sights (LIVE)** | "The factory that cannot see itself — four blind spots, one data spine; sight → reduction" | Current frame, externally verified end-to-end, now fully built |

## 4. Current state (19 Jul 2026 — Sprint 2 complete)

- **Engine:** all four sights working end-to-end; **53/53 tests green**; both Commission worked
  examples (screws-and-nuts, cement) reproduced at rel 1e-9; firms A/B/C reconcile e2e vs ground
  truth at rel 1e-6; the filled 19-sheet workbook independently recomputes in LibreOffice.
- **Correctness debt: zero.** All docs-15-era defects closed in Sprint 2: mark-ups derived from the
  workbook row (fertilisers are flat 1%); grid EF from dated config (2025 industrial **0.466** —
  0.474 is history); certificate prices from dated config with a **hard refusal to quote an
  unpublished quarter** (test-pinned); firm_b/c ground truth derived from emitted rows; short-CN
  lookup guard; sector-label map from the template's own vocabulary; the kill-listed "20% ceiling"
  flag removed from code and tests.
- **Legal gates closed** (both regulations read in full, verdicts in [`FACTS.md`](FACTS.md) §2):
  **no estimation cap of any kind exists in IR 2025/2547**, and the CN 7221 hole is **confirmed in
  the OJ text itself** (`#VALUE!` rows).
- **New modules:** `waste/` (MoneyLoss gross+net type, trailing-window drift + 2σ alert),
  `benchmark/` (k≥5 self-enforcing public schema at `schema/benchmark_row.schema.json`,
  aggregate-only export that refuses violations), `costdelta/fixlist.py` (the ranked screen, negative
  answers pinned by test), LINE commands 「產生報告」「浪費」「排程」「我正常嗎」, `/waste` + `/fixlist`
  API routes.
- **Demo:** `scripts/line_simulator.py` plays all four sights in one session from one photo set
  (verified including the full VLM pass). **Video still to record.**
- **Submission artifact:** proposal Rev 5 (externally verified) in [`../proposal/`](../proposal/).
- **Pilot/partners: targets, not secured** (TIFI member firm; MIRDC / Kaohsiung EPB) — say so
  honestly everywhere.

Stack (settled — don't re-litigate): Python 3.12/uv · Ollama qwen3-vl 8B/4B · docling + PP-OCRv4
backstop · OR-Tools + NumPy MC · openpyxl · FastAPI + LINE. Environment facts: Ollama `num_ctx` ≥
8192; LibreOffice 26.2.4 for recompute checks; TC font (`Arial Unicode.ttf`) for corpus rendering —
reportlab's STSong drops Traditional-Chinese glyphs; 民國-year needs a prompt example.

## 5. Competition (Handbook facts + winners-study lessons)

Dates: submission **31 Jul 17:00** · preliminary 6–16 Aug (**Feasibility 40 / Innovation 30 / Social
Impact 30**) · mentorship mid-Sep–mid-Oct · finals late Oct (**+ Implementation & Verification 30%,
scored on *delta since submission*; demo or code description required**) · awards Dec. Team 3–10, ≥1
non-ROC national, 2 contacts, all English.

Winners-study lessons (2019–2025, 14 Teams of Excellence — full study in
`archive/materials/`): **theme-lock is absolute** — 2023–25 winners are all *AI + named beneficiary
population*, so Mr. Lin (61, Gangshan, thirty employees, his back office is a spreadsheet) stays the
protagonist and inclusion must be **in the demo** (LINE, offline 4B) · **feasibility beats
innovation** — bring the working thing · the **exportable diplomatic story** scores (New Southbound;
the 44× divide as the expansion register) · **winning ≠ surviving** — every winner with an afterlife
had an institution; MOENV/SMESA/TIFI/MIRDC integration is the sustainability plan.

Scheduled natural experiments inside the mentorship window: EP plenary vote on the ~180-category
downstream extension (Sept 2026; committee passed 6 Jul) · first CBAM verifier accreditations
(~Sept 2026; 8 NABs open, moving — see FACTS watch-list).

## 6. Roadmap

1. **Submission (by 31 Jul):** record the demo video (`carbonpass serve` +
   `scripts/line_simulator.py` — the session is scripted as the four sights) · application form
   filled field-by-field from Rev 5 · final watch-list pass ([`FACTS.md`](FACTS.md) §9) · team roster
   + ≥1 non-ROC national confirmed.
2. **Buffer / hardening (Aug):** pilot kit (`pilot/`: zh-TW intake checklist, consent one-pager,
   `carbonpass pilot run <folder>`, yield-measurement protocol, PII scrub script) · ingestion
   hardening (bbox-grounded backstop; real-bill layout variants; firms B/C through the full VLM
   path) · optional GPU re-run of InternVL official weights if the bake-off is challenged.
3. **Mentorship pilot (mid-Sep → mid-Oct) — the decisive test:** ONE real consented firm → all four
   sights on real documents; **measured yield replaces the synthetic 9.1% everywhere, whatever it
   is** (pre-register the three-way reconciliation protocol — invoiced steel in vs shipped tonnes vs
   scrap receipts — BEFORE the pilot so the number is credible; if real loss is 4%, we say so at
   finals: the control-loop value survives, the headline shrinks honestly) · pack reviewed by a
   Taiwanese GHG-verification body · one flexible load actually shifted with before/after ledger ·
   real scrap-sale receipts close the net-money loop · benchmark seeded with real rows (n small,
   labelled) · track the two September events and update the market slide.
4. **Finals (late Oct):** live demo + pilot deltas documented weekly — Implementation & Verification
   is the 30% that did not exist at preliminaries; it is won during mentorship, not on stage.

## 7. Archive map

Everything superseded lives in [`docs/archive/`](archive/), unchanged, under its original number —
code comments citing `docs/NN §…` resolve there. Read order if you ever need the history:
`20` (last master handoff) → `21` (Sprint-2 build order, executed) → `19` (claim audit) → `18`
(frame) → `15` (evidence dossier: legal quotes, workbook forensics, dead defects) → `16` (waste
thesis) → `14` (provability divide) → `13` (Sprint-1 report) → `12/11/10/09/00` (kickoff era) →
`0.` (PHIT handbook) → `materials/` (winners study, old proposal builds) → old submission PDFs.
**Nothing in the archive may source a claim — claims come from [`FACTS.md`](FACTS.md) only.**
