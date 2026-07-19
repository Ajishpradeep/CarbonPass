# THE WASTE NOBODY MEASURES — the live scope extension

**Date:** 17 Jul 2026 · **Status:** 🟢 **LIVE thesis. This supersedes `docs/14` as the direction.**
**Read with:** `docs/15_evidence_dossier.md` (sources, kill-list, defects). `docs/14_scope_extension.md`
is now a **background annex** — its facts are verified and reusable, its *thesis* is not the direction.
**Reproduce everything here:** `uv run python scripts/waste_scan.py out/firm_a_activity.json data/mock_corpus/firm_a`

---

## 1. What changed, and why

Two dead ends taught us the shape of the real problem.

**Dead end 1 — the money.** `docs/09` Rev. 2 honestly killed the €450–750/t claim: Taiwan's real
default is ≈€224/t and firm_a's data is worth **€4.03/t**. Helping a profitable exporter shave €4/t is
not a problem worth a Presidential Hackathon.

**Dead end 2 — the policy pivot.** `docs/14` chased that into a critique of CBAM's fairness, the EU's
accreditation gateway, and a cluster-verification proposal to the Commission. The research is sound and
worth keeping. But it is a **legislation deck**: it argues about nations and regulations, and there is
no person in it. The theme is *"Digital Inclusion in the AI Era"* — **ages, regions, needs**. A jury
does not score a nation's trade advantage.

**The question that broke it open** (owner, 17 Jul): *"this is for a company to report their carbon —
how about actually making them emit less? And if steel fasteners aren't in danger, what does the data
say IS?"*

We asked the data. It answered both, and the answers are the same answer.

---

## 2. The finding: they are throwing it away, and nobody has ever counted it

Every firm in our corpus buys about **1.10 tonnes of steel for every 1 tonne of product it ships.**
Nobody has ever looked at the other 0.10.

Measured by `scripts/waste_scan.py` from documents the pipeline **already** extracts — steel mass *and
unit price* from the MIG 4.0 e-invoice XML, output tonnes from the production log:

| Firm / product | Steel in | Product out | Scrap | Loss | Carbon in the scrap | Money in the scrap |
|---|---|---|---|---|---|---|
| firm_a — carbon screws | 3,300 t | 3,000 t | 300 t | 9.1% | **758 tCO₂e/yr** | **NT$7,350,000/yr** |
| firm_b — carbon screws | 4,650 t | 4,200 t | 450 t | 9.7% | 1,138 tCO₂e/yr | NT$11,207,490/yr |
| firm_b — **stainless** screws | 1,440 t | 1,300 t | 140 t | 9.7% | **742 tCO₂e/yr** | NT$13,430,400/yr |

**firm_b alone buys and bins 1,879 tCO₂e and NT$24.6 million every year.**

Look at the stainless line. It is the *smallest* product in the factory — 1,300 t against 4,200 t of
carbon steel — yet it accounts for **39% of the firm's binned carbon on 24% of its output**, because
every tonne of stainless thrown away carries **2.1× the carbon of a tonne of carbon steel** (5.302 vs
2.528 tCO₂e/t) and **3.9× the money** (NT$95,931 vs NT$24,905/t, from the invoices). §4 explains why.

### Why it moves the CBAM number too (unlike anything else we built)

The SEE formula makes yield a first-class lever, exactly:

```
SEE_direct = own/AL + ratio × SEE_precursor        where ratio = steel_in / product_out
⇒ ΔSEE     = Δ(ratio) × SEE_precursor
```

No allocation model, no uncertainty, no assumptions — the precursor term *is* the ratio. And the mass
CBAM counts is the mass **entering the process, before cutting** (Commission Q&A p.32 §4.11), so **the
scrap is already inside the declared number whether the owner looks at it or not.**

### The comparison that reframes the project

| Lever, firm_a | tCO₂e/yr | Cuts the CBAM number? | NT$/yr |
|---|---|---|---|
| **Yield** — 9.1% → 5% loss | **359** | **Yes** — SEE 2.924 → 2.805 (−€9.01/t, −€27,040/yr) | **NT$3,481,579** |
| Module 2 — grid-aware load shifting (measured, Sprint 1) | **4.49** | **No** — indirect is out of scope for CN 7318 (G7) | NT$399,800 |

