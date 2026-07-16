# CarbonPass — PoC Engineering Blueprint

## Module 1: The CBAM Verifier-Ready Data-Pack Engine (+ Module 2 hooks)

**Status:** material-collection & build plan — *not* idea exploration. Everything below is a concrete resource with a working URL, a named tool with a license, or an explicit gap with a mitigation.
**Scope of this document:** what the data pack actually is, the exact EU material to reproduce it, the Taiwan data to feed it, the open-source AI/tool stack to build it, the reference architecture, a sprint plan to a working PoC by 31 Jul 2026, and an honest gap list.
**Date compiled:** 16 Jul 2026. **Beachhead:** fasteners, CN 7318, Gangshan–Luzhu cluster.

---

## 0. TL;DR — the shape of the build

We are building a pipeline that takes **photographed SME documents** (Taipower bill, steel wire-rod invoices, production log) and emits a **filled EU CBAM Communication Template for installations** (`.xlsx`, the Commission's own file) for each CN-7318 product, with every field flagged `actual / default / needs-verifier-attention` and an uncertainty per line.

```
[LINE photo intake] → [VLM doc-intelligence → structured activity data]
      → [Allocation engine: facility kWh/fuel → per-CN-code]
      → [CBAM rules/SEE engine + emission-factor DB + default-value fallback]
      → [Writer → EU Communication Template .xlsx] + [buyer cost-delta screen]
```

The single most valuable asset we found: **the Commission publishes a *filled* "screws and nuts" example of the template** — i.e., a worked CN 7318 answer key. Our Module-1 output must be byte-for-byte structurally identical to it. (Download in §3.)

**The good news for feasibility:** the entire computation is defined in free EU regulations + a free Excel template, and every Taiwan input has an open dataset or a known format. **The real gaps are data-access (real bills need pilot consent) and the machine-level allocation problem — both already anticipated in our proposal.** See §11.

---

## 1. What the deliverable actually *is*

There are two distinct CBAM artifacts. We must build the first, not the second:

| Artifact | Who makes it | Who receives it | Format | Is this our output? |
|---|---|---|---|---|
| **Communication Template for installations** | The **non-EU producer** (our SME) | The **EU importer / declarant** | Commission `.xlsx` | **YES — this is Module 1's output** |
| **CBAM Declaration** | The EU **authorised declarant** | EU CBAM Registry | Registry portal / system-to-system | No (downstream of us) |

So the SME's job — and ours — ends at producing the **Communication Template**, verifier-ready. The importer then transcribes/uploads it into the CBAM Registry to file their annual declaration (first one due **30 Sep 2027** for 2026 imports). This scoping is exactly right for an SME tool: we produce the artifact the buyer's declarant needs, and we do not touch the EU Registry ourselves.

**What the template captures** (to be locked field-by-field against the real file in Sprint 0): installation identity & location; production processes; **aggregated goods categories per CN code**; fuel & material inputs; electricity consumed; **precursors (purchased + their specific embedded emissions)**; emissions allocation between CBAM and non-CBAM goods and between products; and the computed **direct and indirect Specific Embedded Emissions (SEE)** per good, in **tCO₂e per tonne of product**.

---

## 2. The computation we must reproduce (the SEE math)

**Specific Embedded Emissions (SEE)** = emissions per tonne of a CBAM good. For a **complex good** like a fastener (steel is a *precursor*), embedded emissions = the fastener plant's own process emissions **plus** the embedded emissions of the steel it consumed:

```
SEE_good = (DirectEmissions_process + Σ(mass_precursor_i × SEE_precursor_i)) / activity_level
```

- **Direct emissions** — fuel combustion in the plant's own processes (e.g. natural gas in heat-treatment furnaces). Attributed to the CBAM good via allocation.
- **Precursor emissions** — the embedded emissions of the purchased steel wire rod (from China Steel mill data if available, else CBAM **default precursor value**).
- **Indirect emissions** — from purchased electricity (grid EF × kWh). **Important nuance (verify in IR 2025/2547):** per the definitive-phase rules, **indirect emissions are currently required in the certificate obligation only for cement and fertiliser**, not for iron & steel. They are still *recorded* in the template. → **Consequence for Module 2:** load-shifting reduces *indirect* emissions, which for CN 7318 do **not** currently lower the CBAM certificate cost. Module 2's value is therefore (a) NT$ energy-cost savings via TOU, (b) customer Scope-3 questionnaires, (c) future/DPP readiness, (d) domestic carbon-fee readiness — **not** a direct CBAM-certificate reduction today. Frame it honestly this way. (See gap G7.)
- **Default-value mark-up** for iron & steel: **+10% (2026) → +20% (2027) → +30% (2028)**. Applied when actual data is unavailable. For complex goods, ≥80% of reported emissions must be actual, third-party-verified.

The governing texts (all free, §3): methodology = **IR (EU) 2025/2547**; default values = **IR (EU) 2025/2621** (Annex I direct SEE by country×CN; Annex II indirect EFs; Annex III electricity); verification principles = **IR (EU) 2025/2546**.

---

## 2A. How CBAM actually works in practice — period, cadence, allocation (read this before designing UX)

Several execution assumptions people bring to this project are wrong. The rules below are load-bearing for the product design; get them right or the tool solves the wrong problem.

### It is per-product-per-year, NOT per-shipment
CBAM does **not** attach a carbon number to each shipment or each sales invoice. It wants the **Specific Embedded Emissions (SEE)** — tCO₂e per tonne — of each *product type* (CN code), determined once over a **determination period = the calendar year** (a producer may rebut with evidence of the actual production period, but no period precedes 2026). The EU importer then multiplies **your SEE × the tonnes in each shipment** at declaration time. **One SEE per CN good is reused across every shipment of that good for the year.** Design consequence: the owner's recurring job is a once-a-year data submission per product, not an action per order. Never build or imply per-shipment carbon paperwork.

### Timing: after the fact, filed annually by the importer
The legal duty sits on the **EU importer**, who files **one annual CBAM declaration by 30 September of the following year** (first: 30 Sep 2027 for 2026 imports). Nothing carbon-related gates the shipment itself, and there is no producer-side quarterly report any more (the quarterly *transitional* importer report ended 31 Dec 2025). Our factory hands the importer a **Communication Template** once per period; the importer stores it and uses it at declaration time. So **frequency ≈ once per year**, refreshed only if production materially changes.

### e-GUI is live and universal — use it as the input ledger
Taiwan's electronic invoice (電子發票 / eGUI) has been **mandatory for all business-tax-registered entities since 1 Jan 2021** (B2B + B2C, now **MIG 4.0 XML**, digitally signed, on the MOF platform). A Gangshan fastener SME is therefore already issuing/receiving **structured e-invoice XML** for its steel, gas and chemical purchases. **Opportunity:** the highest-value inputs (steel & fuel purchases) may be pulled as clean XML (with owner consent) rather than OCR'd — reducing our dependence on photo parsing for the numbers that actually move SEE. The Taipower electricity bill remains the main artifact needing photo/PDF parsing. e-GUI is the **input ledger** (what was bought/consumed over the period); it is **not** an allocation-per-shipment mechanism.

### What actually drives the fastener number (input priority)
For a **complex good** like a fastener, most of the ~2 tCO₂e/t is the **purchased steel precursor**, not the factory's own energy. Input importance, high → low: **(1) steel wire-rod quantity + its SEE**, (2) direct fuel (heat-treatment gas), (3) production volumes per CN code, (4) electricity kWh. The electricity bill is the *least* important input to the CBAM number for fasteners (indirect emissions currently aren't in the CN 7318 certificate — see G7); it still matters for the org inventory, indirect reporting, and Module 2 scheduling.

