# SESSION HANDOFF — Pred-hack Project State (as of 13 Jul 2026)

**Purpose:** paste/reference this file in a new session to resume with zero re-research. It compresses everything established across the full working session: the concept, all verified facts, corrections, strategy, deliverables, and next steps.

---

## 1. What this project is

Entry preparation for the **2026 Presidential Hackathon International Track (PHIT)**, theme **"Digital Inclusion in the AI Era."** Submission window: **22 May – 31 Jul 2026, 17:00 GMT+8**. Team rules: 3–10 members, **≥1 non-ROC national**, 2 designated contacts, everything in English. Timeline: preliminary review Aug 6–16 → mentorship mid-Sep–mid-Oct → final review late Oct → awards early-mid Dec. Scoring: prelims **Feasibility 40 / Innovation 30 / Social Impact 30**; finals **30/20/20 + Implementation & Verification 30** (measures progress *between submission and finals*; requires only "a system demo or code design description"). Full deployment is NOT expected — the campaign is a **policy-adoption pipeline** (mentorship, public-private matchmaking, field-validation support, follow-up benefit tracking).

## 2. The final concept: **CarbonPass**

*A local-first AI compliance + energy-optimization copilot for Taiwan's export SMEs, prototyped on the fastener cluster (CN 7318, Gangshan–Luzhu, Kaohsiung).*

- **Module 1 — Data-Pack Engine:** photograph Taipower bills + material invoices + production records in LINE (Mandarin/Taiwanese, voice-friendly) → document AI + **allocation reasoning** (facility energy → product lines/CN codes, uncertainty-quantified) + EU rules engine → **per-CN-code "specific embedded emissions" pack in the European Commission's CBAM template**, flagged field-by-field for the verifier. Killer demo screen: "with your data your buyer pays ≈€150/t; without it €450–750/t and rising."
- **Module 2 — Grid-Aware Scheduler:** hourly grid carbon intensity computed from Taipower's open 10-min generation-by-unit feed + TOU tariffs → MILP+RL shift plans for flexible loads (furnaces, compressors, plating); measured before/after ledger "structured to ISO 14064-2 logic" (never "certified" — verification stays with accredited verifiers).
- **Module 3 — Inclusion Interface:** the LINE/voice conversational front end IS the digital-inclusion claim (handbook axes: **ages** = aging family-firm owners; **regions** = one nameable southern district; **needs** = carbon-verified market access as a de facto digital service).
- **Architecture:** local-first (raw data never leaves factory). Federated learning / TEEs = roadmap only, NOT PoC. NILM virtual sub-metering = labeled stretch goal (public datasets are residential; industrial 3-phase unproven).
- **SDGs:** 8, 9, 12, 13.

## 3. Verified fact base (all sourced & dated; safe to reuse)

**Taiwan carbon fee (first cycle, closed 31 May 2026):** NT$4.97bn from 461 factories / 240 companies; semiconductors NT$2.2bn (44%, incl. 33 TSMC fabs), electricity NT$635m, steel NT$400m, concrete NT$130m. Rates NT$300 standard / NT$100 / NT$50 preferential; 0.2 leakage coefficient (~NT$10/t floor); ~430 applied for preferential, ~28 withdrawn/rejected. Threshold 25,000 tCO2e/yr; to be lowered; fees signalled toward NT$1,200–1,800/t by 2030; ETS pilot ~2027. [Focus Taiwan 3 Jun 2026; Taipei Times 4 Jun 2026; MOENV PR 31552/30237; Eco-Business Jun 2026]

