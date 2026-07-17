# THE PROVABILITY DIVIDE — Scope Extension for CarbonPass

**Date:** 17 Jul 2026 · **Status:** proposed extension, owner-approved direction, not yet merged into
the submission-facing artifacts.
**Read with:** `docs/15_evidence_dossier.md` (every source, quote and correction behind this document).
**Supersedes in part:** `docs/09_master_proposal.md` §2.3/§3.1 framing and `docs/10_poc_blueprint.md`
§2/§2A rules text — see `docs/15` §5 for the exact kill-list.

---

## 1. Why this document exists

The kickoff PoC worked and the pitch broke. `docs/09` Rev. 2 honestly killed the €450–750/t default
claim for Taiwan — the real adopted Taiwanese default is ≈€224/t — and what remained was a stake of
**€4/t (firm_a) to €60/t (firm_c)**, roughly €12k–108k/yr per firm. That is a real business case and
a weak competition case. PHIT scores *Social Impact* and "importance of the problem to be resolved";
margin optimisation for already-profitable exporters does not land there.

This document is the result of a ground-up re-examination of the evidence we already hold (four
research agents, 17 Jul 2026). It found a **larger, better-sourced problem that keeps every module we
have built and re-aims it** — and it found that more of our claims were wrong than we knew.

**Owner decisions taken 17 Jul 2026:**

1. **Scope** → the global provability divide. Taiwan is the **origin and proving ground**, not the market.
2. **Geography** → **ASEAN + South Asia** foreground (New Southbound alignment; India recurs in 4 of 7
   editions per our own winners study). Do not headline gains for Chinese exporters.
3. **Corrections** → document now; fix code and the submission artifacts in a later pass.

---

## 2. The thesis

> **CBAM does not tax carbon. It taxes the inability to *prove* carbon — and proving has a fixed cost
> and a gateway four doors wide, so it falls hardest on the smallest.**

Ten claims. Each is sourced; each is chosen because it survives cross-examination. Full evidence in
`docs/15`.

**1. Defaults are lawful, forever.** The Commission's Q&A (27 May 2026) p.36: declarants "can use
default values for **all types** of CBAM goods other than electricity in cases where verified actual
embedded emissions data for those goods is not available." p.44: "**If operators choose not to offer
this service, declarants will have to use default values.**" There is no legal compulsion on the
factory. The pressure is price and procurement — never legality. *(This kills our own 80/20 claim; see
`docs/15` §5.)*

**2. The only escape is verification.** An accredited CBAM verifier, a **mandatory physical site visit
in year 1** ("always the case for the first site visit", QA §5.15), a team of at least three —
English-competent lead auditor, an auditor speaking the operator's language, English-competent
independent reviewer (QA §5.19) — and **one verification report per installation** (EC verification
page). That is a regulatory cost floor, not a commercial one.

**3. There is no group verification anywhere in CBAM.** No cluster, collective or aggregated
provision exists. Outsourcing (QA §5.8) is not group certification: the accredited verifier "may not
outsource the issuance of the verification report or the technical review". Grouping exists only for
CN codes *within* one installation. FSC, organic and Fairtrade faced structurally identical
small-producer economics and solved them two decades ago.

**4. The gateway is four doors wide.** The Commission's own *State-of-play CBAM accreditation*
(retrieved 17 Jul 2026, re-fetched and parsed by us — totals row verbatim: `Total 24 11 7 4`): of
**24** national accreditation bodies, **11** are ready to accept applications at all, and **4** accept
applications from third-country verifiers — **Italy, Netherlands, Poland, Sweden**. As of July 2026
**zero CBAM verifiers are accredited anywhere in the world**.

**5. The timeline is arithmetic, not opinion.** First accreditations ~Sept 2026 → first verification
reports "expected in early 2027" (QA §5.11) → first declaration due 30 Sep 2027. That leaves roughly
**twelve months of accredited-verifier existence** in which to physically visit every installation on
earth that wants actual values. *This is our own arithmetic from the Commission's own dates.*

