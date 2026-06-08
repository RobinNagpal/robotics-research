# Part 01 — HPLC, in plain language (start here)

> **Job:** Explain what HPLC is, what an **autosampler** does, and why
> the slow, manual vial-prep in front of the instrument is the part this
> project automates. Read this before anything else — it sets the
> vocabulary the rest of the folder assumes.

## Watch this first

A short, plain explanation of how HPLC works:

- **Video — How HPLC works:**
  <https://www.youtube.com/watch?v=9Ns2nhiuNHA&t=37s>

It is worth the few minutes before reading on. Everything below uses the
same picture: a pump pushing liquid through a column, samples injected
one at a time, a detector drawing a graph of what came out.

## What is HPLC?

**HPLC** stands for **High-Performance Liquid Chromatography**. It is the
workhorse analytical method labs use to answer "what is in this liquid,
and how much of each thing?" — the purity of a drug, the level of a
contaminant, the concentration of an active ingredient.

The idea, in one breath: a high-pressure pump pushes a liquid solvent
(the **mobile phase**) through a packed tube (the **column**). A tiny,
precisely measured amount of your prepared sample is **injected** into
that flowing stream. Different molecules in the sample stick to the
column material for different lengths of time, so they come out the far
end **separated in time**. A **detector** at the outlet measures each
one as it exits and draws a peak for it. The pattern of peaks — when they
appear and how big they are — tells you the identity and amount of each
component.

For the terms used across this folder (worklist, diluent, internal
standard, tray, crimp cap, and so on), the
[sample-prep primer](02-lab-bench-new.md) and the
[HPLC workflow](03-hplc-workflow/README.md) docs define each on first
use.

## Where HPLC shows up (everyday examples)

HPLC is behind a lot of quiet "is this really what it says it is?"
checks:

- **Medicines.** Before a batch of pills ships, a lab confirms each one
  holds the labelled dose of active ingredient — and no harmful
  impurities. This is the biggest, most regulated use.
- **Food & drink.** Caffeine in coffee and energy drinks, sugar and
  vitamins in juice, additives and preservatives — all measured this way.
- **Drug & health testing.** Anti-doping tests for athletes and hospital
  tox screens separate and measure compounds in blood or urine.
- **Water & environment.** Pesticides or contaminants in drinking water,
  checked down to tiny concentrations.
- **Supplements & cosmetics.** Confirming a vitamin or skincare product
  actually contains what the label claims.

The common thread: a liquid sample goes in, and out comes a precise
answer about *what is in it and how much*. That answer is only as good as
the sample that was prepared and loaded — which is exactly the manual
work this project targets.

## What is the autosampler?

A modern HPLC instrument does not inject samples by hand. It has an
**autosampler** — a module that holds a **tray** of small **vials**
(usually 2 mL glass) and automatically draws from each one, in order, and
injects it for analysis. The autosampler walks down a **worklist** (an
ordered list of which tray position holds which sample) and runs them one
after another, unattended.

So the instrument's own step — drawing from a vial and injecting it — is
already automated. The part that is **not** automated is everything that
happens *before* the tray reaches the instrument.

## A day on the lab floor

Picture a quality-control lab in the morning. A batch of product —
say, a delivery of headache tablets — arrives with paperwork saying what
to test. A lab tech sits at a bench with a rack of empty **2 mL vials**,
a balance, pipettes, bottles of solvent, a label printer, and the
**autosampler tray** (a grid that holds the vials in numbered slots).

For each sample the tech repeats the same short routine:

1. **Measure** the sample — weigh a little powder, or pipette a little
   liquid — into a vial.
2. **Add diluent** (solvent) to bring it to the right concentration, and
   an internal standard if the method needs one.
3. **Cap** the vial so nothing evaporates or spills.
4. **Label** it with a barcode so it traces back to the right sample.
5. **Place** it in the tray slot its worklist row names.

When the whole tray is filled in worklist order, the tech **slides the
tray into the autosampler**, opens the instrument software, and **starts
the run**. The machine then injects each vial one after another —
often for hours, unattended overnight — and prints a result per vial.

### Why so many vials?

A single run is rarely one sample. To trust the numbers, the tray is
packed with far more than the samples themselves:

- **Calibration standards** — several vials of known concentration the
  instrument uses to "learn the scale" before reading unknowns.
- **Blanks** — vials with solvent only, to prove nothing is contaminating
  the readings.
- **QC / control samples** — known-good references run periodically to
  prove the instrument is still behaving.
- **Replicates** — many samples are prepared and injected two or three
  times so a single bad injection can't decide the result.
- **The actual samples** — often a whole batch's worth at once.

