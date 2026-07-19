# Sprint 1 Report — Bake-off, Backstop, Module 2, Module 3, Caveat Closure

**Date:** 17 Jul 2026 · **Follows:** docs/12 (kickoff handoff) · **Read with:** docs/10 §2A (CBAM
rules), docs/09 Rev.2 (proposal). Everything below is reproducible from the repo; commands in README.

---

## 0. ✅ Sprint 1 COMPLETE — nothing in flight

All three formerly-pending items landed on 17 Jul: LibreOffice recompute verification
**PASS** (§6.1), 4B bake-off **336/336** (§2), InternVL3.5-8B challenger **66% → qwen3-vl
stays** (§2 verdict). 25/25 tests green; every artifact regenerable from committed scripts.
Environment facts a fresh session needs: Ollama serves `qwen3-vl:8b-instruct`,
`qwen3-vl:4b-instruct`, `blaifa/InternVL3_5:8b`; LibreOffice 26.2.4 in /Applications
(installed from `mirror.twds.com.tw` — official TDF host resets long downloads, brew cask
unusable on this link); degraded corpus regenerates via `scripts/degrade_corpus.py`;
bake-off matrix is resumable (`out/bakeoff/results.json`). **Next work = §8.**

---

## 1. What this sprint did

| Block | Deliverable | Status |
|---|---|---|
| A | Workbook-recompute caveat closure (LibreOffice headless) | ✅ **PASS** (§6.1) |
| B | VLM bake-off (degraded corpus) + PP-OCRv4 numeric backstop | ✅ **verdict: qwen3-vl stays** (8B 100%, 4B 100%, InternVL 66%) |
| C | Module 2: grid-aware MILP scheduler, live #8931 feed | ✅ |
| D | Module 3: FastAPI + LINE webhook + credential-free simulator | ✅ |
| E | This report + README/docs/12 updates | ✅ |

## 2. VLM bake-off (Sprint-1 decision rule, docs/10 §6.2)

**Setup:** `scripts/degrade_corpus.py` produces 6 phone-photo degradations (rot ±3–7°, blur
r1.5–2.5, dark 0.45×bright/0.7×contrast, jpeg q30, warp ~2%, combo=rot+dark+jpeg) of the firm_a
corpus → 114 images. `scripts/vlm_bakeoff.py` scores field-level accuracy (6 fields/bill:
peak/half/off/total kWh, total NT$, contract kW) vs ground truth; resumable matrix
{model × variant × ±docling-context}; results in `out/bakeoff/results.json` + `summary.md`.

**Result — qwen3-vl:8b-instruct (Ollama, Q4_K_M, Apple-silicon Metal):**

| variant | field accuracy | avg s/doc |
|---|---|---|
| clean | 54/54 (100%) | 25 |
| dark | 54/54 (100%) | 28 |
| jpeg (q30) | 54/54 (100%) | 38 |
| combo (rot+dark+jpeg) | 54/54 (100%) | 33 |
| rot / blur / warp | 24/24 (100%) each | 25–29 |

**288/288 fields correct across every degradation** (9 bills on the four key
variants, 4 on the rest) at ~25–48 s/doc. The model's robustness
claims (blur/tilt/low-light, docs/10 §6.2) hold on this corpus. Note the honest caveat: these
are synthetic renders degraded synthetically — real consented bills at the pilot remain the
decisive test (gaps G2/G3). *(Extended 8-bill run + challenger results appended below when
their downloads complete.)*

**Result — qwen3-vl:4b-instruct (the CPU/edge tier, G10):**

| variant (4 bills each) | noctx | +docling ctx | s/doc |
|---|---|---|---|
| clean / rot / blur / dark / jpeg / warp / combo | **24/24 (100%) each** | **24/24 (100%) each** | 18–31 |

**336/336 (100%)** — the 4B matches the 8B on every degradation, with or without the docling
pre-pass, and runs *faster* (18–31 vs 25–48 s/doc). Consequences: (a) the smallest-factory
CPU-only tier is validated on this corpus — the local-first story holds down-market;
(b) the docling context adds no accuracy on this corpus (it still powers the PP-OCRv4
backstop, which is its real job); (c) the corpus is now officially too easy to discriminate
models — the pilot's real bills are the decisive test.

**Result — InternVL3.5-8B (approved challenger; community Ollama build `blaifa/InternVL3_5:8b`):**

| variant (4 bills each) | field accuracy | s/doc |
|---|---|---|
| clean | 11/24 (46%) | 35 |
| jpeg | 11/24 (46%) | 44 |
| dark / warp | 15/24 (62%) each | 40–42 |
| blur | 18/24 (75%) | 39 |
| rot | 20/24 (83%) | 42 |
| combo | 21/24 (88%) | 42 |
| **total** | **111/168 (66%)** | 35–44 |

