# CarbonPass — Closing the Carbon Data Divide for Taiwan's Export SMEs

### Master Proposal Document — 2026 Presidential Hackathon International Track ("Digital Inclusion in the AI Era")

*This document is the single consolidated proposal. It supersedes files 1–7 in this project folder: all verified facts, adjudicated conflicts (Claude audit × Gemini audit), handbook-fit analysis, and technical planning are integrated here. Every load-bearing figure is cited with source and date in the References section; claims that are estimates or pending legislation are marked as such in the text.*

*Rev. 2 — 17 Jul 2026. The default-value economics (§2.3, §3.1, §5.2, §8, §9) have been rebuilt from the **adopted** Commission files — the default-values workbook "DVs as adopted v20260204" (machine-readable Reg. 2025/2621) and the CBAM benchmarks workbook (Reg. 2025/2620) — parsed and unit-tested by our own working pipeline [32][33]. The earlier industry-estimate figures (€450–750/t; "30–50% of product value") turn out to describe high-intensity origins such as China and India, **not Taiwan**, whose adopted default is among the lowest in the world. That correction reshapes the pitch (§3.1) and is itself evidence of what the tool does: it reads the regulation so the owner doesn't have to.*

---

## Executive Summary

On 1 January 2026, the European Union began charging real money for the carbon embedded in imported steel goods. Taiwan — the world's top-three fastener exporter — shipped 3.74 million tonnes of CBAM-covered goods to the EU during the mechanism's transitional period, most of it screws, fasteners, and steel produced by roughly 2,600 small and medium enterprises concentrated in the Gangshan–Luzhu district of Kaohsiung [1]. These are archetypal Taiwanese "hidden champions": family-run, hardware-brilliant, digitally under-resourced. From this year, every one of them faces a choice made in Brussels: deliver verified, installation-level, per-product carbon data to their EU buyers, or leave the buyer on country-specific "default values" that are marked up 10% this year and 30% from 2028 [8][32]. Our own parse of the adopted default-value tables (§3.1) shows Brussels has, in effect, handed Taiwan a legislated price advantage — a Taiwanese screw with no data costs its buyer €224/t in certificates; the same screw from China costs €528/t — an advantage that is only bankable, and only grows, for the factory that can *prove* its numbers. The data demand, meanwhile, is unconditional: the EU declarant must file per-product embedded-emissions figures from 2026 regardless, and for complex goods like fasteners at least 80% of a reported actual calculation must be verified data [8].

No tool in Taiwan's current ecosystem produces that data. The government's CAAS portal teaches courses; the MOEA's calculator estimates a rough annual total; the MOENV's new CBAM platform (launched March 2026) answers questions; the Taipower app draws consumption charts; TRE100 records pledges [1][19][20][21][22]. Between "awareness" and "compliance" sits an empty space that today is filled only by consultants, priced per engagement, per product, per year — an economics that works for a corporation and fails for a 12-person screw factory.

**CarbonPass** fills that space. It is a local-first AI system that turns what a factory already has — Taipower electricity bills, material invoices, production records — into the exact artifact its EU customer needs: a verifier-ready, per-product (CN-code-level) embedded-emissions data pack in the European Commission's own format, with a live comparison of what the buyer pays with the factory's data versus without it. Its second layer then uses Taiwan's open 10-minute grid data and time-of-use tariffs to schedule the factory's flexible loads — furnaces, compressors, plating lines — so the electricity bill falls now and the next data pack is measurably cleaner. Its front end is not a dashboard but a conversation, in Mandarin and Taiwanese, inside LINE: the 60-year-old factory owner photographs a bill and gets an answer. That is digital inclusion in the AI era, applied where Taiwan's economy actually bleeds.

The proposal is engineered for what the Presidential Hackathon actually is — a policy-adoption pipeline, not a product launch. We bring a working proof of concept built entirely on open data by the July 31 submission; we use the mentorship phase for one real pilot factory in Gangshan; and we present measured results at finals in late October — by which time the European Parliament will have voted on extending CBAM to ~180 further steel and aluminium product categories, a decision that either triples our addressable market or leaves it at 2,600 firms, and which we track as a live element of the roadmap [10].

---

## 1. The Setting: Taiwan's SME Economy and the Kingdom of Screws

### 1.1 The SME backbone — and why the usual number misleads

Taiwan's economy rests on 1.716 million small and medium enterprises — 98.87% of all registered businesses, employing 9.19 million people, or 79.3% of the national workforce [11]. That figure is often quoted to dramatize the carbon-compliance problem ("1.71 million SMEs must decarbonize"), and this proposal explicitly declines to use it that way: the overwhelming majority of those firms are shops, restaurants, and services facing no carbon obligation of any kind. Honesty about the denominator is what makes the real story credible — because the real story is about concentration, not breadth. Taiwan's SMEs contribute only about 10.3% of national export value directly [11]; but in a handful of industrial clusters, SMEs *are* the export industry. Nowhere is that truer than in fasteners.

### 1.2 The fastener cluster: small firms, world market

The screw and fastener industry, centred on the Gangshan and Luzhu districts of Kaohsiung — locally, the "Kingdom of Screws" — comprises roughly **1,800 manufacturers**, the majority of them SMEs, with about 700 organized under the Taiwan Industrial Fasteners Institute (TIFI) [17][12]. The sector's standing is global:

