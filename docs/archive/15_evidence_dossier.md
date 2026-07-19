# EVIDENCE DOSSIER — CBAM, the adopted tables, and what our engine can prove

**Date:** 17 Jul 2026 · **Companion to:** `docs/14_scope_extension.md` (the thesis this evidence
supports). This file exists so `docs/14` stays readable and so a later pass can rebuild
`docs/09_master_proposal.md` and the submission PDF against primary evidence rather than memory.

**Provenance:** four parallel research passes on 17 Jul 2026 — (1) the adopted default-value and
benchmark workbooks in `data/cbam_official/`; (2) the Commission's Q&A and operator guidance PDFs in
the same directory; (3) the engine and Taiwan data in this repo; (4) external web research on
verification economics and capacity.

**How to read the tags:** **[HARD]** = primary/authoritative and directly on point · **[ANALOGUE]** =
adjacent regime · **[ESTIMATE]** = secondary/commercial/modelled · **[GAP]** = evidence absent, which
is itself a finding · **[OURS]** = our own measurement or arithmetic, reproducible from this repo.

> ⚠️ **The single most important framing note.** Our two guidance PDFs and our Q&A are from
> **different legal regimes**. `guidance_installations_outside_eu_EN/ZH.pdf` is dated **8 Dec 2023**,
> is explicitly **"not legally binding"**, is scoped to *"the transitional period (1 October 2023 to
> 31 December 2025)"* (p.7), and is built on **repealed** Reg. 2023/1773. `cbam_qa.pdf` (27–28 May
> 2026) is the definitive-period document, on IR 2025/2547 / 2025/2621 / 2025/2546. **Several of our
> load-bearing claims came from the expired document.** See §5.

---

## 1. Legal dossier — the definitive-period rules

### 1.1 Defaults: lawful, unlimited, and deliberately expensive

**[HARD]** QA p.36 §4.25:
> "During the definitive period, authorised CBAM declarants can use default values for **all types of
> CBAM goods** other than electricity in cases where verified actual embedded emissions data for those
> goods is not available."

**[HARD]** QA p.44 §5.10 — the most important sentence in the corpus for our product:
> "Only third-country operators producing CBAM goods can decide to monitor and calculate their
> emissions in line with the CBAM methodology rules and to ensure the verification of their
> calculation. **If operators choose not to offer this service, declarants will have to use default
> values.**"

**[HARD]** QA p.39 §4.30 — a complex good (metal part + non-CBAM material), stated **without any 20%
qualification**:
> "When embedded emissions of the complex good are determined based on default values, the default
> values laid down in Annex I of Implementing Regulation (EU) 2025/2621 shall be used."

**[HARD]** QA p.48 §5.17 — for 2026 imports, defaults are *mandatory* absent verified data:
> "For goods imported during the year 2026, the reporting period is legally set to the year 2026… If
> there is not actual verified emissions corresponding to the reporting year 2026, **default values
> must be used.**"

**[HARD]** QA p.37 §4.26 — how punitive the fallback is:
> "Where insufficient reliable data was available, the default values to use are the values in the
> table 'Other countries and territories' of Annex I which **correspond to the average of the ten
> exporting countries with the highest emission intensities per good**."

**[HARD]** QA p.37 §4.25 — mark-ups, and the Commission saying the quiet part out loud:
> "These mark-ups are **10% in 2026, 20% in 2027, and 30% from 2028 onwards**. A lower mark-up of
> **1%** applies to the fertiliser sector from 2026 onwards… Therefore, **it should in most cases be
> more advantageous for authorised CBAM declarants to use the actual values** where these are
> available."

**[HARD]** QA p.37 §4.25 — which table applies:
> "Those default values are country- and year-specific. **Where the CBAM good is not explicitly listed
> or where it is listed but the relevant field shows a '-', CBAM declarants have to use the default
> values from the table 'Other countries and territories'**."

**[HARD]** QA p.36 §4.24 — LCA databases are banned. *This matters for our ISO 14067 claim:*
> "**No**, emission factors from life-cycle assessments (LCA)/life-cycle inventory databases **are not
> accepted** for calculating embedded emissions of CBAM goods."

Corroborated at guidance p.161, which also notes that a monitoring system reporting only *aggregated*
direct+indirect GHG **cannot be used for CBAM** unless it can be split.

### 1.2 The 20% rule — what it really is

**[HARD, but EXPIRED]** Guidance p.158 §6.9.1:
> "Articles 4(3) and 5 of the CBAM Implementing Regulation limit the use of default values… **Without
> time limit, but quantitatively limited: For complex goods, up to 20% of the total embedded emissions
> may be determined using estimations.** Using default values provided by the Commission would qualify
> as 'estimation'. **For you as operator this offers two simplification options for your
> monitoring**…"

Three things follow, and all three matter:

1. The word is **"estimations"**, not "defaults" — defaults are one species of estimation.
2. It is a **simplification offered to the operator**, not a licence condition on the declarant.
3. It is tied to Articles 4(3)/5 of **Reg. 2023/1773 — repealed**. Guidance p.160 frames it as what
   applies *"From 1 January 2025"*; p.158 says *"without time limit"*. **The document contradicts
   itself and could not speak to 2026 either way.**

**[GAP — must close]** The 2026 Q&A **never mentions a 20% limit anywhere** (full-text searched).
Whether an equivalent estimation cap survives in **IR 2025/2547 Annex III** is **not answerable from
this repo** — that regulation is not here. See §8.1.

**[HARD]** And the probable source of our error — guidance p.57, an *unrelated scrap-yield* example
about screws and nuts:
> "if e.g. **20% of the original mass are cut away** (and disposed of as scrap), **100 t precursor are
> required for 80 t of final product**."

### 1.3 Verification

**[HARD]** QA p.43 §5.9:
> "**The declared actual emissions embedded in goods imported from 1 January 2026 must be verified by
> an accredited CBAM verifier.**"

**[HARD]** QA p.46 §5.15 — the site visit, and the year-2 relief that cuts against us:
> "In principle, the verifier is required to carry out a physical site visit at the installation where
> the goods are produced. **This is always the case for the first site visit**, except in case of
> serious, extraordinary and unforeseeable circumstances.
> In a second consecutive year… the physical site visit may sometimes be replaced by a virtual site
> visit or even by a waiver… **strict conditions apply. The installation must not be overly complex**…
> **A physical site visit must take place during the previous reporting period in order to organise a
> virtual site visit during the following year. A physical site visit must take place during the last
> two reporting periods in order to waive the obligation.**"

**[HARD]** QA p.48 §5.19 — the team, i.e. the regulatory cost floor:
> "the verifier must assemble a verification team composed of one CBAM lead auditor, which must have
> demonstrated competence to communicate effectively in English. In addition, the team must include
> **at least one CBAM auditor with the ability to communicate effectively in the language of the
> operator**."

Plus an English-competent independent reviewer. **Minimum three qualified people per engagement, one
of whom must fly to site, and the team must be bilingual.**

**[HARD]** QA p.43 §5.8 — outsourcing is allowed but is **not** group certification:
> "An accredited CBAM verifier may outsource certain verification activities to another verifier… **The
> accredited verifier – and not the outsourced body – will retain full responsibility**… Furthermore,
> **the accredited verifier may not outsource the issuance of the verification report or the technical
> review of the report.**"

**[HARD]** Accreditation mechanics: EN ISO 14065 + 17029 knowledge (§5.1); **only an EU/EEA national
accreditation body may accredit** (§5.2); valid 5 years with annual surveillance (§5.5); **scoped by
aggregated goods category** — a verifier not accredited for your goods "may not be qualified to
undertake the verification" (§5.6).