No API errors — the model simply misreads the numbers, and its misses concentrate on the
TOU table (kwh_half_peak ×17, kwh_off_peak ×19, kwh_total ×19 of 57 misses): exactly the
verifier-relevant fields. It is also slower than both qwen3-vl sizes. Caveat recorded: this
is a community quantization, not OpenGVLab-official weights — but a 34-point gap is beyond
what quantization noise plausibly explains on an OCR-bound task.

### Bake-off verdict (Sprint-1 decision rule, docs/10 §6.2 — executed)

**qwen3-vl stays, at both sizes.** 8B = 288/288, 4B = 336/336 (±context), InternVL3.5-8B =
66%. The 4B's parity-at-lower-latency validates the CPU/edge tier for the smallest factories
(G10). The docling pre-pass adds no accuracy on this corpus but remains in the pipeline as
the independent text source for the PP-OCRv4 numeric backstop (§3). Re-run the InternVL cell
with official weights on a GPU box before finals if anyone challenges the comparison; the
matrix is one command per row and resumable.

## 3. Numeric backstop (PP-OCRv4)

`src/carbonpass/ingestion/backstop.py`: every numeric field the VLM returns is checked for
literal presence in an independent OCR pass of the same image (PaddleOCR **PP-OCRv4**
recognition models, served via docling's RapidOCR/ONNX — same model family as the blueprint's
PaddleOCR-VL, which needs a GPU box and stays on the roadmap). Mismatch ⇒ document flagged
`needs-attention` + field confidence capped at 0.25 (which widens the quantity's uncertainty
downstream). Wired into the ingestion pipeline whenever docling context is available.

**Catch-rate proof** (`tests/test_backstop.py`): 3 injected error classes — last-digit misread
(…149→…146), transposition (18019→18091), leading-digit hallucination (393838→493838) — **all
3 caught**, correct fields untouched, confidence downgrade verified. 5 tests green.

Limitation (honest): the check is presence-based — an OCR text that happens to contain the
wrong number elsewhere can mask an error; field-anchored matching (bbox grounding) is the
upgrade path and pairs with qwen3-VL's grounding output at the pilot.

## 4. Module 2 — grid-aware scheduler (MILP, live feed)