### Allocation = two steps, over the period, never per shipment
Per IR 2025/2547: (1) attribute installation-level period emissions to production processes and split CBAM vs non-CBAM goods; (2) attribute each process's emissions to each CN-code product by production mass, machine power ratings and operating hours. Our engine does step 2 (OR-Tools + priors) with **quantified uncertainty per line** — computed **once per year**, tightened later with 15-min AMI / sub-metering at the pilot. The uncertainty is a feature verifiers want.

### The "hassle-free for a non-technical owner" claim — where it holds and where it doesn't
Holds **because** it's annual and per-product: the recurring run is "once a year, authorize/photograph a document set and confirm a few numbers," tool does allocation + template. Two honest limits: **(a) first-time setup** (defining the installation system boundary and process map) is the real effort — absorb it once in onboarding; **(b) the accredited verifier is not removable** — to use *actual* data and beat punitive defaults, a third-party verifier must check it, with an **on-site audit in year 1** and a **5% variance threshold**. Our tool makes the pack *verifier-ready*; it never replaces the verifier or emits "certified."

---

## 3. Official CBAM material — download inventory (exact URLs)

> These are binary/legal files; download them into `/data/cbam_official/` as the first build step. (All on `taxation-customs.ec.europa.eu` / EUR-Lex — public.)