**The yield lever is 80× the carbon of our flagship "environmental" module** — and unlike load shifting
it actually moves the compliance number. We built a scheduler that saves 4.49 tonnes a year while the
same factory throws 758 tonnes in a skip, and we never looked.

---

## 3. The person, and the actual divide

Mr. Lin, 61, Gangshan. Thirty employees. His back office is his daughter-in-law and a spreadsheet.

To see the table in §2, he must reconcile **22 steel e-invoices across 12 months against a production
log, per CN code, for a whole year** — matching grades to products, netting off the coil ends, and
knowing that CN 7213 wire rod carries 2.53 tCO₂e per tonne. That is an ERP job with a sustainability
analyst attached.

**Every large manufacturer already has this.** SAP + MES + a sustainability team; yield is on a
dashboard, reviewed weekly, and a 1% improvement is somebody's KPI. Mr. Lin's competitor in the same
district, with 3,000 employees, sees his waste in real time. Mr. Lin has never seen his once.

**That gap is the digital divide, stated in the Handbook's own three axes:**

- **Ages** — an analog-native owner-operator, no data professional in the building, being asked to
  operate capabilities that are ordinary in a corporation.
- **Regions** — Gangshan–Luzhu, ~1,800 firms of exactly this shape.
- **Needs** — not "market access" in the abstract: **NT$3.5 million a year and 359 tonnes of CO₂ he
  cannot see.**

And the AI is the reason the gap closes rather than merely being described: a **4B-parameter model,
100% field accuracy across six phone-photo degradations, 18–31 s/doc, on a laptop, offline, no GPU, no
cloud** (`out/bakeoff/`). The capability that costs a corporation an ERP licence costs Mr. Lin a
photograph. **That is digital inclusion in the AI era, with a number attached.**

---

## 4. What is actually in danger: stainless — and we had hidden it from ourselves

The owner asked what the data says is in danger, given fasteners are not. We scanned all **244** of
Taiwan's goods against every other country in the adopted tables. Percentile 1.0 = worst in the world.

| Taiwan's good | Value | World median | Percentile |
|---|---|---|---|
| Carbon wire rod — CN 7213 | 2.298 | 2.325 | 0.41 — unremarkable |
| Other alloy bars — CN 7227 | **2.17** | 3.48 | **0.00 — best on earth** |
| Stainless flat/bar/wire — CN 7218–7223 | 8.63 – 10.0 | ~3.27 | **0.97–1.00 — worst on earth** |
| **Stainless wire rod — CN 7221** | **no value at all** | 3.27 | — **a hole in the book** |

Taiwan's whole stainless block sits **~2.6× the world median** — systematic, not a typo. So the
"CBAM is a tariff on Taiwan's competitors" story from `docs/09` Rev. 2 is **true for carbon steel and
inverted for stainless.**

**But the precursor a fastener plant actually buys is CN 7221** — *"bars and rods of stainless steel,
hot-rolled, in irregularly wound coils"*, the exact stainless twin of CN 7213. (Not CN 7223, which is
drawn *wire*: a fastener plant buys rod and draws it in-house — there is a 抽線機 in every firm's
machine list.) And here is the finding:

> **Of the 33 countries with a full steel book, exactly three have no CN 7221 value at all:
> Taiwan, Thailand and Vietnam** — the three fastener exporters. Taiwan's 7221 row literally reads
> *"see below"* with nothing below it.

Q&A p.37 §4.25 sends an unlisted good to the *"Other countries and territories"* table — **"the
average of the ten exporting countries with the highest emission intensities"** (§4.26) — **4.82**,
marked up to **5.302** in 2026. **The EU's book has a hole precisely where the cluster buys its
stainless, and the hole is expensive.**