| Indicator | Value | Source, date |
|---|---|---|
| Global rank | Top-3 exporter worldwide (#2 by value in 2023 reporting; #3 by volume in 2025–26 reporting) | CommonWealth (2023); Kaohsiung Times (2026) [12][14] |
| Share of global production | ~10–13% | Kaohsiung Times (2026); PRNewswire (2024) [12][17] |
| Export volume | ~1.2 million tonnes (2025); ~936k tonnes in Jan–Sep 2024 | Kaohsiung Times (2026); Fastener World (2025) [12][27] |
| Export value | US$4.59 bn (2023); ~US$4.28 bn (2024, est.) | Fastener World industry data (2024–25) [27] |
| Share destined for Europe | ~one quarter | CommonWealth (2023) [14] |
| Firm structure | Predominantly family-run; nationally, 51.79% of SMEs are sole proprietorships/family businesses, 58.22% operating >8 years | MOEA White Paper data (2025) [11][13] |

Economically, the cluster is a textbook "hidden champion" ecosystem: firms with aerospace-grade precision supplying European automakers, yet administered by family members on spreadsheets, with aging workforces, succession pressures, and no in-house data or ESG personnel [13]. (Sector-wide employment is not published in official statistics; given ~1,800 firms of typical SME scale, cluster employment plausibly runs to several tens of thousands of workers — an estimate, flagged as such.)

### 1.3 The environmental profile of a screw

Environmentally, fastener making is steel plus electricity plus heat. The main energy loads are wire drawing, cold forging, thread rolling, and above all heat treatment and surface treatment (electroplating) — continuous, electricity-hungry processes. Industry analyses put the embedded emissions of finished fasteners at roughly **2 tCO2e per tonne of product** once the steel wire-rod precursor is included [18]. Two structural facts define the sector's footprint:

- **The grid it draws from:** Taiwan's electricity emission factor was **0.474 kgCO2e/kWh in 2024** [24] — high by European standards, because the grid remains fossil-heavy. Every kilowatt-hour a fastener plant consumes carries that weight into the product's carbon account, and into the EU's tariff math.
- **The precursor it buys:** the wire rod comes overwhelmingly from the domestic steel value chain (China Steel Corp and re-rollers), whose emissions become the fastener's "embedded" emissions under EU accounting. The SME controls neither the grid nor the mill; what it *can* control — process efficiency, scheduling, and above all **proving its actual numbers rather than being assigned worst-case ones** — is precisely what it currently has no tools for.

This is the economic-environmental double exposure: the cluster earns its living from carbon-intensive processes sold into the world's most carbon-regulated market.

---

## 2. The Mandate: The Legislation Closing In From Both Sides

### 2.1 The planetary and legal frame

Taiwan wrote net-zero into law: the **Climate Change Response Act (2023)** establishes net-zero greenhouse gas emissions by 2050 as a statutory goal, and in 2025 the government adopted **NDC 3.0** — emissions cuts of 28%±2% by 2030, 32%±2% by 2032, and **38%±2% by 2035** against 2005, among the most ambitious targets in Asia [23]. These targets are not abstractions for industry: they are the legal engine behind everything that follows.

### 2.2 Taiwan's domestic carbon price — live since this year

Under the Act, the Ministry of Environment (MOENV) began levying carbon fees on large emitters, and the first payment cycle closed on **31 May 2026**. The verified results define the domestic landscape [2][3]:

- **NT$4.97 billion** collected from **461 factories run by 240 companies** (threshold: >25,000 tCO2e/year, Scope 1+2).
- Sector burden: semiconductors NT$2.2 bn (44%, incl. 33 TSMC fabs), electricity NT$635 m, steel NT$400 m, concrete NT$130 m.
- Rates: **NT$300/t standard**, with preferential rates of **NT$100/t or NT$50/t** for approved Self-Determined Reduction Plans; high-leakage-risk industries apply a 0.2 adjustment coefficient (effective floor ~NT$10/t) [4][5].
- Of ~430 factories applying for preferential rates, **~28 were withdrawn or rejected** — evidence that even resource-rich corporations struggle to produce reduction plans that survive regulatory scrutiny [2][3].

Three forward signals matter for SMEs. First, MOENV has signalled **gradual lowering of the 25,000 t threshold** and fee escalation (potentially NT$1,200–1,800/t by 2030) [23b]. Second, a **pilot emissions-trading system** is planned (~2027), converting today's fee into a dual-track carbon market [3][23b]. Third — a correction this proposal carries deliberately, because earlier drafts got it wrong — **preferential rates depend on the emitter's own Scope 1+2 reductions only; they do not run on supplier Scope 3 data** [4][5]. Supplier carbon pressure in Taiwan is real, but it flows from SBTi/RE100 commitments and customer programs (e.g., TSMC's NT$5.5 bn supplier carbon-reduction subsidy scheme [14b]), not from the fee mechanism. An SME therefore cannot today monetize a reduction plan through preferential rates; its incentives are its customers, its power bill, and its future — and, as Section 6 shows, the regulations coming next.

### 2.3 The EU's border carbon price — the binding constraint

The **Carbon Border Adjustment Mechanism** covers six Annex I categories — **cement, iron & steel, aluminium, fertilisers, electricity, hydrogen** — and, critically for Taiwan, the iron & steel chapter has included downstream articles such as **CN 7318 (screws, bolts, nuts, washers) from the outset** [6][15]. After the 2023–2025 transitional reporting phase, the mechanism entered its **definitive (paying) regime on 1 January 2026** [6][7]:

- EU importers must purchase and surrender **CBAM certificates** priced quarterly at the EU ETS auction average — **€75.36/tCO2e for Q1 2026, €75.28 for Q2 2026** (official Commission figures) [26].
- The first certificate surrender falls in **September 2027**, covering 2026 imports [1][7].
- The 2025 "Omnibus" package added a **50-tonne annual de minimis** that exempts ~90% of importers while retaining ~99% of covered emissions — but the threshold is computed **cumulatively at the importer level**, so an EU distributor buying small lots from five Taiwanese SMEs can cross it and must then demand data from all five. MOENV's Climate Change Administration Director-General publicly warned of exactly this aggregation effect [1][6][7].
- **Default values were not abolished — they were made country-specific.** Importers may still use them, and they carry escalating markups: **+10% (2026), +20% (2027), +30% (2028 onward)** [8][32]. But the adopted tables (Reg. 2025/2621, published as the Commission workbook "DVs as adopted v20260204" [32]) set one value per product **per country of origin**, reflecting each country's observed production intensity — not a single global worst case. For Taiwan, CN 7318 fasteners carry a default of **2.70719 tCO2e/t direct** (indirect: N/A — electricity is not in the iron & steel certificate scope), among the lowest assigned to any exporting country; China's is 6.375, India's 5.72, and the fallback for unlisted countries 4.80 (§3.1 table). For complex goods, defaults are capped at 20% of reported embedded emissions; at least **80% must be actual data, verified by an accredited third party** [8].
- **A free-allocation adjustment softens the phase-in but not the data race.** Certificates surrendered are reduced by an EU-benchmark deduction (CBAM benchmarks workbook, Reg. 2025/2620: 1.364 tCO2e/t for carbon-steel fasteners, 1.154 for stainless [33]) times the share of free allocation EU producers still receive, which phases out to zero by 2034. Because the deduction is identical whether the buyer uses defaults or the factory's actual data, **it lowers everyone's bill during phase-in but preserves every default-vs-actual difference euro for euro** — and the full amounts land as free allocation disappears. *(Exact phase-in factors to be re-verified against the legal text before submission.)*

The design intent is explicit: make real data the economical option, and push the burden of producing it down the supply chain — across the EU's border, into places like Gangshan. What the adopted numbers add — and what most commentary has missed — is that the same tables now also **price national production cleanliness**: Taiwan's cleaner fastener chain is written into EU law as a per-tonne cost advantage over its largest competitor, an advantage a factory can only claim, widen and defend with data.

---

## 3. Problem Statement: What Breaks, When, and For Whom

### 3.1 The immediate problem (2026–2027): what the adopted numbers actually say

*The figures below are not estimates. They are computed directly from the Commission's adopted default-value workbook ("DVs as adopted v20260204", the machine-readable Reg. 2025/2621) and the official Q2 2026 certificate price of €75.28/tCO2e — parsed, unit-tested and reproduced by our working rules engine, which also reproduces the Commission's own filled CN 7318 template example to nine decimal places [32][34][26]. To our knowledge no public commentary on Taiwan's CBAM exposure has yet been built from these tables.*

**Table A — the certificate cost of a tonne of carbon-steel fasteners (CN 7318), by scenario:**

| Scenario | SEE applied (tCO2e/t) | Buyer's certificate cost | Basis |
|---|---|---|---|
| Taiwan origin, **verified actual data + mill EPD** for the wire rod | ~2.18 | **≈€164/t** | our pilot-corpus engine run [34]; CSC-class precursor data |
| Taiwan origin, verified actual data, **no mill EPD** (precursor on default) | ~2.92 | ≈€220/t | engine run; precursor = TW default CN 7213 [32] |
| Taiwan origin, **no data → default**, 2026 (+10%) | 2.978 | **€224/t** | [32][26] |
| Taiwan origin, default, 2027 (+20%) / 2028+ (+30%) | 3.249 / 3.519 | €245/t / **€265/t** | [32][26] |
| **China origin, default, 2026 / 2028+** | 7.013 / 8.288 | **€528/t / €624/t** | [32][26] |
| India / Türkiye / unlisted-country fallback, default 2026 | 6.29 / 5.97 / 5.28 | €474 / €450 / €398/t | [32][26] |
| Vietnam / Thailand, default 2026 | 3.03 / 2.65 | €228 / €199/t | [32][26] |

*(Full certificate scope shown; the free-allocation benchmark deduction (§2.3) reduces every row equally during phase-in, so all differences between rows hold euro for euro.)*

Three findings follow, each load-bearing for this proposal:

**Finding 1 — the widely quoted €450–750/t penalty is real, but it describes Taiwan's competitors, not Taiwan.** Industry commentary priced the no-data scenario at 3–5× the verified cost [18]; the adopted tables assign that fate to Chinese (€528–624/t), Indian (€474/t) and unlisted-origin (€398/t) fasteners. Taiwan's own default — reflecting its cleaner, CSC-anchored production chain — is **€224/t, among the lowest in the world**. Earlier drafts of this proposal carried the industry range for Taiwan; we correct it here, from the primary source, deliberately: a claim that would not survive expert cross-examination in October is worth more to us corrected in July.

**Finding 2 — Brussels has legislated Taiwan a ~€300/t head start over China, and only data can bank it.** A Taiwanese screw with *no* data already costs its EU buyer ~€304/t less than a Chinese one; with a verified pack and a mill EPD the gap widens to **~€364/t** — roughly 10–12% of the sector-average export unit value (US$3,400–3,600/t [27]), and far more on commodity lines. This inverts the threat narrative honestly: CBAM is not primarily a tax *on* Gangshan; it is a **tariff on Gangshan's competitors** that Gangshan can only cash in by proving its numbers — because a buyer consolidating suppliers will demand the same data discipline from everyone, and because the EU declarant needs per-product figures from 2026 regardless of who pays what.

**Finding 3 — for a Taiwanese SME, nearly all the recoverable money sits in one document.** Because Taiwan's default is mild, a factory whose data pack still uses the *default precursor value* for its steel saves its buyer only ~€4/t. Add the **mill's environmental product declaration (EPD) for the wire rod** — one document from the steel supplier — and the saving becomes **~€60/t, ≈NT$3.9 million a year for a 1,800 t/yr exporter**, growing automatically with the mark-up ratchet (+20% in 2027, +30% from 2028) and with every certificate-price rise. No consultant engagement is economical for the €4 case; a near-zero-marginal-cost tool that computes the pack *and tells the owner which single document unlocks the other €56* is economical for both. That concentration of value — discovered by running our own engine against the adopted tables — is now a designed feature of the product (§5.2).

Set against those numbers, the procurement logic is unchanged and remains the binding constraint: an EU importer facing two otherwise identical Taiwanese suppliers will keep the one whose verifier-ready pack arrives and drop the one whose doesn't — the 50-tonne de minimis is cumulated at the importer level, the declarant's filing duty is annual and unconditional, and for complex goods at least 80% of a reported actual calculation must be verified data [6][7][8]. MOENV estimates ~**2,600 Taiwanese SMEs** produce the affected goods [1]. The legal obligation sits on the EU importer — the declarant — which is exactly what makes the SME's position precarious: it is not summoned by a regulator it can petition; it is silently re-scored by a procurement spreadsheet in Rotterdam.

And the capability to respond is demonstrably thin. Sector surveys found 60% of fast-growing SMEs had not completed any carbon inventory, 80% had no reduction targets, and half cited talent shortage as the binding constraint [14]. The firms that have obtained ISO 14067 product-footprint verification (Chan Chin C., Fang Sheng Screws, via subsidized MIRDC counseling) prove the task is *tractable* — and, priced as consultant engagements, that it is **not repeatable at SME economics**: certificates are one-off snapshots, while CBAM demands installation-level data per product, per period, in the Commission's format, indefinitely [25].

### 3.2 The compounding problem (2027–2030): four curves bending the wrong way

1. **The default-value ratchet, twice over:** markups climb 10% → 20% → 30% through 2028 (Taiwan's CN 7318 default: €224 → €245 → €265/t at today's certificate price [32][26]), while the free-allocation deduction that currently softens every bill phases out toward 2034 (§2.3) — so both the level and the default-vs-actual gap grow automatically each year without any new legislation.
2. **The scope ratchet:** in December 2025 the European Commission proposed extending CBAM to **~180 downstream steel- and aluminium-intensive product categories** (fastener-adjacent goods, wire, springs, hand tools, household metal articles) with certificate obligations **from 1 January 2028**. The Council adopted its position in June 2026; the **European Parliament plenary vote is expected in September 2026** [10]. If it passes, the affected Taiwanese exporter population multiplies well beyond 2,600.
3. **The product-passport ratchet:** the EU's Ecodesign for Sustainable Products Regulation launches the central **Digital Product Passport registry (from July 2026)**, with mandatory passports for batteries in 2027 and phased extension toward textiles, iron, steel, and electronics in 2027–2030 — product-level, machine-readable sustainability data as a condition of market access [28].
4. **The domestic ratchet:** Taiwan's fee threshold is set to fall, rates to rise, and an ETS pilot to begin (~2027) [3][23b]. Firms outside the fee today will not all remain outside it; those that begin measuring now inherit a baseline, those that don't inherit a scramble.

The comparison across time is stark: in 2024 a Gangshan SME's carbon ignorance cost it nothing; in 2026 it leaves NT$ millions of legislated advantage over Chinese competitors unbanked, up to ~€60/t of buyer savings unclaimed, and the relationship exposed to any competitor who shows up with a verifier-ready pack; by 2028 the mark-up is a third higher, the free-allocation cushion thinner, the covered catalogue potentially ~180 categories larger, and the domestic regulator closer to its own gate. The problem is not a wave — it is a rising floor.

---

## 4. The Gap: Why the Existing System Doesn't Solve This

Taiwan's government has moved — but every existing instrument stops short of the artifact that decides procurement outcomes. Verified capability audit of the current stack:

| Instrument (operator, date verified) | What it does | What it does **not** do |
|---|---|---|
| **CAAS 中小企業減碳服務站** (SMESA/MOEA) [20] | Courses, articles, green-product promotion, consultant referrals | No computation of any kind; not a reporting tool |
| **IDB Carbon Emissions Calculator** (MOEA) [22] | Free web tool: bills + fuel lists → rough annual organizational CO2e | Not ISO-grade; no product-level allocation; no CN-code output; no reduction planning |
| **MOENV CBAM Help Platform** (Mar 2026) [1] | Information hub, two-way consultation channel for affected SMEs | Explicitly informational; computes nothing |
| **Taipower app / eBill** [21] | Consumption charts, tariff simulation, usage alerts for AMI customers | No emissions conversion; no compliance artifacts |
| **TRE100** (CIER, Dec 2025) [29] | RE-pledge registry for firms below RE100's threshold — credibility signaling | No accounting, no measurement tooling |
| **Private ESG SaaS** (Sustaihub et al.) | Organizational inventories; CBAM advisory content | Subscription + consultant-mediated; per-product CBAM packs for micro-SMEs remain manual services |
| **Consultants + MIRDC counseling** [25] | Real ISO 14064-1/14067 certifications, subsidized in part | One-off, per-engagement economics; cannot service recurring per-product, per-quarter data demands across ~2,600 firms |

**The gap, stated precisely:** no instrument in Taiwan converts *SME-native documents* (a Taipower bill, a stack of invoices, a production ledger) into *importer-ready, verifier-structured, per-CN-code specific embedded emissions data* — repeatably, at near-zero marginal cost, in the Commission's format. The government stack ends at awareness; the market stack prices out the small end; the compliance artifact in between belongs to no one. That is the space CarbonPass occupies — and because MOENV has already built the informational front door [1], a computational layer designed for integration completes a stack the state has visibly started building, rather than competing with it.

---

## 5. The Proposed Solution: CarbonPass

### 5.1 Concept

**CarbonPass is a local-first AI compliance and optimization copilot for export SMEs, prototyped on Taiwan's fastener cluster.** One sentence of user experience: *photograph your electricity bill and invoices in LINE, answer three questions in Mandarin or Taiwanese, and receive (a) the carbon data pack your European buyer needs, (b) the number it saves them, and (c) a schedule that cuts your power bill and makes next quarter's number better.*

### 5.2 The three modules

**Module 1 — the Data-Pack Engine (compliance core).**
Document intelligence ingests Taipower bills, material invoices (wire rod, fuels, plating chemicals), and production records — photographed or uploaded, processed **on-device/on-premises**. The engine then performs the two computations that generic calculators cannot:

- *Allocation:* splitting facility-level energy across product lines and CN codes using production volumes, machine ratings, and operating-hour heuristics, with per-line uncertainty quantification — the step CBAM's product-level "specific embedded emissions" (SEE) methodology strictly requires and invoices alone don't contain.
- *SEE assembly per the EU rulebook:* simple-vs-complex-goods logic, precursor emissions from mill certificates where available (CSC documentation) or CBAM default values as the conservative fallback, output rendered in the **European Commission's communication template structure**, flagged field-by-field as "actual / default / needs verifier attention."

Outputs: ① the per-CN-code CBAM data pack the importer's declarant needs; ② an organizational ISO 14064-1-style inventory as a by-product (domestic readiness, bank requests, customer questionnaires); ③ the **decision screen**, computed from the adopted tables, that answers the owner's three real questions: *what does my buyer pay with my data vs without it* (e.g. €164 vs €224/t, growing to €265/t by 2028); *what single action is worth the most* — typically "request the mill EPD for your wire rod from 中鋼: it unlocks ~€60/t ≈ NT$3.9 M/yr for your buyer" (the pipeline flags this automatically when a precursor is on a default value); and *is verification worth it for me this year* — data value vs accredited-verifier cost, answered per firm, honestly, including "not yet" [32][34]. One screen, sourced, that converts an abstract regulation into a retention argument the owner can forward to the customer — plus the comparison no competitor can make for him: *your screw already beats a Chinese screw by ~€300/t in Brussels; here is how to widen that to €364 and keep the order.*

**Module 2 — the Grid-Aware Scheduler (the environmental-economic engine).**
Taiwan publishes its power system's **generation by unit every 10 minutes** as open data (real-time: data.gov.tw #8931; historical: #37331) [30]. CarbonPass computes an hourly grid-carbon-intensity curve from that public feed, overlays **Taipower time-of-use tariffs** (summer peak rates several times the off-peak rate [21b]), and runs a scheduling optimizer (MILP baseline, RL refinement) over the factory's *flexible* loads — heat-treatment furnaces, compressors, plating rectifiers — against order deadlines the owner states in the chat. Input is 15-minute AMI interval data exported by the customer from their own Taipower account (consent-based CSV; no third-party API dependency). Outputs: a shift plan, projected NT$ savings, projected tCO2e reduction, and a **monitored before/after ledger** — a continuously documented reduction trajectory structured to the baseline-and-monitoring logic of ISO 14064-2, stated carefully: *structured to the standard's logic; certification remains the verifier's act.* This module is what makes CarbonPass environmentally aware rather than merely bureaucratically useful: it doesn't just report carbon, it removes some — and every removed tonne shrinks the next data pack's electricity line and the buyer's Scope-3 figures (stated precisely: indirect emissions are recorded in the CBAM template but are not currently part of the iron & steel certificate scope [32]; the module's bankable benefits are the NT$ bill, Scope-3 questionnaires, DPP readiness and the domestic carbon-fee trajectory).

**Module 3 — the Inclusion Interface (the reason this belongs in this hackathon).**
The entire system fronts as a **conversational assistant in LINE, Mandarin/Taiwanese-first, voice-friendly, zero ESG vocabulary**. "拍一張電費單" — snap a photo of the power bill — is the whole onboarding. The design premise is that the excluded party here is a person: a 60-plus owner-operator in a family firm who will never log into a European portal or read Regulation 2025/2621's 2,400 pages [8], and should not have to. Digital inclusion, in the Handbook's own terms of "ages, regions, and needs," is delivered as an interface property, not a slide.

**Architecture principle — local-first by design.** Taiwanese SMEs treat granular energy and production data as trade secrets and resist centralized cloud tools (a barrier both independent audits confirmed). Raw documents therefore never leave the factory; only computed outputs (the data pack the SME chooses to send its buyer) do. Roadmap hardening — federated learning across the cluster, TEE-based confidential computing — follows the architectural precedent Taiwan's financial sector has already normalized (the banks' federated anti-fraud alliances), but is explicitly *not* claimed for the PoC.

