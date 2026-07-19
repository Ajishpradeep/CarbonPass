# CarbonPass — Facts & Claim Discipline

**Date:** 20 Jul 2026 · **Status:** 🟢 LIVE — **the only place a pitch, slide, or line of code may
take a fact from.** Every entry is verified against a primary source (EUR-Lex legal texts now
in-repo, the Commission's Q&A/workbooks, Taiwanese government publications, or our own reproducible
engine runs). Sources for each block are named inline; the raw evidence trail (full quotes,
forensics, research provenance) is preserved in `archive/15_evidence_dossier.md` and
`archive/19_claim_verification_register.md`.

**Rules of engagement:** never un-kill a dead claim (§7) · every headline ships with its net/actual
twin in the same sentence · no undated price or factor, anywhere · provisional numbers stay labelled
provisional · the tool prepares verification, it never certifies.

---

## 1. The regime in one table (definitive period, live rules)

| Fact | Detail | Source |
|---|---|---|
| Obligation vs cash | Certificate obligation accrues from **1 Jan 2026**; certificate **sales open 1 Feb 2027** (Common Central Platform); first declaration + surrender **30 Sep 2027**; from 2027 declarants must hold 50% of YTD emissions quarterly | Q&A p.20–24 |
| Period | One SEE per CN code per **calendar year** — never per shipment; period cannot precede 2026; alternative periods ≥3 consecutive months | Q&A §4.14 |
| Scope by sector | **Direct emissions only for iron/steel, aluminium, hydrogen**; cement & fertilisers declare direct **and** indirect | Q&A §4.16 |
| Fastener processes | Plating, cutting, welding, finishing are **out of scope**; wire drawing is in | Q&A §4.31 |
| **Mass before cutting** | "operators shall use the mass of precursors as entering the production process (before cutting)" — and in the law: activity level = mass of goods **leaving** the process; *"off-spec products, by-products, waste, and scrap … shall not be included"* → **scrap sits inside the declared SEE**. The yield lever's legal basis | Q&A §4.11 + **IR 2025/2547 Annex III §F** |
| De minimis | **50 t / declarant / year, net mass** — a cliff, not an allowance; exempts ~90% of importers (~182k), keeps ~99% of emissions; hydrogen/electricity no threshold. (The €150/consignment rule is expired transitional folklore) | Q&A §4.30, Reg 2025/2083, COM(2025) 783 |
| EU-origin precursors | Count as zero but must still be reported by quantity | Q&A §4.18 |
| LCA factors banned | "emission factors from LCA/life-cycle-inventory databases are **not accepted**" — ISO 14067 certs are not CBAM-usable as factors | Q&A §4.24 |
| 2026 has no history | Goods produced before 1 Jan 2026 cannot have compliant actual data (no verifier existed) → **defaults mandatory for 2026 imports absent verified data** | Q&A §5.17, §5.20 |
| Record retention | **Six years** after the reporting period, at the installation | IR 2025/2547 Annex II A.1.4 |

## 2. Defaults & the two legal-gate verdicts (both regulations read in full, 20 Jul 2026)

**Defaults are lawful, unlimited, forever.** Q&A §4.25: usable for "**all types of CBAM goods**"
absent verified data; §5.10: "If operators choose not to offer this service, declarants will have to
use default values."

**✅ GATE A — NO estimation cap exists in IR 2025/2547** (closes the old kill-list question in the
"no cap" direction):
- Annex II A.1.2: an operator can use actual values, default values, **"or combine actual values and
  default values"** — no percentage limit anywhere.
- Annex II A.3.1(a): where monitoring is technically not feasible or costs are unreasonable, default
  values *"shall be used"* — the prescribed fallback, not a rationed concession.
- Annex III (attribution rules) contains **zero** estimation/default/percentage language.
- The only obligation attached to default use is **disclosure**: Annex IV requires reporting "the
  share of embedded emissions for which default values were used". Reported, never capped.
- (The old "20% cap" was a transitional rule on *estimations* under **repealed** Reg. 2023/1773; the
  "≥80% actual" folklore probably originated in an unrelated scrap-yield example in the expired
  guidance, p.57.)

**Mark-ups — from the row, never hard-coded.** The workbook's marked-up column applies to **TOTAL**
(not direct): steel/cement/aluminium/hydrogen carry **10% (2026) / 20% (2027) / 30% (2028+)**;
**fertilisers a flat 1% in every year, non-compounding** (verified at 100% of rows). "It should in
most cases be more advantageous … to use the actual values" — the Commission saying the design
intent out loud (Q&A §4.25). Engine: `DefaultValue.derived_markup()/for_year_direct()`.