| # | Item | Why we need it | URL |
|---|---|---|---|
| C1 | **CBAM Communication Template for installations** (`.xlsx`, 1.27 MB, 18 Dec 2024) | **The exact output schema** | `https://taxation-customs.ec.europa.eu/document/download/2c15cd0e-2447-4ef8-ab70-68b80b66ede8_en?filename=CBAM%20Communication%20template%20for%20installations_en_20241213.xlsx` |
| C2 | **Communication template — filled EXAMPLES** (`.zip`, 7.77 MB) incl. **steel screws and nuts** | **Answer key for CN 7318** | `https://taxation-customs.ec.europa.eu/document/download/8d00a979-e57d-4e53-a11f-8b01370236a9_en?filename=Communication-template-examples.zip` |
| C3 | **IR (EU) 2025/2547** — methods for calculating embedded emissions | The SEE algorithm | `https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202502547` |
| C4 | **IR (EU) 2025/2621** — default values (HTML legal) | Default SEE + mark-ups | `https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202502621` |
| C5 | **Default values — Excel** (`.xlsx`, 858 KB, "DVs as adopted v20260204") | Machine-readable defaults by country×CN | `https://taxation-customs.ec.europa.eu/document/download/1c05d211-80cb-4aaa-8ef0-e08005a95d7e_en?filename=DVs%20as%20adopted_v20260204%20.xlsx` |
| C6 | **Benchmarks — Excel** (IR 2025/2620) | Free-allocation adjustment | `https://taxation-customs.ec.europa.eu/document/download/9877523c-2a02-4926-a211-aefae7cf6d0d_en?filename=CBAM%20Benchmarks_20260206.xlsx` |
| C7 | **IR (EU) 2025/2546** — verification principles | What a verifier will check | `https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202502546` |
| C8 | **Guidance for installation operators outside the EU** (PDF, 4.24 MB) — **also in Chinese** | Operator how-to; onboarding copy | EN: `https://taxation-customs.ec.europa.eu/document/download/2980287c-dca2-4a4b-aff3-db6374806cf7_en` · ZH: `https://taxation-customs.ec.europa.eu/document/download/1dd68ee3-0364-47a5-9a2e-010b2568541c_en?filename=TAXUD-2023-01191-00-00-ZH-TRA-00.pdf` |
| C9 | **Guidance for importers** (PDF, 1.65 MB) | Buyer-side context | `https://taxation-customs.ec.europa.eu/document/download/bc15e68d-566d-4419-88ec-b8f5c6823eb2_en?filename=TAXUD-2023-01189-01-00-EN-ORI-00.pdf` |
| C10 | **CBAM Q&A** (PDF, 28 May 2026) | Edge-case rules | `https://taxation-customs.ec.europa.eu/document/download/013fa763-5dce-4726-a204-69fec04d5ce2_en?filename=CBAM_Questions%20and%20Answers.pdf` |
| C11 | **CBAM Registry / reporting reg** IR 2024/3210 (amended 2025/2550) | XSD/registry structure (downstream ref) | `https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=OJ:L_202403210` |
| C12 | **Downstream scope extension proposal** (CELEX 52025PC0989, ~180 categories, Sep-2026 EP vote) | Roadmap / market slide | `https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A52025PC0989` |
| C13 | **CBAM certificate price page** (€75.36 Q1 / €75.28 Q2 2026) | Cost-delta screen | `https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism/price-cbam-certificates_en` |

