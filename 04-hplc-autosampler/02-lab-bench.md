# Part 02 — The lab bench, person by person

> **Job:** Put a face on the bench. The arm is being built to take work
> off real people, so here are **three lab workers** whose day it could
> change — a pharma QC analyst, a high-volume contract-lab technician,
> and an R&D method-development scientist. For each we walk the whole
> day, section by section, and mark every task as **Full-auto**,
> **Human-assisted**, or **Human-led** for a first-generation
> fixed-arm cell. The pattern that falls out is the v1 scope.

> **Note.** The three people are realistic composites, not specific
> individuals. Times, volumes, instruments, and method names are typical
> industry examples and vary by lab — treat numbers as `~` and re-check
> before quoting. See [`01-hplc-intro.md`](01-hplc-intro.md) for the
> plain-language background this builds on.

## Why this matters to you (even if you've never seen a lab)

You rely on these labs every day without noticing. Almost nothing you
swallow, drink, or put on your skin reaches you until a person at a bench
has answered one question about it: *is this really what the label says,
and is it safe?*

A few things you have probably used today, and the lab work behind them:

| Something you used today | The question a lab answered | Who below |
|---|---|---|
| A painkiller or a vitamin | Does each pill hold the right dose, with no harmful impurities? | Priya |
| A glass of tap water | Is it free of lead, pesticides, and sewage? | Marco |
| Washed salad or imported fruit | Are pesticide residues under the legal limit? | Marco |
| A brand-new medicine or supplement | Does the test that proves all this even exist yet? | Sarah |
| The expiry date on any of them | How fast does it go off, and how should you store it? | Sarah |

Behind every one of those answers is the slow, repetitive bench work this
document walks through — and that bench work is exactly the part a robot
arm could take over. You need no chemistry to follow along; just keep the
product in your hand in mind as you read.

## How to read this

Every task below gets one of three labels. The whole point of the
document is to sort the day into these three buckets:

- **Full-auto** — the fixed-arm cell can do this **end to end,
  unattended**: well-defined, repetitive, fixed-geometry work on
  standard labware. This is the v1 target.
- **Human-assisted** — the arm does the **repetitive bulk**, but a
  person sets it up, supervises, or handles the exceptions. A later
  milestone, or a shared human-plus-arm station.
- **Human-led** — stays with a person for now: it needs **judgment,
  fine dexterity, or a regulatory signature** the arm should not own.

A quick mental test: *if the same motion repeats on identical labware in
a fixed place, it's Full-auto; if it needs a decision or a delicate,
variable touch, it drifts toward Human-led.*

## Index

