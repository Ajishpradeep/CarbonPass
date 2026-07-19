# CarbonPass — The Factory That Cannot See Itself

**2026 Presidential Hackathon · International Track — "Digital Inclusion in the AI Era"**

> A 3,000-person factory sees its carbon, its waste and its energy on a dashboard.
> A 30-person factory cannot. CarbonPass restores that sight from a photograph —
> offline, in Taiwanese, on the factory's own laptop.

**Corresponding SDGs:** 8 · 9 · 12 · 13 · **Submission:** 31 July 2026 · All content in English
**Beachhead:** the fastener cluster of Gangshan–Luzhu, Kaohsiung — the "Kingdom of Screws".
Every figure in this document is computed by the team's own working engine from primary EU
regulation and Taiwan open data. *(This is the Markdown edition of the submission PDF, Rev 5 —
fully verified against official sources; see docs/19_claim_verification_register.md.)*

---

# Executive Summary

Two factories sit a few streets apart in Gangshan, the district of
Kaohsiung the world calls the “Kingdom of Screws”. One has
3,000 employees, an ERP system, a manufacturing-execution
system and a sustainability team; its material yield, its energy use and
its product carbon numbers are on a dashboard, reviewed weekly — a
one-percent improvement is somebody’s KPI. The other has thirty
employees, and its entire information system is its owner — Mr. Lin, 61
— his daughter-in-law, and a spreadsheet. Both factories generate the
same kinds of data every day: electricity bills, steel invoices,
production logs, a scrap pile sold to the recycler. The large factory
turns that data into sight. The small one files it in a drawer.

**That is the digital divide of the AI era, stated precisely: not the
absence of connectivity, but the absence of organizational
self-knowledge.** Industry research finds **54% of small and mid-sized
plants worldwide still run production on pen, paper and spreadsheets**
(IoT Analytics, 2025), and the quality literature puts the cost of what
un-instrumented factories cannot see — scrap, rework, hidden
inefficiency — at **10–20% of revenue** (ASQ cost-of-poor-quality
studies; scrap and rework alone average ~2% in APQC
benchmarks).<sup>\[21\]</sup> Corporations closed this gap over twenty
years with enterprise software and analysts. A 30-person exporter cannot
— there is no analyst in the building to hire, and no software he could
operate if there were. CarbonPass closes it with what he already has: a
photograph of his own paperwork.

**The forcing function arrived on 1 January 2026.** The EU began
charging importers for the carbon embedded in steel goods, and Taiwan
shipped 3.74 million tonnes of covered products — largely from
~2,600 small factories like Mr. Lin’s.<sup>\[1\]</sup> We
are deliberate about the magnitude: our own engine, run over the
Commission’s adopted tables, shows Taiwan’s default is among the mildest
in the world, so CBAM alone will not bankrupt Gangshan — for a
carbon-steel maker, supplying data is worth only about 4/t. But the
buyer’s letter still demands an answer only an *instrumented* factory
can produce, and it is the first such demand of many (product passports,
domestic carbon fees, customer Scope-3 audits). CBAM’s real significance
for a small factory is this: **the first document Europe asks for is the
one that forces the factory to finally see itself — and once it can,
everything else comes into view.**

**CarbonPass turns one photograph into four kinds of sight.** Inside
LINE, in Mandarin or Taiwanese, Mr. Lin photographs a Taipower bill and
a folder of invoices; a local-first AI — raw documents never leave the
factory — returns the four answers a corporate dashboard would give him:
*What carbon is in my product?* (the verifier-ready CBAM data pack, in
the Commission’s own template); *What do I lose between buying and
shipping?* (a waste map: every firm in our sample buys ~1.10 tonnes of
steel per tonne shipped, and the scrapped tenth carries ~758
tCO<sub>2</sub>e of purchased carbon and a net NT$4–5 million a year for
a typical firm — a pile he *sells* but has never been able to *read*);
*When should my machines run?* (a schedule worth a measured
NT$399,800/yr); and *Am I normal?* (the first anonymised
sector benchmark, so 1,800 firms can finally know what a
good yield is). One data spine, four blind spots removed.

And the point of sight is *reduction*, not paperwork. Cutting scrap is
the one lever that lowers real emissions, real cost and the EU-declared
number at once — our measurements put it at **80 times** the carbon
impact of energy scheduling — and the cluster benchmark turns one
factory’s improvement into a sector-wide mechanism, the same way
corporate yield KPIs did. The tool ranks every lever honestly, including
telling an owner when something is *not* worth doing this year.

The inclusion claim is not argued on a slide; it is in the demo. The
document reader is a **4-billion-parameter** vision-language model that
reads a Traditional-Chinese utility bill at **100% field accuracy across
six phone-photo distortions, in 18–31 seconds, on a laptop, offline,
with no GPU and no cloud** — AI that runs on the excluded side of the
wall. The proof of concept is built entirely on Taiwan’s open data and
the EU’s published methodology, and it gives data back, openly licensed.

A note on method, because it is our differentiator: every number here is
computed by our own working code from primary sources, and where our
earlier drafts overstated — a widely repeated 450–750/t “penalty” that
turns out to describe Taiwan’s competitors, not Taiwan; a waste figure
first quoted at purchase price rather than net of scrap resale — we
corrected ourselves in the open. Section 2.3 is written so a
non-specialist can follow it and a specialist can audit it.

## Team composition and eligibility

The team comprises between three and ten members as required by the
Handbook, including at least one member holding a nationality other than
that of the Republic of China (Taiwan), with a designated primary and
secondary contact. Members span software and machine-learning
engineering, carbon-accounting/CBAM domain knowledge, and the Taiwanese
manufacturing-SME field. All project content and this document are in
English, per the submission rules.

## Originality and commitments

The entry is the original work of the team, created for this
competition; it has not been sold or awarded elsewhere, so the 50%
modification rule does not apply. Intellectual-property arrangements
among members follow the Handbook’s terms. The team commits to full
participation in the mentorship period, implementation-result
presentations, field validation, and the follow-up benefit tracking
required of advancing teams.