Labs deliberately **batch everything into one long sequence** so the
instrument can run unattended. The result: a typical tray is **dozens to
well over a hundred vials**, and the tech spends a big part of the day
just preparing and loading them — the same five steps, over and over,
hundreds of times.

That repetition, on the critical path of every result, is the target.

## The part we automate

The five-step bench routine above — measure, dilute, cap, label, place —
is the whole manual front-end, and it is exactly where silent mistakes
creep in — a wrong dilution, a vial in the wrong slot, a mislabeled or
uncapped sample. The instrument cannot tell; it just injects whatever is
physically there.

**This project automates that manual front-end** — the prepare, cap,
label, and tray-load steps — with a single fixed-mount 6-DoF robot arm
working a bench of fixed stations, proven in simulation first and then
transferred to hardware. The instrument keeps doing what it already does
well: the actual injection and analysis.

## How big is this, and who pays for it?

> **Figures are approximate (`~`), come from market-research summaries,
> and drift fast — re-check before quoting.**

A robot arm that prepares and loads vials is not a niche toy. The same
manual bench work it replaces happens in **tens of thousands of labs**
worldwide, every single day.

**The money in play.** HPLC instruments and consumables alone are a
**~$4.5–5 billion/year** market. But the arm doesn't care that it's an
HPLC — it picks, moves, dispenses, and loads. That puts it in the much
larger **lab-automation** market (**~$7–9 billion/year, growing
~8–10%/yr**), where liquid-handling and sample-prep robots are already
the biggest slice. The industries *behind* those labs are bigger still:
global pharma alone spends **~$280–300 billion/year on R&D**, on top of
the manufacturing QC that tests every batch it ships.

**Who owns and runs the labs.** Three broad types:

- **In-house QC/R&D labs** at the manufacturers themselves — every
  pharma, food, cosmetics, and chemical company runs its own.
- **Contract testing labs (CROs / testing networks)** that other
  companies pay to run the tests. These are huge: **Eurofins** runs
  **950+ labs** with ~65,000 staff and does **~450 million tests a
  year**; **Intertek** runs **1,000+ labs**; **SGS**, **LabCorp**, and
  **Quest** are comparable.
- **Public labs** — hospital/clinical, government, regulatory (FDA, EPA),
  and university research labs.

**Who uses it, and how often:**

| Industry | What they test | How often |
|---|---|---|
| Pharma & biotech | drug purity, dose, impurities | **every batch**, daily |
| Food & beverage | additives, vitamins, contaminants | continuous QC |
| Clinical / hospital | compounds in blood and urine | millions of tests/yr |
| Environmental | pesticides, water contaminants | routine monitoring |
| Cosmetics, agrochem, forensics, cannabis | active ingredients, residues | routine |

**Not just HPLC.** The same arm motions — pick a vial or microplate,
move it, dispense into it, load it into an instrument — cover a whole
family of nearby lab jobs: LC-MS / GC-MS sample prep, dissolution
testing, ELISA and microplate handling, PCR / DNA-sequencing prep,
microbiology plating, weighing and dispensing. That's why this is worth
getting right once.

> **Scope for now:** this first project deliberately focuses on **just
> HPLC vial prep and loading**. Learn one real workflow end to end before
> trying to generalize to the rest.

## What a single bench looks like

Zoom all the way back from the market to one person at one bench. This is
where the requirements for the robot actually come from, so it is worth
getting concrete. (Throughput and timing numbers below are typical
industry figures and vary by lab and method — treat them as `~`.)

### The analyst and their workload

A lab analyst is a trained chemist — usually a B.Sc. or M.Sc. — who
**owns a handful of methods at once**. A *method* is a fixed, validated
recipe for one test on one product: it spells out exactly how much sample
to weigh, what solvent to add, what dilution to hit, and how to run it. A
realistic personal load looks like:

- *"Assay for Product A"* — how much active ingredient each tablet holds
  (e.g. "is this a true 200 mg ibuprofen tablet?").
- *"Related substances for Product B"* — which impurities are present and
  at what level (the safety-critical test).
- *"Stability study for Product C"* — the same tests repeated on samples
  pulled from storage at 1, 3, 6, 12… months to prove shelf life.

They typically tend **1–3 instruments** and, across those projects,
prepare and inject **~50 to a few hundred vials a day**. Crucially, the
instruments run largely **unattended — often overnight** — so the
analyst's real day is spent at the **bench preparing samples**, not
watching the machine.

### Why a "simple" test is never one vial

Here is the part outsiders miss. A request to "assay one batch" never
means one vial. Regulated methods — the pharmacopoeia standards such as
**USP <621>** — force a whole supporting cast into every tray before a
single real result is allowed to count:

- **A blank** — solvent only, to prove the prep itself isn't
  contaminating the signal.