**The fallback rule is legal text** (IR 2025/2621 Annex I preamble): where a listed country shows no
value or "–", the *"Other countries and territories"* table applies = **"the average of the ten
exporting countries with the highest emission intensities per good"** (Q&A §4.26) — deliberately
expensive. Engine: `defaults.resolve()`.

**✅ GATE B — the CN 7221 hole is in the published law itself.** In the Official Journal text of IR
2025/2621: **Taiwan's CN 7221 row reads literally `see below N/A see below #VALUE! #VALUE!
#VALUE!`** — unresolved spreadsheet errors enacted into law, upgrading "probably a publishing
defect" to **demonstrated**. Thailand and Vietnam show all dashes. Of the 33 full-book countries,
**only these three fastener exporters lack CN 7221**; all resolve to the fallback **4.82 → 5.302
(2026)**. Grep-able texts beside the PDFs in `data/cbam_official/legal/`.

## 3. The adopted tables, measured (our engine, reproducible)

*Reproduce: `uv run python scripts/atlas_scan.py`; workbook = IR 2025/2621 as published.*

- **The 33/87 split:** of 120 country sheets, **33 carry a CN 7318 15 row, 87 carry none at all**
  (reached by sheet omission, not dashes). Coverage is bimodal: 58 countries hold <50 goods.
- **CN 7318 15 across the 33:** min 1.37 (Philippines) · median 2.80 · max 8.23 (Indonesia) — a
  6.0× spread. **Taiwan 2.70719 → €224.18/t in 2026** — mild, below median. China 6.375, India
  5.72, fallback 4.8012.
- **The fallback is punitive by construction:** exceeds the listed-country median for 255/260 goods
  (98.1%), median ratio 1.61×.
- **Wire rod CN 7213:** Taiwan 2.298; spread 58.79× and **route-driven** — the four lowest are all
  route (E) EAF/scrap. (CN 7213 is byte-identical to CN 7207 11 11 across all 33 countries — a
  propagation, see §6.)
- **The 44× "same factory, moved" table** (hold firm_a's measured 2.924 tCO₂e/t fixed, change only
  the passport; €75.28/t): Thailand **−€20.74/t** (proving makes you worse off — the Thailand-row
  discipline) · Taiwan +€4.03 · Vietnam +€7.58 · fallback +€177.43 · India +€253.52 · Indonesia
  **+€461.36/t**. The reward for proving is set by the book, not the carbon.
- **Stainless:** Taiwan's stainless block (CN 7218–7223) sits at percentile 0.97–1.00 — **~2.6× the
  world median, systematic**; yet Taiwan's CN 7227 (2.17) is the lowest value on earth. The flat
  7318 default (a carbon-steel number) under-counts an honest stainless maker **~2×**: honest actual
  ≈ 6.003 vs default 2.978 → the buyer would pay **€228/t more for honesty** (firm_b: €296k/yr), so
  nobody reports, and the problem stays legally invisible.
- **Benchmarks workbook (2025/2620):** 73181100 → 1.364 · 73181210 → 1.154 (byte-verified in-repo;
  column A vs B never defined in the file). 402 CN codes have a benchmark but no default; **4
  aluminium codes have neither benchmark, default, nor fallback** — a genuine hole.
- **Taiwan's own government disagrees with the default:** MOENV coefficient DB lists
  螺絲(含球化與表面皮膜處理及電鍍) = **3.41 tCO₂e/t** vs the CBAM Taiwan default 2.707 and our firm_a
  2.924.

## 4. Verification & the provability divide (expansion register, not the headline)

- **Zero CBAM verifiers accredited** (first accreditations ~Sept 2026). Declared actuals from 2026
  **must** be verified (Q&A §5.9). One report **per installation**, year-1 physical site visit,
  bilingual 3-person minimum team, **no group verification anywhere in the regime**; certificates
  cannot be transferred even within a corporate group.
- **NABs accepting third-country applicants: 8** (EA list, 2 Jul 2026 — up from 4; the EC's own
  state-of-play table said 4 and disagrees with EA on Belgium → always cite by retrieval date).
  NL–TURKAK and SE–NAAU bilaterals prove accommodation is possible — its absence for Taiwan is a
  choice.
- **Taiwan's own admission** (MOENV, 13 Feb 2026): 20 domestic GHG verification bodies, 200+
  specialists, **zero EU applications** — because the EU had not opened them; blockers are EU-side.
  ~2,600 exposed manufacturers, 3.74 Mt, 13th place. No Taiwanese verification subsidy exists (only
  stated intent); India is reportedly designing a 90% reimbursement — a government does not subsidise
  a cost it thinks is trivial.