`src/carbonpass/scheduler/`: `grid.py` reads Taipower's **live 10-min generation-by-unit feed**
(#8931; endpoint `service.taipower.com.tw/data/opendata/apply/file/d006001/001.json`, dict rows,
UTF-8-BOM) → per-fuel MW → intensity via documented per-fuel EFs; offline-safe cached snapshot;
single-snapshot anchor × diurnal shape (pilot upgrade: integrate logged feed / #37331 backfill).
`tariffs.py` (shared TOU table — corpus imports it now), `loads.py` (furnace/compressor =
flexible Mon–Sat 24h; formers fixed), `milp.py` (GLOP LP: weekly energy conservation, kW rating,
contract-capacity cap, NT$+CO₂ objective), `ledger.py` (ISO 14064-2-**logic** ledger).

**Measured (firm_a, live anchor 0.5157 kgCO₂e/kWh — night mix, sanity ×1.09 of the 0.474
annual mean):**

- Week: NT$113,524 → NT$105,528 (**save NT$7,996/wk**)
- Year estimate: **save NT$399,800 + 4.49 tCO₂e**

**G7 framing enforced in the output itself:** the ledger JSON and every LINE/CLI message state
that the CO₂ saving lands on the indirect-emissions line / buyer Scope-3 — **not** the CN 7318
CBAM certificate (only cement & fertiliser include indirect today). Module 2's bankable value =
the power bill, Scope-3 questionnaires, DPP/domestic-fee readiness. 5 scheduler tests green
(feasibility, conservation, capacity cap, never-worse-than-baseline, TOU banding).

Modeling notes: baseline = price-blind flat operation Mon–Sat 24h (multi-shift reality — a
06:00–22:00 window is infeasible for a 5,800 h/yr furnace, found the hard way); real order
deadlines arrive via LINE at the pilot; RL (PPO) refinement stays roadmap.

## 5. Module 3 — FastAPI + LINE webhook + simulator

`carbonpass serve` → FastAPI at :8787: `/health`, `/ingest`, `/pack`, `/costdelta`, `/schedule`,
`/line/webhook`. The webhook verifies X-Line-Signature (HMAC-SHA256) when
`LINE_CHANNEL_SECRET` is set; without it it runs in **simulator mode** and returns replies in
the HTTP response. zh-TW conversation, zero ESG vocabulary: photos → stored per-user session;
「狀態」/「產生報告」/「排程」 commands. e-invoices enter via the e-GUI consent path (G11) —
photos are only needed for the Taipower bill, exactly as the blueprint argues.

**Demonstrated end-to-end without a LINE channel** (`scripts/line_simulator.py`): two bill
photos in → acknowledgement, status, and the schedule reply “每週可省 NT$7,996 … 減碳 4.49
tCO2e/年（屬用電間接排放；不影響 CBAM 憑證金額）”. Wiring a real channel = set the two
`.env` values and point the LINE console at `/line/webhook`. 6 API tests green.

## 6. Caveat closure

1. **“SEE cells recompute in Excel/LibreOffice” — ✅ VERIFIED (PASS, 17 Jul).**
   `scripts/verify_workbook_recalc.py` round-trips the filled workbook through headless
   LibreOffice 26.2.4 (xlsx→xlsx forces a full recalculation, because openpyxl saves formulas
   *without* cached values) and diffs the workbook-computed SEE against the engine sidecar:

   | Summary_Products row 10 (CN 73181542) | workbook (LO recalc) | engine | verdict |
   |---|---|---|---|
   | SEE direct | 2.92436398666 | 2.924363986610001 | OK |
   | SEE indirect | 0.094799842 | 0.094799842 | OK |
   | SEE total | 3.01916382866 | 3.019163828610001 | OK |
   | embedded electricity | 0.199999666666667 | 0.1999996666666667 | OK |

   The Commission's own formula chain — including the hidden `InputOutput` array-formula
   matrix — independently reproduces the engine's numbers at rel 1e-6 (agreement is actually
   ~1e-11; the last digits differ only by LO's binary float serialization). Method notes:
   CSV export was unusable for this check (it rounds to displayed precision); the xlsx
   round-trip preserves full precision.
2. **Conditional-formatting extensions dropped by openpyxl** — unchanged, cosmetic; the
   dropped bits are Excel “extLst” conditional-formatting extras, not formulas or values.

## 7. Findings & watch-items (this sprint)

- **F1 — the corpus discriminates models, not qwen sizes:** both qwen3-vl sizes hit 100%
  through every degradation (and the 4B is faster), yet the same corpus dropped
  InternVL3.5-8B to 66% with misses clustered on the TOU table — so the benchmark is
  meaningful, the qwen family is simply strong on zh-Hant documents, and size can be chosen
  by hardware tier rather than accuracy. Real pilot bills remain the final check.
- **F2 — #8931 feed quirks:** rows are dicts keyed 機組類型/淨發電量(MW) with a UTF-8 BOM;
  night-time intensity ~0.52 kg/kWh vs 0.474 annual mean — the diurnal spread is real and
  worth money to shift against.
- **F3 — furnace window:** heat treatment at ~5,800 h/yr *cannot* fit a daytime-only window —
  any scheduler that assumes “shift within working hours” is infeasible for the sector's
  biggest flexible load. Mon–Sat 24h is the honest baseline.
- **F4 — `curl | tail` masks brew failures** (pipe exit = tail's): the LibreOffice “success”
  marker printed after a failed download. Check artifacts, not echoes.
- **W1 — backstop is presence-based** (see §3) — bbox-anchored matching is the upgrade.
- **W2 — TOU table is stylized** from the published schedule; re-verify the current rates
  before submission (also flagged in docs/10 §5.2).

## 8. Remaining blockers / next steps

> ⚠️ **POINTER (17 Jul 2026):** this list is superseded by **`docs/14_scope_extension.md`** §6, which
> re-aims the project on the *provability divide* thesis. Item 8 below is now **closed in part** —
> `docs/15` §2.8 confirms the phase-in factors are in **neither** official workbook. Item 8's other
> half (IR 2025/2547) is now **critical**: see `docs/15` §8.1.

1. ✅ ~~Challenger + 4B rows~~ (done — §2; invoice-task bake-off still open as a nice-to-have).
2. ✅ ~~Recompute verdict~~ (PASS — §6.1).
3. Pilot (mentorship window): real consented bills; verifier/MIRDC review of a generated pack;
   one real load shifted & measured (before/after ledger is ready for it).
4. PaddleOCR-VL full backstop + InternVL official weights on a GPU box; bbox-grounded
   numeric matching.
5. LINE production channel + onboarding Q&A flow (replaces the seeded firm.json).
6. Module 2: integrate logged 10-min feed into a true historical curve; real AMI CSV import.
7. Demo video for 31 Jul submission (simulator makes it recordable today).
8. Verify IR 2025/2621 legal text vs the parsed xlsx + the 2025/2620 phase-in factor
   (15 min; flagged in docs/09 Rev.2 and docs/12 §4b).