**[HARD]** QA p.45 §5.13 — where liability sits:
> "**The declarant is the only person legally responsible for the content of the CBAM declaration,
> which includes the verification report.**"

**[HARD]** QA p.44 §5.11 — the Commission warning importers off buying verification:
> "**If anyone else contacts importers to offer you a verification report, it is likely a scam.**"

**[GAP]** **Who pays is never stated.** It follows structurally from §5.10/§5.12 ("Operators may have
recourse to any verifier…", "They will then need to find an accredited CBAM verifier") and §5.8
("**The operator will also need to provide its consent** to outsource"). The operator engages the
verifier; therefore the operator pays. **No document states it, and no document gives a cost.**

**[GAP]** **No numeric materiality threshold exists.** Both PDFs searched exhaustively. The only
standard is qualitative — "reasonable assurance that the operator's emissions report is free from
material misstatement and non-conformities" (QA p.46). **The "5% variance threshold" in `docs/10` §2A
is in no source document.** (The only 5% figures in the corpus are unrelated alloy-content rules.)

### 1.4 No SME relief — exhaustively confirmed

Exact-string counts across the **full text** of both PDFs:

| Term | `cbam_qa.pdf` | `guidance_EN.pdf` |
|---|---|---|
| `SME` / `SMEs` | **0** | **0** |
| `small and medium` | **0** | **0** |
| `micro-enterprise` | **0** | **0** |
| `simplified regime` | **0** | **0** |
| `lighter` | **0** | **0** |

The only size-sensitivity anywhere: the 50 t importer threshold (§1.5), the "unreasonable costs"
doctrine (§1.6), and accreditation fees *for verifiers* varying by applicant size (QA p.41 §5.3).

### 1.5 De minimis — 50 t, per declarant, per year, by net mass

**[HARD]** QA p.9: importers below "the annual single-mass based threshold (50t)" need no
authorisation; hydrogen and electricity have **no** threshold.

**[HARD]** QA p.39 §4.30 — the computation, and it is our CN 7318 case:
> "**The net mass of this CN code in the Customs Declarations will be taken into account to assess if
> the importer is above the 50 tonnes threshold. When imports of a CBAM declarant of this assembled
> product… exceed 50 tonnes per calendar year, then the declarant is subject to all obligations.**"

Level = the **importer/declarant**, aggregated across all suppliers for the year. Metric = **net mass**
including the non-CBAM material of an assembled good — while the *embedded emissions* count only the
metallic part. It is a **cliff, not an allowance**. Returned goods still count (QA p.62 §7.20). TARIC
Y128 (expects to exceed) vs Y137 (does not) — QA p.63 §7.23.

**[HARD]** COM(2025) 783 (16 Dec 2025): the threshold exempts *"around 90% of importers, primarily
SMEs… while 99% of embedded emissions remain covered"* — ≈182,000 importers.

**🚩 [SUPERSEDED]** Guidance p.227 gives a **completely different rule**: *"the value of these goods is
negligible, that is to say does not exceed **EUR 150 per consignment**."* Value/consignment vs
mass/declarant/year. **Use the 50 t rule. Never ship the €150 rule.**

### 1.6 The real burden on a 12-person factory

*(All from the transitional guidance — indicative of **shape**, not authority on 2026 detail, but these
mechanics derive from EU ETS practice that 2025/2547 continues.)*

**Monitoring Methodology Documentation (MMD)** — guidance p.105 §6.4.1:
> "you should document the monitoring methodologies… **This monitoring methodology documentation (MMD)
> should define the system boundaries of your installation and each of your production processes**…"

p.106 §6.4.2:
> "the **MMD serves as a 'rule book' for all your installation staff, as well as for training of new
> staff**… As installations undergo technical changes over the years, the MMD and written procedures
> should be considered **living documents that should be regularly reviewed and updated**."

MMD content (p.106–107) includes *"Sampling of materials and fuels"*, *"Laboratory analyses"*,
*"Maintenance and calibration of meters"*, *"Data archiving (including security to guard against
manipulation)"* and — **the detail that tells the story** —
> "**Control activities (e.g. four-eyes principle for data collection).**"

*In a 12-person factory, dedicating two people to independently check emissions data is a headcount
claim.*

**A second document set — written procedures** (p.107 §6.4.3): responsibilities and competency, data
flow and control procedures, QA measures, estimation methods for data gaps, **a sampling plan and
process for revision**, **procedure for demonstrating equivalence to EN ISO/IEC 17025 accreditation of
laboratories**, version control across all staff.

**100% whole-site attribution — including the non-CBAM half.** Guidance p.105:
> "**At this stage the aim is to attribute 100% of the installation's emissions to goods, without gaps
> and double counting**… **Also, goods which are not covered by the CBAM have to be considered in
> order to reach this 100% target.**"

Confirmed live — QA p.38 §4.28: *"the relevant emissions of an installation should be 100% covered by
production processes for CBAM goods and any non-CBAM goods… if there are shared equipment, shared
'source streams' or shared emission sources, inputs, outputs and emissions should be attributed to the
different production processes with an appropriate share."*

**ISO 17025 labs** (p.126) — a small factory's in-house lab **fails the first criterion by
definition**:
> "Laboratories not accredited may be used… **only where there is evidence that access to accredited
> laboratories is technically not feasible or would incur unreasonable costs**… • **It is economically
> independent of the operator**… • **regularly carries out quality assurance… including regular
> participation in proficiency testing schemes**…"

**Uncertainty** (p.121): 1.5% for the biggest sources, *"for the smallest sources, uncertainty lower
than **7.5%** is considered acceptable"* — the closest thing to an SME accommodation in the entire
corpus, and it is (a) in the expired document, (b) "for orientation", (c) not an exemption.