- **The documented voids** (absence-of-evidence as the finding): no published CBAM verification
  price · no published count of in-scope non-EU installations · no NAB fee schedule · no group
  provision · no verifier travel-cost data.
- **Registry gap:** operator-to-operator precursor sharing via the Registry only **from 2028**; until
  then the mill-EPD → fastener-maker handoff travels by private channels while the importer carries
  sole liability.
- **Field evidence (India, Jan 2026, journalistic):** first shipment seizures; MSME levies tripling
  €70–80 → €240–300/t as firms fall onto defaults.
- **Counter-evidence we concede:** the 50 t de minimis is real relief (for importers, not
  producers) · year-2+ site-visit waivers favour exactly the simple installations we champion (scope
  the claim to the year-1 cold start) · Taiwan's default is mild — which is why Taiwan is the lab,
  not the victim.

## 5. Engine-measured anchors (all reproducible from this repo, 53/53 tests)

| Anchor | Value |
|---|---|
| Commission worked examples reproduced | screws-and-nuts AND cement, rel 1e-9 (`tests/golden/`) |
| Firms A/B/C e2e vs ground truth | rel ≤1e-6 (GT derived from emitted document rows) |
| firm_a (carbon screws, 3,000 t) | SEE 2.924 direct; loss 9.1%; **758 tCO₂e/yr gross embodied in scrap · NT$7.35M purchase / NT$4.41–5.15M net**; 5%-scenario: 359 t + NT$3.48M; buyer delta €4.03/t → fix-list says **"not worth it this year"** |
| firm_b (carbon + stainless) | stainless SEE 6.003 via the 7221 fallback; the smallest line carries the most money in scrap (NT$13.4M gross / NT$7.4–8.7M net) |
| firm_c (mill EPD) | default share 95%→0%; buyer delta **€60.31/t ≈ €108k/yr** |
| Yield vs scheduler | **80×** (359 vs 4.49 tCO₂e on the same firm) — and only yield moves the declared SEE |
| Scheduler | NT$399,800/yr, live #8931 feed, verified TOU 9.39/5.85/2.53 (HV 3-tier summer, eff. 1 Oct 2025) |
| VLM bake-off | qwen3-vl **4B: 336/336 (100%)** across six phone-photo degradations, 18–31 s/doc, laptop, offline; 8B: 288/288; InternVL3.5-8B: 66% |
| Workbook integrity | 19-sheet template filled without touching a formula; LibreOffice independently recomputes the engine's SEE (re-verified at grid EF 0.466) |
| Config discipline | grid EF 2025 industrial **0.466** (dated, provenance in every output); certificate €75.36 Q1 / €75.28 Q2 2026; **requesting an unpublished quarter raises** (test-pinned) |

## 6. Defects in the Commission's own files (the give-back payload)

The reason the atlas is a public good and the answer to the form's "suggestions for modifying open
data": ① five cement rows (Angola/Argentina) use a compounding mark-up contradicting their own sheet
headers (~2.4% overstatement by 2028) ② four aluminium goods have neither benchmark nor fallback ③
CN formatting is inconsistent (22 unspaced codes — the whole aluminium block; a naive join silently
drops the sector) ④ three different dash characters encode "no value" ⑤ 873 `see below` heading
rows inflate the catalogue ⑥ CN 7213 ≡ CN 7207 11 11 byte-identical across all 33 countries ⑦ **CN
7221 missing for exactly TW/TH/VN, with Taiwan's row carrying literal `#VALUE!` errors in the OJ**
⑧ Mali hydrogen = 0.00 exactly ⑨ benchmarks version date "2025-02-06" (likely a 2026 typo) ⑩
production-route codes (A)–(H)/(J) never defined in either workbook ⑪ `total ≠ direct+indirect` in
711 rows is **2-dp rounding, not an error** — pre-empt the careless-reader scandal.

## 7. KILL-LIST — never say, in any artifact

- **€450–750/t for Taiwan** (Taiwan ≈ €224/t; €397–681 is the *fallback/India/Indonesia* — the
  folklore described the unlisted and the dirty, never Taiwan)
- **"80% must be verified actual data" / any 20% default-or-estimation cap** (no cap exists —
  legally closed, §2 Gate A)
- **"5% variance threshold"** (no numeric materiality threshold exists anywhere — and do not invent
  one, including in our own product heuristics without labelling them ours)
- **"Verification costs €5k–50k"** (untraceable lead-gen folklore) · **"403 verifiers"** (that's EU
  ETS; the CBAM count is zero)
- **"Developing countries get worse defaults"** (false by measurement — both tails of the percentile
  ranking are developing economies; the driver is route and grid, not income)