**Sprint-0 task:** unzip C2, open the *screws and nuts* workbook, and transcribe its exact sheet list + cell map into `schema/cbam_template_map.yaml`. That file becomes the contract our writer fills. (We cannot auto-download binaries in this research session; the engineer does this first.)

---

## 4. The data pack, field by field — what each field needs and where it comes from

| Template input | Physical meaning | Source in the SME | How we get it | Fallback |
|---|---|---|---|---|
| Installation identity | Name, address, coords | Owner-provided once | LINE onboarding form | — |
| Production volume per CN good | tonnes of each screw type | Production log / ERP | VLM parse of log; owner confirms | — |
| Electricity consumed (kWh) | Scope-2 activity | **Taipower bill** | VLM parse of bill | AMI CSV (15-min) at pilot |
| Fuel inputs (NG, diesel) | Direct-emission activity | **Fuel invoices** | VLM parse (MOF e-invoice) | Owner Q&A |
| Steel wire-rod mass | Precursor activity | **Material invoices** | VLM parse (MOF e-invoice) | Owner Q&A |
| Emission factors (fuel/material/process) | kgCO₂e per unit | — | **MOENV coeff. DB #28176** (§5) | CBAM defaults |
| Grid EF (Scope-2) | kgCO₂e/kWh | — | **0.474 (2024)** / hourly from #8931 | national annual |
| Precursor SEE (steel) | tCO₂e/t steel | China Steel mill cert | Uploaded EPD if available | **CBAM default precursor value (C5)** |
| Allocation shares | split facility → product | machine ratings, run-hours | **Allocation engine (§6)** | conservative even-split + high uncertainty |
| Certificate price | €/tCO₂e | — | EC price page (C13) | last published quarter |

---

## 5. Taiwan input data & formats — collected resources

### 5.1 Emission factors (MOENV / 環境部)
- **Carbon-footprint emission coefficients (碳足跡排放係數)** — the core EF database.
  - data.gov.tw dataset **#28176**: `https://data.gov.tw/dataset/28176`
  - MOENV env-data platform record **CFP_P_02**: `https://data.moenv.gov.tw/dataset/detail/CFP_P_02`
  - **OpenAPI / Swagger:** `https://data.moenv.gov.tw/swagger/` (programmatic pull, JSON)
  - Free coefficient lookup site: `https://cfp-calculate.tw` ; product CFP portal `https://cfp.moenv.gov.tw`
- **Taiwan product carbon-footprint info (台灣產品碳足跡資訊)** — benchmarks/sanity checks.
  - data.gov.tw **#8992**: `https://data.gov.tw/dataset/8992` · MOENV **CFP_P_01**: `https://data.moenv.gov.tw/dataset/detail/CFP_P_01`
- **GHG annual emissions (溫室氣體年排放量)** — large-emitter registry (CSC precursor benchmark).
  - data.gov.tw **#16059**: `https://data.gov.tw/dataset/16059`
- **Grid electricity emission factor:** 0.474 kgCO₂e/kWh (2024), MOEA Energy Admin — `https://www.moeaea.gov.tw/ECW/English/content/Content.aspx?menu_id=24200`

### 5.2 Grid telemetry & tariffs (Taipower / 台電) — Module 2
- **Generation by unit, 10-minute (各機組發電量)** → compute hourly grid carbon intensity.
  - real-time **#8931**: `https://data.gov.tw/dataset/8931` · historical **#37331**: `https://data.gov.tw/dataset/37331`
