# CLAIM VERIFICATION REGISTER — full external audit of the submission proposal

**Date:** 18 Jul 2026 · **Method:** three parallel research agents verified every load-bearing claim
against official sources (DG TAXUD, EUR-Lex, MOENV, MOEA, Taipower, data.gov.tw, industry data),
plus an internal consistency check against this repo's primary files. **All corrections below are
applied in the submission PDF (Rev 5) and `docs/17_final_proposal_source.tex`.**

Verdicts: ✅ CONFIRMED · 🟡 PARTLY TRUE → corrected · 🔴 WRONG/UNSUPPORTABLE → replaced or dropped.

---

## 1. EU / CBAM regulatory claims

| Claim | Verdict | Finding & action |
|---|---|---|
| Definitive regime from 1 Jan 2026; importers buy certificates | 🟡 | Obligation accrues from 2026, but certificate **sales only open Feb 2027** on the common central platform. **Fixed:** proposal now says "2026 imports accrue a certificate obligation… sales open February 2027; first declaration and surrender 30 September 2027." |
| Certificate prices €75.36 (Q1) / €75.28 (Q2 2026) | ✅ | Official Commission publications (7 Apr / 6 Jul 2026). **Q3 2026 not yet published** (due 5 Oct 2026) — never quote one. |
| First surrender September 2027 | ✅ | Confirmed **30 Sep 2027** (DG TAXUD, 23 Jun 2026); Omnibus did not move it. Date precision added. |
| CN 7318 in scope from the start | ✅ | Annex I, Reg. 2023/956. |
| Country-specific defaults, mark-ups 10/20/30% | ✅ | IR (EU) 2025/2621. (Fertilisers ~1% — not used by us.) |
| Fallback = average of 10 dirtiest exporters | ✅ | Reg. recital + Commission Q&A. |
| Iron & steel: only DIRECT emissions certificated; electricity (indirect) recorded but not charged | ✅ | Confirmed. Proposal already states the scheduler's carbon lies **outside the certificate scope for steel** — the exact nuance the owner flagged; wording double-checked everywhere (benefits table, Sight 3, lever 4). |
| Mass counted "before cutting" → scrap inside declared SEE | ✅ | IR 2025/2547 mass-balance methodology confirms the substance. |
| 50 t de minimis; ~90% importers exempt / ~99% emissions kept | ✅ | Reg. (EU) 2025/2083. |
| Zero verifiers accredited; **only 4 NABs accept third-country applicants** | 🔴 → corrected | Zero-accredited ✅ and first accreditations ~Sept 2026 ✅. But the EA directory (2 Jul 2026) lists **8 NABs** accepting third-country applications (BE, FR, GR, IT, NL, PL, SK, SE). **Fixed: "eight (up from four earlier in the year)" — and Sept-2026 accreditations land inside the mentorship window (a timing gain, not a loss).** |
| Downstream extension: ~180 categories, obligations 2028, EP plenary Sept 2026 | ✅ | Council general approach 12 Jun 2026; ENVI committee vote 6 Jul 2026; plenary Sept 2026. Committee stage added to the proposal. |
| DPP registry from Jul 2026; batteries 2027 | 🟡 | Registry: ESPR Art. 13, by 19 Jul 2026 ✅. Battery passport 18 Feb 2027 — legally under the **Batteries Regulation**, not ESPR (wording kept generic). |
| "a 2,400-page regulation" | 🔴 → replaced | No official page count exists. **Replaced with:** "a rulebook that now spans eleven legislative acts and their annexes" (Dec 2025 package = 11 acts + 13 supplementary docs — verifiable). |
| One report per installation; year-1 physical site visit; no group verification | ✅ | DG TAXUD + DR (EU) 2025/2551. |
| Benchmarks 1.364 / 1.154 tCO₂e/t (CN 7318 carbon/stainless) | ✅ (internally) | Agent couldn't find them online; **byte-verified in the official Reg. 2025/2620 benchmarks workbook in-repo** (73181100→1.364 (C); 73181210→1.154 (1)). Not quoted in the proposal anyway. |

## 2. Taiwan claims