**The genuine relief — "unreasonable costs"** (p.108 §6.4.4, p.110 §6.4.5):
> "the legislation acknowledges that administrative burden and costs should be limited. To this end,
> the concepts of 'technical feasibility' and 'unreasonable costs' are introduced. **These allow you to
> go for '2nd best' (or even 3rd best') data sources**…"
> "the costs of a monitoring approach or improvement measure must **exceed its benefit**."

And the single most SME-friendly sentence anywhere (p.155):
> "**Since quantities of produced and sold goods are usually essential elements of a company's
> financial report, such data should be available for the CBAM without additional effort.**"

**[GAP]** **Record-retention period is stated nowhere** in either document.

### 1.7 Scope details that affect our engine

**[HARD]** QA p.34 §4.16 — confirms G7:
> "**The CBAM scope is limited to direct emissions for iron/steel, aluminium and hydrogen**, while
> importers of cement and fertilisers (and of agglomerated iron ore) have to declare both direct and
> indirect emissions."

**[HARD]** QA p.39 §4.31 — good news for fasteners; plating/cutting/welding are **out of scope**:
> "…re-heating, re-melting, casting, hot rolling, cold rolling, forging, pickling, annealing, coating,
> galvanising, wire drawing, and **exclude plating, cutting, welding, and finishing** of iron or steel
> products."

**[HARD]** QA p.32 §4.11 — but the mass trap:
> "**operators shall use the mass of precursors as entering the production process (before cutting)**,
> even if emissions from cutting activities will not be accounted for."

**[HARD]** Other operative rules: EU-origin precursors count as **zero** but must still be reported by
quantity (§4.18) · negative obligations floor at 0 and cannot offset other goods (§4.32) · the mass
balance chain-of-custody model **cannot** be used (§4.13) · single-installation precursor sourcing must
be **proven to the verifier**, else weighted average (§4.10) · determination period = calendar year,
**cannot precede 2026**, alternative periods ≥3 consecutive months (§4.14).

**[HARD]** QA p.48–49 §5.20 — a hard, universal fact:
> "CBAM applies to all imports of CBAM goods into the EU from 2026 onwards, **regardless of when the
> goods were produced**… **For the year 2026 specifically, it is not possible to provide emissions data
> corresponding to the production of goods produced before 1 January 2026**… there was **no CBAM
> verification at the time, and no accredited CBAM verifier**."

### 1.8 The registry gap

**[HARD]** QA p.44 §5.10: *"**In 2027, operators are not required to register in CBAM Registry.** They
may send the information to declarants outside the CBAM Registry."* But p.44 §5.11: *"The third-country
operator **should already register**…"* — and if not, data travels via **"private channels"** and the
importer keys it in while carrying sole liability (§5.13).

**[HARD]** QA p.48 §5.18: *"**From 2028 onwards**, operators will be able to share with each other
actual verified emissions of precursors via the CBAM Registry. **In the meantime, they will have to
exchange this information outside the CBAM Registry.**"* — *i.e. the mill-EPD → fastener-maker handoff
our firm_c case depends on has no official channel until 2028.*

### 1.9 Dates

| Date | Event | Source |
|---|---|---|
| 1 Jan 2026 | Definitive period; actual emissions must be verified | QA p.43 |
| **~Sept 2026** | First CBAM accreditations issued by NABs | QA p.45 |
| 2026 | Reporting period fixed to 2026; no verified data → **defaults mandatory** | QA p.48 |
| **early 2027** | First verification reports expected | QA p.44 |
| 1 Feb 2027 | Common Central Platform opens; certificate sales start | QA p.22 |
| 2027 | Registry declaration module opens | QA p.44 |
| **30 Sep 2027** | First annual declaration (for 2026) + surrender | QA p.20, p.24 |
| 2028 | Operator-to-operator precursor sharing via Registry | QA p.48 |
| 2028 | Mark-up reaches 30% | QA p.37 |
| 2034 | 100% coverage, no free allocation | Guidance p.21 |

**[HARD]** QA p.22 §3.1: from 2027 declarants must hold **50% of YTD emissions** in certificates each
quarter.

---

## 2. Workbook dossier — `data/cbam_official/default_values.xlsx`

**[OURS]** Both workbooks contain **zero formula cells** (verified with `data_only=False` across every
sheet). Every number is a hard-coded literal — no `None`-formula ambiguity. No hidden sheets, no cell
comments, no defined names.

### 2.1 Structure

**One sheet per country**, not per sector. 122 sheets: `Overview` (disclaimer), `Version History`, 119
country sheets, `_Other Countries and Territorie` (truncated at Excel's 31-char limit). v1, 2026-02-04,
"Default values based on Implementing Regulation (EU) 2025/2621 published on 17 December 2025".

Columns: A CN code · B description · C direct · D indirect · E total · F 2026 (incl. mark-up) · G 2027
· H 2028+ · I production route. Sector header rows carry the mark-up rule in F/G/H. Sector order:
Cement, Fertilisers, Aluminium, Hydrogen, Iron and steel.

### 2.2 Coverage

**[OURS]** 12,532 data rows; minus 873 `see below` heading rows → **11,659 real good-rows**; **267
distinct CN codes / 269 distinct (CN, description) goods**.

| Sector | Goods | Indirect? |
|---|---|---|
| Iron and steel | 205 | **N/A** (6,805 rows N/A; 28 numeric — unexplained exception) |
| Aluminium | 28 | **N/A** (all 1,632 rows) |
| Fertilisers | 27 | numeric (2,416 rows) |
| Cement | 8 (on 6 CN codes) | numeric (337 rows) |
| Hydrogen | 1 | **N/A** (90 rows) |

**Electricity is entirely absent** — no sector, no CN codes, and **no Annex III per-country grid
emission factors anywhere**. (This is why our `GRID_EF` hard-code cannot simply be data-driven from
this file — see §6.)

Sheets are ragged: 4 rows (Equatorial Guinea, Laos, Papua New Guinea, Sierra Leone, Curaçao — 1 data
row each) to 296.

### 2.3 The 33/87 split — the headline finding

**[OURS]** Reproduce with `uv run python scripts/atlas_scan.py`:

```
sheets: 122 · country-like: 120
coverage: 120 scanned · full(>=200)=33 · thin(<50)=58 · with CN731815=33 · without=87
median goods/country: 51.5
```

- **33 sheets carry a CN 7318 15 row** (32 countries + the fallback). **87 carry none at all.**
- **A country listing "–" is not the same as a country omitting the row.** Zero of the 33 are dashed —
  the other 87 have **no row whatsoever**. The fallback is reached by **sheet omission**.
- Coverage is **bimodal**: 58 countries hold <50 goods with a value; only 33 hold ≥200.

**[OURS]** Fallback conservatism:
```python
n = d[d.country != FB].dropna(subset=['dir']); f = d[d.country == FB].dropna(subset=['dir'])
m = n.groupby(['cn','desc']).dir.median().rename('med')
j = f.set_index(['cn','desc']).join(m, how='inner')
(j.dir > j.med).sum(), len(j), (j.dir/j.med).median()   # -> 255, 260, 1.610
```
- Fallback exceeds the listed-country median for **255/260 goods (98.1%)**; median ratio **1.61×**.
- Fallback ≥ max of all listed countries for **4 goods**.
- Anchors: 7318 15 → **4.8012** (median 2.80) · 7213 → 3.995879 (median 2.34) · 7227 → 5.40 (median
  3.50) · hydrogen → 17.74 (median 10.82) · grey clinker → 1.37 (median 1.08, 3rd-highest of 89).

### 2.4 CN 7318 15 — the full ranked table (all 33 rows)

**CN 7318 itself is a `see below` heading row with no value**; the values live on 8-digit subcodes.
min **1.37** · max **8.23** · median **2.80** · **ratio 6.01×**. All route **(C)**, indirect **N/A**.

| Country | Direct | 2026 | 2028+ | | Country | Direct | 2026 | 2028+ |
|---|---|---|---|---|---|---|---|---|
| Philippines | 1.37 | 1.507 | 1.781 | | Mexico | 2.90 | 3.19 | 3.77 |
| Iran | 2.11 | 2.321 | 2.743 | | Algeria | 3.00 | 3.3 | 3.9 |
| Azerbaijan | 2.14 | 2.354 | 2.782 | | Australia | 3.00 | 3.3 | 3.9 |
| Chile | 2.17 | 2.387 | 2.821 | | Ukraine | 3.153 | 3.4683 | 4.0989 |
| Myanmar_Burma | 2.30 | 2.53 | 2.99 | | Uzbekistan | 3.21 | 3.531 | 4.173 |
| Thailand | 2.408 | 2.6488 | 3.1304 | | Russia | 3.21 | 3.531 | 4.173 |
| Serbia | 2.44 | 2.684 | 3.172 | | South Korea | 3.474 | 3.8214 | 4.5162 |
| Argentina | 2.47 | 2.717 | 3.211 | | South Africa | 4.03 | 4.433 | 5.239 |
| Canada | 2.48 | 2.728 | 3.224 | | **_Other (fallback)_** | **4.8012** | **5.28132** | **6.24156** |
| North Macedonia | 2.48 | 2.728 | 3.224 | | Kazakhstan | 5.18 | 5.698 | 6.734 |
| Brazil | 2.56 | 2.816 | 3.328 | | Türkiye | 5.43 | 5.973 | 7.059 |
| United States | 2.58 | 2.838 | 3.354 | | India | 5.72 | 6.292 | 7.436 |
| Colombia | 2.68 | 2.948 | 3.484 | | China | 6.375 | 7.0125 | 8.2875 |
| **Taiwan** | **2.70719** | **2.977909** | **3.519347** | | Indonesia | 8.23 | 9.053 | 10.699 |
| Vietnam | 2.75 | 3.025 | 3.575 | | | | | |
| United Kingdom | 2.77 | 3.047 | 3.601 | | | | | |
| Japan | 2.80 | 3.08 | 3.64 | | | | | |
| Bosnia and Herzegovina | 2.81 | 3.091 | 3.653 | | | | | |
| New Zealand | 2.82 | 3.102 | 3.666 | | | | | |

### 2.5 Spread, and the thesis we tested and rejected

**[OURS]** Workbook-wide (258 goods with ≥5 countries): overall median max/min ratio **4.83×**, p90
**58.79×**.

| Sector | goods | median ratio | max ratio |
|---|---|---|---|
| Cement | 8 | 1.21 | 1.70 |
| Fertilisers | 27 | 3.15 | 4.19 |
| Aluminium | 24 | 6.90 | 9.66 |
| Iron and steel | 198 | **7.12** | **63.15** |

**[OURS] "Developing countries get worse defaults" is FALSE by measurement.** Ranking countries by mean
percentile across goods (≥20 goods each):

- **Most favourable:** Bolivia 0.087 · Tanzania 0.148 · Zambia 0.168 · Zimbabwe 0.171 · Libya 0.173 ·
  Philippines 0.176 · Azerbaijan 0.187
- **Most penalised:** Mozambique 0.986 · India 0.914 · Indonesia 0.897 · Kazakhstan 0.885 · China
  0.866 · South Africa 0.836 · Kyrgyzstan 0.830

Both tails are developing economies. The driver is **production route and grid intensity, not income**.
**🚩 Caveat, flagged not resolved:** the low-percentile group is partly an artifact — Bolivia/Tanzania/
Zambia hold only 24–53 goods (cement + fertiliser, the narrow-spread sectors) while India/China hold
~256 including the wide-spread steel book. **Not a like-for-like league table.**

### 2.6 Precursors — the fastener chain

**CN 7213 (wire rod)** — n=33 · min **0.14** (Azerbaijan) · max **8.23** (Indonesia) · median 2.34 ·
**ratio 58.79×** · fallback 3.995879 · Taiwan 2.297829.
The spread is **route-driven**: the four lowest are all route **(E)** (EAF/scrap) — Azerbaijan 0.14,
Myanmar 0.47, Philippines 0.74, Thailand 1.9195. Uzbekistan is the outlier (route (E), 3.21). North
Macedonia's route cell is **blank**.

**CN 7227** — n=33 · min **2.17 (Taiwan)** · max 10.02 (Indonesia) · median 3.50 · ratio 4.62× ·
fallback 5.40. Compound routes `(C)/(F)` mostly, `(E)/(H)` for Azerbaijan/Philippines/Uzbekistan/
Myanmar/Thailand.

**7207 11 11** — min 0.14 · max 8.23 · median 2.34 · ratio 58.79× · fallback 3.995879.

**🚩 [OURS]** **CN 7213 and CN 7207 11 11 have byte-identical country distributions** — same 33
countries, same values, same ratio. The Commission evidently propagated the semi-finished value
straight onto wire rod.

### 2.7 Mark-up mechanics — and the bug this exposed

**[OURS]** The mark-up applies to **TOTAL**, not direct:
```python
np.isclose(x.d26_n, x.total_n*1.1, rtol=1e-6).mean()   # 1.0000  ← total
np.isclose(x.d26_n, x.direct_n*1.1, rtol=1e-6).mean()  # 0.9966  ← coincidence (steel indirect is N/A)
```
Per sector: Cement / Aluminium / Hydrogen / Iron and steel = **10/20/30%**. **Fertilisers = flat
1%/1%/1%** — verified `d26==d27==d28` at 100%, and **non-compounding** (`d28 == total*1.01³` matches
**0%**). Fertilisers are dramatically privileged: 1% vs 30%.

**This is the source of engine bugs 1 and 2 — see §6.**

### 2.8 Benchmarks workbook (Reg. 2025/2620)

3 sheets, zero formulas. v1, dated **2025-02-06** (🚩 likely a typo for 2026 — it precedes the
default-values file's 2026-02-04 yet cites a Dec 2025 regulation). **Country-independent.** Columns: CN
code (**integer, unspaced**) · description · Column A BMg · Column A route · Column B BMg · Column B
route. 1,804 value rows, **570 distinct CN codes**.

**🚩 Column A vs Column B is never defined in the file.** They differ in **1,765 of 1,804 rows**;
Column A contains 9 zeros, Column B none. The pattern (A ≈ own-process only; B ≈ including precursors —
white portland cement A=0 because all its emissions sit in the clinker precursor) is **strongly
suggestive but unstated**. Flagged, not asserted.

**[OURS] Cross-workbook coverage gap:** benchmarks hold **570** 8-digit CN codes, defaults hold
**172**. **402 CN codes have a benchmark but no default.** **4 CN codes have a default but no
benchmark** — `76151010`, `76151030`, `76151080`, `76152000` (aluminium) — and those same 4 are **the
only goods missing from the fallback sheet**. So for aluminium sanitary ware and cast/foil articles
there is **neither a benchmark nor a fallback default**: a genuine hole in the regime as
machine-readably published.

**[GAP]** **No phase-in factors in either workbook.** The free-allocation phase-in schedule must come
from Reg. 2023/956 Art. 31 / the regulation text. *(This closes an open item in `docs/09` §2.3.)*

---

## 3. Verification economics and capacity

### 3.1 The strongest evidence we have — the Commission's own scoreboard

**[HARD]** European Commission, **"State-of-play CBAM accreditation"** (2-page PDF), linked from the
DG TAXUD CBAM verification page. **Independently re-fetched and parsed 17 Jul 2026 — the totals row
below is verbatim from the file.**

> 🚩 **Sourcing precision:** the PDF itself carries **no visible publication date**. "10 July 2026" is
> the date of the *page linking to it*, not of the document. Internal evidence dates it to July 2026 —
> Austria and France read "No (**July 2026**)" and Hungary "No (**August 2026**)". **Cite it as
> "retrieved 17 Jul 2026", not "dated 10 July 2026".**

| | Agreed to provide CBAM accreditation | **Ready to accept applications** | Agreed to accredit third-country applicants | **Already accepting third-country applications** |
|---|---|---|---|---|
| **Total** | **24** | **11** | **7** | **4** |

The four: **Italy (Accredia) · Netherlands (RvA, "Yes + Agreement with TK's TURKAK") · Poland (PCA) ·
Sweden (Swedac, "Yes + Agreement with UA's NAAU")**. *(All four verified in the file, 17 Jul 2026.)*

Agreed to accredit third countries but **not yet accepting**: France (COFRAC — "No (July 2026)"),
Greece (ESYD), Slovakia (SNAS). Declined CBAM accreditation entirely: **Cyprus, Estonia, Ireland,
Malta**. Ready for domestic applicants but **"No"** to third-country: Germany (DAkkS), Spain (ENAC),
**Belgium (BELAC)**, Finland (FINAS), Denmark (DANAK), Bulgaria (BAS), Luxembourg (ILNAS).

**The Turkey and Ukraine bilaterals are the sharpest form of the thesis: accommodation is possible, so
its absence for Taiwan/India/Brazil/Thailand/Vietnam is a choice.**

**🚩 [HARD] Discrepancy to flag if cited:** European Accreditation's list (**2 Jul 2026**, 8 days
earlier) marks **8** NABs for third-country verifiers **including BELAC (Belgium)** — which the EC
table says **No**. EA's own footnote also warns a NAB "**may offer accreditation in specific third
countries only**", so even "7 or 8" overstates access for any given country. **The real number
available to a Taiwanese verifier could be zero, and nobody has published it.**

### 3.2 Taiwan — the government's own admission

**[HARD]** MOENV (Taiwan), *Major Environmental Policies*, **March 2026**, "MOENV Ready for EU CBAM by
Working with MOEA and Verification Bodies":

> "The MOENV Minister **Peng Chi-Ming** invited the Ministry of Economic Affairs (MOEA) and **20
> domestic greenhouse gas (GHG) emission verification bodies** over a discussion **13 February 2026**…
> **the government and verification bodies will be prepared and lower the cost on verifications**…"

> "However, the EU is yet to release instructions or guidelines detailing executions on verification,
> **nor has any verification body submitted applications**"

> "The MOENV conducted a survey on 20 approved GHG verification bodies in Taiwan… these bodies pointed
> out several major issues, such as **excessively frequent changes of EU regulations, lack of official
> EU-approved training materials, and unclear review procedures and evaluation items**…"

> "A verification body outside the EU will have to submit its application to the National Accreditation
> Bureau (NAB) of an EU member state. **The application procedure is tedious** since documents proving
> the complete technical capability are required with the NAB conducting **onsite field examinations**…"

> "those susceptible to the CBAM are approximately **2,600 steel product manufacturers**, which puts
> Taiwan at the **13th place**… total product weight up to **3.74 million tons**."

Minister Peng: MOENV *"is in partnership with 20 verification bodies and more than 200 verification
specialists."*

**Why this is unbeatable: a government's own publication concedes that domestic capability is not the
constraint (20 bodies, 200+ specialists), that zero had applied, and that the blockers are EU-side.**

**[GAP]** **No Taiwanese verification subsidy exists.** MOENV has stated an *intention* to "lower the
cost". No figure, no budget, no mechanism. Contrast India (§3.4). Date-stamp this claim; it may change.

### 3.3 No group verification — verified across every source

**[HARD]** EC verification page: the verifier's role is to *"visit the installations of a third-country
operator and issue **one verification report per installation**."*
**[HARD]** QA §4.3: installation = *"a stationary technical unit where a production process is carried
out."* Verification attaches to that unit; **no aggregation upward is contemplated anywhere.**
**[HARD]** Grouping in CBAM exists only **within** one installation (QA §4.4–4.5 goods grouping; §4.17
"bubble approach").
**[HARD]** QA §3.4 — the regime is systematically anti-pooling: certificates *"cannot be transferred nor
sold to another person, even if that person is an entity which belongs to same group."*

**There is no FSC/organic/Fairtrade-style group certification analogue in CBAM. This is the strongest
single structural claim available to us.**

### 3.4 India — the thesis happening in the field

**[ESTIMATE — journalism, specific]** Business Standard, *"Indian MSME exporters hit by seizures as
CBAM payment phase begins"*, **28 Jan 2026**:
- First wave of **shipment seizures at European ports** and order cancellations over missing compliance
  reports
- **25,000–30,000 MSMEs** exporting indirectly; **3,000–4,000 direct exporters**
- Levies for most MSMEs **tripled from €70–80 to €240–300/t** because they are pushed onto defaults
- *"Most MSMEs are unable to secure emissions data from dozens of small vendors in their supply chains"*
- No CBAM concession in the EU–India FTA signed 27 Jan 2026

**[ESTIMATE — government-adjacent]** Free Press Journal, **9 Jul 2026**: certification ≈ **Rs 10 lakh
per company** (≈€10,000); government considering reimbursing **up to 90%** of CBAM certification and
verification costs for micro/small steel exporters via **TRACE** under the Export Promotion Mission;
proposal with DGFT, pending. *Journalistic, unnamed officials, scheme not approved.* **But a government
does not design a 90% subsidy for a cost it thinks is trivial.**

### 3.5 Fasteners — independent corroboration of our Taiwan finding

**[HARD]** Jamie McLeod (Crowe UK), *"The new reality of CBAM"*, **Fastener + Fixing Magazine**,
**9 Feb 2026** — at a €90/t carbon price, for heading 7318:
- **Actual data** (~2 tCO2/t): **€50–100/t**
- **Defaults**: Taiwan **€150/t** · Türkiye **€400/t** · China **€500/t**

> "physical site visits will be needed in year one to suppliers, regardless of where they are… every
> supplier producing CBAM goods will need to be verified by a reputable, credible, approved body"

**An independent trade-press source confirms Taiwan's default is mild.** This cuts against a
Taiwan-victim story and *for* the Taiwan-as-lab framing (`docs/14` §4).

### 3.6 Analogues — EU ETS proportionality that CBAM lacks

**[ANALOGUE — strong]** EU ETS excludes installations under **25,000 tCO2e/yr**; **simplified MRV**
under 5,000 t; aviation small emitters may use the Small Emitter Tool and *"submit without further
verification"*, and *"your verifier may decide that a site visit is not necessary."*
**CBAM has no third-country equivalent — the only relief is on the EU importer side (50 t).**

**[HARD, adjacent]** European Commission, *Evaluation of EU ETS MRV administration costs* (2016):
emission reporting and verification account for **over 50% of average total administrative costs**. The
strongest available support for "MRV, not the carbon price, is where the burden sits."

**[ANALOGUE — weak]** UK DECC/AEA report 895 (2009 survey): average annual EU ETS verification cost
**£9,000**. *17 years old, UK-only, domestic verifiers, no long-haul travel.* A floor at best.

### 3.7 The academic gap — our opportunity, honestly stated

**[ACADEMIC]** *"Reforming the European Union's CBAM: Stakeholder perspectives from India, Indonesia,
and Vietnam"*, ScienceDirect (2026), S2772427126000963. **🚩 Returned HTTP 403; extracts from search
results only — obtain the full text before quoting.** Reported:
> "Establishing and operating MRV systems was described as involving substantial fixed costs, including
> data collection systems, third-party verification, and staff training, **which are proportionally
> more burdensome for small- and medium-sized exporters**"
> "Up to 90% of interviewees… highlighted the absence of adequate technical or financial assistance"

**This is the fixed-cost regressivity argument in a peer-reviewed journal. It is our single best
academic citation — and we do not yet hold it.** See §8.7.

**[ACADEMIC]** *"CBAM and Its Implications for Developing Economies: A Systematic Literature Review"*,
Indonesian Journal of Energy (extracts, unverified): *"**The inability to provide verified emissions
data may lead to the application of default values, thereby increasing the effective compliance
burden**"* and *"small exporters… **have been overlooked in much macro-level modeling**."*

**[GAP — the important one]** **No UNCTAD, World Bank, LSE/Grantham, Brookings, WTO or African Union
publication on verification cost or verifier access as the regressive vector.** The institutional
literature is about the carbon **price** and trade flows. **Our specific framing is under-served — that
is the opportunity, but it means we cannot lean on a big-institution citation. We build it from primary
regulation + the Commission's own accreditation table + our own arithmetic.**

### 3.8 The six documented voids

1. **No CBAM verification price exists anywhere** — no verifier is accredited, so no market price exists.
2. **No published count of in-scope non-EU installations.** Not from the Commission, EA, or academia.
   *The EU built a regime requiring physical audit of every installation opting for actual values and
   has apparently not published how many that is.*
3. **No NAB has published a CBAM accreditation fee schedule.**
4. **No group verification provision.**
5. **No Taiwanese verification subsidy.**
6. **No verifier travel-cost data.**

**Framed as absence-of-evidence, this is more damning than any number — and it is unfalsifiable in the
right way.**

### 3.9 Counter-evidence — engage, do not ignore

1. **The 50 t de minimis is real relief** (~182,000 importers, ~90%). *Rebuttal:* relieves **importers,
   not producers**; aggregates per declarant (§1.5).
2. **Year-2+ site-visit waivers explicitly favour SIMPLE installations** — exactly the small plants we
   champion. **This genuinely cuts against us. Concede it and scope the claim to the year-1 cold start.**
3. **Outsourcing (§5.8) can cut travel cost** via local subcontracting.
4. **TAIEX / Global Europe capacity building exists** (COM(2025) 783 Annex 2; €200bn 2028–2034, 30%
   climate target). *Rebuttal:* aimed at candidate/neighbourhood **public administrations**, starts
   **2028**, funds no verification fees.
5. **NL–TURKAK / SE–NAAU prove the system can accommodate third countries.** *Double-edged — use it as
   proof that absence elsewhere is a choice.*
6. **Governments are stepping in** (India's TRACE; Taiwan's stated intent). *Rebuttal:* national
   workarounds for an EU design flaw, available only to exporters whose governments can afford them —
   which is the regressive story one level up.
7. **Taiwan's default is mild** — the injury to a TW fastener SME is €50–100/t, real but not
   existential. **Pre-empt it; it is why Taiwan is the lab.**
8. **[ESTIMATE, unverified]** Reportedly a later enforcement deadline (30 Jun 2027) and "simplified
   declarations for small and micro primary producers" exist. **Not verified in the primary regulation
   — verify before relying on it, and before claiming "no accommodation whatsoever".**

---

## 4. Engine capability inventory

**[OURS]** `uv run pytest` → **25 passed** (17 Jul 2026). CLI: `carbonpass {ingest, pack, costdelta,
schedule, serve}`.

**The computational core is already global.** Verified by running it:

- `rules/defaults.py` — parsed **120/120 country sheets, 12,532 rows, 0 failures, ~12s**. Taiwan alone:
  283 rows, 245 with a direct value. `"Taiwan"` and `"7318"` appear only as **default arguments and
  docstrings** — no logic branches on them.
- `rules/see.py` — **sector-agnostic**. The complex-goods recursion keys off nothing. Ran live, with
  **zero code changes**, on Indian cement (CN 25232900), Chinese aluminium (76041010) and Vietnamese
  urea (31021019).
- `allocation/engine.py` — knows only kW, hours, tonnes. Sector-neutral. Firm A: ±1.06% 1σ from 10k MC
  samples.
- `costdelta/screen.py` — ran on a Chinese aluminium extruder: **€142.56/t ≈ €712,782/yr** vs firm_a's
  €4.03/t. *(Retained as evidence of engine reach; per owner decision, not used as a headline — see
  `docs/14` §1.)*
- `writer/fill.py` — structurally general; the whole cell contract is `schema/cbam_template_map.yaml`.

**Genuinely Taiwan-specific — and correctly so, because this is the moat:** the VLM prompts (Taipower
bill, 電子發票, 民國 year), the e-invoice regexes, `FUEL_CONSTANTS` (natural gas only), the wire-rod-only
precursor mapping, the Taipower TOU table, `FLEXIBLE_PAT` (熱處理/furnace/compressor), and the grid feed.

**Provable today, no new data, no new code:**

1. One engine, **120 countries, 5 sectors, 12,532 default rows**, 0 failures.
2. The Commission's own worked example reproduced at **rel 1e-9** (`tests/golden/`).
3. SEE computed for cement, aluminium and fertiliser across countries — **⚠️ but see §6 bugs 1–2**.
4. **qwen3-vl 4B: 336/336 (100%)** across six phone-photo degradations, **18–31 s/doc**, ±docling
   (`out/bakeoff/`) — matches the 8B and runs *faster*. InternVL3.5-8B: 66%.
5. Numeric backstop catches misread/transposition/hallucination — **3/3 injected errors**, pinned.
6. Uncertainty per line: ±1.06% 1σ.
7. An EPD flips default share **95.1% → 0%** (firm_a vs firm_c) — both artifacts on disk.
8. The real 19-sheet Commission workbook filled without touching a formula (910 KB + 53-cell sidecar);
   SEE cells independently recompute in LibreOffice to the sidecar at ~1e-11.
9. **[OURS, new]** The atlas scan and the "same factory, moved" table — `scripts/atlas_scan.py`.

**Untapped assets sitting in the repo:** 6 of the 7 Commission example workbooks
(`data/cbam_official/template_examples/`) are **unused** — cement, blast furnace, EAF alloys,
fertiliser, aluminium, hydrogen. `data/ef/moenv_coefficients.json` (1,164 rows, 1,062 distinct names,
2013–2025) is held but **wired into nothing** (`rules/ef.py` is dead code) — and it contains
**螺絲(含球化與表面皮膜處理及電鍍) = 3.41 kgCO2e/kg**, i.e. **Taiwan's own government publishes a fastener
footprint of 3.41 tCO2e/t** against the CBAM Taiwan default of 2.707 and our computed firm_a 2.924.

---

## 5. KILL-LIST ADDITIONS

*Extends `docs/00` §4 and `docs/12` §4. **Never reuse these.***

| # | Dead claim | Where it lives | Why it is dead |
|---|---|---|---|
| **1** | **"For complex goods, ≥80% must be actual data, verified by an accredited third party"** | `docs/09` §2.3, §3.1; `docs/10` §2; submission PDF | **In no document.** "80%" never appears in that rule. The real rule is a **transitional** cap on *estimations* at 20% (guidance p.158), from **repealed** Reg. 2023/1773. The live QA says the opposite: defaults are usable for **all types** of goods (p.36) and for 100% of a complex good (p.39). **Probable origin: the unrelated scrap-yield example at guidance p.57 ("100 t precursor for 80 t of final product").** |
| **2** | **"Defaults are capped at 20% of reported embedded emissions for complex goods"** | same | Transitional-period operator-monitoring rule under repealed 2023/1773. The 2026 Q&A **never mentions any 20% limit**. Whether an equivalent survives in **IR 2025/2547 Annex III** is **unanswerable from this repo** — see §8.1. Until then: **do not assert it in either direction.** |
| **3** | **"5% variance threshold"** | `docs/10` §2A | Appears in **no** source document. **No numeric materiality threshold exists** in the corpus; the standard is qualitative ("free from material misstatement"). |
| **4** | **"€450–750/t default" / "30–50% of product value"** | 🔴 **submission PDF — Executive Summary, Figure 1, Table 5** | Already killed for Taiwan in `docs/09` Rev. 2, but **the submission-facing artifact still contradicts our own analysis**. **Hard blocker for 31 Jul.** *(Note the irony the atlas surfaced: €397–681/t is roughly right — for the **fallback**, India and Indonesia. The folklore described the unlisted and the dirty, never Taiwan.)* |
| **5** | **Citing `guidance_installations_outside_eu_EN/ZH.pdf` as a rule source** | `docs/10` §3 (C8) | Dated **8 Dec 2023** · explicitly **"not legally binding"** · scoped to a period that ended **31 Dec 2025** · built on **repealed** Reg. 2023/1773 · carries a de-minimis rule (**€150/consignment**, p.227) that flatly contradicts the live **50 t** rule. **Keep it for mechanics and worked examples only; re-validate every rule against 2025/2547.** |
| **6** | **"403 accredited verifiers"** | not yet ours — **pre-empt** | Those are **EU ETS** verifiers (the authors say so in their own footnote). The actual CBAM count is **zero**. An expert catches this instantly. |
| **7** | **"Verification costs €5,000–50,000 per installation"** | not yet ours — **pre-empt** | Traces to **one anonymous commercial lead-gen site** citing unnamed "market data as of April 2026" — no publisher, no author, no method. Its apparent corroboration is **circular re-quotation**. |
| **8** | **"Developing countries get worse defaults"** | tempting — **never adopt** | **False by measurement** (§2.5). Both tails are developing economies. |
| **9** | **UNCTAD's "$5.9bn / $10.2bn / 1.4–2.4%"** | not yet ours — **pre-empt** | Unverified in the primary document; models a **2021** policy design materially changed since. Heavily recycled, which is exactly why it is dangerous. |
| **10** | **"ISO 14067 preparation" as a CBAM by-product** | `docs/09` §3.1, §5.3 | **QA §4.24: LCA/life-cycle-inventory emission factors are NOT accepted for CBAM.** The cluster's existing ISO 14067 certs (Chan Chin C., Fang Sheng) may not be CBAM-usable. The "one ingestion, many artifacts" claim survives only if restated carefully. |

---

## 6. Engine defects — recorded, fix in a later pass

*Per owner decision (17 Jul): document now, fix later. **All are invisible today because every test and
every corpus firm is CN 7318**, where indirect is N/A so direct == total.*

| # | Defect | Detail | Size |
|---|---|---|---|
| **1** | **Mark-up basis is TOTAL, not direct** | The workbook's marked-up column matches `total × 1.1` at **100%** (§2.7). `rules/see.py:124-125` assigns it to `psd` (direct) and sets `psi = 0.0` → **cement/fertiliser fold indirect into direct SEE**. Our India cement run returned 1.551 = `total 1.41 × 1.10`, not `direct 1.35 × 1.10 = 1.485`. | ~10 lines: add `for_year_direct()` |
| **2** | **`markup_for_year()` hard-codes 10/20/30** | **Fertilisers carry a flat 1%** in every year. `see.py:127-128` prints `"CBAM default CN 28141000 (Vietnam) 3.46 +10% mark-up = 3.6461"` — but 3.46 × 1.10 = 3.806. **The provenance note prints arithmetic that does not add up. A verifier would catch this.** `costdelta` reports the same wrong `markup` field. | ~5 lines: derive from the row |
| **3** | **Grid EF is Taiwan's, unconditionally** | `GRID_EF_KGCO2_PER_KWH = 0.474` (`config.py:41`) applied in `pack.py:99` **regardless of `installation.country`**. Blocks any non-TW indirect claim. **Note: the default-values workbook contains no per-country grid EFs** (§2.2) — this needs genuinely new data. | New data required |
| **4** | **`rules/ef.py` is dead code** | MOENV lookup referenced only by one test, wired into nothing. The 1,164-row table is held but unused. | Wiring |
| **5** | **Writer is steel-labelled** | Three hard-coded `"Iron or steel products"` strings (`writer/fill.py:92,97,104`) are the **only** blocker to filling the template for cement/alu/fertiliser. | ~1 line + sector→label map |
| **6** | **No non-steel golden test** | 6 of 7 Commission example workbooks unused. **Transcribing one would have caught defects 1 and 2.** | Sprint task |
| **7** | **Certificate price is two hard-coded quarters** | `config.py:38` `{"2026Q1": 75.36, "2026Q2": 75.28}`; takes the max key. Stale by design; re-verify quarterly. | Small |
| **8** | ✅ **FIXED 17 Jul — stainless precursor mapped to the wrong CN (2.16× understatement)** | `ingestion/pipeline.py::_precursor_cn()` returned **`"7227"`** for stainless. CN 7227 is *"Bars and rods of **alloy steel other than stainless**"* — **Taiwan 2.17, the lowest value assigned to ANY country (percentile 0.00)** — so a stainless screw came out *cleaner than a carbon one*. The precursor a fastener plant actually buys is **CN 7221** (*"bars and rods of stainless steel, hot-rolled, in irregularly wound coils"* — the stainless twin of CN 7213; **not** 7223, which is drawn *wire*: plants buy rod and draw it in-house). **Taiwan has no CN 7221 value at all** → Annex I fallback 4.82 → **5.302** in 2026. firm_b stainless SEE **2.774 → 6.003**. **Fix:** 7227→7221 + `defaults.resolve()` (defect 12) + corpus/ground-truth regen + 2 pinning tests. 27/27 green. | Done |
| **11** | 🔴 **Ground truth is computed from exact totals the documents do not carry** | `make_mock_corpus.py` computes `ground_truth.json` from intended annual totals (4200 / 1300 / 1800 t) while the production logs it writes carry **rounded monthly rows summing to 4199.9 / 1300.1 / 1799.8** (gas likewise: 200.001 / 329.999 / 117.998 vs 200 / 330 / 118). So engine-vs-ground-truth drifts **rel 7.5e-5 (firm_b), 1.1e-4 (firm_c)**. firm_a's rows happen to sum exactly (rel 2.5e-7) — **which is why firm_a was the only firm that ever reconciled**, and why `docs/12` §6 item 4 ("run firms B & C e2e") was still open. **Ground truth is not a golden for firm_b/c until fixed.** Fix: derive ground truth from the rows actually emitted. | Small; unblocks golden-testing B/C |
| **12** | ✅ **ADDED 17 Jul — the engine had no country-fallback rule** | `defaults.lookup()` returned `None` when a country has no row for a good, and `see.py` **raised**. But Q&A p.37 §4.25 requires the *"Other countries and territories"* table in exactly that case. New `defaults.resolve(cn, country) -> (dv, used_fallback)` implements it and `see.py` records the fallback in the provenance note + `needs_attention`. This is not hypothetical: **of the 33 full-book countries, only Taiwan, Thailand and Vietnam lack CN 7221** — Taiwan's row reads "see below" with nothing below it. | Done |
| **9** | ⚠️ **`markup_for_year()` returns a FRACTION (0.10), not a multiplier (1.10)** | Not a bug in the engine — `costdelta` renders it as `{markup:.0%}` correctly — but it is a **loaded footgun** for any new caller. It cost us a 10× error while writing `scripts/waste_scan.py`. Prefer `DefaultValue.for_year()` (the workbook's own marked-up column) over applying the mark-up by hand. | Doc/naming |
| **10** | ⚠️ **`defaults.lookup()` fails silently on a query SHORTER than the stored row** | It is a longest-**prefix** match (`cn.startswith(row.cn_code)`), so `lookup("7223")` returns **None** even though row `"722300"` exists with a value; `lookup("722300")` works. Any caller passing a 4-digit code for a good stored at 6+ digits gets a silent `None` → a skipped precursor. | Guard or fuzzy fallback |

**Consequence, enforced in `docs/14`:** publish **steel and aluminium only** until defects 1–2 are
fixed. Every figure in `docs/14` respects this.

---

## 7. Defects in the Commission's own files — the atlas give-back payload

**[OURS]** These are the reason the Provability Atlas is a genuine public good rather than a
re-publication, and they answer the application form's "suggestions for modifying open data".

1. **🚩 Five cement rows use a compounding mark-up contradicting their own sheet headers.**
   332 of 337 cement rows use the declared flat 1.2 / 1.3. Five use **1.1² = 1.21 and 1.1³ = 1.331** —
   **Angola** (grey clinker, grey Portland cement, grey hydraulic cements) and **Argentina** (grey
   clinker, grey Portland cement). Angola grey clinker: total 1.26 → file gives 1.5246 / 1.67706; the
   flat rule gives 1.512 / 1.638 — a **~2.4% overstatement in 2028**. *(Angola and Argentina are also
   the two sheets with anomalous column counts — likely the same hand-edited provenance.)* **Flagged as
   a probable defect, not resolved.**
2. **Four aluminium goods have neither a benchmark nor a fallback default** — `76151010`, `76151030`,
   `76151080`, `76152000`. A genuine hole in the regime as machine-readably published.
3. **CN code formatting is inconsistent and will silently break joins.** 22 codes are stored
   **unspaced** while the rest use `NNNN NN NN` — the **entire aluminium block** plus `28141000`,
   `28142000`. One code, `761090`, is 6-digit. **Any naive string join on CN drops the aluminium
   sector without error.**
4. **Three different dash characters** encode "no value": en-dash `–` (699), underscore `_` (26),
   hyphen `-` (2). Any `== '–'` test misses 28 cells.
5. **873 `see below` heading rows** across 27 four-digit (and two six-digit) parents inflate the
   catalogue 269 → 287 if treated as goods.
6. **CN 7213 ≡ CN 7207 11 11**, byte-identical across all 33 countries — semi-finished propagated onto
   wire rod.
6b. **🚩 CN 7221 (stainless wire rod) is missing for Taiwan, Thailand and Vietnam** — the only three of
   the 33 full-book countries without it, and all three are fastener exporters. Their 7221 row reads
   **`see below` with no sub-rows beneath it**, while the other 30 countries carry the value on the
   bare 4-digit row (China 5.59, India 6.48, Indonesia 8.69, Korea 3.65…). The benchmarks workbook
   *does* carry 7221 (`72210010`/`72210090`, colB 1.225), so the good exists in the regime — the
   defaults sheet just has a hole. Consequence: every Taiwanese stainless fastener resolves to the
   Annex I fallback (4.82). **✅ Verified against the legal text (20 Jul, §8.1 Gate B): Taiwan's
   row in the published OJ reads `see below … #VALUE! #VALUE! #VALUE!` — a demonstrated publishing
   defect, in law.**
7. **Mali hydrogen = 0.00** exactly, across all mark-up years, against a 10.82 median. Sentinel or gap —
   **not determinable from the file**.
8. **Benchmarks version date 2025-02-06** — likely a typo for 2026.
9. **Production route codes (A)–(H)** in defaults and **(A)–(J) + (1)/(2) compounds** in benchmarks are
   **never defined in either workbook**. They are the single strongest explanator of the spread (§2.5–2.6).
   **Decoding them against the guidance PDF is the most valuable unexploited step available.**
10. **Benchmarks Column A vs Column B is never defined** (§2.8).
11. **`total ≠ direct + indirect` in 711 of 10,931 rows** — but max residual is exactly **0.010** and
    none exceed 0.011. **This is 2-dp rounding of the total column, NOT an error.** State it as such;
    it is the kind of thing a careless reader would report as a scandal.

---

## 8. Unresolved — must verify before the submission

### 8.1 Legal-text gate verdicts (20 Jul 2026 — read from the PDFs in `data/cbam_official/legal/`, grep-able `.txt` beside each)

**Gate A — IR 2025/2547 estimation cap: ✅ RESOLVED — NO CAP EXISTS.** Kill-list #2 closed in the
"no cap" direction. Evidence from the act itself (OJ L, 22.12.2025):
- **Annex II A.1.2** (txt line 1187): *"An operator can either determine actual values of embedded
  emissions, or make use of the default values made available in accordance with Annex IV of
  Regulation (EU) 2023/956, **or combine actual values and default values**."* — no percentage limit.
- **Recital 29**: flexibility to combine "actual values for the emissions of the production
  processes … with the use of default values for other precursors" — again uncapped.
- **Annex II A.3.1(a)**: where a monitoring method is technically not feasible or incurs
  unreasonable costs, default values *"shall be used"* — defaults are the prescribed fallback, not
  a rationed concession.
- **Annex III** ("Rules for attributing emissions to goods", txt lines 2853–3446) contains **no
  estimation/default/percentage language at all** — grep for `estimat|default value|per cent`
  returns nothing inside it.
- The only obligation attached to default-value use is **disclosure**: Annex IV (emissions-report
  template) requires reporting *"the share of embedded emissions for which default values were
  used"* (txt lines 3509, 3625). Reported, not capped.
- **Bonus (the yield lever's legal basis, now in legal form):** Annex III §F "Monitoring of
  activity levels" (txt line 2634): activity level = *"total mass of the goods **leaving** the
  production process"*; *"Off-spec products, by-products, waste, and scrap … **shall not be
  included** in the determination of the activity level."* — scrap reduces AL, so its embodied
  emissions sit inside the declared SEE of shipped goods. Cite as **IR 2025/2547 Annex III §F**
  (stronger than Q&A §4.11).
- Also settles §8.2: **record retention = six years** (Annex II A.1.4-adjacent, txt line 1244:
  "kept at the installation … for at least six years after the reporting period").

**Gate B — IR 2025/2621 Annex I at CN 7221: ✅ CONFIRMED, and better than claimed.** The
TW/TH/VN hole is in the **published legal text**, not just the workbook (OJ L, 31.12.2025):
- **Taiwan** (txt line 56210): the CN 7221 row reads literally
  `see below N/A see below #VALUE! #VALUE! #VALUE!` — **unresolved Excel error artifacts in the
  Official Journal**. This upgrades "probably a publishing defect" (§7.6b) to **demonstrated**: a
  formula referencing a value that was never filled in survived into law.
- **Thailand** (txt ~57926) and **Vietnam** (txt ~69164): CN 7221 rows are all dashes `– – – – – –`.
- **The fallback rule is legal text, not just Q&A** (txt line 118, Annex I preamble): *"Where a
  country or territory is explicitly listed but no value is provided or the relevant field shows
  '–', the default value for the respective good from the table 'Other countries and territories'
  needs to be selected."* — confirms `defaults.resolve()` exactly.
- **'Other countries and territories' CN 7221 = 4,820 → 5,302 (2026)** (txt line 71806) —
  byte-matches the workbook and the engine's fallback. The "hole in the book" line and the
  stainless-fallback logic **stand as written**; cite the `#VALUE!` rows as primary evidence.

### 8.2 Still unresolved

1. ~~IR 2025/2547 is not in this repo~~ **Resolved — see §8.1 Gate A.**
2. ~~Record-retention period~~ **Resolved — six years** (IR 2025/2547 Annex II, see §8.1 Gate A).
3. **Numeric materiality threshold** — absent. **Do not invent one.**
4. **EC vs EA discrepancy** on BELAC/Belgium (§3.1) — flag whenever either list is cited.
5. **"France warns of verifier shortage"** — blog → newsletter → unnamed authority. Chase the primary
   (DGEC / Douanes françaises) or attribute precisely as third-hand.
6. **UNCTAD figures** — verify page-level in UNCTAD/OSG/INF/2021/2 or drop (kill-list #9).
7. **🔴 The India/Indonesia/Vietnam stakeholder paper** (ScienceDirect S2772427126000963) returned HTTP
   **403**. Its fixed-cost quote is **our single best academic citation** and we do not hold it.
   **Obtain the full text and the exact page.**
8. **TIFI / MIRDC positions** — no evidence found either way. **Do not assert from silence.** One
   possible lead: *"TIFI Chairman: Industry Turns Focus to Net Zero"*, Fastener World FW_201_E_124.pdf
   (unopened).
9. **Certificate price** — re-verify quarterly (defect §6.7).
10. **Number of in-scope non-EU installations** — **no published figure exists**. Do not invent one;
    **make the absence the point** (§3.8).
11. **The "simplified declarations for small and micro primary producers" / 30 Jun 2027 deadline**
    (§3.9 item 8) — unverified in the primary regulation. **Verify before claiming "no accommodation
    whatsoever" anywhere.**
12. **Fong Prean** single-firm CBAM case study (*Fastener + Fixing*) — potentially useful, unopened.