- **Time-of-Use rate tables (各類電價表及計算範例)** — two-part tariff: 契約容量 (contract-capacity basic charge) + time-banded energy charge; summer peak (high-voltage) 16 May–15 Oct; commercial peak reported up to ~NT$9.39/kWh (Oct 2025 schedule); industrial rates held flat in the 2025 review.
  - rate-table hub: `https://www.taipower.com.tw/2289/2290/46940/`
  - full rate PDF: `https://www.taipower.com.tw/media/ba2angqi/各類電價表及計算範例.pdf?mediaDL=true` *(re-verify current table before submission)*
- **AMI 15-minute interval data:** customer-exported CSV via Taipower eBill/app (consent-based; no third-party API). PoC uses a synthetic profile shaped to the TOU calendar until a pilot supplies real data.

### 5.3 Document formats — the ingestion targets
- **MOF electronic invoice / eGUI (電子發票)** — material & fuel invoices arrive here.
  - Standard: **MIG 4.0 XML** (Message Implementation Guidelines), digitally signed; B2B (file within 7 days) and B2C (2 days); transmit via MOF **Turnkey** or a certified VAC.
  - **Open-source reference implementation** (Turnkey + MIG file format): `https://github.com/phidiassj/TaiwanEInvoiceOpenAPI` — use to **generate valid mock e-invoices** for the corpus and to learn the schema.
  - MOF e-invoice platform: `https://www.einvoice.nat.gov.tw`
- **Taipower bill** — no open machine-readable format; it's a printed/PDF bill. → we parse it with the VLM from a photo. Build the parser against public bill layouts + the eBill sample; collect a few real (consented) layouts at pilot. (Gap G3.)

---

## 6. The AI / tool stack (open-source, with licenses)

### 6.1 Selected components

| Layer | Choice (primary) | Alt / notes | License | Why |
|---|---|---|---|---|
| **Doc-intelligence VLM** | **Qwen3-VL-8B-Instruct** | 4B-Instruct for edge/CPU; 32B-Instruct for accuracy ceiling (vLLM) | Apache-2.0 | Top open-weight OCR (OCRBench ~896 vs ~820 field); OCR in 32 languages incl. **Traditional-Chinese**; robust on tilted/low-light phone photos; grounding/bbox + reliable structured JSON; ~12 GB @ 4-bit |
| VLM challenger | **InternVL3.5-8B** | head-to-head in Sprint 1 | open (Apache/MIT base) | Strongest reasoning/versatility rival; decide zh-Hant empirically on our corpus |
| Layout/OCR backstop | **PaddleOCR-VL** (OmniDocBench v1.6 leader ~96.3%); **DeepSeek-OCR** (MIT) for bulk throughput | cross-check dense numeric tables / line items | Apache-2.0 / MIT | Validate the figures a verifier scrutinizes — defense-in-depth on numbers |
| **Doc pre-processing** | **Docling** (IBM) | PDF/scan → structured layout | MIT | Robust layout, tables, reading order before/with the VLM |
| **Local serving (PoC)** | **Ollama** (`qwen3-vl:8b-instruct`; `qwen3-vl:4b-instruct` edge) | one-command local, LINE-friendly | MIT | Fast to stand up, on-prem = local-first story |
| **Serving (scale/structured)** | **vLLM** with `guided_json` | production throughput + schema-locked output | Apache-2.0 | Enforces our JSON schema at decode time |
| **Structured-output contract** | JSON Schema / Pydantic | shared by VLM + rules engine | — | Every extraction validated |
| **Allocation engine** | **Google OR-Tools** (MILP) + **Monte-Carlo** (NumPy) | facility→product split w/ per-line uncertainty | Apache-2.0 | The genuine ML/OR problem; produces the uncertainty a verifier wants |
| **CBAM rules/SEE engine** | Python module encoding IR 2025/2547 + defaults (C5) | pytest golden-tests vs C2 example | (our code) | Deterministic, auditable |
| **Template writer** | **openpyxl** → fill C1 workbook | preserves EU formulas/format | MIT/BSD | Output = the Commission's own file |
| **Scheduler (Module 2)** | OR-Tools MILP baseline + **Gymnasium/PPO** RL refinement | grid-intensity + TOU | Apache-2.0 / MIT | Shift plan + before/after ledger |
| **Conversational front end** | **LINE Messaging API** + webhook | Mandarin/Taiwanese, voice, photo | SDK (free tier) | The inclusion interface |
| **Orchestration/API** | Python 3.11, **FastAPI**, SQLite/DuckDB | glue + local store | MIT | Simple, local-first |