| Claim | Verdict | Finding & action |
|---|---|---|
| 3.74 Mt shipped; 13th-largest; ~2,600 SMEs | ✅ | Taipei Times 2 Mar 2026 + MOENV release 13 Feb 2026. |
| "Top-3 fastener exporter" | 🟡 → corrected | True **by volume**; **#4 by value** (2023: US$4.594 bn, behind CN/DE/US). **Fixed in Table 1: "Top-3 by volume; #4 by value (2023)".** |
| ~1,800 manufacturers / ~700 TIFI / ~1.2 Mt (2025) / ~13% world production / ~¼ to Europe | ✅ | Confirmed ("¼ to Europe" a fair approximation; Taiwan = 2nd-largest EU supplier at 21.1% of EU market). |
| Grid EF 0.474 (2024) | 🔴 → superseded | **2025 factor published 2 Jun 2026: 0.467 overall, 0.466 industrial** (first-ever split). **Fixed in data table + refs; engine todo: update `GRID_EF` and prefer the industrial figure.** |
| Taipower #8931 / #37331 open datasets | ✅ | Confirmed (deep archive may require request). |
| TOU summer rates 9.39 / 5.85 / 2.53 NT$/kWh | ✅ | **Exact match** to the current high-voltage 3-tier schedule (effective 1 Oct 2025; unchanged in Apr 2026 review). The old "stylized table" caveat is retired — scheduler numbers on firm ground. |
| MOENV CBAM platform (Mar 2026), informational | ✅ | Confirmed (joint MOENV+MOEA; live by Apr 2026). |
| 20 verification bodies / 200+ specialists / zero EU applications | ✅ (nuance) | MOENV 13 Feb 2026. Nuance now reflected: bodies hadn't applied because the **EU had not yet opened applications** — the gate, not the will. |
| SME structure 51.8% family / 58.2% >8 yrs | 🔴 → dropped | Not found in accessible official summaries of the 2025 White Paper. **Replaced with confirmed figures (1.715 M SMEs, >98% of firms).** |
| Scrap NT$8–15/kg; CFR ~US$345/t; wire rod ~NT$24.5k/t; 40% recovery | 🟡 → corrected | CFR Taiwan ~**US$325/t** (15 Jul); wire rod ~**NT$27,350/t** (Apr 2026, rising); realistic factory scrap ~NT$8–10/kg. **Recovery corrected to ~30–40% → net loss = 60–70% of gross** (Firm A net ≈ NT$4.4–5.1M — the stated NT$4–5M stands). Stainless recovery ratio similar (~35–45%), absolute value 3–4×. |
| Net-zero 2050 law; 25,000 t fee threshold to fall | 🟡 | Law + threshold ✅; "set to fall" softened — official language is "phased adjustments," no number announced. |

## 3. Industry / technical claims

| Claim | Verdict | Finding & action |
|---|---|---|
| Cold forming 85–95% utilization | ✅ | Multiple industry sources. (Machining comparator is actually 25–35% utilization — our old "50–70%" was too *generous*; comparator simplified out.) |
| Whole-chain loss band 5–15% | 🟡 kept w/ caveat | Defensible synthesis; no single published plant figure. Stated as "documented industry band," pilot calibrates — already the proposal's framing. |
| ">50% of factories on paper/spreadsheets" | 🟡 → precise | Actual stat: **54% of SMALL/MID-SIZED plants** use pen+paper/spreadsheets as their MES; 8% commercial MES (IoT Analytics, Dec 2025). **Fixed with exact attribution — and it's stronger for us: the stat is about exactly our population.** |
| "5–8% of revenue lost" (Symestic) | 🔴 → replaced | Vendor marketing, weakly sourced. **Replaced with ASQ cost-of-poor-quality: 10–20% of revenue; APQC scrap+rework ~2.2% median** — better sourced AND a bigger number. |
| Heat treatment + plating = dominant electricity loads | ✅ (directional) | Confirmed by engineering sources; stated without a hard percentage. |
| Fasteners ~2–2.5 tCO₂e/t; Commission example 2.41 | ✅ | Order of magnitude independently supported. Agent flagged "2.41 = Thailand default" — **misattribution: the 2.41 figure is from the Commission's own filled example workbook "CBAM SEE V2.1 Example Steel 3 Screws and nuts", present in-repo and golden-tested at 1e-9.** Claim stands as written. |
| Stainless rod 3–4× carbon rod price | ✅ | Market data 2.3–4.3×; ours 3.86×. |
| qwen3-VL 4B exists, runs on laptop | ✅ | Official Ollama library; 8–16 GB RAM. |
| Scrap sold & remelted; owners know aggregate tonnage | ✅ | Standard practice — confirming the Rev-4 reframe ("pile visible, information invisible"). |

## 4. New gains surfaced by the audit (not just corrections)

1. **The paper/spreadsheet stat is *about our exact population*** — 54% of SME plants, not "factories in general." The inclusion framing sharpened for free.
2. **Cost-of-poor-quality is 10–20% of revenue (ASQ)** — a bigger, better-sourced number than the vendor 5–8% we dropped.
3. **Verifier accreditation lands ~Sept 2026, inside the mentorship window, with 8 doors now open** — the "gateway" is opening exactly while we'd be piloting; turned from an error into a timing argument.
4. **Taiwan's grid EF fell 0.474 → 0.467 (industrial 0.466)** and now has an industrial split — evidence both that the grid is cleaning and that compliance numbers *move*, which is the argument for a living tool over a one-off consultant PDF.
5. **TOU tariffs verified exact** — scheduler savings now rest on the real current schedule.
6. **EP committee stage passed (6 Jul)** — the Sept plenary "natural experiment" is on track.
7. **Steel prices rising (wire rod ~NT$27.3k)** — every waste figure quoted at NT$24.5k is, if anything, conservative at current prices.

## 5. Standing rules (extends docs/15 §5 and docs/18 §2)

- Never quote a Q3-2026 certificate price (doesn't exist until 5 Oct 2026).
- Never say "2,400 pages"; say "eleven legislative acts and annexes."
- Never say importers "buy certificates in 2026"; obligation accrues 2026, sales Feb 2027, surrender 30 Sep 2027.
- Always "top-3 by volume; #4 by value."
- Always grid EF 0.467/0.466 (2025) — 0.474 is history.
- Always "54% of SME plants (IoT Analytics)" and "10–20% of revenue (ASQ COPQ)."
- Always scrap recovery "~30–40% at current prices"; net = 60–70% of gross.
- "Eight NABs accept third-country verifier applications (EA, 2 Jul 2026)" — re-check before finals; it is rising.