# Project Information

## Project name and introduction

**Project name:** CarbonPass — a local-first AI copilot that gives a
small export factory the operational self-knowledge a large one gets
from enterprise software, starting from a photograph of its own
paperwork.

CarbonPass is a conversational artificial-intelligence system. It
converts the ordinary documents a small factory already keeps —
electricity bills, material invoices and production records — into the
four kinds of sight a corporate dashboard provides: the product-carbon
data pack its European customers now request, a per-line map of its
material waste, an energy schedule, and its position against sector
peers. The whole user experience is one sentence: *photograph an
electricity bill and your invoices inside LINE, answer a few questions
in Mandarin or Taiwanese, and receive (a) the verifier-ready carbon data
pack your EU buyer needs, (b) a map of what you lose between buying and
shipping, worth millions of NT$ a year, and (c) a ranked, honest list of
what to fix first.*

### Detailed description of AI usage

CarbonPass is an AI system, not an arithmetic calculator with a chat
interface — and its AI does not *replace* anyone, because in a 30-person
factory there is no analyst to replace. It supplies a capability that
never existed in the building. Three distinct AI/ML subsystems carry the
product, and each is already running:

**(1) Document intelligence with allocation reasoning.** A
vision-language model parses heterogeneous, mixed-language,
*photographed* documents — Taipower electricity bills, Ministry of
Finance electronic invoices (MIG 4.0 XML), and production logs — into
structured activity data with per-field confidence. The non-trivial
machine-learning problem is *allocation*: splitting one facility-wide
electricity figure across many product lines and customs (CN) codes,
which the EU’s product-level methodology strictly requires but invoices
never contain. The system solves this as a constrained-optimization
problem over production volumes, machine power ratings and
operating-hour priors, and attaches a quantified uncertainty (% at one
standard deviation on our corpus, from 10,000 Monte-Carlo
samples) to every line. A second, independent OCR pass (PP-OCRv4)
back-checks every number the vision model returns and flags any mismatch
for human attention.

**(2) A carbon-and-price-aware scheduling optimizer.** Using Taiwan’s
open 10-minute grid-generation feed and Taipower’s time-of-use tariffs,
the system computes an hourly grid-carbon-intensity curve and schedules
a factory’s flexible loads (heat-treatment furnaces, compressors)
against real order deadlines — a mixed-integer optimization no existing
Taiwan tool attempts.

**(3) A compliance rules engine.** The engine encodes the operative
parts of the EU’s methodology — simple-versus-complex-goods logic,
precursor emissions, country-and-year-specific default values, the
Annex I fallback — and renders output in the Commission’s own template.
It is validated by reproducing the Commission’s *own* worked “screws and
nuts” example to nine decimal places in automated tests. This is what
lets the tool read a rulebook that now spans eleven legislative acts and
their annexes *for* the owner and tell him, in one screen, what it means
for him.

## Corresponding SDGs

CarbonPass maps directly onto four UN Sustainable Development Goals, and
the mapping is quantified rather than decorative:

  - **SDG 12 — Responsible Consumption and Production.** The core of the
    product: it measures and reduces material waste (~10% of steel
    input) that is today invisible to the firms generating it.

  - **SDG 13 — Climate Action.** Every tonne of avoided scrap and every
    shifted kilowatt-hour is a measured, documented emission reduction,
    structured to recognised monitoring logic.

  - **SDG 9 — Industry, Innovation and Infrastructure.** It brings
    corporate-grade data infrastructure to micro-manufacturers on
    commodity hardware.

  - **SDG 8 — Decent Work and Economic Growth.** It defends the export
    livelihood of a 2,600-firm cluster against a
    market-access barrier that would otherwise pick winners by
    administrative capacity, not product quality.

## Problem to be resolved and its importance

### The setting: a world industry run on spreadsheets