### 6.2 Model rationale (evidence)
**Why Qwen3-VL-8B (not the 2.5 generation or a pure-OCR model).** The choice is driven by our exact job — Traditional-Chinese documents photographed by non-technical owners, from which we must extract *numbers* reliably, map them to a schema, and (for verifier traceability) know *where on the page* each value came from — under an on-prem, permissive-license constraint. Qwen3-VL (released Oct 2025, Apache-2.0) is the current open-weight OCR leader (OCRBench ~896, ahead of the ~820 field and its own 2.5 predecessor), does OCR in 32 languages including CJK, is explicitly robust to blur/tilt/low-light (real phone photos), provides 2D grounding for field-level provenance, and emits stable structured JSON — with first-class Ollama/vLLM support (`guided_json` for schema-locked decoding). A **specialist alternative** (PaddleOCR-VL leads OmniDocBench at ~96.3%; DeepSeek-OCR is MIT and extremely high-throughput) is *stronger at raw layout/table OCR* but weaker at the reasoning step of turning a messy bill into our activity-data schema — so we use it as a **numeric cross-check**, not the primary. Published Traditional-Chinese benchmarks are thin across all models, so the **Sprint-1 bake-off is the real decision rule**: Qwen3-VL-8B vs **InternVL3.5-8B**, ± Docling pre-pass, ± PaddleOCR-VL numeric backstop, scored on field-level accuracy on real Taipower bills + MOF e-invoices. The 4B-Instruct covers CPU/edge factories; 32B-Instruct (vLLM) is the accuracy ceiling.

### 6.3 Hardware
- PoC dev: single 12–24 GB GPU (7B @ 4–8 bit) or Apple-silicon via Ollama.
- On-prem "local-first" pilot target: a mini-PC/workstation with one consumer GPU, or CPU-only 3B for the smallest factories.

---

## 7. Reference architecture

```
                         ┌────────────────────────────┐
   Owner (LINE, 台語/中文)│  Module 3: Inclusion UI     │
   photo of bill/invoice │  LINE Messaging API + voice │
                         └──────────────┬─────────────┘
                                        │ images + answers
              ┌─────────────────────────▼──────────────────────────┐
              │ Ingestion: Docling layout → Qwen3-VL (Ollama/vLLM)  │
              │ → JSON (activity data + confidence), schema-validated│
              └─────────────────────────┬──────────────────────────┘
                                        │ activity data
        ┌───────────────────────────────▼───────────────────────────────┐
        │ Allocation engine (OR-Tools MILP + Monte-Carlo)                │
        │ facility kWh/fuel → per-CN-code, uncertainty per line          │
        └───────────────────────────────┬───────────────────────────────┘
                                        │ allocated activity
   ┌────────────────────────────────────▼────────────────────────────────────┐
   │ CBAM rules/SEE engine (IR 2025/2547)                                      │
   │  • MOENV EF DB #28176 (Scope-1/materials)   • grid EF / hourly (#8931)     │
   │  • precursor SEE: mill EPD else default (C5) • mark-up 10/20/30%           │
   └───────────────┬───────────────────────────────────────┬──────────────────┘
                   │                                        │
   ┌───────────────▼───────────────┐        ┌───────────────▼───────────────┐
   │ Writer → EU Communication      │        │ Cost-delta screen              │
   │ Template .xlsx (C1 structure), │        │ actual €150/t vs default €450– │
   │ fields flagged actual/default  │        │ 750/t (C13 price)              │
   └────────────────────────────────┘        └────────────────────────────────┘

   Module 2 (parallel): #8931 → hourly grid intensity + TOU tables
        → OR-Tools/PPO shift plan → NT$ + tCO₂e ledger (ISO 14064-2 logic)

   Privacy: all parsing/compute on-prem; only the chosen .xlsx leaves.
```