- [Why this matters to you](#why-this-matters-to-you-even-if-youve-never-seen-a-lab)
- [How to read this](#how-to-read-this)
- [Person 1. Priya, a pharmaceutical QC analyst](#person-1-priya-a-pharmaceutical-qc-analyst)
  - [What Priya actually tests — three familiar drugs](#what-priya-actually-tests--three-drugs-from-your-bathroom-cabinet)
  - [P1. Sample receipt and login](#p1-sample-receipt-and-login)
  - [P2. Weighing and measuring](#p2-weighing-and-measuring)
  - [P3. Sample preparation](#p3-sample-preparation)
  - [P4. Standards and reagents](#p4-standards-and-reagents)
  - [P5. Filling, capping and labelling vials](#p5-filling-capping-and-labelling-vials)
  - [P6. Building the tray and loading the instrument](#p6-building-the-tray-and-loading-the-instrument)
  - [P7. Starting and watching the run](#p7-starting-and-watching-the-run)
  - [P8. Data review and reporting](#p8-data-review-and-reporting)
  - [P9. Documentation and compliance](#p9-documentation-and-compliance)
  - [P10. Housekeeping and cleanup](#p10-housekeeping-and-cleanup)
  - [Priya summary table](#priya-summary-table)
- [Person 2. Marco, a contract-lab sample-prep technician](#person-2-marco-a-contract-lab-sample-prep-technician)
  - [What Marco actually tests — three everyday samples](#what-marco-actually-tests--three-samples-from-everyday-life)
  - [M1. Sample receipt and accessioning](#m1-sample-receipt-and-accessioning)
  - [M2. Aliquoting and batching](#m2-aliquoting-and-batching)
  - [M3. Adding surrogates and internal standards](#m3-adding-surrogates-and-internal-standards)
  - [M4. Extraction](#m4-extraction)
  - [M5. Concentration](#m5-concentration)
  - [M6. Filling, capping and labelling vials](#m6-filling-capping-and-labelling-vials)
  - [M7. Loading the autosamplers](#m7-loading-the-autosamplers)
  - [M8. Holding times and batch QC](#m8-holding-times-and-batch-qc)
  - [M9. Monitoring and re-prep](#m9-monitoring-and-re-prep)
  - [M10. Cleanup and waste](#m10-cleanup-and-waste)
  - [Marco summary table](#marco-summary-table)
- [Person 3. Sarah, an R&D method-development scientist](#person-3-sarah-an-rd-method-development-scientist)
  - [What Sarah actually builds — the test behind a familiar pill](#what-sarah-actually-builds--inventing-the-test-behind-a-familiar-pill)
  - [S1. Designing the experiment](#s1-designing-the-experiment)
  - [S2. Forced-degradation sample prep](#s2-forced-degradation-sample-prep)
  - [S3. Standards and serial dilutions](#s3-standards-and-serial-dilutions)
  - [S4. Column and mobile-phase changeover](#s4-column-and-mobile-phase-changeover)
  - [S5. Filling, capping and labelling vials](#s5-filling-capping-and-labelling-vials)
  - [S6. Running short sequences](#s6-running-short-sequences)
  - [S7. Reading the data and deciding](#s7-reading-the-data-and-deciding)
  - [S8. Iterating](#s8-iterating)
  - [S9. Documentation](#s9-documentation)
  - [S10. Validation runs](#s10-validation-runs)
  - [Sarah summary table](#sarah-summary-table)
- [What this means for v1 scope](#what-this-means-for-v1-scope)

---

## Person 1. Priya, a pharmaceutical QC analyst

> **Where you've already met her work:** every tablet in your bathroom
> cabinet — the paracetamol you take for a headache, your grandparent's
> blood-pressure pill, your child's antibiotic — was checked by someone
> doing Priya's job before a regulator allowed it onto a shelf. When the
> box says *500 mg*, she is the reason you can believe it.

Priya works in the quality-control (QC) lab of a mid-size generic-drug
manufacturer. Everything she touches is under **GMP** (Good Manufacturing
Practice), every record is governed by **21 CFR Part 11** (the US rule
for electronic records and signatures), and her methods come straight
from the **USP** (the United States Pharmacopeia) or the company's own
validated copies of them. She tests **finished products** — tablets and
capsules — and **incoming raw materials**, running four staple kinds of
test: **assay** (how much active ingredient), **related substances**
(impurities), **dissolution** (how fast the drug releases), and
**content uniformity** (dose-to-dose consistency).

Her bench has three liquid-chromatography systems — a mix of HPLC and
UHPLC (think Agilent 1260 / Waters Alliance class) — all driven from a
single **chromatography data system** (CDS) such as Waters Empower. Next
to them sit an **analytical balance** readable to **0.1 mg**, a rack of
**Class A volumetric flasks** (10, 25, 50, 100 mL), micropipettes, a
sonicator, a box of **2 mL autosampler vials** with 9 mm screw caps, a
syringe-filter bin, and a label printer wired to the **LIMS** (the
Laboratory Information Management System that hands her the day's
worklist).

A typical day: she gowns up and logs in by 7:30, reviews her LIMS
worklist, and pulls the day's samples from controlled storage. From about
8:00 to noon she is **at the bench preparing samples and standards**. By
midday she has built a sequence of **60–100 vials**, loaded an
autosampler, and started a run that finishes overnight. The afternoon is
**dissolution testing, second-person review of a colleague's paperwork,
and reviewing yesterday's chromatograms** — including any result that
fell outside specification and triggered an investigation. The arm would
empty out her morning; it barely touches her afternoon.

### What Priya actually tests — three drugs from your bathroom cabinet

Priya's four staple tests sound abstract until you pin each one to a
tablet you have actually swallowed. So here is every test made concrete
on a **very familiar drug** — the exact question it answers, what she is
physically measuring, and step by step how the sample travels from the
blister pack to the 2 mL vial.

> **Numbers are illustrative.** Weights, volumes, wavelengths, and limits
> below are representative of published pharmacopoeial methods (USP and
> equivalents) but **vary by monograph, strength, and lab**. Treat every
> figure as `~` and check the current monograph before quoting it.

A one-line orientation on the four tests, each tied to its example below:

| Test | The plain-English question | Example drug |
|---|---|---|
| **Assay** | Is the labelled dose really in there? | Paracetamol 500 mg |
| **Related substances** | Has any of it turned into something harmful? | Aspirin ~300 mg |
| **Dissolution** | Will it release in your body in time? | Ibuprofen 200 mg |
| **Content uniformity** | Does *every* tablet carry the same dose? | Ibuprofen 200 mg |

#### 1. Assay — "is there really 500 mg in this paracetamol tablet?"

**The drug:** plain paracetamol (US name: acetaminophen; brands Panadol,
Tylenol) — the 500 mg tablet in nearly every home.

**What she is answering:** does each tablet hold **90–110%** of its
labelled 500 mg of active ingredient? Below that the patient is
under-dosed; above it edges toward the dose that harms the liver. The
assay is the test that would catch a mixing or compression error that
left a whole batch sitting at, say, 430 mg or 560 mg a tablet.

**What she physically measures:** the **size of the paracetamol peak**
from the sample, compared with the peak from a known-weight **reference
standard**. The HPLC separates paracetamol from everything else in the
tablet (binder, filler, coating), and the detector — set to **~243 nm**,
the wavelength paracetamol absorbs strongly — draws one clean peak whose
**area is proportional to how much drug is present**.

**How the sample is prepared** — the chain Priya runs at the bench:

1. **Sample the batch fairly.** Take **≥20 tablets** at random from the
   batch, weigh them all together, and grind to a fine, even powder, so
   one scoop represents the *average* tablet, not one lucky pill.
2. **Weigh out one tablet's worth.** If the average tablet weighs
   ~600 mg, weigh ~600 mg of the powder (≈500 mg of paracetamol) on the
   0.1 mg balance into a **500 mL volumetric flask**.
3. **Dissolve.** Add ~350 mL of **diluent** (typically a water/methanol
   mix), **sonicate** ~10–15 min to break up the powder and dissolve the
   drug, then let it cool back to room temperature.
4. **Make to the mark.** Top the flask up to exactly the 500 mL line and
   mix. The solution is now nominally **~1 mg/mL** of paracetamol.
5. **Dilute into range.** The detector would be saturated at 1 mg/mL, so
   she pipettes **5 mL into a 50 mL flask** and fills to the mark
   (→ ~0.1 mg/mL), often repeating once more to land near the method's
   working **~0.01 mg/mL**.
6. **Filter into the vial.** Draw the final solution through a 0.45 µm
   syringe filter into a 2 mL vial (first ~0.5 mL to waste so the filter
   is rinsed), cap, and barcode-label it.
7. **Prepare the standard identically.** Weigh ~50 mg of **USP
   Acetaminophen Reference Standard** and carry it through the *same*
   dilution chain to the *same* ~0.01 mg/mL, so sample and standard are
   directly comparable.

**Reading it:** % of label ≈ (sample peak area ÷ standard peak area) ×
(standard concentration ÷ sample's nominal concentration) × 100,
corrected for the exact weights used. A result of **99.2%** passes;
**112%** or **88%** fails and triggers an out-of-spec investigation (see
[P8](#p8-data-review-and-reporting)).

#### 2. Related substances — "is this aspirin turning into something harsher?"

**The drug:** aspirin (acetylsalicylic acid), the ~300 mg tablet.

**The everyday hook:** that **vinegar smell from an old bottle of
aspirin** is this test made audible. Aspirin slowly **hydrolyses** back
into **salicylic acid** (harsher on the stomach) plus acetic acid (the
vinegar smell). The "related substances" test measures exactly how much
salicylic acid has formed.

**What she is answering:** is **free salicylic acid** below its limit —
typically **~0.3%** of the aspirin content? This is the safety-and-
stability test: run on fresh batches, and again on samples pulled from
storage at 3, 6, 12 months to set the **expiry date**.

**What she physically measures:** a **tiny** salicylic-acid peak sitting
beside the huge aspirin peak. Because the impurity is hundreds of times
smaller than the drug, the prep is *flipped* from the assay: she injects
a **concentrated** sample (so a small impurity is actually visible) and
compares it against a **very dilute** salicylic-acid standard set right
at the limit.

**How the sample is prepared:**

1. Powder **≥20 tablets** as before.
2. Weigh powder equal to **~1 tablet (~300 mg aspirin)** into a flask and
   dissolve in a **cold** diluent — kept cold and run **quickly**,
   because warmth and standing time create *more* salicylic acid and
   would fail a good batch by accident.
3. Make to volume at a **high** concentration — no big dilution this
   time; she *wants* the impurity visible.
4. Separately make a **limit standard**: a salicylic-acid solution at
   ~0.3% of the sample's aspirin concentration.
5. Filter both into vials, cap, label, and run them **promptly**.

**Reading it:** if the salicylic-acid peak in the sample is **smaller
than** the peak from the 0.3% limit standard, the batch passes; bigger,
and it fails. The same logic guards the paracetamol above against
**4-aminophenol** (a toxic process/breakdown residue, limit on the order
of ~50 ppm) — a tiny impurity peak checked against a tiny standard.

#### 3. Dissolution — "will this ibuprofen actually release in time?"

**The drug:** ibuprofen 200 mg (Advil, Nurofen).

**What she is answering:** a tablet with the perfect dose is useless if
it passes straight through you without dissolving. Dissolution asks: does
**≥80%** (the method's **"Q"** value) of the ibuprofen **release within
~30–45 minutes** under conditions that mimic the gut?

**What she physically measures:** how much drug has dissolved into a
warm, stirred bath over time. This test *starts* on a **dissolution
apparatus**, not the HPLC:

1. Drop **one tablet into each of 6 vessels**, each holding **~900 mL**
   of a **pH ~7.2 phosphate buffer** (an intestine stand-in), held at
   **37 °C** (body temperature).
2. A **paddle stirs at ~50 rpm**. At set times (e.g. 30, 45, 60 min) she
   **withdraws a few mL** from each vessel.
3. Each withdrawn aliquot is **filtered** straight into a 2 mL vial — and
   from here it is the **same vial-prep loop** as the assay.
4. HPLC (or a direct UV reading) measures the ibuprofen concentration in
   each time-point vial; multiplied by the ~900 mL volume, that gives the
   **% released** at each time.

**Reading it:** every one of the 6 vessels should clear the Q threshold
within the window. A batch that releases too slowly — an over-compressed,
"too hard" tablet, for instance — fails even if its assay is a perfect
100%, which is exactly why dissolution and assay are *both* required.

#### 4. Content uniformity — "does every single tablet carry the same dose?"

**The drug:** ibuprofen 200 mg again (the test matters most for
low-dose or potent drugs, but the principle is general).

**What she is answering:** the assay above grinds 20 tablets *together*,
so it only proves the **average** is right. Content uniformity proves no
**individual** tablet is wildly off — a real risk if the powder blend
wasn't perfectly mixed before it was pressed into tablets.

**What she physically measures:** the dose in **10 individual tablets,
assayed one at a time**.

**How the sample is prepared:**

1. Take **10 tablets separately** — *not* pooled and ground together.
2. Put **each tablet in its own flask**, dissolve, dilute to the method's
   working concentration, and filter into its **own** vial.
3. Run all 10 (plus the standard) and calculate the **individual** dose
   of each tablet.

**Reading it:** all 10 must sit close to label claim, and the spread
between them — rolled into an "acceptance value" from their mean and
standard deviation — must be small. A single rogue tablet at 140% or 60%
fails the batch even when the 10-tablet average looks fine.

**Why every one of these ends in the same vial.** Notice the shape: the
*questions* differ — total dose, impurity, release speed, tablet-to-
tablet spread — and the *front* of each prep differs (grind 20 together;
keep aspirin cold and fast; stir ibuprofen in a 37 °C bath; isolate 10
tablets one by one). But they all funnel into the **identical last
move**: a prepared solution drawn through a filter into a **2 mL vial**,
capped, labelled, and loaded in worklist order. That convergence is the
whole reason the arm is worth building — it lands exactly on the step
every one of Priya's tests shares ([P5](#p5-filling-capping-and-labelling-vials)–[P6](#p6-building-the-tray-and-loading-the-instrument)),
no matter which drug or which question started the day.

### P1. Sample receipt and login

Priya signs the day's samples out of the controlled sample-storage room.
Each one is matched against its LIMS record, its container condition is
checked, and the sign-out is recorded with a timestamp and her
initials. The packaging is wildly variable — a bottle of tablets, a
blister strip, a sealed drum of raw powder, a foil pouch — and the chain
of custody is a real, audited record.

> **Automation: Human-led.** Variable, non-standard packaging and a
> custody record that needs a human signature keep this with Priya.
> A barcode scanner and auto-logging make it faster, but the arm has no
> business opening a random drum in v1.

### P2. Weighing and measuring

For an assay she weighs **~20–50 mg** of reference material or a counted
number of crushed tablets on the 0.1 mg balance: open the draft shield,
tare the weighing boat or flask, dispense powder to the target weight,
read, and let the balance push the exact weight straight into LIMS. For
dissolution she measures **900 mL** of dissolution medium into each
vessel. Static cling, spillage, and the last milligram of a powder are
fiddly even for people.

> **Automation: Human-assisted.** Moving and presenting vessels, taring,
> and capturing the weight are arm-friendly, but dispensing a fine powder
> to ±0.1 mg is a specialist job — the real answer is an **automated
> dosing balance** (e.g. Mettler Quantos) that the arm feeds and unloads,
> not the arm pinching powder itself.

### P3. Sample preparation

This is the long part. She transfers the crushed tablet or weighed powder
into a volumetric flask, adds a measured volume of **diluent**, sonicates
to dissolve, lets it cool, makes up to the mark, and mixes. Then she
takes a precise **aliquot** and dilutes again — often two or three
dilution stages — to land in the method's working range. Each transfer
uses Class A volumetric pipettes or calibrated micropipettes, and each
one is a chance to introduce error.

In plain terms: this is the test that catches a batch of vitamin D
tablets accidentally pressed at triple strength, or a painkiller that is
quietly under-dosed — but it only catches them if every dilution here is
exact, which is precisely why a tired hand at the bench is a risk.

> **Automation: Human-assisted, trending Full-auto.** The **fixed-volume
> liquid transfers** — aliquot this, add that much diluent, mix — are
> exactly what a liquid-handling arm does best and most repeatably. The
> dissolve-sonicate-cool-make-to-volume steps still want handling and
> timing, so for v1 the arm owns the repetitive dispensing while a person
> shepherds the dissolution.

### P4. Standards and reagents

In parallel she prepares the **reference standard**: weigh it, dissolve,
and serially dilute to the **system-suitability** and calibration
concentrations the method demands. She also makes the **mobile phase** —
weigh buffer salts, dissolve, adjust pH with a meter, filter through a
0.45 µm membrane, and degas. Standards and samples must be prepared the
same way so they are comparable.

> **Automation: split.** The **standard dilutions** are Full-auto liquid
> handling. **Mobile-phase prep** — weighing buffer salts and titrating
> to a target pH — is **Human-led** for v1: pH adjustment is a feedback
> task with a probe, not a fixed pour.

### P5. Filling, capping and labelling vials

The heart of the loop. Each prepared solution is drawn up and pushed
through a **0.45 µm PTFE syringe filter** into a 2 mL vial (the first
~0.5 mL is discarded to waste so the filter is rinsed), the vial is
**capped** (9 mm screw or 11 mm crimp), and a **barcode label** tying it
to its LIMS ID is applied. She does this **dozens of times** a morning,
identically, on standard 2 mL vials in fixed racks.

> **Automation: Full-auto.** This is the canonical arm task and the
> literal centre of the project — standard labware, fixed geometry, the
> same motion every time, and the step where human slips (wrong cap,
> wrong label, unfiltered carryover) are most costly. If the cell does
> nothing else, it does this.

### P6. Building the tray and loading the instrument

She places the finished vials into the autosampler tray **in worklist
order** — blank first, then the five-to-six system-suitability standard
injections, bracketing standards, then samples in duplicate — and slides
the tray into the instrument, confirming each position matches the
sequence.

> **Automation: Full-auto.** Pick-and-place into known tray coordinates
> in a known order is squarely in scope, and getting the *order* exactly
> right is something the arm does more reliably than a tired human at
> 11:45.

### P7. Starting and watching the run

In Empower she builds the **sequence** — sample IDs, the method, the
injection volume — and starts it. She watches the first few injections:
does the pressure look right, is the standard's peak shape good, did
**system suitability** pass (e.g. ≤2% RSD across the standard
injections)? If yes, she walks away and the run finishes overnight.

> **Automation: mixed.** Physically starting the run is Full-auto, and
> building the sequence could be **Human-assisted** via a LIMS/CDS
> handshake. But the suitability **judgment** — "is the system fit to
> trust today?" — is **Human-led**.

### P8. Data review and reporting

Next morning she reviews every chromatogram: confirm suitability held,
integrate peaks (sometimes correcting the software's baseline by hand),
calculate the result, compare to the specification, and route it for a
**second-person review**. A result outside limits triggers a formal
**out-of-specification (OOS) investigation**.

> **Automation: Human-led.** Integration calls, OOS judgment, and release
> decisions are scientific and regulatory acts. The arm's contribution is
> upstream — by removing prep variability it makes the data *cleaner* to
> review — not doing the review.

### P9. Documentation and compliance

Every weight, every dilution, every instrument event is recorded —
historically in a bound notebook, increasingly in an **ELN** — under
**ALCOA+** data-integrity expectations (Attributable, Legible,
Contemporaneous, Original, Accurate, …) with a second person verifying
critical entries.

> **Automation: Human-led, with an arm bonus.** A robot logs **every
> action automatically** with a timestamp — a tamper-evident,
> contemporaneous record that is a *compliance asset*. But the human
> review and sign-off stay human.

### P10. Housekeeping and cleanup

Wash glassware, dispose of solvent waste correctly, wipe down the balance
and bench, restock vials, caps, filters and solvent, and store columns
properly.

> **Automation: Human-assisted.** Consumable staging (keeping the vial,
> cap, and filter hoppers full) is arm-friendly; solvent-waste handling
> and glassware washing stay human for v1.

### Priya summary table

| Task | Level | Why |
|---|---|---|
| P1 Receipt & login | Human-led | Variable packaging, custody signature |
| P2 Weighing | Human-assisted | Powder dosing needs a dosing balance |
| P3 Sample prep | Human-assisted → Full-auto | Fixed-volume transfers are arm-ideal |
| P4 Standards / reagents | Split | Dilutions auto; pH/mobile phase human |
| P5 Fill, cap, label vials | **Full-auto** | The core loop |
| P6 Tray build & load | **Full-auto** | Ordered pick-and-place |
| P7 Start & watch run | Mixed | Start auto; suitability call human |
| P8 Data review | Human-led | Integration, OOS, release |
| P9 Documentation | Human-led (+auto log) | Signatures human; arm auto-logs |
| P10 Housekeeping | Human-assisted | Consumable staging only |

---

## Person 2. Marco, a contract-lab sample-prep technician

> **Where you've already met his work:** the glass of water from your
> tap, the fish in your freezer, the soil dug up for a new school
> playground, the bag of pre-washed salad — someone doing Marco's job
> tested them for lead, pesticides, or sewage before anyone certified
> them safe. Every "results came back clean" headline starts at his
> bench.

Marco works in a large **environmental contract-testing lab** — the kind
of operation that runs inside a Eurofins, SGS, or regional equivalent,
where outside clients (municipalities, engineering firms, factories) send
in samples to be tested for a fee. His world is **volume**. Coolers of
water and soil arrive all day, each with a **chain-of-custody** form that
is a legal document, and each test has a **holding time** — a legal clock
(say, extract within 7 days, analyze within 40) after which the sample is
worthless. He runs standardized **EPA methods** (for example 8270 for
semi-volatiles, 8260 for volatiles, 525-series for drinking water) into
banks of **GC-MS and LC-MS** instruments.

His bench is built for throughput: a receiving area with a fridge and a
thermometer, racks of **40 mL VOA vials** and amber bottles, **solid-phase
extraction (SPE)** manifolds, separatory funnels, a **nitrogen blow-down**
concentrator (a TurboVap-class unit), trays of **2 mL GC vials with
0.3 mL micro-inserts**, and autosampler racks that hold **96+** vials per
instrument. Where Priya prepares 60–100 vials with great ceremony, Marco
pushes **hundreds of samples a day** through a standardized pipeline.

A typical day: log in the morning's deliveries against their custody
forms; aliquot and batch samples with their QC; spike surrogates and
internal standards; extract; concentrate; transfer to vials; load the
instruments; and keep the **holding-time clock** from running out on
anything. It is repetitive, deadline-driven, chemical-heavy work — and
several of its steps are the strongest case in this whole document for an
arm.

### What Marco actually tests — three samples from everyday life

Marco's day sounds abstract — "8270," "SPE," "surrogates" — until you pin
it to water or dirt you would actually worry about. So here are three
real contaminants, each in a sample you can picture, walked from the
cooler to the GC-MS vial: the legal question each answers, what he is
physically measuring, and exactly how the sample is prepared. Marco's
prep **pipeline** is the constant — aliquot, spike, extract, concentrate,
vial — and each example shows a different *shape* of it.

> **Numbers are illustrative.** Limits, volumes, and holding times below
> are representative of US EPA methods and their drinking-water limits
> (**MCLs**, maximum contaminant levels) but **vary by method, state, and
> revision**. Treat every figure as `~` and check the current method
> before quoting it.

| Sample you can picture | The plain-English question | Example contaminant |
|---|---|---|
| Well / tap water | Did a fuel leak reach the water? | **Benzene** |
| Drinking water | Is weed-killer in the supply? | **Atrazine** |
| Garden / playground soil | Is soot-borne carcinogen in the dirt? | **Benzo[a]pyrene** |

#### 1. Volatiles — "did a petrol leak reach this well water?"

**The sample:** a 40 mL vial of water from a private well or tap near a
leaking fuel station or buried tank.

**The everyday hook:** when a buried petrol tank or pipeline leaks, one
of the first things to reach groundwater is **benzene** — a component of
gasoline and a known human carcinogen. It is the lead actor in countless
"contaminated well water" stories.

**What he is answering:** is benzene below its drinking-water limit — in
the US, an **MCL of ~5 µg/L (5 ppb)**? At those vanishing levels, "a few
parts per billion" *is* the whole question.

**What he physically measures:** benzene and its gasoline cousins —
toluene, ethylbenzene, xylenes, together **"BTEX"** — pulled *out* of the
water as vapour and counted on a **GC-MS** (EPA 8260 / 524 style).

**How the sample is prepared** — note there is barely any "prep," and
that is the point:

1. **Collect with zero headspace.** Volatiles escape into any air gap, so
   the **40 mL VOA vial** is filled to a reverse meniscus with **no
   bubbles**, preserved with a drop of acid, and kept **≤6 °C**. A single
   trapped bubble can void the result — which is why receipt (M1) is so
   fussy.
2. **Don't open it.** Marco does not pour or pipette this sample; opening
   it loses the analyte. Instead the instrument's **purge-and-trap** draws
   a fixed **~5–25 mL** straight from the vial.
3. **Purge.** Inert gas (helium) bubbles through the water, sweeping the
   volatiles out of the liquid.
4. **Trap and desorb.** The swept-out vapour is caught on a small sorbent
   trap, then **flash-heated** to inject it as one sharp plug into the
   GC-MS.
5. **Spike first.** Before purging, fixed **surrogates and internal
   standards** are added (M3) so recovery can be proven.

**Reading it:** the GC-MS separates BTEX in time and identifies each by
its mass spectrum; benzene's peak area against its standard gives µg/L.
Above ~5 ppb, the water fails its limit.

#### 2. Pesticides — "is weed-killer in the drinking water?"

**The sample:** ~1 litre of finished drinking water.

**The everyday hook:** **atrazine** is one of the most common weed-killers
sprayed on corn and lawns, and it runs off into the rivers and reservoirs
that feed taps — a perennial drinking-water headline.

**What he is answering:** is atrazine below its **MCL of ~3 µg/L
(3 ppb)**? Again the answer lives in parts per billion, far too dilute to
inject straight — so the contaminant must be **pulled out of a whole
litre and concentrated** first.

**What he physically measures:** atrazine (often alongside other
pesticides in the same run) on a GC-MS or LC-MS (EPA 525 style), after
**solid-phase extraction (SPE)**.

**How the sample is prepared** — this is the SPE shape of the pipeline:

1. **Aliquot the litre** (M2) and spike **surrogate standards** (M3) so
   recovery is tracked from the very start.
2. **Pull it through a cartridge.** The whole ~1 L is drawn through a
   small **SPE cartridge** packed with C18 sorbent; the atrazine
   **sticks** to the sorbent while the water passes to waste (M4). One
   litre becomes a loaded cartridge the size of a thumb.
3. **Dry and elute.** The cartridge is dried, then a few mL of solvent
   (e.g. dichloromethane / ethyl acetate) **washes the atrazine back
   off**, now in a tiny volume.
4. **Concentrate.** That extract is blown down under nitrogen (M5) to
   **~1 mL** — turning a litre of tap water into one millilitre carrying
   all of its atrazine.
5. **Add internal standard, then vial.** A fixed internal standard goes
   in, and the ~1 mL is transferred into a **2 mL GC vial** (M6), capped
   and labelled.

**Reading it:** the GC-MS gives atrazine's concentration in the final
1 mL; dividing back by the litre extracted gives µg/L. The **surrogate
recovery** (did the spiked marker come back at, say, ~70–130%?) proves
the extraction itself worked — without it, a clean result could just mean
the analyte was lost on the way.

#### 3. Semi-volatiles — "is there soot-borne carcinogen in this soil?"

**The sample:** ~30 g of soil from a garden, playground, or old
industrial lot.

**The everyday hook:** **benzo[a]pyrene** is a **PAH** (polycyclic
aromatic hydrocarbon) — the same family of compounds in soot, char,
creosote-soaked railway sleepers, and diesel exhaust. It is a potent
carcinogen and it lingers in soil for decades, which is why ground for a
new school or playground gets tested before children play on it.

**What he is answering:** is benzo[a]pyrene below the site's cleanup
limit (often **single-digit µg/kg up to low mg/kg**, depending on how the
land will be used)?

**What he physically measures:** benzo[a]pyrene and its PAH relatives on
a GC-MS (EPA 8270 style), after **solvent extraction** of the soil.

**How the sample is prepared** — the solid-matrix shape, the heaviest
prep of the three:

1. **Weigh out the soil** (M2): ~30 g into an extraction vessel, with a
   separate portion dried to correct the result to **dry weight** (wet
   soil would dilute the answer).
2. **Spike surrogates** (M3) — typically **deuterated PAHs** (heavy
   look-alikes that behave like the real thing but are told apart by
   mass), so their recovery proves the extraction.
3. **Extract** (M4): soak and agitate the soil in **dichloromethane** (by
   sonication, shaking, or Soxhlet), pulling the PAHs out of the dirt and
   into the solvent.
4. **Clean up and concentrate** (M5): filter off the soil, optionally
   pass the extract through a cleanup column to strip interferences, then
   blow it down under nitrogen to **~1 mL** — *watched* so it is never
   taken to dryness, which would lose the lighter PAHs.
5. **Vial** (M6): the ~1 mL extract goes into a 2 mL GC vial — often with
   a **micro-insert** because the final volume is so small — capped and
   labelled.

**Reading it:** the GC-MS quantifies benzo[a]pyrene in the final extract;
back-calculated against the 30 g and corrected to dry weight, that gives
µg/kg of soil. Surrogate recovery again vouches for the whole prep.

**Why every one of these ends in the same vial.** Three very different
front-ends — *don't even open* the volatile water, pull a litre through a
cartridge, soak grams of dirt in solvent — but all three converge on the
**same last move**: a ~1 mL extract in a **2 mL GC vial**, capped,
labelled, and racked in batch order on a 96-position autosampler. The
chemistry that gets there is Marco's; the **fixed-volume spiking
([M3](#m3-adding-surrogates-and-internal-standards)), the vialling
([M6](#m6-filling-capping-and-labelling-vials)), and the rack loading
([M7](#m7-loading-the-autosamplers))** that bracket it are the
repetitive, identical motions the arm is built for — which is why his
job, chemically nothing like Priya's, lights up the same green band.

### M1. Sample receipt and accessioning

Coolers are opened, the internal **temperature is checked** (many methods
require ≤6 °C on arrival), the contents are reconciled against the
chain-of-custody form, and every sample is **logged into LIMS**, given an
ID, barcoded, and shelved. A mismatch between the form and the bottles is
a hold-everything event.

> **Automation: Human-led.** Legal custody reconciliation, temperature
> acceptance, and endlessly variable client packaging keep receipt with a
> person. Barcoding and shelving are **Human-assisted** at best.

### M2. Aliquoting and batching

He measures defined amounts into extraction vessels — say **1 L** of
water into a separatory funnel, or **30 g** of soil into a jar — and
assembles an **extraction batch**: typically up to 20 field samples plus
the mandatory QC (a **method blank**, a **laboratory control sample**, a
**matrix spike**, and a **duplicate**).

> **Automation: Human-assisted.** Pouring fixed volumes from *standard*
> containers is arm-friendly; the messiness of real field samples
> (sediment, debris, odd bottles) means a person still oversees it.

### M3. Adding surrogates and internal standards

Into every sample and QC vessel he injects a precise small volume —
often **0.1–1 mL** — of surrogate and internal-standard solution with a
micro-syringe or dispenser. Identical, precise, and done hundreds of
times a day.

> **Automation: Full-auto, trending.** Precise **fixed-volume
> dispensing** repeated across a rack is exactly what a liquid-handling
> arm or dispenser is for — high value, low judgment.

### M4. Extraction

The chemistry step: pull each water sample through an **SPE cartridge**
and elute the trapped analytes with solvent, or shake-and-separate in a
**liquid-liquid extraction**. Some of this is already semi-automated with
SPE manifolds and dedicated extractor robots.

This is the step behind a headline like *"lead found in school drinking
water"* or *"pesticide residues on imported grapes"*: the contaminant is
present in vanishingly small amounts, so it first has to be pulled out of
litres of water or grams of soil and concentrated before any instrument
can see it. No extraction, no headline — and no warning.

> **Automation: Human-assisted.** Cartridge SPE on a fixed manifold is
> partly automatable and a good arm-feeding job; judging a **phase
> separation** in liquid-liquid extraction (where's the interface?) is a
> human eye for v1.

### M5. Concentration

Extracts are evaporated down — under a stream of nitrogen in a blow-down
unit — from tens of millilitres to **~1 mL**. It is slow and has to be
watched so samples aren't taken to dryness and lost.

> **Automation: Human-assisted.** Dedicated concentrators already exist;
> the arm's role is **loading and unloading tubes** and moving them
> between stations, not reinventing the evaporator.

### M6. Filling, capping and labelling vials

The concentrated extract is transferred into a **2 mL GC vial** (often
with a **micro-insert** because the final volume is tiny), capped, and
labelled. Same canonical loop as Priya's P5, just at higher volume and
with inserts in play.

> **Automation: Full-auto.** Standard vials, standard caps, fixed
> positions, endless repetition — the core arm task again, and the place
> Marco's repetitive-strain risk is highest.

### M7. Loading the autosamplers

Vials go into the **GC-MS / LC-MS autosampler racks** — frequently
**96-position** trays across several instruments — in batch order, and
the racks are seated in the instruments.

> **Automation: Full-auto.** High-count, ordered pick-and-place across
> multiple instruments is a natural fit and a throughput multiplier.

### M8. Holding times and batch QC

He keeps a constant eye on **holding-time clocks** and on whether each
batch's QC passed (blank clean? spike recovery in range?). Miss a holding
time and the result is legally void; fail QC and the whole batch
re-runs.

> **Automation: Human-led.** The **tracking** is software, but the
> decisions — re-prep now, prioritize that cooler, accept this QC — are
> human calls under client and regulatory pressure.

### M9. Monitoring and re-prep

When a sample reads over-range or a QC fails, he **dilutes and re-runs**
or **re-extracts**. Physically routine; the trigger is a judgment.

> **Automation: Human-assisted.** The **re-dilution and re-injection**
> are arm-friendly mechanical loops; *deciding* to re-run stays human.

### M10. Cleanup and waste

Solvent and **hazardous-waste** handling, glassware washing, spent
cartridge disposal, and restocking the high-burn consumables.

> **Automation: Human-led.** Hazardous-solvent handling is a safety and
> compliance matter for people; the arm only **stages clean
> consumables**.

### Marco summary table

| Task | Level | Why |
|---|---|---|
| M1 Receipt & accessioning | Human-led | Legal custody, temp, packaging |
| M2 Aliquoting & batching | Human-assisted | Messy real-world matrices |
| M3 Surrogate / IS spiking | **Full-auto** | Precise fixed-volume, high repeat |
| M4 Extraction | Human-assisted | SPE auto-able; phase calls human |
| M5 Concentration | Human-assisted | Arm loads/unloads concentrator |
| M6 Fill, cap, label vials | **Full-auto** | The core loop, with inserts |
| M7 Load autosamplers | **Full-auto** | 96-position ordered placement |
| M8 Holding times & QC | Human-led | Deadline and acceptance decisions |
| M9 Monitor & re-prep | Human-assisted | Re-dilute auto; trigger human |
| M10 Cleanup & waste | Human-led | Hazardous handling |

---

## Person 3. Sarah, an R&D method-development scientist

> **Where you've already met her work:** before any of those checks can
> exist, someone has to invent them. The new weight-loss injection
> everyone is talking about, a next-generation sunscreen, a reformulated
> vitamin gummy — each needs a brand-new test designed and proven first.
> That is Sarah's job: she builds the test that Priya later runs every
> day.

Sarah works in **analytical development** in pharma R&D. She doesn't
*follow* methods — she **invents and validates** them. When a new drug
candidate needs an assay and an impurity method, she figures out which
**column**, **mobile phase**, and **gradient** separate everything
cleanly, proves the method is **stability-indicating** (it can see
degradation products), and then validates it for precision, accuracy,
linearity, and robustness before handing it to QC labs like Priya's.

Her work is the mirror image of Marco's: **low volume, high variability,
and heavy on judgment**. Some days she prepares only a dozen vials, but
she runs many **short experiments**, changes one variable at a time, and
spends much of her day **reading chromatograms and deciding what to try
next**. Her bench has an HPLC/UHPLC with a **photodiode-array (PDA)** or
mass detector, a shelf of **a dozen different columns**, multiple
mobile-phase bottles, an **electronic lab notebook (ELN)**, and often
method-development software (Fusion QbD, ACD/Labs) for **design of
experiments (DoE)**. Stressed, light-sensitive samples and a stopwatch
are never far away.

A typical day: plan a small DoE; prepare **forced-degradation** (stressed)
samples; screen two or three column/mobile-phase combinations with short
runs; prepare **serial dilutions** for a linearity check; and iterate —
read, adjust, re-run — several times before lunch and again after. The
arm can't do her thinking, but it can erase the **repetitive prep between
her decisions**, which is where her day leaks time.

### What Sarah actually builds — inventing the test behind a familiar pill

Sarah doesn't follow a recipe; she **writes** it. The clearest way to see
her day is to watch her build the very method **Priya** will later run
every morning — using drugs you already know. Here are three slices of
that work, with the sample prep spelled out, all on familiar tablets.

> **Numbers are illustrative** (`~`), and method-development conditions
> change by the hour — that churn *is* the nature of the job.

| Slice of method development | The plain-English question | Example drug |
|---|---|---|
| **Forced degradation** | Can the test *see* the drug breaking down? | Paracetamol |
| **Separating a combo** | Can it tell apart everything in the pill? | Paracetamol + caffeine |
| **Linearity / validation** | Are the numbers trustworthy across the range? | Ibuprofen |

#### 1. Forced degradation — "can the test even see paracetamol breaking down?"

**The drug:** paracetamol — the same one Priya assays, but here Sarah is
*proving the test works* before Priya ever touches it.

**What she is answering:** is the method **stability-indicating** — can it
**see** the drug decomposing, rather than reporting a degraded sample as
still-perfect? A method that can't see degradation is worse than useless:
it would quietly pass an expired, harmful batch.

**What she does to the drug:** she deliberately **abuses** a paracetamol
solution under five separate stresses, each for a controlled time, to
*force* it to break down so she can check the method catches the
products:

1. **Acid** — heat it with dilute HCl.
2. **Base** — heat it with dilute NaOH.
3. **Oxidation** — mix it with hydrogen peroxide.
4. **Heat** — hold the dry drug hot.
5. **Light** — leave it under UV.

**How the samples are prepared:**

1. Make a stock paracetamol solution at the assay concentration.
2. Split it; to each portion add the stress reagent (acid, base, peroxide)
   or apply the condition (heat, UV) for a **timed** interval — timing
   matters, because too much stress destroys everything and too little
   shows nothing.
3. **Neutralize** the acid and base portions (so they don't keep reacting
   or attack the column) and **dilute** every portion back to the
   method's working concentration.
4. Filter into vials — the **same canonical loop** — and run them quickly.
5. Run an **unstressed control** alongside for comparison.

**Reading it:** on each chromatogram she checks that the **paracetamol
peak shrank** and **new degradant peaks appeared** (e.g.
**4-aminophenol** — the very impurity Priya's "related substances" test
then polices), that those new peaks are **fully separated** from
paracetamol, and that **peak purity** (via the photodiode-array or MS)
confirms nothing is hiding *underneath* the main peak. She also checks
**mass balance**: drug lost ≈ degradants gained. If all that holds, the
method is stability-indicating.

#### 2. Separating a combo — "can it tell apart everything in a cold-and-flu pill?"

**The drug:** a **paracetamol + caffeine** tablet — the familiar
cold-and-flu / "extra-strength" combination.

**What she is answering:** a combo pill needs **one** method that measures
*every* active at once and keeps each one — plus all their degradation
products — **separated** from the others. The challenge is **resolution**:
paracetamol, caffeine, and their breakdown peaks must not overlap.

**What she physically measures:** the **resolution** (the gap) between
adjacent peaks, as she **screens conditions** trying to spread them out.

**How she works the problem** (this is the "iterate" loop):

1. Prepare a mixed standard of paracetamol + caffeine at known levels,
   plus the stressed samples from above.
2. **Screen variables one at a time** — try a different **column**
   chemistry, change the **mobile-phase** organic ratio or pH, adjust the
   **gradient** or temperature — running a short sequence after each
   change.
3. Each screening run is a few freshly prepared vials: standards plus a
   sample or two, the **same fill-cap-label loop**, just small batches
   prepared **often**.
4. Read the chromatogram, keep the change that pushed two peaks apart,
   and **repeat** — many short cycles a day.

**Reading it:** she is hunting for a condition where **every** peak — both
actives and all degradants — is **baseline-separated** (a clean gap,
usually resolution ≥ ~2.0 between the closest pair). The prep between
each try is identical and repetitive; the **decision** of what to change
next is hers alone.

#### 3. Linearity & validation — "are the numbers trustworthy across the range?"

**The drug:** ibuprofen — proving the finished method before handover.

**What she is answering:** does the detector respond **proportionally**
across the whole range the method must cover — typically **50% to 150%**
of the target concentration — so any reading can be trusted to convert
into a real dose?

**What she physically measures:** a **calibration curve** — peak area vs.
concentration — built from a **serial dilution**.

**How the samples are prepared:**

1. From one accurately weighed ibuprofen stock, prepare a ladder of
   concentrations at, say, **50, 80, 100, 120, 150%** of target by
   precise, fixed-volume dilution.
2. Add precision **replicates** at each level (the same prep made
   independently several times).
3. Filter each into its own vial — a **textbook liquid-handling task**,
   and the step most exposed to dilution error.
4. Run the ladder; plot area vs. concentration; the points should fall on
   a **straight line** (correlation near 1.000).

**Reading it:** a straight, tight line means the method is linear and the
arithmetic Priya later uses is valid. A kink or scatter usually traces
back to **dilution error** — exactly the step automation removes — which
is why this prep is the strongest **Full-auto** case in Sarah's day.

**Why even the inventor's bench ends in the same vial.** Sarah's value is
the *thinking* — which stress to apply, which column to try, when a
separation is good enough — and no arm touches that. But look at what
surrounds every decision: timed neutralize-and-dilute, serial dilutions,
small standard sets, all funnelled into the **same fill-cap-label-load
loop** as Priya and Marco, just in **frequent small batches** instead of
one big overnight tray. The arm can't invent her method, but by erasing
the repetitive prep *between* her decisions it hands her **more shots per
day** — and the method she ships is the one Priya then runs on the drugs
in your cabinet.

### S1. Designing the experiment

She defines the question, picks the variables to screen (organic ratio,
pH, temperature, gradient slope, column chemistry), and lays out a DoE.
Pure knowledge work at a screen and whiteboard.

> **Automation: Human-led.** This is the creative core of the job. No
> part of it is the arm's.

### S2. Forced-degradation sample prep

To prove a method is stability-indicating she **stresses** the drug:
acid, base, hydrogen peroxide, heat, and UV light, each for a controlled
time, then **neutralizes** and dilutes to concentration. Conditions
vary every time; the timing matters.

This is why your medicine carries an expiry date and a *"store below
25 °C, keep out of direct sunlight"* line. Sarah deliberately ages and
abuses the drug — bakes it, soaks it in acid, leaves it under a lamp — to
learn how it breaks down, so the label can warn you before it happens in
your bathroom cabinet.

> **Automation: Human-assisted.** Setting the stress conditions is
> judgment, but the **timed neutralization and dilution** — and getting
> stressed samples into vials fast and consistently — are repetitive
> steps an arm can take over once Sarah sets the recipe.

### S3. Standards and serial dilutions

For linearity she builds a **calibration curve** — a serial dilution
across, say, **50% to 150%** of the target concentration — plus precision
replicates. Careful, repetitive, precise pipetting.

> **Automation: Full-auto.** **Serial dilution** is a textbook
> liquid-handling task: fixed volumes, fixed sequence, standard labware.
> High value because dilution error is a top source of bad linearity.

### S4. Column and mobile-phase changeover

Between screening runs she **swaps HPLC columns** (unscrewing fittings,
purging, re-equilibrating) and **changes mobile-phase bottles**. She may
do this several times a day.

> **Automation: Human-led for v1.** Threading column fittings is a
> **fine-dexterity, force-sensitive** task that a first-generation arm
> should not attempt; swapping a mobile-phase **bottle** is more
> tractable but still Human-assisted at best.

### S5. Filling, capping and labelling vials

She fills a **handful** of vials — a few standards plus the stressed and
control samples — caps and labels them. Smaller trays than QC, but done
frequently, all day.

> **Automation: Full-auto.** Same canonical loop. The batch is small, but
> the motion is identical to Priya's and Marco's, so the same cell
> covers it.

### S6. Running short sequences

She builds a **short sequence**, starts it, and often **babysits** it for
a quick turnaround so she can decide the next experiment without waiting
overnight.

> **Automation: Human-assisted.** Starting and loading are auto; the
> *waiting and quick-look* is hers because the next decision hangs on it.

### S7. Reading the data and deciding

She inspects each chromatogram for **resolution** between peaks, **peak
purity** (using PDA or MS to confirm one compound under a peak), and
**mass balance**, then decides whether the separation is good enough or
what to change. This *is* the job.

> **Automation: Human-led.** Deep scientific judgment. The arm only makes
> the inputs cleaner and the cycles faster.

### S8. Iterating

Change one variable, re-prepare, re-run, re-read — many cycles a day.
The loop that defines method development.

> **Automation: Human-led decisions, arm-shortened cycles.** Sarah owns
> every decision; the arm's value is collapsing the **prep time between
> iterations** so she gets more shots per day.

### S9. Documentation

She records conditions, chromatograms, and rationale in the **ELN** —
not just what happened but *why she chose it*, which a future validation
and audit will lean on.

> **Automation: Human-led (+auto log).** The scientific narrative is
> hers; the arm contributes an exact, automatic record of **what was
> prepared and how**.

### S10. Validation runs

Once the method is fixed, she runs formal **validation** — precision,
accuracy, linearity, robustness — which suddenly looks like QC: **high
vial counts**, many standards and replicates, ordered sequences.

> **Automation: Full-auto for the prep/loading.** Validation's vial prep
> and loading are as automatable as Priya's day; only the **design and
> acceptance** stay with Sarah.

### Sarah summary table

| Task | Level | Why |
|---|---|---|
| S1 Experiment design | Human-led | Creative / scientific |
| S2 Forced-degradation prep | Human-assisted | Conditions human; dilution auto |
| S3 Standards & serial dilutions | **Full-auto** | Classic liquid handling |
| S4 Column / mobile-phase swap | Human-led (v1) | Fine-dexterity fittings |
| S5 Fill, cap, label vials | **Full-auto** | The core loop, small batch |
| S6 Run short sequences | Human-assisted | Quick-turn babysitting |
| S7 Read data & decide | Human-led | Resolution, purity judgment |
| S8 Iterate | Human-led (+faster) | Arm shortens prep cycle |
| S9 Documentation | Human-led (+auto log) | Rationale is hers |
| S10 Validation runs | **Full-auto** prep | Looks like QC at scale |

---

## What this means for v1 scope

Lay the three people side by side and the same band lights up green in
every column — even though their jobs could not be more different:

- **The Full-auto core is identical for all three:** draw a prepared
  solution through a filter into a **2 mL vial**, **cap** it, **label**
  it, build the **tray in order**, and **load the autosampler** — plus
  the **fixed-volume liquid handling** (aliquots, diluent adds, serial
  dilutions, IS/surrogate spikes) that feeds it. This is the same five
  hand-motions the [intro](01-hplc-intro.md) called out, and it is
  **exactly the v1 project**: the prepare-cap-label-load loop on standard
  HPLC labware.

- **The Human-assisted band is the next milestone:** powder weighing (via
  a dosing balance the arm feeds), extraction and concentration (the arm
  loads and unloads dedicated units), and re-prep loops. Worth doing
  later; out of scope for v1.

- **The Human-led band stays human:** sample receipt and custody, pH and
  mobile-phase prep, data review and OOS/validation judgment, method
  design, fine-dexterity column fittings, and every regulatory signature.
  The arm's job there is only to make the data **cleaner** and to
  **auto-log** what it did.

The lesson for scope is encouraging: **one well-built vial-prep cell
serves the QC analyst, the high-volume technician, and the R&D scientist
alike**, because their green band is the same band. That is why we can
build narrow and still land broad — and why the **first project stays
deliberately on HPLC**: nail the shared core on one workflow before
reaching for the assisted and human-led bands or other instruments.

**The bottom line, for the reader who started at the top:** the robot we
are building is the thing that fills, caps, labels, and loads the little
vials behind the dose in your painkiller, the safety of your tap water,
and the expiry date on your medicine. It does not replace the scientist's
judgement — it hands back the hours they currently lose to the same five
hand-motions, so they can spend that time deciding what the results
actually mean.

Next: the per-layer breakdown of how that cell is actually built lives in
[`03-high-level-solution/README.md`](03-high-level-solution/README.md).