**Our own engine hid it.** `_precursor_cn()` mapped stainless → **CN 7227** — *"alloy steel **other
than stainless**"*, and Taiwan's 7227 (2.17) is **the lowest value assigned to any country on earth**.
So a stainless screw came out *cleaner* than a carbon one. **Fixed 17 Jul** (`docs/15` §6 defect 8):
7227 → 7221, plus `defaults.resolve()` implementing the Annex I fallback the engine never had.

### Why this is an emissions problem, not a paperwork problem

The EU gives stainless fasteners the **same 2.70719 default as carbon fasteners** — a carbon-steel
number. So for a Taiwanese stainless screw maker (firm_b, 1,300 t/yr, engine-verified):

| | tCO₂e/t | Buyer pays |
|---|---|---|
| EU default (what the buyer uses today) | 2.978 | **€224/t** |
| Honest actual, correct precursor + fallback | **6.003** | **€452/t** |

Reporting honestly costs the buyer **€228/t — €296,006/yr**. So nobody reports. The default is a
**2.0× under-count** and a subsidy, and **Taiwan's worst carbon problem stays legally invisible.**
Nobody sees it, so nobody fixes it.

That is precisely why the product must not be a filing tool. **A filing tool tells a stainless maker to
stay quiet. A waste tool tells him the stainless in his scrap bin is the most expensive thing he throws
away** — **742 tCO₂e and NT$13.4M a year on his smallest product line**, more money than the carbon
line three times its size — and that is true, actionable, and worth it to him **whatever he files.**

---

## 5. The product

**Stop selling the filing. The same photograph that files the report finds the waste.**

```
[photo: Taipower bill + steel e-invoices + production log]  ← unchanged
        ↓ ingestion (qwen3-vl 4B, offline, 18-31 s/doc)     ← unchanged
        ↓ activity data                                      ← unchanged
   ┌────┴─────────────────────────────┐
   │                                  │
[CBAM pack]  ← the door-opener   [WASTE MAP]  ← the product
             (buyer asked for it)  "you binned 758 tCO2e and NT$7.35M this year;
                                    here is where, and here is what 5% loss is worth"
```

| # | Build | Status |
|---|---|---|
| 1 | **Waste screen** — yield per product per CN code, carbon and NT$ in the scrap, from e-invoice mass **and unit price** + production log. | ✅ **Working today** — `scripts/waste_scan.py`, run on firm_a and firm_b |
| 2 | ~~Fix the stainless precursor CN~~ (7227 → **7221**) + `defaults.resolve()` for the Annex I fallback. | ✅ **Done 17 Jul** — corpus + ground truth regenerated, 27/27 tests green |
| 3 | **Monthly yield tracking + alert** — the e-invoices are dated; loss per month per line, so a drifting die shows up in weeks, not never. Turns a once-a-year report into a control loop. | New — the highest-value build |
| 4 | **Reduction ranking** — yield first (80×), then fuel, then scheduling. Honest ordering, including "your scheduler is rounding error". | Reframe of the cost-delta screen |
| 5 | **Module 2 keeps its real job** — NT$399,800/yr is genuine money. It is demoted from "the environmental module" to "the bill module", which is what it always was. | Reframe only |

**Nothing built is thrown away.** Ingestion, allocation, SEE engine, writer, scheduler, LINE, the
golden tests, the 4B edge tier — all survive. The output gains a second, better half.

---

## 6. Competition fit

- **Theme.** A person (61, Gangshan, no data staff), a need (NT$3.5M and 359 tCO₂e he cannot see), and
  an AI that closes a capability gap corporations closed twenty years ago with ERP. The inclusion claim
  is demonstrated in the demo, not asserted on a slide.
- **Social Impact (30%).** ~1,800 firms in one district, each binning ~10% of its steel. And it
  *reduces* — this is SDG 12/13 in the literal sense, not carbon accountancy.
- **Feasibility (40%, heaviest).** The screen runs today on two firms from real document formats;
  25/25 tests green; the Commission's own worked example reproduced at rel 1e-9.
- **Innovation (30%).** Everyone else computes the number to *file* it. We compute it to *cut* it —
  and the scrap-yield lever falls straight out of the Commission's own SEE formula, where nobody looked
  because they were reading it as an accounting rule instead of an optimisation target.