**EU CBAM:** definitive (paying) phase since 1 Jan 2026; sectors: cement, iron & steel (incl. **CN 7318 fasteners from the original Annex I**), aluminium, fertilisers, electricity, hydrogen. Certificate price = quarterly ETS average: **€75.36 (Q1 2026), €75.28 (Q2 2026)** [official EC figures]. First surrender Sep 2027 (covers 2026). **Default values NOT abolished** — set at highest observed intensity, marked up +10% (2026) → +20% (2027) → +30% (2028); complex goods: ≥80% must be actual third-party-verified data. 50t de minimis exempts ~90% of importers (keeps ~99% of emissions) but is counted **cumulatively per EU importer** → small suppliers swept in (MOENV director-general publicly warned of this). **Downstream extension:** ~180 steel/Al product categories proposed Dec 2025, obligations 1 Jan 2028; Council position adopted Jun 2026; **EP plenary vote expected Sep 2026 — inside the mentorship window** (pending legislation; never book as current benefit). [DG TAXUD; ICAP Oct 2025; O'Melveny 2026 (Reg. 2025/2621, "2,400 pages"); Akin/Covington 2026; Taipei Times 2 Mar 2026]

**Taiwan exposure:** 13th-largest CBAM exporter to EU; **3.74M tonnes** Oct 2023–Dec 2025, mostly screws/fasteners/steel; **~2,600 SMEs** produce them (MOENV, 2 Mar 2026 — the anchor number). MOENV launched a **CBAM help platform (Mar 2026) — informational only, computes nothing**.

**Fastener sector:** ~1,800 manufacturers (TIFI ~700 members); top-3 global exporter (#2 by value 2023 / #3 by volume 2025-26 — always say "top-3"); ~10–13% world production; ~1.2M t exported (2025); US$4.59bn (2023) / ~US$4.28bn (2024); ~¼ to Europe; ~2 tCO2e/t product (industry est.); default-value exposure up to 30–50% of product value on commodity lines (industry est.). Cluster firms Chan Chin C. and Fang Sheng hold ISO 14067/14064-1 certs via subsidized MIRDC counseling → task tractable but consultant economics don't scale.

**Macro:** 1.716M SMEs = 98.87% of firms, 9.19M employed (79.3%), ~10.3% of export value, 51.79% family-run/sole proprietorship, 58.22% >8 yrs [MOEA 2025 White Paper]. Net-zero 2050 statutory (CCRA 2023); **NDC 3.0: −28±2% (2030), −32±2% (2032), −38±2% (2035) vs 2005**. Grid EF **0.474 kgCO2e/kWh (2024)** [MOEA Energy Admin].

**Existing-solutions gap audit (verified Jul 2026):** CAAS (sme.gov.tw) = courses only; MOEA/IDB calculator = rough org totals, no product level/CN codes; MOENV CBAM platform = info only; Taipower app = charts/tariff simulation, no emissions; tre100 (CIER, Dec 2025) = RE pledge registry; consultants = per-engagement, non-recurring economics. **Nobody converts SME documents → importer-ready per-CN-code SEE data.**

## 4. Kill-list — claims that are WRONG (never reuse)

1. ~~"1.71M SMEs need carbon reporting"~~ → real compelled core = **2,600** (+ est. 10k–15k under customer Scope-3 pressure).
2. ~~"SMEs can submit ISO 14064-2 plans for preferential rates"~~ → preferential rates are **only for regulated large emitters** and depend on **their own Scope 1+2**, not supplier data. SME incentives = customer retention, cost pass-through, energy savings, readiness. (Voluntary Reduction Mechanism exists: credits 1.2:1 offset, 10% cap, hard eligibility/additionality — multi-year path, not an app feature.)
3. ~~"CBAM no longer accepts default values"~~ → legal but punitive (markups above).
4. ~~"ASML is a Taiwan emitter"~~ → correct names: TSMC, Taipower, China Steel, Formosa Petrochemical, TCC.
5. ~~"Big Sectors Section 3"~~ → garbled Scope 3 + CBAM Annex I.
6. ~~B.E.N.Z. 2022 = "AI smart agriculture"~~ → actually GIS urban-forest/tree placement (official history page). Also 2019 honor roll ambiguous (Cartelogy vs Mentadak — flag, don't resolve).
7. TSMC supplier pressure comes from **SBTi/RE100/customer programs (NT$5.5bn supplier subsidy)**, not the carbon fee.
8. Layer-2 machine optimization from monthly bills = **mathematically impossible** (both audits agree); needs 15-min AMI interval data (customer CSV export — no third-party API).

## 5. Winners study conclusions (own research, Jul 2026)

14 Teams of Excellence 2019–2025 examined individually. **Verdict: quality is the entry ticket; national timing is the selector** — no winner ever beat the year's theme. **Half pre-existed the event** (SISOCS 2014, A/B Street 2018, HysonTech & GreenHope = operating companies). **Afterlife split exactly 7/7**: every surviving winner had an institution/company behind it; every pure hackathon team vanished from the public record. India recurs in 4/7 editions (diplomatic dimension). → Strategy: theme-lock + arrive with something working + multinational team + **integration targets (MOENV platform, SMESA/CAAS, TIFI/MIRDC) are survival-critical, not decoration**.

## 6. PoC datasets (all open, verified)

data.gov.tw **#28176** (MOENV emission coefficients, OpenAPI at data.moenv.gov.tw/swagger) · **#8992** (product CFP registry) · **#8931** (Taipower real-time 10-min generation by unit) + **#37331** (historical) → derive hourly grid intensity · Taipower TOU rate schedules (taipower.com.tw) · EC CBAM default values Reg. (EU) 2025/2621 + templates (DG TAXUD) · EC quarterly certificate prices · Eurostat Comext / MOF customs (CN 7318 flows) · MOENV GHG registry (CSC precursor benchmarks) · AMI 15-min CSV via customer consent · mock bill/e-invoice corpus (MOF spec public). **Give back** (scored by form): cleaned hourly grid-intensity dataset + anonymized fastener SEE benchmark. Stretch-only: MIMII/UK-DALE/REFIT (residential/acoustic — label as proxy).

## 7. Deliverables inventory

**In `/Pred-hack` folder (markdown):**
- `6. Critical Research Audit…` — my adversarial audit (verdict, A–F answers, risks)
- `7. UNIFIED FINAL REPORT - CBAM Copilot…` — Claude×Gemini consensus/variance adjudication + handbook-fit + deployment-expectation analysis
- `8. MASTER PROPOSAL - CarbonPass…` — the single end-to-end narrative proposal (supersedes 1–7 for content)
- Files 1,2,3,5 = original uploaded research (treat with suspicion — see kill-list); `6-G` = Gemini audit; `PHIT_2026_HANDBOOK_EN.pdf`

**In session outputs folder `carbonpass/` (PDFs + TeX sources + charts — copy into Pred-hack to keep!):**
- `CarbonPass - Educational Proposal (PHIT 2026).pdf` — 17pp explainer for newcomers, 5 charts, 8 tables, clickable refs
- `CarbonPass - Competition Entry Proposal (PHIT 2026).pdf` — 13pp submission-framed (campaign context → winner patterns → application-form structure)
- `PHIT Winners Study - What Actually Wins (2019-2025).pdf` — 9pp evidence review
- TeX sources: `main.tex/sec1-7/refs.tex`, `prop_main.tex/p1-p5`, `study_main.tex/s1-s3/srefs`; charts `chart1–8*.png` (matplotlib scripts recreate them)
- Build recipe: sandbox has **no Chromium/npm/pip** → use **XeLaTeX** (fonts: DejaVu Serif + Noto Serif CJK TC; compile 2–3×; pdftoppm for visual checks)

## 8. Open items / next steps

1. **Team assembly** (3–10, ≥1 foreign national) — only unfillable blank in the entry PDF.
2. **Build PoC v0**: Module 1 on 3-firm mock corpus + Module 2 on synthetic load vs live #8931 feed + LINE bot + demo video — due before 31 Jul.
3. **Outreach**: TIFI member firm / MIRDC / Kaohsiung EPB advisory team for expressions of interest (targets, not secured).
4. Fill the official online application form field-by-field (Section 8.3 of master proposal maps every field).
5. During mentorship: 1 real Gangshan pilot; track **EP plenary vote (Sep)** and update market slide.
6. Not yet done: verify current Taipower TOU table before submission; sector employment figure doesn't exist officially (don't invent).