- **System-suitability standards** — typically **5–6 injections of the
  same reference standard**, whose peak areas must agree to within
  **~2% RSD** (modern methods tighten this to under ~1%) *before* the
  instrument is trusted to read anything.
- **Calibration / bracketing standards** — known concentrations run at
  the start, and often again in the middle and at the end, to prove the
  instrument didn't drift over a long run.
- **The actual samples**, usually prepared and injected **in duplicate**
  (two independent preparations), sometimes more.
- **QC check standards** sprinkled through the sequence as periodic
  re-proof.

So a single product batch easily becomes **20–40+ vials** before you
count a second batch. Multiply by the two or three batches an analyst
handles in a day and the tray fills to **dozens, often 100+, vials** —
exactly the packed tray from the earlier section, now explained.

### The clock: prep is the bottleneck, not the run

Run time per injection is real but modest — a **single injection commonly
takes ~10–60 minutes**, and the analyst does not sit and watch it.
Counted end to end on one instrument:

| Method style | Time per sample (run) | Samples/day, one instrument |
|---|---|---|
| Classical HPLC | ~75 min incl. equilibration + cleaning | ~6 |
| Modern UHPLC | <6 min | ~90 |
| High-throughput (dual pump, column switching) | — | up to ~600 |

But those are *machine* numbers, and they are only reached by **batching
everything into one long unattended sequence**. The human number is
different, and worse: industry sources consistently find that **sample
preparation eats the majority of an analyst's hands-on time** and is the
**single largest source of analytical error**. Sample processing alone
accounts for at least a third of total method error, operator-generated
error for roughly another fifth, and **automating the prep can cut a
method's error by as much as ~50%**.

In short: the machine got fast; the bench did not. The hours a person
loses are in **measure → dilute → cap → label → load**, repeated
hundreds of times — and that is precisely the loop this project removes.

### A day in the life — three real shapes

**1. QC analyst, pharma manufacturing (the core case).** She arrives to
three released batches of a painkiller — say an ibuprofen or
acetaminophen tablet. For each batch she weighs and crushes a set number
of tablets, extracts the powder into a measured volume of solvent,
dilutes to the method's concentration, filters, and fills vials. She also
weighs and dilutes the reference standard to make the suitability and
calibration vials. By late morning she has built a sequence of **~80
vials** in worklist order, slid the tray into the autosampler, and
started a run that finishes overnight. Her **next** morning is spent
**reviewing chromatograms and chasing any out-of-spec result** — not more
pipetting. The bottleneck was the four hours of identical hand motions
before lunch.

**2. Method-development / R&D analyst (the iteration case).** He is
*inventing* the recipe, not following it, so he runs **5–10 smaller
experiments a day**: a few standards plus a couple of samples, changing
one variable (solvent ratio, column temperature, gradient) between runs
and reading the result before deciding the next. Fewer vials per tray,
but far more trips to the bench and far more decisions — a different
automation shape (frequent small batches, constant changeover) than
high-volume QC.

**3. Contract / clinical testing lab (the volume case).** An analyst at a
testing network like **Eurofins** (950+ labs, ~450 million tests a year)
or a hospital lab runs the **same validated method hundreds of times a
day** against incoming customer or patient samples. Here throughput is
everything: trays turn over continuously, and the prep is so repetitive
that these labs are already the heaviest buyers of liquid-handling
automation. This is the case where a vial-prep arm pays for itself
fastest.

### What this tells the robot project

Three requirements fall straight out of the bench:

1. **The unit of work is a *tray*, not a vial** — dozens of vials,
   prepared in a fixed order, including standards and blanks, not just
   the samples themselves.
2. **The win is in prep, not the run** — measure, dilute, cap, label,
   load. The instrument is already automated; the human hours are not.
3. **The same five motions generalize** — QC, R&D, and high-volume
   testing are the same hand motions at different batch sizes, which is
   why the arm is worth building even though we scope the **first**
   project to HPLC alone.

## Where to go next

- **[02 — Sample-prep primer](02-lab-bench-new.md):** how HPLC sample
  prep works in a real lab, broken into the discrete tasks a robotic
  arm could realistically automate.
- **[03 — HPLC workflow](03-hplc-workflow/README.md):** the eight prep
  steps, each in its own deep, plain-language file, walked through two
  real examples.
- **[04 — Hello-worlds](04-hello-worlds/README.md):** small, runnable
  milestones that build the simulated cell one capability at a time.
- **[05 — myCobot 280 implementation](05-mycobot-280-impl/README.md):**
  a concrete, per-concern build worked out on one low-cost arm.
- **[06 — Arms comparison](06-arms-comparison.md):** which arm to
  simulate first, before buying.
- **[07 — Learning checklist](07-learning-checklist.md):** the skills to
  pick up along the way.