---

## 8. Build plan — sprints to a working PoC (submission 31 Jul 2026)

- **Sprint 0 (days 1–3) — lock the target.** Download C1–C5, C8. Unzip C2, transcribe the *screws & nuts* workbook into `schema/cbam_template_map.yaml` + golden expected outputs. Pull MOENV EF DB via Swagger into `/data/ef/`. Stand up repo, FastAPI skeleton, Ollama + `qwen3-vl:8b-instruct`.
- **Sprint 1 (week 1–2) — ingestion.** Build the 3-firm mock corpus (§9). VLM bake-off (Qwen3-VL-8B vs InternVL3.5-8B, ±Docling, ±PaddleOCR-VL). Ship bill-parser + e-invoice-parser → validated JSON with confidences.
- **Sprint 2 (week 2–3) — allocation + rules.** OR-Tools MILP allocation with Monte-Carlo uncertainty; CBAM SEE engine encoding IR 2025/2547 + default fallback (C5) + mark-ups; pytest golden-tests reproduce the C2 *screws & nuts* numbers within tolerance.
- **Sprint 3 (week 3–4) — output + UX.** openpyxl writer fills C1; field flags actual/default/needs-attention; cost-delta screen (C13); LINE bot end-to-end (photo → pack).
- **Sprint 4 (week 4–5) — Module 2 + polish.** Hourly grid intensity from #8931; OR-Tools shift plan on synthetic load vs live feed; before/after ledger. Record demo video. Publish the two give-back datasets (cleaned hourly grid intensity; anonymised sector benchmark).
- **Mentorship (Sep–Oct):** one real Gangshan pilot — real bills in, real pack out, structure reviewed by MIRDC engineer/verifier; one load shifted & measured.

---

## 9. Mock-corpus plan (no real bills needed to start)

Because real bills/invoices require pilot consent, build a **synthetic but format-faithful** corpus for 3 archetypal firms:
1. **Bills:** reproduce Taipower TOU bill layout (from the public rate PDF + eBill sample); vary contract capacity, peak/off-peak kWh, summer/non-summer.
2. **E-invoices:** generate **valid MIG 4.0 XML** with the open Turnkey library (§5.3) for steel wire-rod, natural gas, plating chemicals; render to PDF/photo for the VLM.
3. **Production logs:** synthetic per-CN-code volumes (CN 7318 15 xx variants) with realistic machine mixes (wire draw → cold forge → thread roll → heat treat → plate).
4. **Ground truth:** hand-compute each firm's SEE so the pipeline has a golden answer; cross-check method against the C2 *screws & nuts* example.

Deliverable: `/data/mock_corpus/{firm_a,firm_b,firm_c}/` + `ground_truth.json`.

---

## 10. Verifier-readiness (so the pack survives scrutiny)
Encode IR 2025/2546 (C7) checks as an output linter: every emission figure traces to a source (actual/default) with a document reference; allocation shares sum to 1 with stated method; uncertainty reported per line; precursor origin stated. The tool **prepares** verification; the accredited verifier still verifies. Never emit the word "certified."

---

## 11. GAP ANALYSIS — what we have vs. what's missing