### 5.3 Extended uses: one engine, both directions of readiness

The same data spine serves the SME **internationally** — CBAM packs today, customer Scope 3 questionnaires (TSMC-chain, brand supply chains) [14b], ISO 14067 preparation, and Digital Product Passport payloads as ESPR phases in [28] — and **domestically**: a standing organizational inventory as the carbon-fee threshold descends; a documented reduction ledger positioned for MOENV's Voluntary Reduction mechanism (credits usable against fee liability at 1.2:1, capped at 10%, tradeable on TCX — with its additionality and eligibility rules honestly acknowledged as a multi-year path) [5b]; and bank-ready carbon data as Green Finance 3.0 pushes Taiwanese lenders to demand SME emissions figures for sustainability-linked lending. One ingestion, many artifacts: that is what converts a compliance chore into infrastructure.

---

## 6. Beyond Current Scope: The Mandates That Prove the Idea's Future

A hackathon proposal must justify its life after the demo. CarbonPass's forward case rests on dated, citable regulatory trajectories, not speculation:

1. **CBAM downstream extension (pending — decision imminent):** ~180 added product categories, obligations from 1 Jan 2028; Council position adopted June 2026; **EP plenary vote expected September 2026 — inside this Hackathon's mentorship window** [10]. The proposal treats this correctly as pending legislation, and turns the timing into a live roadmap event: by final review in late October, the team will present with the vote's outcome known — either an addressable market grown from 2,600 firms to the exporters of 180 categories, or a confirmed beachhead with more preparation time. Few proposals anywhere get a natural experiment scheduled between their submission and their finals.
2. **ESPR / Digital Product Passport:** registry infrastructure from July 2026; batteries mandatory 2027; textiles, iron, steel, electronics phased 2027–2030 [28]. DPP payloads are machine-readable product sustainability data — structurally, the same output class CarbonPass already generates.
3. **Domestic escalation:** threshold lowering, fee increases toward NT$1,200–1,800/t by 2030, ETS pilot ~2027 [3][23b]. Every step converts more of Taiwan's 150,000+ manufacturing SMEs from spectators into reporters — with CarbonPass's org-inventory by-product as their on-ramp.
4. **NDC 3.0 arithmetic:** a 38%±2% cut by 2035 [23] cannot be delivered by the ~500 directly regulated entities alone; the state will need measurement and reduction capillaries into the SME layer. A tool the government can adopt (the Hackathon's own pipeline — Section 8.3) is precisely such a capillary.

The beachhead-to-platform sequence is therefore: fasteners (2026, live compulsion) → downstream steel/aluminium categories (2028, pending) → DPP sectors (2027–2030) → domestic carbon-fee entrants (2027 onward). Same spine, widening catalogue.

---

## 7. Technical Analysis: How It Gets Built

### 7.1 System architecture

```
[LINE Bot / Web PWA  —  Mandarin/Taiwanese, voice-in, photo-in]
        │
[Ingestion Layer]  Vision-language document parsing (open VLM, e.g. Qwen3-VL-class,
        │          fine-tuned on a mock corpus of Taipower bill layouts + MOF e-invoice
        │          formats) → structured activity data w/ confidence scores
        │
[Knowledge & Rules Layer]
        │   • MOENV emission-coefficient DB (data.gov.tw #28176, OpenAPI)          [19]
        │   • Electricity EF 0.474 kgCO2e/kWh (MOEA Energy Admin, 2024)             [24]
        │   • CBAM SEE rules engine: simple/complex goods, precursor logic,
        │     default-value tables extracted from Reg. (EU) 2025/2621 (CN 7318 rows)[8]
        │   • Certificate price feed (Commission quarterly publications)            [26]
        │
[Allocation Engine]  constrained optimization: facility kWh + fuels → product lines
        │            (production volumes, machine ratings, operating-hours priors);
        │            Monte-Carlo uncertainty per line item
        │
[Outputs A]  CBAM data pack (Commission template structure, XML/XLSX) per CN code
             ISO 14064-1-style org inventory (PDF, bilingual)
             "Default vs. actual" buyer-cost delta screen
        │
[Scheduler — Module 2]
        │   • Hourly grid carbon intensity computed from Taipower 10-min
        │     generation-by-unit open data (#8931 real-time / #37331 historical)    [30]
        │   • Taipower TOU tariff tables                                            [21b]
        │   • 15-min AMI interval CSV (customer-exported, consent-based)
        │   • MILP baseline (OR-Tools) + RL policy (Gymnasium env; PPO) over
        │     flexible loads subject to order-deadline constraints
        │
[Outputs B]  Shift plan; NT$ and tCO2e deltas; monitored before/after ledger
        │
[Privacy]   All parsing & computation on-premises/on-device; only chosen outputs
            leave. Roadmap: federated benchmark learning across cluster; TEEs.
```

**Stretch module (labeled, not load-bearing):** NILM "virtual sub-metering" — Seq2Point-style disaggregation to machine-level baselines without hardware. Public datasets (UK-DALE, REFIT, REDD) are residential and MIMII is acoustic; industrial three-phase disaggregation is *not* validated by open data. It is presented as post-pilot roadmap, demonstrated only on synthetic profiles — a deliberate honesty both audits converged on, and a defense against the strongest technical cross-examination a judge can mount.

### 7.2 Why this clears the "sophisticated AI" bar honestly

Bill-parsing arithmetic alone would not justify the AI framing — both independent audits said so. The defensible AI substance is: (i) **document intelligence over messy, multi-format, mixed-language artifacts with allocation reasoning and quantified uncertainty** — a genuine ML problem, not regex (working PoC: 100% field extraction across a 12-bill synthetic Taipower corpus via an on-premises 8B vision-language model); (ii) **carbon- and price-aware scheduling under constraints** with a live grid signal — an optimization/RL problem no existing Taiwan tool attempts; (iii) a **compliance rules engine** encoding a 2,400-page regulation into field-level guidance — already validated by reproducing the European Commission's own filled CN 7318 "screws and nuts" template example to nine decimal places in automated golden tests [34]. The Handbook's application form requires describing AI usage in detail; this is a description that survives expert reading. Equally, the PHIT rubric weights **Feasibility (40%) above Innovation (30%)** in preliminaries — so the exotic roadmap items (federated learning, NILM, TEEs) stay in the roadmap, and the demo stays working.

### 7.3 Datasets and resources for the PoC (all accessible now, no partnerships required)

| # | Resource | Access | Role |
|---|---|---|---|
| 1 | MOENV carbon-footprint emission coefficients | data.gov.tw **#28176**; OpenAPI data.moenv.gov.tw/swagger [19] | Material/fuel/process EFs |
| 2 | Taiwan product carbon footprint registry | data.gov.tw **#8992**; cfp.moenv.gov.tw [19] | Benchmarks, sanity checks |
| 3 | Electricity EF 0.474 kgCO2e/kWh (2024) | MOEA Energy Administration [24] | Scope 2 & scheduler math |
| 4 | Taipower generation by unit, 10-min | **#8931** (real-time), **#37331** (historical) [30] | Hourly grid-intensity curve |
| 5 | Taipower TOU rate schedules | taipower.com.tw [21b] | Price signal (re-verify current table pre-submission) |
| 6 | CBAM default values & methodology | Implementing Reg. (EU) 2025/2621 — Commission workbook "DVs as adopted v20260204" (per-country tables), CBAM benchmarks workbook (Reg. 2025/2620), communication template + filled CN 7318 example; all downloaded, parsed, unit-tested in the PoC [8][32][33][34] | Output schema; per-country CN 7318 default rows; delta screen; golden tests |
| 7 | Official CBAM certificate prices | Commission quarterly publications (€75.36 Q1 / €75.28 Q2 2026) [26] | Live cost math |
| 8 | Eurostat Comext + Taiwan MOF customs statistics | Public trade databases | CN 7318 flows for impact quantification |
| 9 | MOENV GHG registry disclosures (large emitters) | MOENV platform | Precursor (CSC) benchmarks |
| 10 | AMI 15-min interval data | Customer CSV export via Taipower app/eBill (consent) | Scheduler input; PoC uses synthetic profile shaped to Taiwan TOU calendar until pilot |
| 11 | Bill/invoice sample corpus | Public Taipower bill formats + MOF e-invoice (電子發票) specification; mock corpus built by team | Ingestion training/eval |
| 12 | (Stretch only) MIMII (Zenodo), UK-DALE/REFIT/REDD | Public | NILM/anomaly simulation — proxy, labeled |

**Open-data reciprocity (scored by the application form):** CarbonPass publishes back (a) a cleaned, hourly **Taiwan grid-carbon-intensity dataset** derived from #8931/#37331, and (b) an anonymized **fastener-sector SEE benchmark table** from the pilot — directly answering the form's "provision of open data" and "suggestions for modifying open data" fields.

### 7.4 Build plan against the official PHIT calendar

| Window (Handbook §IV) | Deliverable |
|---|---|
| **Now → 31 Jul 2026, 17:00 (GMT+8)** — submission | Team of 3–10 (≥1 non-ROC national; 2 designated contacts; all materials in English). PoC v0: **Module 1 is already running end-to-end as of 16 Jul** — 3-firm mock corpus (synthetic Taipower TOU bills, MIG 4.0 e-invoices, production logs) → on-prem VLM ingestion (100% field extraction) → OR-Tools allocation with Monte-Carlo uncertainty → rules engine (reproduces the Commission's filled CN 7318 example at 1e-9 in golden tests) → filled Communication Template with actual/default/needs-attention flags → buyer cost-delta screen computed from the adopted default tables [32][34]. Remaining for submission: Module 2 on one synthetic fastener load profile with the **live** #8931 grid feed; LINE-bot walkthrough; demo video; proposal written field-by-field to the application form (SDGs 8, 9, 12, 13; stakeholders; differences vs. existing solutions per Section 4; quantifiable benefits per Section 3.1; open data used + given back). Target: expressions of interest from a TIFI member firm and/or MIRDC / Kaohsiung EPB's Voluntary Emission Reduction Advisory Team *(target — not yet secured)* |
| **Aug 6–16** — preliminary review | Scored 40% Feasibility / 30% Innovation / 30% Social Impact — the proposal + credible start is the whole game here |
| **Mid-Sep → mid-Oct** — mentorship | One real pilot SME in Gangshan: actual bills in, actual data pack out; structure reviewed by an MIRDC engineer or verifier; one flexible load shifted and measured. Use PHIT's own mentorship levers (public-private matchmaking, field-validation support). **Track the EP plenary vote (Sept) and update the market slide with the outcome** |
| **Late Oct** — final review | Live demo: pack generation + grid-aware schedule + pilot before/after ledger. Implementation & Verification (30%) is scored on progress *between submission and finals* and requires "a system demo or code design description" — measured pilot deltas, documented weekly, are the winning currency |
| **Early–mid Dec** — awards | — |

### 7.5 What this campaign expects — and what past winners prove

The Presidential Hackathon is not a procurement exercise; it is the government's civic-tech **adoption pipeline**. The Handbook scores early-stage reality explicitly (development-stage and future-plans fields; Implementation & Verification measured as *delta during mentorship*; "system demo **or code design description**"), and the rewards are pipeline mechanics: 1-on-1 mentorship, technical consultant matching, **public-private collaboration facilitation, field-validation support**, and mandatory follow-up benefit tracking for advancing teams. The track record confirms proposals live on: MODA's 2026 launch event brought back GreenhopeBCTW, CropNow, and Beyond Hearing to present post-victory implementation progress; five Teams of Excellence per year receive government guidance with outcome tracking; and at least one past project (the One-Stop Emergency Response and Disaster Management System) matured into government policy [31]. **The correct ambition level is therefore exactly what this proposal stages: a working PoC at submission, a government-connected pilot by finals, and an adoption path — integration with MOENV's CBAM platform and SMESA's service network — as the explicit endgame.** Claiming full deployability now would score *worse* under Feasibility than demonstrating an honest, moving trajectory.

---

## 8. Alignment With "Digital Inclusion in the AI Era"

The Handbook's theme objective (1) is *"enabling people of different **ages, regions, and needs** to access technology and participate in digital services on equal footing."* CarbonPass maps onto all three axes without stretching the text: **ages** — the family-run, spreadsheet-administered firms of a >8-year-old industrial cluster, whose owners are being asked to operate EU-grade data infrastructure overnight; **regions** — a single, nameable southern-Taiwan district whose economic identity is at stake; **needs** — participation in what has become a de facto digital service (carbon-verified market access) that currently requires capabilities only corporations possess. Objective (2), *"Building Smarter Services… and beyond,"* is served by turning open government data (MOENV coefficients, Taipower grid telemetry) into a public-benefit service layer. Historical precedent supports economic-inclusion winners (Fiscal Force 2020; BRSDM agricultural carbon 2022; GreenhopeBCTW carbon wallet 2024; CropNow 2025) [31]. And the inclusion claim is engineered into the product — the LINE/voice Mandarin-Taiwanese interface — so judges see it in the demo rather than take it on faith.

**The competitive claim, in one paragraph (every figure sourced above):**

> On 1 January 2026 the EU began taxing the carbon inside Taiwan's exports. 3.74 million tonnes of Taiwanese steel goods — made largely by ~2,600 family-run factories around Kaohsiung's "Kingdom of Screws," a top-3 global fastener exporter — are now priced, tonne by tonne, by Brussels' adopted carbon tables. We parsed those tables with our own working engine, and they say something nobody has told these factories: a Taiwanese screw already beats a Chinese screw by ~€300 per tonne in certificate cost, a legislated advantage that only a factory able to *prove* its numbers can bank, widen to ~€364/t, and defend — while the no-data default ratchets from €224 to €265/t by 2028 and the buyer's declarant demands verified per-product data either way. The knowledge needed to claim that advantage is buried in a 2,400-page European regulation that a 60-year-old factory owner with a spreadsheet cannot read — and no tool in Taiwan's current stack reads it for him. That is the real digital divide of the AI era. CarbonPass closes it with a photograph: a local-first AI that turns an electricity bill and a folder of invoices into the verifier-ready data pack his European buyer must have — it already reproduces the Commission's own worked example to nine decimals — then tells him the one document that unlocks NT$ millions a year (his steel mill's EPD), and schedules his furnaces against Taiwan's own open grid data so the next pack is cheaper and cleaner. One cluster first. Then the 180 product categories Europe votes on this September.

---

## 9. Statistical Annex

**Taiwan macro / SME:** 1.716 M SMEs, 98.87% of enterprises; 9.19 M employed (79.3%); ~10.3% of export value; 51.79% family-run/sole proprietorship; 58.22% >8 years old [11][13]. Net-zero 2050 in law; NDC 3.0: −28%±2% (2030), −32%±2% (2032), −38%±2% (2035) vs 2005 [23]. Grid EF 0.474 kgCO2e/kWh (2024) [24].

**Carbon fee (first cycle, closed 31 May 2026):** NT$4.97 bn; 461 factories / 240 companies; semiconductors NT$2.2 bn (33 TSMC fabs), electricity NT$635 m, steel NT$400 m, concrete NT$130 m; NT$300/100/50 rates; 0.2 leakage coefficient; ~430 preferential applications, ~28 withdrawn/rejected; threshold 25,000 tCO2e; ETS pilot ~2027; fee trajectory toward NT$1,200–1,800/t by 2030 [2][3][4][5][23b].

**CBAM:** definitive phase 1 Jan 2026; certificate €75.36 (Q1 2026) / €75.28 (Q2 2026); first surrender Sep 2027; 50 t importer-level de minimis (~90% of importers exempt, ~99% of emissions retained); **per-country defaults (adopted tables, direct SEE tCO2e/t for CN 7318): Taiwan 2.707 · Thailand 2.408 · US 2.580 · Vietnam 2.750 · Japan 2.800 · S. Korea 3.474 · unlisted-country fallback 4.801 · Türkiye 5.430 · India 5.720 · China 6.375 · Indonesia 8.230; indirect N/A for iron & steel; +10/20/30% markups (TW: €224/€245/€265 per t at €75.28)** [32][26]; free-allocation benchmark deduction 1.364 (carbon) / 1.154 (stainless) tCO2e/t, phasing out to 2034 [33]; complex goods ≥80% verified actual data; Commission's own filled CN 7318 example: 2.41 tCO2e/t carbon-steel / 4.23 stainless — confirming the ~2 t industry estimate [34][18]; Annex I includes CN 7318 from origin; downstream extension: ~180 categories proposed Dec 2025, obligations 1 Jan 2028 pending, EP plenary vote expected Sep 2026 [6][7][8][10][15].

**Taiwan exposure:** 13th-largest CBAM exporter to the EU; 3.74 M t (Oct 2023–Dec 2025); ~2,600 SMEs (MOENV) [1]. Fasteners: ~1,800 manufacturers (TIFI ~700 members); top-3 exporter, ~10–13% of world production; ~1.2 M t (2025) / 936 k t (Jan–Sep 2024); US$4.59 bn (2023) / ~US$4.28 bn (2024); ~¼ to Europe; ~2 tCO2e/t product (industry estimate); DPP registry from Jul 2026, steel/textiles/electronics 2027–2030 [12][14][17][18][27][28].

## References

[1] Taipei Times, "MOENV to set up CBAM help platform for SMEs," 2 Mar 2026 — primary MOENV statements (3.74 M t; ~2,600 SMEs; importer-level aggregation; platform launch). [2] Focus Taiwan, 3 Jun 2026, first carbon-fee cycle results. [3] Taipei Times, 4 Jun 2026; Eco-Business, Jun 2026 (sector breakdown; ETS pilot; rate plans). [4] MOENV press releases 30237/31552 (2024–25), carbon-fee rate regulations. [5] RESET Carbon (2025–26), preferential-rate mechanics; [5b] MOENV Voluntary GHG Reduction regulations & offset platform (1.2:1 ratio, 10% cap, eligibility rules). [6] European Commission DG TAXUD, CBAM pages (definitive regime; de minimis). [7] ICAP, "EU adopts simplifications of CBAM rules…," Oct 2025. [8] O'Melveny (2026), Reg. (EU) 2025/2621 analysis (default markups; 80/20; 2,400 pp). [9] Bipartisan Policy Center (2026), default-value analysis. [10] Akin (Jan 2026); Covington (Feb 2026); SteelOrbis (Jun 2026) — downstream extension proposal, Council position, EP committee vote & plenary timing. [11] MOEA SMESA, 2025 White Paper on SMEs press release. [12] Kaohsiung Times (2026), "Kingdom of Screws" green shift (1.2 M t; #3; ~13%). [13] taiwan.md / MOEA White Paper synthesis — hidden champions, family-firm structure. [14] CommonWealth Magazine, "The screw triggering a battle worth NT$200 billion," Jul 2023; [14b] TSMC ESG, supplier carbon-reduction subsidy program (NT$5.5 bn). [15] CarbonChain, CBAM CN-code guide (7318 in Annex I). [17] Goebel Fasteners / PRNewswire (2024), ~1,800 manufacturers; TIFI profile (~700 members). [18] Special Insert (Apr 2026); Fastener World (2026) — ~2 tCO2e/t; default-cost multiples; 30–50% impact estimates. [19] data.gov.tw datasets #28176, #8992; MOENV OpenAPI. [20] SMESA CAAS portal (fetched 12 Jul 2026). [21] Taipower Smart Grid, AMI data applications & app features; [21b] Taipower rate schedules. [22] MOEA, "The Carbon Emissions Calculator, an IDB New Released Tool." [23] MOENV/Executive Yuan (2025–26), NDC 3.0 press releases (28/32/38% targets; net-zero 2050 statutory); [23b] Reccessary / Eco-Business, fee-trajectory and threshold-lowering signals. [24] MOEA Energy Administration, 2024 electricity carbon emission factor (0.474). [25] Chan Chin C. ISO 14067 verification statement; Fastener World, Fang Sheng certifications; MIRDC (MOEA DoIT profile). [26] European Commission, CBAM certificate price publications (Q1 €75.36, 7 Apr 2026; Q2 €75.28); Fastmarkets/EUROMETAL coverage. [27] Fastener World no. 211/213 (2025), export value/volume series. [28] ESPR (EU) 2024/1781 analyses — DPP registry Jul 2026; batteries 2027; steel/textiles/electronics 2027–2030. [29] CIER, tre100 launch releases, Dec 2025. [30] data.gov.tw #8931 (real-time generation by unit, 10-min) and #37331 (historical). [31] MODA press releases 20076 (2026 launch, returning winners) & 18226; Learning Health Systems (Wiley/PMC, 2025), Presidential Hackathon adoption pipeline; PHIT 2026 Handbook (May 2026) — theme, eligibility, criteria, schedule, rewards, application form. [32] European Commission, **"DVs as adopted_v20260204.xlsx"** — machine-readable default values per Implementing Reg. (EU) 2025/2621, per-country × CN-code tables (DG TAXUD download, in-repo at `data/cbam_official/default_values.xlsx`); parsed and unit-tested by the CarbonPass rules engine, 16–17 Jul 2026 — primary source for all default-value figures in §2.3/§3.1/§9, **superseding the industry estimates in [18] for Taiwan-origin goods**. [33] European Commission, **CBAM Benchmarks workbook (20260206)** per Implementing Reg. (EU) 2025/2620 — free-allocation adjustment benchmarks (CN 7318: 1.364 tCO2e/t carbon steel, 1.154 stainless); in-repo at `data/cbam_official/benchmarks.xlsx`. [34] European Commission, **CBAM Communication Template for installations v2.1 + filled example "Steel 3: Screws and nuts"** (in-repo at `data/cbam_official/`); the CarbonPass engine reproduces the example's specific embedded emissions (2.4135 tCO2e/t carbon-steel; 4.2312 stainless) at 1e-9 relative tolerance in automated golden tests, and its cost-delta screen and pilot-corpus figures (€164/€220/€224 per t; EPD lever ≈€60/t) derive from [32]+[26].