Taiwan’s fastener cluster is a textbook “hidden champion” ecosystem —
globally dominant firms, administered like corner shops. It is a
top-three fastener exporter worldwide, making an estimated 10–13% of
global production, and it sends about a quarter of its output to Europe.
Yet the typical firm is family-run, its workforce ageing, with no
in-house data or ESG staff. Table [\[tab:sector\]](#tab:sector) sets the
scene.

Y r **Indicator** & **Value**  
Global export rank & Top-3 by volume; \#4 by value (2023)  
Share of global production & ~10–13%  
Manufacturers in the cluster (Gangshan–Luzhu) & ~1,800
(~700 in the industry institute, TIFI)  
Annual export volume & ~1.2 million tonnes (2025)  
Annual export value & ~US$4.3–4.6 billion  
Share destined for Europe & ~one quarter  
Firm structure & Predominantly family-run SMEs (Taiwan: 1.715 M SMEs,
\>98% of all firms, MOEA White Paper 2025)  
CBAM-exposed steel-product SMEs (MOENV estimate) &
~2,600  
Taiwan’s CBAM export rank to the EU & 13th largest; 3.74 million tonnes
shipped  

### The door: a carbon border tax that lands in Rotterdam, not Gangshan

The EU’s Carbon Border Adjustment Mechanism (CBAM) puts a price on the
carbon embedded in imported steel, and screws and bolts (customs heading
CN 7318) have been in scope from the start. Since 1 January 2026 the
mechanism is in its definitive phase: 2026 imports accrue a certificate
obligation priced at the EU carbon market (official price 75.28 per
tonne of CO<sub>2</sub>e for Q2 2026); certificate sales open on the
common central platform in February 2027, and the first declaration and
surrender, covering 2026 imports, falls on 30 September
2027.<sup>\[6\]\[7\]</sup>

The legal duty sits on the *EU importer*, not on Mr. Lin — and that is
exactly what makes his position precarious. He is not summoned by a
regulator he can petition; he is silently re-scored by a procurement
spreadsheet in Rotterdam. If he supplies no data, his buyer falls back
on a country-specific “default value” that is deliberately marked up
(10% in 2026, rising to 30% from 2028).<sup>\[8\]\[32\]</sup>
Figure [1](#fig:country) shows what that default costs, by country of
origin.

![The certificate cost an EU buyer pays for a tonne of fasteners when
the supplier provides *no* data, by country of origin (2026, computed
from the Commission’s adopted default-value tables at the Q2-2026
certificate price). Taiwan’s default is among the mildest in the world;
the punitive figures belong to its competitors and, above all, to
countries with no entry in the book at
all.](proposal_assets/fig_cn7318_by_country.png)

Two facts follow, and we state both plainly because a judge will.
**First, Brussels has, in effect, written Taiwan a competitive advantage
into law**: a Taiwanese screw already costs its buyer about 300/t less
than a Chinese one, before anyone lifts a finger. **Second, precisely
because Taiwan’s default is mild, pure compliance is worth very little
to a Taiwanese carbon-steel maker** — about 4 per tonne, roughly NT$0.4
million a year. This is the honest correction at the centre of this
proposal: an earlier, widely repeated figure priced the “no-data
penalty” at 450–750/t. When we parsed the Commission’s *adopted*
tables with our own engine, that range turned out to describe China,
India and book-less countries — never Taiwan. We killed the claim rather
than ship it.

So CBAM, for Taiwan, is an *assist*, not a catastrophe — and the
proposal does not need it to be one. Its real role is as a **forcing
function**: the buyer’s letter is the first demand, of many now arriving
(EU product passports, Taiwan’s descending carbon-fee threshold,
corporate Scope-3 questionnaires), that only an *instrumented* factory
can answer. A factory that instruments itself to answer the letter has,
in the same act, acquired the sight it always lacked — and that sight,
not the 4, is where the value is. The next subsection shows what the
sight reveals.

### The first thing sight reveals: a pile the owner sells but cannot read

Here is the finding that reframes the whole project — stated carefully,
because the careless version of it is false. Mr. Lin is not blind to his
scrap: he collects it, sells it to a recycler, and banks the payment.
What he cannot see is the *information* inside the pile. The same
invoices and production logs that produce the compliance pack contain,
in plain sight, the ratio of steel bought to product shipped. In our
modelled sample that ratio is about **1.10 to 1**: for every tonne that
leaves as a finished screw, roughly 110 kg entered — the missing tenth
is heading slugs, trimming, coil ends, setup and rejects. Industry data
brackets the real range at about 5–15% (cold forming runs 85–95%
material utilization<sup>\[22\]</sup>), and some loss is physics — it
cannot go to zero. What varies, firm to firm and month to month, is *how
far above the floor* a factory is running — and that is exactly what
nobody in a 30-person firm can currently know, because knowing means
reconciling 22 dated invoices against a production log, per product
line, per month, for a year. Because the EU counts the mass *entering*
the process before cutting, this loss also sits inside the declared
carbon number whether anyone looks or not.
Table [\[tab:waste\]](#tab:waste) is our engine’s per-line output — the
attribution no small firm has ever seen — on three product lines from
two modelled firms.

Y r r r r r **Firm / product** & **Steel in** & **Product
out** & **Loss** & **Carbon (gross)** & **Purchase value**  
Firm A — carbon screws & 3,300 t & 3,000 t &
9.1% & 758 tCO<sub>2</sub>e/yr & NT$7.35 M/yr  
Firm B — carbon screws & 4,650 t & 4,200 t &
9.7% & 1,138 tCO<sub>2</sub>e/yr & NT$11.21 M/yr  
Firm B — **stainless** screws & 1,440 t &
1,300 t & 9.7% & 742 tCO<sub>2</sub>e/yr & NT$13.43 M/yr  
**Firm B total (gross / ~net)** & & & & **1,879
tCO<sub>2</sub>e/yr** & **NT$24.6 M / ~15–17 M**  

Read the stainless row twice. It is the *smallest* product in Firm B —
1,300 tonnes against 4,200 tonnes of carbon
steel — yet it accounts for 39% of the firm’s lost carbon and the single
biggest cash loss, because every tonne of scrapped stainless carries
about twice the carbon and nearly four times the money of a tonne of
carbon steel. The loss is not evenly spread, and without per-line
attribution the owner cannot know where it concentrates — or notice when
a wearing die quietly moves a line from 7% to 11% for three months.
Attribution plus the invoice dates is what turns a once-a-year
accounting curiosity into a *control loop*.

Now compare this lever with the “green” feature we built first — a
scheduler that shifts flexible loads to cleaner, cheaper hours. It is
genuinely useful and saves Firm A about NT$400,000 a year.
But as a *carbon* lever it is a rounding error next to yield, and it
does not touch the compliance number at all. Figure [2](#fig:lever) puts
the two side by side.

![For one factory, a 9.1%\(\rightarrow\)5% loss scenario removes about
359 tonnes of purchased embodied CO<sub>2</sub>e a year from the supply
chain — 80 times the 4.49 tonnes the grid-aware scheduler saves — and,
uniquely, it also lowers the declared CBAM number, because the scrapped
steel’s carbon is already inside the reported
figure.](proposal_assets/fig_waste_lever.png)

![Per-line attribution of the loss — gross embodied carbon, and money
stated both ways (purchase value and net of scrap resale). The smallest
line (stainless) is the largest loss: the kind of pattern that is
obvious on a corporate dashboard and invisible to a factory reconciling
invoices by hand once a year.](proposal_assets/fig_waste_by_product.png)

**We are careful with this number, and the tool is too — four
disciplines, enforced in the output itself.** (1) *The pile is not
trash:* scrap is sold and remelted; the owner already knows his
aggregate tonnage. What the tool adds is attribution, drift, carbon
linkage and benchmark — information, not the discovery of the pile.
(2) *Gross and net together:* the money column is purchase value;
resale recovers roughly 30–40% at current scrap prices, so the net cash
loss for Firm A is about NT$4–5 million, not NT$7.35 million — and the
tool prints both, at live prices. (3) *Reported vs. atmospheric carbon:*
the effect on the declared CBAM figure is exact and one-to-one (mass is
counted before cutting); the atmospheric effect is real but smaller than
the gross tonnage, because remelting recovers the iron, not the energy
already spent making the rod. We never claim 758 tonnes “avoided”.
(4) *The magnitude is provisional:* 9.1% is a synthetic mid-range
figure inside a documented industry band of ~5–15%; the mechanism is
certain, the pilot measures the magnitude, and the tool shows the owner
the curve rather than promising a number. It also does not yet claim to
know the process fix for his particular dies — that is a question for
the field, and for MIRDC’s engineers, not for a language model.

### What is actually in danger: stainless, and a hole in the EU’s book

The owner asked a sharp question: if Taiwanese carbon-steel fasteners
are safe, what does the data say is *not*? We scanned all 244 of
Taiwan’s goods against every other country in the EU’s adopted tables.
Carbon steel is unremarkable. But Taiwan’s entire *stainless* block sits
at roughly 2.6 times the world median — among the worst-rated on earth —
and the precursor a fastener plant actually buys, stainless wire rod
(CN 7221), has **no Taiwanese value in the EU’s book at all**. Of the
33 countries with a full steel book, exactly three lack this one row —
Taiwan, Thailand and Vietnam, the three fastener exporters — so every
Taiwanese stainless screw resolves to the EU’s punitive fallback (the
average of the ten dirtiest exporters).

The consequence is a paradox that only a tool reading the regulation
could surface, shown in Figure [4](#fig:stainless): the EU gives
stainless fasteners the *same mild default as carbon fasteners*, so the
honest actual number is more than double the default. Reporting
truthfully would cost the buyer an extra 228/t — so nobody reports, and
Taiwan’s worst carbon problem stays legally invisible.

![For stainless screws the EU default (224/t) is roughly half the honest
actual figure (452/t). The gap is a disincentive to tell the truth —
which is exactly why a *filing* tool would tell a stainless maker to
stay quiet, and a *waste* tool tells him the stainless in his scrap bin
is the most expensive thing he throws away, whatever he
files.](proposal_assets/fig_stainless_undercount.png)

This is the decisive argument for building a sight tool rather than a
filing tool. A filing tool, pointed at stainless, counsels silence. A
sight tool tells the same owner that his stainless line loses more than
the carbon-steel line three times its size — 742 tonnes of embodied
CO<sub>2</sub>e and NT$13.4 million a year at purchase value — and that
is true and actionable no matter what he sends to Brussels. (The absent
CN 7221 row may be a publishing defect rather than deliberate; either
way it is worth reporting to the Commission, which is part of our
open-data give-back in Section 5.2.)

### The divide, in the Handbook’s own three axes

The competition theme is “Digital Inclusion in the AI Era — ages,
regions, needs”. CarbonPass answers all three literally, with a number
attached to each:

  - **Ages.** An analog-native, sixty-plus owner-operator with no data
    professional in the building, asked to operate capabilities that are
    ordinary in a corporation.

  - **Regions.** Gangshan–Luzhu, a single nameable district of about
    1,800 firms of exactly this shape, whose economic
    identity is at stake.

  - **Needs.** Not “market access” in the abstract, but **NT$3.5 million
    a year and 359 tonnes of CO<sub>2</sub> that Mr. Lin cannot see** —
    and the enterprise-software capability to see them, delivered for
    the price of a photograph.

The gap is concrete: his 3,000-employee competitor runs
enterprise resource planning, a manufacturing execution system and a
sustainability team; yield is a weekly KPI. Mr. Lin has never seen his
once. That asymmetry — not broadband — is the digital divide this
project closes.

## Related stakeholders and their roles

The target audience is deliberately the party with the least capacity
and the most exposure: the owner-operator of a micro or small fastener
firm. Table [\[tab:stake\]](#tab:stake) lists the stakeholders and why
the SME owner is the chosen user.

l Y **Stakeholder** & **Role and benefit**  
**SME fastener owner-operator** & **Primary user and target audience.**
Photographs documents; receives the compliance pack, the waste map and
the fix-list. Chosen because the burden is heaviest and the existing
tools serve him least.  
EU importer / declarant & Legally liable for the CBAM declaration; the
party demanding data. CarbonPass produces the artifact they need in the
Commission’s format, protecting the trade relationship.  
Steel mill (e.g. China Steel) & Precursor supplier; an environmental
product declaration from the mill materially improves the pack. The tool
tells the owner exactly when to ask.  
MOENV / MOEA & Government front door (the CBAM help platform is
informational). CarbonPass is the missing computational layer, designed
to integrate rather than compete.  
MIRDC / TIFI & Industry research body and fastener institute; pilot
partners and channel to the cluster; source of real yield benchmarks.  
Accredited CBAM verifier & Independent assurance of actual data. The
tool produces the documentation a verifier needs; it never claims to
replace verification.  

## Description of solution functions

CarbonPass is a single pipeline with a conversational front end: one
extraction feeding four answers — the four questions a corporate
dashboard answers daily and a small factory has never been able to ask.
The owner never sees the machinery; he sees a chat that asks for a photo
and returns answers. Figure [\[fig:pipe\]](#fig:pipe) shows the flow.

**PHOTO** electricity bill · steel e-invoices · production log  
\(\downarrow\)*on-device ingestion — qwen3-VL 4B, offline, 18–31
s/doc*  
**ACTIVITY DATA** energy, material mass & price, output tonnes (with
uncertainty)  
\(\downarrow\)\(\downarrow\)\(\downarrow\)\(\downarrow\)  

|                                                                          |                                                                           |                                                       |                                               |
| :----------------------------------------------------------------------- | :------------------------------------------------------------------------ | :---------------------------------------------------- | :-------------------------------------------- |
| **“What’s in my product?”**CBAM data pack — the buyer’s letter, answered | **“What do I lose?”**waste map: per-line loss, gross & net, monthly drift | **“When should machines run?”**schedule + bill saving | **“Am I normal?”**anonymised sector benchmark |

**Sight 1 — “What carbon is in my product?” (the Data-Pack Engine).**
Document intelligence ingests bills, invoices and production records
on-device. The engine then does the two computations generic calculators
cannot: *allocation* of facility energy across product lines and CN
codes with quantified uncertainty, and *assembly* of the per-product
specific embedded emissions in the Commission’s own template, every
field flagged actual / default / needs-attention. It also produces an
organizational inventory as a by-product for banks, the descending
domestic carbon-fee threshold, and customer questionnaires.

**Sight 2 — “What do I lose between buying and shipping?” (the Waste
Map).** From the same extracted data — steel mass *and* unit price from
the e-invoices, output tonnes from the production log — it computes
yield per product per CN code, the carbon and the money in the loss
(gross and net of scrap resale, always both), and what a target loss
rate is worth. Because the invoices are dated, it tracks loss month by
month, turning a once-a-year blind spot into a control loop that flags a
drifting die in weeks. This is the sight no competitor offers and the
one that *reduces* rather than merely reports (Section 2.5.1).

**Sight 3 — “When should my machines run?” (the Grid-Aware Scheduler).**
Using Taiwan’s open 10-minute grid feed and time-of-use tariffs, it
shifts flexible loads (furnaces, compressors) against order deadlines to
cut the electricity bill and grid-driven emissions, with a documented
before/after ledger. We are precise about its place: it saves real money
(a measured NT$399,800/yr for Firm A) but its carbon effect
is small and outside the CBAM certificate scope for steel, so the tool
itself ranks it last, honestly.

**Sight 4 — “Am I normal?” (the sector benchmark).** No fastener SME can
currently know whether its loss rate or its energy per tonne is good,
bad or ordinary, because no benchmark exists. CarbonPass aggregates
anonymised yield and energy-intensity figures across participating firms
and gives every owner his percentile. This is also the project’s
open-data give-back (Section 5.3) — and, as Section 2.5.1 argues, the
mechanism that turns one firm’s sight into sector-scale reduction.

**The interface — and the inclusion claim.** The whole system fronts as
a conversational assistant in LINE, Mandarin/Taiwanese-first,
voice-friendly, with zero ESG vocabulary. “拍一張電費單” — snap a
photo of the power bill — is the entire onboarding. And it runs on the
excluded side of the wall: the document model is a 4-billion-parameter
vision-language model that reads the bill offline, on a laptop, with no
GPU and no cloud. Raw documents never leave the factory; only the
outputs the owner chooses to send do. That is digital inclusion
delivered as a property of the product, not a promise on a slide.

### How this actually reduces emissions

A reporting tool changes a spreadsheet; a reduction happens in the
factory. Our theory of reduction is the oldest one in industry — *you
can only manage what you can measure* — and it is the same mechanism
that made yield a weekly KPI in every corporation: information, not
exhortation. CarbonPass makes the measurement free and then ranks the
levers honestly, in the order our own numbers support:

1.  **Yield** (structural). Every percentage point of loss is roughly
    one percent of the firm’s steel purchases and of its precursor
    emissions, and it moves the declared EU number one-for-one. At
    Firm A, a 9.1%\(\rightarrow\)5% scenario is worth ~359
    tCO<sub>2</sub>e and ~NT$3.5M a year — **80\(\times\)** the
    scheduler’s carbon effect. The monthly drift alert is the operative
    feature: catching a wearing die in weeks instead of never.

2.  **Precursor choice and the mill EPD** (supply chain). One document
    from the steel mill — an environmental product declaration — changes
    the buyer’s cost by a measured ~60/t (Firm C); and the EU’s own
    tables price electric-arc (scrap-route) wire rod at a fraction of
    blast-furnace rod, so the tool can quantify, per firm, what cleaner
    sourcing is worth. The factory cannot decarbonise the mill, but it
    can choose, ask, and prove.

3.  **Process energy** (the heat-treatment load). Heat treatment and
    surface treatment are the cluster’s dominant electricity draws.
    Per-tonne energy intensity, benchmarked across firms, exposes the
    outliers — and today an outlier cannot know it is one. Sight
    precedes every retrofit.

4.  **Load shifting** (timing). Measured NT$399,800/yr and
    4.49 tCO<sub>2</sub>e for Firm A — real money, small carbon, ranked
    last by the tool itself.

5.  **The cluster multiplier.** The anonymised benchmark converts each
    firm’s private improvement into sector-wide pressure, exactly as
    corporate KPI culture did — ~1,800 firms discovering
    what “normal” is, with no mandate required.

Trust is part of the reduction mechanism: a tool that states gross and
net, distinguishes the declared number from the atmosphere, and is able
to tell an owner “this lever is not worth it for you this year” is a
tool an owner will follow into the levers that are.

## Differences from existing solutions

Taiwan’s government has moved, but every existing instrument stops short
of the artifact that decides procurement — and none of them looks at
waste at all. Table [\[tab:audit\]](#tab:audit) is a verified capability
audit.

l Y Y **Instrument** & **What it does** & **What it does
*not* do**  
CAAS SME service station (MOEA) & Courses, articles, consultant
referrals & No computation of any kind  
IDB Carbon Calculator (MOEA) & Rough annual organizational
CO<sub>2</sub>e from bills & No product-level allocation; no CN-code
output; no waste  
MOENV CBAM Help Platform (2026) & Information hub, consultation channel
& Explicitly informational; computes nothing  
Taipower app / eBill & Consumption charts, tariff simulation & No
emissions conversion; no compliance artifact  
Private ESG SaaS & Organizational inventories; advisory content &
Subscription + consultant-mediated; no per-product packs for micro-SMEs;
no yield analysis  
Consultants + MIRDC counseling & Real ISO/CBAM certifications, partly
subsidised & One-off, per-engagement; cannot service recurring
per-product data across 2,600 firms  
**CarbonPass** & **SME documents \(\rightarrow\) importer-ready pack
*and* a waste map, on-device, near-zero marginal cost** & **—**  

The gap, stated precisely: no instrument in Taiwan converts *SME-native
documents* into an *importer-ready, per-CN-code embedded-emissions pack*
at near-zero marginal cost — and *none of them measures the waste at
all*. The government stack ends at awareness; the market stack prices
out the small end; and nobody has turned the compliance data around to
show the owner his own losses. Two things are genuinely novel. First,
the **waste lever falls straight out of the Commission’s own emissions
formula** — where the ratio of input mass to output is a first-class
term — yet everyone read that formula as an accounting rule to satisfy,
never as an optimization target to attack. Second, the **edge tier**: a
4-billion-parameter model that reads a Traditional-Chinese bill
perfectly on commodity hardware is the inclusion argument made concrete,
not a footnote about efficiency.

## Expected benefits (quantified)

Table [\[tab:benefits\]](#tab:benefits) gives the quantified benefits,
each with its basis and its honest caveat. Figures are per firm and per
year unless stated; all are engine-computed from the sources in
Section 5.

Y l Y **Benefit** & **Quantification** & **Basis /
caveat**  
Loss made visible (carbon, gross) & 758 tCO<sub>2</sub>e/yr (Firm A);
1,879 t (Firm B) & Engine from invoices + log; remelt
caveat always stated  
Loss made visible (money) & gross NT$7.35 M / net ~NT$4–5 M (Firm A) &
Purchase value from e-invoices; net after ~30–40% scrap resale
recovery<sup>\[23\]</sup>  
Recoverable at 5% target loss & ~359 tCO<sub>2</sub>e and NT$3.5 M/yr
(Firm A) & Scenario, not a promise; owner sets the target  
Yield’s effect on the CBAM number & SEE 2.924 \(\rightarrow\) 2.805;
9/t, 27k/yr to the buyer & Exact 1:1 via the mass-before-cutting rule  
Electricity bill saving (scheduler) & NT$399,800/yr + 4.49
tCO<sub>2</sub>e (Firm A, measured) & Live grid feed + TOU tariff; small
carbon, real money  
Compliance / trade-relationship & Buyer keeps the supplier whose pack
arrives & Retention argument; Taiwan default mild (~4/t)  
Time and cost to produce the pack & Minutes, near-zero marginal cost &
vs. per-engagement consultant economics  
Cluster-scale potential & ~1,800 firms \(\times\) ~10%
steel binned & Extrapolation; pilot will calibrate the loss rate  

The headline is deliberately not the 4/t compliance margin — we retire
that overstatement rather than lean on it. The headline is that a single
photograph now surfaces *millions of NT$ and hundreds of tonnes of
CO<sub>2</sub> per firm* that were previously invisible, in a cluster of
about 1,800 firms, using a tool that costs the owner
nothing per use.

# Project maturity

## Development stage

CarbonPass is an advanced, working proof of concept, not a concept
sketch. As of mid-July 2026 the following is demonstrable and
reproducible from the repository, with 25+ automated tests green:

  - **End-to-end ingestion** of a Taipower bill photograph, MIG 4.0
    e-invoices and a production log into structured activity data, with
    a second OCR pass back-checking every number.

  - **The compliance engine** reproduces the European Commission’s own
    worked “screws and nuts” example to a relative tolerance of
    \(10^{-9}\), and fills the Commission’s real 19-sheet template such
    that its formula cells independently recompute to the engine’s
    values.

  - **The rules engine is already global**: it parses all 120 country
    sheets and 12,532 default-value rows of the adopted
    tables with zero failures, and computes emissions for cement,
    aluminium and fertiliser as well as steel.

  - **The Waste Map** runs today on two firms from real document
    formats, producing Table [\[tab:waste\]](#tab:waste).

  - **The scheduler** runs against Taipower’s live 10-minute feed and
    produces the measured NT$399,800/yr plan.

  - **Module 3** runs as a FastAPI service with a LINE webhook and a
    credential-free simulator demonstrating the full conversation
    end-to-end.

The single most important maturity result is the edge-tier benchmark in
Figure [5](#fig:4b), because it is the inclusion claim in numbers.

![Field-extraction accuracy on phone-photo utility bills across six
synthetic distortions. The 4-billion-parameter model runs offline on a
laptop at 100% and 18–31 s per document; a larger challenger model drops
to 66%, concentrating its errors on exactly the tariff-table fields a
verifier cares about. The small model is not a compromise — on this
corpus it is the better tool, and it is the one Mr. Lin can actually
run.](proposal_assets/fig_4b_accuracy.png)

## Project adjustments

The project has not been sold or awarded elsewhere; no 50% modification
applies. Internally, we made two adjustments in the open and carry them
as evidence of rigour rather than hiding them: (1) we retired the
450–750/t “penalty” figure once our engine showed it described
Taiwan’s competitors, not Taiwan; and (2) we corrected a
precursor-mapping error that had made stainless screws look cleaner than
carbon ones, which is what surfaced the stainless finding in
Section 2.3.4. Both corrections came from checking our own claims
against primary sources — the discipline we are asking a judge to
reward.

## Demonstration

The submission includes a recorded walkthrough: two bill photographs
into the LINE simulator, returning the acknowledgement, the compliance
pack, the waste map and the schedule reply. The engine, tests and
reproduction commands are in the repository; every figure and table in
this document regenerates from committed scripts.

## Existing validation fields

Validation to date is on a deterministic synthetic corpus modelled on
real formats (public Taipower bill layouts and the Ministry of Finance
e-invoice specification), which lets us pin correctness against ground
truth. The decisive external validation — real consented bills, real
yields — is the explicit purpose of the mentorship-phase pilot in
Gangshan, in cooperation with a cluster firm and, we hope, MIRDC or the
Kaohsiung EPB advisory team. We do not overstate: the mechanism is
proven; the field magnitudes are what the pilot measures.

## Existing validation results and verification plan

Measured results so far: 100% field extraction across six phone-photo
distortions on the 4B and 8B models; the Commission worked example
reproduced at \(10^{-9}\); the waste map computed for three product
lines; the scheduler’s NT$399,800/yr plan against the live
grid feed. The verification plan is staged to the PHIT calendar
(Table [\[tab:calendar\]](#tab:calendar)). We are candid about the
regulatory reality behind “verification”: as of mid-July 2026 no CBAM
verifier is yet accredited anywhere in the world; eight EU national
accreditation bodies now accept applications from third-country
verifiers (up from four earlier in the year), and the Commission expects
the first accreditations around September 2026 — squarely inside this
Hackathon’s mentorship window. The pilot’s aim is therefore to have a
generated pack reviewed for structure by a Taiwanese GHG-verification
body (Taiwan has 20 such bodies and 200+ specialists whose path to EU
accreditation is only now opening), not to claim a certification that
does not yet exist for anyone.

l Y **Window** & **Deliverable**  
Now \(\rightarrow\) 31 Jul (submission) & Working PoC: ingestion,
compliance engine, waste map, scheduler, LINE simulator; demo video;
this proposal.  
6–16 Aug (preliminary) & Scored on proposal + credible start
(Feasibility 40%, Innovation 30%, Social Impact 30%).  
Mid-Sep \(\rightarrow\) mid-Oct (mentorship) & One real pilot firm in
Gangshan: real bills in, real pack + waste map out; structure reviewed
by a verification body; one flexible load shifted and measured; first
real yield benchmark.  
Late Oct (final) & Live demo + measured pilot deltas (Implementation &
Verification, 30%, scored on progress since submission).  
Dec (awards) & —  

# Future plans

## Promotion and adoption plan

The Presidential Hackathon is a policy-adoption pipeline, not a product
launch, and CarbonPass is engineered for it. The adoption path is: (1) a
working PoC at submission; (2) a government-connected pilot in Gangshan
during mentorship, using PHIT’s own public-private matchmaking and
field-validation support; (3) integration with the front door the state
has already built — MOENV’s informational CBAM platform and MOEA’s SME
service network — as the computational layer they lack. Distribution to
the cluster runs through the fastener institute (TIFI, ~700 members)
and MIRDC counseling channels, and through the one interface every owner
already uses, LINE. Claiming full national deployment now would score
*worse* under Feasibility than demonstrating an honest, moving
trajectory — so we stage it.

## Engaged collaboration units

The proof of concept requires no partnerships and uses only open data,
by design. For the pilot we are pursuing expressions of interest from a
TIFI member firm and from MIRDC / the Kaohsiung Environmental Protection
Bureau’s advisory team. We state plainly that these are targets, not yet
secured commitments, as of submission.

## Future planned collaboration units and the expansion sequence

The same engine that serves Taiwan’s cluster is already global in its
computational core, which is why the idea has a future well beyond
fasteners. Table [\[tab:expand\]](#tab:expand) gives the sequence.

l Y **Stage** & **Description**  
Beachhead (2026) & Taiwan fasteners (CN 7318), live compulsion; MOENV /
MOEA / MIRDC / TIFI.  
Downstream steel & aluminium (2028) & The EU has proposed extending CBAM
to ~180 further product categories (obligations from 1 Jan 2028); the
Council agreed its position in June 2026, the Parliament’s committee
stage passed in July, and the plenary vote is expected September 2026 —
inside this Hackathon’s mentorship window. If it passes, the exposed
Taiwanese population multiplies well beyond 2,600 firms.  
Digital Product Passport sectors (2027–2030) & The EU’s product-passport
registry demands machine-readable product sustainability data —
structurally the same output CarbonPass already generates.  
Domestic carbon-fee entrants (2027 onward) & As Taiwan’s fee threshold
falls, more of its 150,000+ manufacturing SMEs become
reporters; the org-inventory by-product is their on-ramp.  
New Southbound economies & Taiwan builds and proves the tool on its own
cluster, then offers it to the ASEAN and South Asian producers who need
it most — the international track’s entire purpose.  

That last row rests on a finding worth stating, because it is the
strongest social-impact argument the project has. Holding a factory’s
physics fixed and changing only its country of origin, the reward for
proving its carbon ranges from about 4/t in Taiwan to 177/t in a country
with no entry in the EU’s book — 44 times the reward for identical
emissions, decided by a passport (Figure [6](#fig:moved)). The cruelty
is in the correlation: the reward for proving is highest exactly where
the capacity to prove is lowest. Taiwan — which needs the tool least,
and has world-class open data, idle verification capacity and a
government at the front door — is best placed to build it and give it to
the economies that need it most.

![The same factory, the same carbon, moved between countries: the reward
for proving actual emissions is set not by how clean the factory is but
by whether the EU happens to hold a data book for its country. This is
the global provability divide the beachhead tool is designed to travel
to. (For Thailand the reward is negative — its default is cleaner than
its truth — and the tool must be honest enough to say “don’t bother”,
which ours is.)](proposal_assets/fig_same_factory_moved.png)

# Open data

## Open-data sources used

The proof of concept is built entirely on open data and published
methodology. Table [\[tab:opendata\]](#tab:opendata) lists the sources;
all are accessible now, with no partnership required.

Y Y **Source** & **Role**  
MOENV carbon-footprint emission coefficients (data.gov.tw \#28176;
OpenAPI) & Material / fuel / process emission factors  
Taiwan product carbon-footprint registry (data.gov.tw \#8992) &
Benchmarks, sanity checks  
Electricity emission factor: 0.467 kgCO<sub>2</sub>e/kWh for 2025, first
published with an industrial split of 0.466 (MOEA Energy Administration,
Jun 2026; supersedes 2024’s 0.474 — the tool tracks the moving figure) &
Scope-2 and scheduler math  
Taipower generation-by-unit, 10-minute (data.gov.tw \#8931 live /
\#37331 historical) & Hourly grid-carbon-intensity curve  
Taipower time-of-use rate schedules & Price signal for the scheduler  
EU CBAM adopted default values (Impl. Reg. 2025/2621) and benchmarks
(2025/2620) & Output schema; per-country default rows; the waste and
cost math  
EU CBAM communication template + filled “screws and nuts” example &
Output format; golden test  
Official CBAM certificate prices (Commission quarterly) & Live cost
conversion  
Ministry of Finance e-invoice (MIG 4.0) specification & Ingestion of
steel and fuel invoices  

## Suggestions for modifying open data

Parsing the EU’s adopted tables with our own engine surfaced concrete,
reportable defects that we will feed back to the Commission, DG TAXUD
and MOENV. The most consequential: **stainless wire rod (CN 7221) has no
value for Taiwan, Thailand or Vietnam** — the three fastener exporters —
so their stainless resolves to the punitive fallback; this is most
likely a publishing omission and is worth correcting. We also documented
inconsistent CN-code formatting that will silently break naive data
joins (the entire aluminium block is stored unspaced), three different
dash characters used for “no value”, a handful of aluminium goods with
neither a benchmark nor a fallback, and five cement rows whose mark-up
contradicts their own sheet headers. Each is a small fix that materially
improves a dataset thousands of firms will rely on.

## Provision of open data (given back)

CarbonPass publishes two open datasets in return. First, a cleaned,
machine-readable **hourly Taiwan grid-carbon-intensity dataset** derived
from the Taipower 10-minute feed — directly useful to any firm or
researcher doing carbon-aware scheduling. Second, and more valuable to
the cluster, the first anonymised **fastener-sector yield benchmark**: a
table that lets every firm see whether its ~10% loss is good, bad or
ordinary — something no firm can learn today, and worth more to the
sector than any grid dataset. Both are openly licensed, and the team is
willing to release the compliance-engine core as open source.

# References

Taipei Times, “MOENV to set up CBAM help platform for SMEs,” 2 Mar 2026
(3.74 M t; ~2,600 SMEs; 13th-largest CBAM exporter;
importer-level aggregation).

Focus Taiwan / Taipei Times, first carbon-fee cycle results, Jun 2026.

European Commission, DG TAXUD — CBAM definitive-regime pages, Q\&A
(27–28 May 2026) and operator guidance.

European Commission, “CBAM default values as adopted” workbook
(machine-readable Impl. Reg. (EU) 2025/2621), v20260204 — per-country
\(\times\) CN-code tables; parsed and unit-tested by the CarbonPass
engine.

European Commission, CBAM benchmarks workbook (Impl. Reg. (EU)
2025/2620) — free-allocation adjustment benchmarks.

European Commission, CBAM communication template for installations v2.1
+ filled “Steel 3: Screws and nuts” example — reproduced by the engine
at \(10^{-9}\).

European Commission, CBAM certificate price publications (75.36 Q1 2026;
75.28 Q2 2026).

European Commission, “State-of-play CBAM accreditation” (retrieved 17
Jul 2026): 24 accreditation bodies, 4 accepting third-country
applications; zero verifiers accredited worldwide as of mid-2026.

MOENV (Taiwan), *Major Environmental Policies*, Mar 2026 — 20
GHG-verification bodies and 200+ specialists; zero EU applications;
EU-side blockers.

Akin / Covington / SteelOrbis (2026) — CBAM downstream extension (~180
categories), Council position, EP plenary vote timing.

MOEA SME Administration, 2025 White Paper on SMEs (1.716 M SMEs;
family-firm structure).

CommonWealth Magazine (2023); Kaohsiung Times (2026); Fastener World
(2024–25) — fastener cluster scale, export value/volume, share to
Europe.

Goebel Fasteners / PRNewswire (2024); TIFI profile —
~1,800 manufacturers, ~700 institute members.

MOEA Energy Administration — electricity emission factors: 0.474
kgCO<sub>2</sub>e/kWh (2024); 0.467 overall / 0.466 industrial (2025,
published 2 Jun 2026).

J. McLeod (Crowe UK), “The new reality of CBAM,” *Fastener + Fixing
Magazine*, 9 Feb 2026 — independent corroboration that Taiwan’s default
is mild (150/t vs Türkiye 400, China 500).

data.gov.tw open datasets \#28176 (MOENV coefficients), \#8992
(product-footprint registry), \#8931 / \#37331 (Taipower
generation-by-unit).

ESPR (EU) 2024/1781 — Digital Product Passport registry (from Jul 2026);
staged sector rollout 2027–2030.

Business Standard (28 Jan 2026); Free Press Journal (9 Jul 2026) —
Indian MSME CBAM impact and proposed certification-cost subsidy (context
for the global divide).

MODA / Taipei Computer Association — 2026 Presidential Hackathon
International Track Handbook (theme, criteria, schedule, application
form).

Ministry of Finance (Taiwan) — electronic-invoice MIG 4.0 specification.

IoT Analytics, *MES Market Report 2025–2031* (Dec 2025): 54% of small-
and mid-sized plants use pen & paper or spreadsheets as their MES; only
8% use a commercial MES. ASQ cost-of-poor-quality literature: typically
10–20% of revenue; APQC benchmarks: scrap and rework ~2.2% of revenue
at the median.

MacLean-Fogg, “Cold Forming vs. Machining”; The Federal Group USA;
industry cold-heading analyses — cold-forming material utilization
85–95%, far above machining.

Argus / LME Steel Scrap CFR Taiwan (US$345–360/t in Q2 2026, ~US$325/t
mid-July 2026); Taiwan domestic wire-rod prices
~NT$27,000/t (Apr 2026); Taiwan scrap-recycling price
surveys — basis of the ~30–40% resale-recovery estimate. All prices
move; the tool computes gross and net at current prices.

*Reproducibility note.* Every quantitative claim in this proposal
— the waste table, the country default chart, the same-factory-moved
comparison, the stainless under-count, the model-accuracy benchmark and
the scheduler ledger — is generated by the team’s own code from the open
sources in Table [\[tab:opendata\]](#tab:opendata) and the EU’s
published tables, and regenerates from committed scripts. Where a figure
is a scenario, an estimate or a synthetic-corpus magnitude, it is
labelled as such in the text.