**6. Taiwan proves the bottleneck is the EU's gateway, not anyone's capability.** MOENV's own bulletin
(March 2026): Taiwan has **20 approved GHG verification bodies and 200+ specialists**, and "the EU is
yet to release instructions or guidelines detailing executions on verification, **nor has any
verification body submitted applications**." MOENV names the blockers as EU-side: "excessively
frequent changes of EU regulations, lack of official EU-approved training materials, and unclear
review procedures and evaluation items."

**7. The EU knows how to do proportionality, and chose not to here.** EU ETS excludes installations
under 25,000 t, gives simplified MRV under 5,000 t, and lets small emitters report **without
verification**. CBAM gives third-country operators none of it. Exact-string searches across the Q&A
and the operator guidance return **zero hits** for `SME`, `small and medium`, `micro-enterprise` and
`simplified regime`.

**8. Accommodation is therefore a choice.** The Netherlands has a bilateral arrangement with Turkey's
TURKAK; Sweden with Ukraine's NAAU. Taiwan, India, Vietnam, Thailand and Brazil have nothing. The
system *can* reach a third country when there is political will.

**9. The book itself is bimodal — data poverty priced as tariff.** Measured from the adopted workbook
in this repo (`uv run python scripts/atlas_scan.py`): of 120 country sheets, **33 carry a CN 7318 15
row and 87 carry none at all**. Coverage is bimodal — **58 countries hold fewer than 50 goods with a
value; only 33 hold 200 or more**; the median country holds 51.5. Countries with no row reach the
fallback **by sheet omission**, and the fallback is, in the Commission's own words (QA p.37), "the
average of the ten exporting countries with the highest emission intensities per good". It exceeds the
listed-country median for **255 of 260 goods (98.1%)**, at a median ratio of **1.61×**.

**10. The harm is already real, in the region we chose.** Indian MSME carbon levies tripled from
€70–80 to €240–300/t by being pushed onto defaults, with shipment seizures at EU ports in January
2026; 25,000–30,000 MSMEs are exposed; India is now mooting **90% reimbursement** of certification
costs via TRACE/EPM. A government does not design a 90% subsidy for a cost it thinks is trivial.

**And six documented voids.** There is no published CBAM verification price anywhere; no count of
in-scope installations; no NAB fee schedule; no group verification; no Taiwanese verification subsidy;
no verifier travel-cost data. *In a regime that has already commenced and is already seizing
shipments.* The absence is a more damning argument than any number would be — and we should say so
rather than fill the gap with a number we cannot defend.

---

## 3. The measurement that makes it arithmetic

Hold the physics fixed. Take firm_a's **measured** SEE — 2.924364 tCO2e/t direct, the engine's own
output, pinned against ground truth — and change nothing about the factory except its country of
origin. Certificate price €75.28 (Q2 2026), determination period 2026.

| Origin | Default (2026) | Buyer pays **without** data | Buyer pays **with** data | **Reward for proving** | At 1,800 t/yr |
|---|---|---|---|---|---|
| Thailand | 2.6488 | €199.40 | €220.15 | **−€20.74/t** | −€37,340 |
| **Taiwan** | 2.9779 | €224.18 | €220.15 | **€4.03/t** | €7,256 |
| Vietnam | 3.0250 | €227.72 | €220.15 | **€7.58/t** | €13,637 |
| **No book → fallback** | 5.2813 | €397.58 | €220.15 | **€177.43/t** | **€319,377** |
| India | 6.2920 | €473.66 | €220.15 | **€253.52/t** | €456,328 |
| Indonesia | 9.0530 | €681.51 | €220.15 | **€461.36/t** | €830,455 |

*(Reproduce: `uv run python scripts/atlas_scan.py` → `out/atlas/`.)*

**The same factory. The same carbon. Forty-four times the reward for proving it, decided by a
passport.** The value of your data is not set by how clean you are. It is set by whether the European
Commission happens to hold a book for your country.

Two honest readings we must carry, not bury:

- **Thailand is negative.** A Thai factory with firm_a's exact physics is *worse off* proving: its
  adopted default (2.6488) is cleaner than its measured truth (2.924). For that firm the honest answer
  is "don't". A tool that cannot say that is a sales instrument, not a compliance instrument — which is
  precisely why the Provability Screen (§5) must be able to answer **"not yet"**, and why we should
  publish this row rather than drop it.
- **The cruelty is in the correlation.** The reward for proving is highest exactly where the capacity
  to prove is lowest. A Malaysian, Bangladeshi or Sri Lankan fastener maker has **no row in the book**,
  so its buyer pays the ten-dirtiest average — and its country has no accreditation arrangement, no
  domestic verifier gateway, and no subsidy. Taiwan, which needs it least, is best equipped to get it.

---

## 4. Why Taiwan is the lab, not the market

This is the correction the previous drafts could not make, because they needed Taiwan to be the
victim.

Taiwan's adopted default (2.70719) is already close to a real Taiwanese fastener's measured SEE
(firm_a: 2.924). Brussels has, in effect, already told the truth about Taiwan. Independent trade press
agrees: Crowe UK in *Fastener + Fixing* (9 Feb 2026) prices Taiwanese fasteners at **€150/t** on
defaults against €50–100/t on actual data, versus **Türkiye €400** and **China €500**. The injury to a
Gangshan SME is real but not existential.

That is not a weakness in the tool. It is a statement about where the tool should point. We built a
**global instrument and aimed it at the one market where it has least to say.**

What Taiwan uniquely offers is everything *except* the injury:

- **World-class open data** — MOENV coefficients, Taipower's 10-minute generation feed, TOU tariffs.
- **Idle verification capacity** — 20 accredited bodies, 200+ specialists, zero EU applications.
- **The archetype** — 2,600 CBAM-exposed SMEs, 3.74 M t shipped, a nameable district.
- **A government already at the front door** — MOENV's CBAM platform is informational; the
  computational layer is exactly what is missing.
- **A standing foreign policy that this fits** — New Southbound, and "Taiwan can help" as practice
  rather than slogan.

**Taiwan builds it, proves it on its own cluster, and gives it to the economies that need it most.**
That is the international track's entire purpose, and it converts our weakest number into the reason
for the architecture.

---

## 5. Geography: ASEAN + South Asia

CN 7318 15 (threaded screws and bolts), 2026 marked-up defaults, buyer cost at €75.28
(`out/atlas/summary.md`):

| Country | Direct | Buyer €/t | Route | In the book? |
|---|---|---|---|---|
| Philippines | 1.37 | €113.45 | (E) EAF/scrap | ✅ — **cleanest of all 33 listed** |
| Myanmar | 2.30 | €190.46 | (E) | ✅ |
| Thailand | 2.408 | €199.40 | (E) | ✅ |
| **Taiwan** | 2.70719 | €224.18 | (C) | ✅ |
| Vietnam | 2.75 | €227.72 | (C) | ✅ |
| **_Other Countries_ (fallback)** | 4.8012 | **€397.58** | (C) | — |
| India | 5.72 | €473.66 | (C) | ✅ |
| Indonesia | 8.23 | €681.51 | (C) | ✅ |
| **Malaysia · Singapore · Cambodia · Laos · Brunei · Pakistan · Bangladesh · Sri Lanka · Nepal** | — | **€397.58** | — | ❌ **no row at all** |

**Nine of fifteen focus countries have no fastener row.** Their exporters are priced at the
ten-dirtiest average not because their factories are dirty but because the Commission has no data on
them. Note also that coverage is *per sector, not per country*: Malaysia, Singapore, Pakistan,
Bangladesh and Sri Lanka **do** have aluminium rows (CN 7604/7606) while having no fastener row at
all — the book is patchy in ways no exporter could predict.

**Discipline — two things we will not claim:**

