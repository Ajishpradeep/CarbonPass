# Sprint 1 Report — Bake-off, Backstop, Module 2, Module 3, Caveat Closure

**Date:** 17 Jul 2026 · **Follows:** docs/12 (kickoff handoff) · **Read with:** docs/10 §2A (CBAM
rules), docs/09 Rev.2 (proposal). Everything below is reproducible from the repo; commands in README.

---

## 1. What this sprint did

| Block | Deliverable | Status |
|---|---|---|
| A | Workbook-recompute caveat closure (LibreOffice headless) | ⬜ *(fills in below)* |
| B | VLM bake-off (degraded corpus) + PP-OCRv4 numeric backstop | ✅ 8B done · challenger ⬜ |
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
| clean | 24/24 (100%) | 25 |
| rot / blur / dark / warp | 24/24 (100%) each | 25–29 |
| jpeg (q30) | 24/24 (100%) | 48 |
| combo (rot+dark+jpeg) | 24/24 (100%) | 34 |

**168/168 fields correct across every degradation** at ~25–48 s/doc. The model's robustness
claims (blur/tilt/low-light, docs/10 §6.2) hold on this corpus. Note the honest caveat: these
are synthetic renders degraded synthetically — real consented bills at the pilot remain the
decisive test (gaps G2/G3). *(Extended 8-bill run + challenger results appended below when
their downloads complete.)*

- **InternVL3.5-8B (approved challenger):** servable via the community Ollama build
  `blaifa/InternVL3_5:8b` — ⬜ result pending pull.
- **qwen3-vl:4b-instruct (CPU/edge path):** ⬜ result pending pull.
- **±docling context:** deferred for 8B (100% without context ⇒ context can only help weaker
  models; will be measured on the 4B).

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

1. **“SEE cells recompute in Excel/LibreOffice” — ⬜ verification pending LibreOffice install**
   (first download attempt died on a connection reset; retry running).
   `scripts/verify_workbook_recalc.py` exports Summary_Products headlessly and diffs the
   workbook-computed SEE against the engine's sidecar at rel 1e-6. The test is decisive by
   construction: openpyxl saves formulas *without* cached values, so the exporter is forced to
   evaluate the Commission's formula chain (incl. the hidden InputOutput array-formula matrix).
   *(Result appended below when the install lands.)*
2. **Conditional-formatting extensions dropped by openpyxl** — unchanged, cosmetic; the
   dropped bits are Excel “extLst” conditional-formatting extras, not formulas or values.

## 7. Findings & watch-items (this sprint)

- **F1 — 8B robustness:** 100% field accuracy through every synthetic degradation; the
  bake-off's discriminating power now depends on real pilot bills, not harsher synthetic noise.
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

1. ⬜ Append challenger (InternVL3.5-8B) + 4B rows to §2 when pulls land; extend to invoices.
2. ⬜ §6.1 recompute verdict when LibreOffice lands.
3. Pilot (mentorship window): real consented bills; verifier/MIRDC review of a generated pack;
   one real load shifted & measured (before/after ledger is ready for it).
4. PaddleOCR-VL full backstop + InternVL on a GPU box; bbox-grounded numeric matching.
5. LINE production channel + onboarding Q&A flow (replaces the seeded firm.json).
6. Module 2: integrate logged 10-min feed into a true historical curve; real AMI CSV import.
7. Demo video for 31 Jul submission (simulator makes it recordable today).