- **"2,400-page regulation"** (no official page count; say "a rulebook of eleven legislative acts
  and their annexes" — ironically IR 2025/2621 alone happens to be 2,400 OJ pages, but the claim
  stays dead)
- **"Throwing scrap away / nobody counts it"** (scrap is sold; the owner knows the tonnage; say
  **information gap** — attribution, drift, carbon-linkage, net price, benchmark)
- **Gross waste money without net** (recovery ~30–40% carbon / 35–45% stainless → net = 60–70% of
  gross) · **"avoided" for gross embodied carbon** (say "carbon purchased that never ships"; remelt
  caveat always attached)
- **0.474 as the current grid EF** (2024 figure; current = 0.467 overall / 0.466 industrial, MOEA
  2 Jun 2026)
- **"Only four NABs"** (8 as of 2 Jul 2026 and rising; cite retrieval date; EC vs EA lists disagree)
- **"Top-3 fastener exporter" without qualification** (top-3 **by volume**; **#4 by value**, 2023)
- **Any Q3-2026 certificate price** (does not exist until 5 Oct 2026 — the engine refuses; so must
  every slide)
- **ISO 14067 as a CBAM by-product** (LCA factors not accepted, Q&A §4.24)
- **Citing the 2023 guidance PDFs as a rule source** (expired, repealed basis, contradicts the live
  de-minimis — mechanics and worked examples only)
- **The first-draft stainless numbers** (CN 7223 / 4.61× / €703/t / 1,539 t — wrong code; the
  correct finding is CN 7221 / ~2× / €228/t / 742 t)
- **UNCTAD's $5.9bn/$10.2bn** (unverified in the primary; models a 2021 design since changed)

## 8. Always-say

- Certificates: obligation 2026 · sales Feb 2027 · surrender 30 Sep 2027.
- Electricity/indirect: recorded but **not certificated for iron & steel** — the scheduler's carbon
  never touches CBAM money for CN 7318; label it on every surface (the ledger and fix-list do).
- Mass counts **before cutting** (IR 2025/2547 Annex III §F) — scrap sits inside the declared SEE.
- **54% of small/mid-sized plants** run pen+paper/spreadsheets as their MES (IoT Analytics, Dec
  2025 — the stat is about exactly our population); cost of poor quality **10–20% of revenue**
  (ASQ); APQC scrap+rework ~2.2% median.
- Loss band **5–15%** (documented synthesis; cold forming runs 85–95% material utilization);
  **9.1% is synthetic mid-range until the pilot measures it** — labelled in every surface.
- Pilot partners are **targets**, not secured.
- A negative answer is a feature: the tool can and does say "not worth it this year"
  (Thailand-row discipline; test-pinned).

## 9. Watch-list (re-verify before 31 Jul and again before finals)

| Number | Current (19–20 Jul 2026) | Moves |
|---|---|---|
| CBAM certificate price | €75.28 (Q2) | Q3 published **5 Oct** |
| Grid EF | 0.467 overall / 0.466 industrial (2025) | annually ~Jun |
| NABs accepting third-country verifiers | 8 (EA, 2 Jul) | rising; EC vs EA disagree — cite date |
| Scrap CFR Taiwan | ~US$325/t (15 Jul) | weekly |
| Wire rod (domestic) | ~NT$27,350/t (Apr) | monthly — waste figures at NT$24.5k are conservative |
| TOU tariff | 9.39/5.85/2.53 (eff. 1 Oct 2025) | next review ~Oct 2026 |
| EP plenary vote (downstream ~180 categories) | expected Sept 2026 | update market slide with outcome |
| MOENV platform / verifier-subsidy news | platform live Apr 2026; no subsidy announced | any week |
| CBAM Q&A version | 27–28 May 2026 | check before submission + finals |

## 10. Still unresolved (do not assert either way)

1. EC vs EA discrepancy on BELAC/Belgium — flag whenever either list is cited.
2. "France warns of verifier shortage" — third-hand; chase the primary or attribute precisely.
3. The India/Indonesia/Vietnam stakeholder paper (ScienceDirect S2772427126000963) — our best
   academic citation for fixed-cost regressivity, still behind a 403; obtain before quoting.
4. TIFI / MIRDC institutional positions — no evidence either way; do not assert from silence.
5. Why Taiwan's stainless is dirty — NPI/ferronickel import hypothesis, unverified; do not assert.
6. "Simplified declarations for small/micro primary producers" + 30 Jun 2027 enforcement date —
   unverified in the primary regulation.
7. Number of in-scope non-EU installations — no published figure; **make the absence the point**.