| ID | Gap | Severity | Have / Don't have | Mitigation |
|---|---|---|---|---|
| **G1** | Exact template cell-map not yet transcribed | Low | Have the file (C1) + worked example (C2); haven't opened binaries this session | Sprint-0 task; deterministic once opened |
| **G2** | Real SME bills/invoices need consent | **High** | Formats known; no real samples | Synthetic corpus now (§9); real data at pilot |
| **G3** | Taipower bill has no open machine-readable schema | Med | Have layout via public PDF/eBill | VLM-parse from photo; collect consented layouts at pilot |
| **G4** | Machine-level allocation is genuinely hard from bill-level data | **High** | Method designed (OR-Tools + priors) | Ship with quantified uncertainty; tighten with 15-min AMI + pilot run-hours (this is the core AI contribution, not a bug) |
| **G5** | China Steel per-product wire-rod SEE not public at needed granularity | Med | CSC aggregate footprint + "carbon-neutral wire rod" line exist; GHG registry #16059 | Use **CBAM default precursor value (C5)** as conservative fallback; request mill EPD at pilot |
| **G6** | Default-value Excel (C5) column semantics per CN 7318 need parsing | Low | Have the file + reg (C4) | Sprint-2 parse; unit-test against a known CN 7318 15 88 row |
| **G7** | Indirect (electricity) emissions currently excluded from the CN 7318 certificate (only cement/fertiliser include indirect) | Med (framing) | Confirmed via rules (see §2A) | Reframe Module 2 benefit as **NT$ cost + Scope-3 + DPP/future + domestic-fee** readiness, **not** a CBAM-certificate reduction; re-confirm against IR 2025/2547 text |
| **G11** | Owner's *received* e-invoice XML access on the MOF platform (consent + auth) | Low/Opportunity | e-GUI universal & structured (§2A) | Prefer structured XML pull for steel/fuel inputs over OCR; fall back to photo parse; formalize consent flow at pilot |
| **G8** | Live #8931 pull cadence / auth / schema stability | Low | Dataset IDs confirmed | Wrap in a cached fetcher; historical #37331 as backfill |
| **G9** | Taiwanese-language ASR for voice input | Low | LINE supports audio; Mandarin ASR mature, Taiwanese (Hokkien) weaker | Start text+Mandarin; Taiwanese voice = stretch |
| **G10** | On-prem hardware for the "local-first" pilot | Low | 7B runs on one consumer GPU | Spec a mini-workstation; 3B CPU path for smallest firms |

**Bottom line:** no *blocking* unknowns remain for a submission-grade PoC. The two high-severity items (G2 real data, G4 allocation) are exactly the pilot-and-uncertainty story the proposal already tells; everything else is a scheduled task with a resource in hand.

---

## 12. Immediate next actions (shopping list)
1. Create repo; download C1–C10 into `/data/cbam_official/`; unzip C2 and transcribe the **screws & nuts** map (Sprint-0).
2. Pull MOENV EF DB via `data.moenv.gov.tw/swagger`; snapshot the default-values Excel (C5) and parse CN 7318 rows.
3. `ollama pull qwen3-vl:8b-instruct`; stand up the FastAPI + LINE webhook skeleton.
4. Generate the 3-firm mock corpus (Taipower bills + MIG 4.0 e-invoices via the open Turnkey lib + production logs) with ground truth.
5. Wire the pipeline end-to-end on Firm A; reproduce the C2 example numbers in pytest.

---

### Source index (key URLs)
CBAM template & examples, methodology (2025/2547), default values (2025/2621 + Excel), verification (2025/2546), guidance (EN/ZH), Q&A, registry (2024/3210), downstream proposal (52025PC0989), certificate price — all under `taxation-customs.ec.europa.eu` / `eur-lex.europa.eu` (see §3). Taiwan: MOENV EF `data.gov.tw/dataset/28176` + `data.moenv.gov.tw/swagger`; product CFP `#8992`; GHG `#16059`; Taipower generation `#8931`/`#37331`; Taipower rate tables `taipower.com.tw/2289/2290/46940`; e-invoice MIG/Turnkey open API `github.com/phidiassj/TaiwanEInvoiceOpenAPI`. Stack: Qwen3-VL (`huggingface.co/Qwen/Qwen3-VL-8B-Instruct`, `ollama.com/library/qwen3-vl`), InternVL3.5-8B (`huggingface.co/OpenGVLab/InternVL3_5-8B`), PaddleOCR-VL, DeepSeek-OCR (MIT), Docling, vLLM, OR-Tools, openpyxl, LINE Messaging API.