- **Give-back.** An anonymised **fastener-sector yield benchmark** — the first of its kind — is worth
  more to the cluster than any grid dataset, because it tells every firm whether its 9.1% is good.

---

## 7. Honest limits (carry these into every artifact)

1. **Scrap is recycled.** It is sold and remelted. The **SEE effect is exact and 1:1** (CBAM counts
   mass entering before cutting). The **atmospheric effect is real but smaller than the gross figure** —
   remelting recovers the iron, not the energy already spent reducing, rolling and drawing the rod.
   **Always state the gross and the caveat together. Never claim 758 t "avoided".**
2. **9.1% is synthetic.** Our corpus is generated, not observed. The *mechanism* is certain; the
   *magnitude* needs the pilot. Real cluster yields are the first thing to ask MIRDC/TIFI for.
3. **5% is a scenario, not a promise.** We do not yet know what is achievable per process. The tool
   should show the curve and let the owner set the target.
4. **We cannot yet tell him HOW to cut it.** Today we can tell him *that* he wastes it, *where*, and
   *what it is worth*. Die life, setup scrap and coil-end optimisation are domain problems for the
   pilot — **do not claim process expertise we do not have.**
5. **The stainless numbers moved once already — do not quote the old ones.** The first draft of this
   doc used CN **7223** (drawn wire, Taiwan 10.0) and claimed a 4.61× understatement, a €703/t honesty
   penalty and 1,539 tCO₂e of stainless scrap. **All wrong** — 7223 is not what a fastener plant buys.
   The correct code is **7221**, Taiwan has no value, the Annex I fallback (4.82 → 5.302) applies, and
   the real figures are **2.16×**, **€228/t** and **742 tCO₂e**. The finding survived; its size halved.
   Kill the old numbers on sight.
6. **Verify CN 7221's absence against the IR 2025/2621 legal text** (`docs/15` §8.1) before publishing
   the "hole in the book" headline. The workbook is machine-readable convenience; the regulation is the
   law, and a "see below" with nothing below it is as likely a **publishing defect** as a deliberate
   omission. If it is a defect, that is worth reporting to the Commission — and it is worth more to
   Taiwan than to us.
7. **Why Taiwan's stainless is dirty is unexplained.** *Hypothesis, unverified:* the route runs on
   imported nickel pig iron / ferronickel (Indonesia's is coal-fired; Indonesia's stainless is 8.69).
   **Do not assert this without a source.**
8. **The €4/t finding stands.** Filing is worth almost nothing to a Taiwanese carbon-steel maker. That
   is now a *feature of the argument*: the compliance pack is the door-opener, the waste is the value.
9. **firm_b and firm_c do not reconcile to ground truth at 1e-6** (rel 7.5e-5 / 1.1e-4). **Pre-existing,
   not caused by the CN fix** — the corpus generator computes ground truth from exact intended totals
   (4200 / 1300 / 1800 t) while the production logs it writes carry rounded monthly rows summing to
   4199.9 / 1300.1 / 1799.8. firm_a happens to sum exactly, which is why it was the only firm that ever
   reconciled. **Ground truth is therefore not yet a golden for firm_b/c** — fix the generator to derive
   ground truth from the rows it actually emits (`docs/15` §6 defect 11).

---

## 8. Pointers

| Doc | Status |
|---|---|
| **`docs/16` (this)** | 🟢 **LIVE thesis** |
| `docs/15_evidence_dossier.md` | 🟢 Live — sources, kill-list, engine defects. Defect 8 = the stainless CN bug. |
| `docs/14_scope_extension.md` | 🟡 **Background annex.** Facts verified and reusable (the 33/87 book split, the four accreditation doors, the "same factory, moved" table). Its *thesis* is superseded by this doc. |
| `docs/09_master_proposal.md` | 🔴 Rev. 3 needed, on this doc. §2.3/§3.1 80/20 claim dead. |
| Submission PDF | 🔴 Still carries €450–750/t. Hard blocker for 31 Jul. |