- **"Developing countries get worse defaults" is false, and we tested it.** Both tails are developing
  economies: Bolivia, Tanzania and Zambia are the *most* favourably treated; Mozambique, India and
  Indonesia the least. The Philippines beats every industrialised country on fasteners. The driver is
  **production route and grid intensity, not income** — route (E), electric-arc/scrap, is what buys
  the Philippines its 1.37. *(The country ranking is also confounded by ragged coverage — 24 goods on
  some sheets versus 256 on others — so it is not a like-for-like league table. Flagged, not resolved.)*
- The honest finding is stronger than the tempting one: **the divide is not wealth. It is whether the
  EU has your data.**

---

## 6. What we build

| # | Item | Status today |
|---|---|---|
| 1 | **The Provability Atlas** — a cleaned, machine-readable, defect-annotated edition of the adopted default + benchmark tables, plus the "who is in the book" coverage map. Published open. | **Computable today.** The engine parses 120/120 sheets, 12,532 rows, 0 failures. `scripts/atlas_scan.py` exists and runs. |
| 2 | **Verification Dossier Generator** — from the same activity data, emit what the *verifier* actually needs: the Monitoring Methodology Documentation, written procedures, system-boundary map, data-flow and control procedures, sampling plan, uncertainty statement. **This attacks the real barrier** — and it is exactly what a language model is good at and what nobody offers. | New module — the flagship build |
| 3 | **The Provability Screen** — replaces the cost-delta screen. Answers: what does proving cost me, what is it worth, what is my break-even export volume, and *should I bother this year?* Must be able to say **"no"** (see Thailand, §3). | Reframe of `costdelta/screen.py` |
| 4 | **Cluster verification, as a policy proposal** — CBAM has none; FSC/organic/Fairtrade have had it for twenty years; Taiwan has 20 idle verification bodies and 200+ specialists. PHIT is a policy-adoption pipeline, and this is a proposal it can actually carry to MOENV and the Commission. | Policy artifact |
| 5 | **The edge tier as the inclusion claim** — qwen3-vl **4B**: 336/336 (100%) across six phone-photo degradations, 18–31 s/doc, on a laptop, offline, no cloud, no GPU (`out/bakeoff/`). | **Already proven** |

Item 5 is the one to say out loud. A 4-billion-parameter model that reads a Traditional-Chinese
utility bill perfectly on commodity hardware is not a footnote about efficiency. It is the entire
inclusion argument: **AI that runs on the excluded side of the wall**, in a country with no cloud
budget, no GPU, and no EU accreditation arrangement.

Everything already built survives: the ingestion pipeline, the OR-Tools allocation with Monte-Carlo
uncertainty, the SEE engine (golden-tested at rel 1e-9 against the Commission's own worked example),
the template writer, the grid-aware scheduler, the LINE interface. **Nothing is thrown away. It is
re-aimed.**

---

## 7. Competition fit

- **Theme — "Digital Inclusion in the AI Era."** The divide we name is *provability*: not the absence
  of broadband but the inability to produce the proof that now decides market access. The Handbook's
  three axes still answer literally — **ages** (the analog-native family firm), **regions** (Gangshan,
  then the districts like it across ASEAN), **needs** (carbon-verified market access as a de facto
  digital service). What changes is that the excluded population is no longer 2,600 exporters' margins
  but small producers across ASEAN and South Asia locked out by a gateway four doors wide.
- **Feasibility (40%, the heaviest weight).** 120 countries × 5 sectors running today; 25/25 tests
  green; the Commission's own worked example reproduced at rel 1e-9; a filled 19-sheet workbook on
  disk whose SEE cells independently recompute in LibreOffice to the engine's sidecar.
- **Innovation (30%).** Nobody has published the atlas. Nobody generates verification dossiers. And
  the framing itself is an original contribution: the institutional literature (UNCTAD, World Bank,
  academic CGE work) is overwhelmingly about the carbon **price** and trade flows — **the claim that
  the data and audit infrastructure is the regressive vector is under-served**, conceded even by the
  systematic reviews ("overlooked in much macro-level modeling"). We cannot cite our way into it. We
  build it from primary regulation, the Commission's own accreditation table, and our own arithmetic.
- **Social Impact (30%).** See §3 and §10.
- **Timing.** Verifier accreditation lands **~Sept 2026 — exactly inside the mentorship window**; the
  first verification reports are due early 2027; the EP plenary vote on the ~180-category downstream
  extension is still expected Sept 2026. Few proposals get two scheduled natural experiments between
  submission and finals.

---

## 8. Honest limits (non-negotiable — carry these into every artifact)

1. **Scope the claim to the year-1 cold start and the accreditation gateway — not to a permanent
   recurring cost.** Year-2+ site-visit waivers explicitly favour installations that are "not overly
   complex" (QA §5.15) — i.e. exactly the small single-product plants we champion. Overclaim here and
   the thesis breaks.
2. **Taiwan's default is mild.** Say it first, before a judge does. It is the reason for the
   architecture, not an embarrassment.
3. **The 50 t de minimis is real relief** — ~182,000 importers, ~90%, exempted (COM(2025) 783). But it
   relieves **EU importers, not third-country producers**, and it aggregates per declarant (QA §4.30),
   so a sub-50t producer can be pulled in with none of the SME relief.
4. **Outsourcing (QA §5.8) genuinely cuts travel cost**, and TAIEX/Global Europe exist — though they
   target candidate/neighbourhood *public administrations*, and Global Europe starts in 2028, two
   years after CBAM bites.
5. **We do not know what verification costs.** No CBAM price exists anywhere. Do not use the
   €5,000–50,000 figure circulating online — it traces to a single anonymous commercial site citing
   unnamed "market data" (`docs/15` §5). The honest move is to make the absence the argument.
6. **Defaults can be a subsidy.** Thailand's row is negative. Publish it.
7. **Our own engine is not yet right outside steel and aluminium.** Two bugs (`docs/15` §6) mean
   cement and fertiliser numbers are not publishable until fixed. Every figure in this document is
   steel or aluminium for that reason.

---

## 9. What this changes in the existing docs

Pointers only for now; the rewrite is the next pass.

| Doc | Status |
|---|---|
| `docs/09_master_proposal.md` | §2.3/§3.1 80/20 claim **dead**; §5.3 ISO 14067 claim weakened (LCA factors are not accepted — QA §4.24). Rev. 3 should rebuild on this document. |
| `docs/10_poc_blueprint.md` | §2/§2A 80/20 and the "5% variance threshold" **dead**; §3 C8 guidance PDFs are **not a rule source**. |
| `docs/12`, `docs/13` | Next-step lists superseded by §6 above. |
| **Submission PDF** | **Still carries "€450–750/t" and "30–50% of product value" in the Executive Summary, Figure 1 and Table 5.** This contradicts `docs/09` Rev. 2 and is a **hard blocker for 31 Jul**. First item of the next pass. |

---

## 10. The claim, in one paragraph

> On 1 January 2026 the European Union began charging for the carbon inside imported steel. It did not
> build a machine that taxes carbon. It built a machine that taxes **proof** — and then it published,
> in its own annexes, exactly who is able to supply it. We parsed those annexes with our own engine:
> for the world's most traded fastener line, **33 countries have a book and 87 have no entry at all**,
> and everyone without an entry is priced at the average of the ten dirtiest exporters on earth. To
> escape that, a factory needs an accredited verifier to fly to it — and as of July 2026 there are
> **none**, anywhere, because only **four** of the EU's twenty-four accreditation bodies will even
> accept an application from a third country. Taiwan has twenty verification bodies and two hundred
> specialists sitting idle behind that gate. Hold a factory's physics fixed and move it: proving your
> carbon is worth **€4 a tonne in Taiwan and €177 in a country with no book** — forty-four times the
> reward, for identical emissions, decided by a passport. That is the digital divide of the AI era:
> not who has broadband, but who can prove. CarbonPass closes it with a photograph and a
> four-billion-parameter model that runs offline on a laptop — because the factories that need it most
> are the ones with no cloud, no GPU, and no seat at the accreditation table. Taiwan does not have this
> problem. Taiwan has the answer to it.
