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

For a fuller glossary of the terms used across this folder (worklist,
diluent, internal standard, tray, crimp cap, and so on), the
[high-level solution](02-high-level-solution/README.md) docs define each
on first use.

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

## Where to go next

- **[02 — High-level solution](02-high-level-solution/README.md):** the
  scope, the manual workflow we replace, and a per-concern breakdown
  (vial handling, decapping, liquid handling, tray loading, perception,
  orchestration, compliance, hardware).
- **[03 — Hello-worlds](03-hello-worlds/README.md):** small, runnable
  milestones that build the simulated cell one capability at a time.
- **Arm implementations:**
  [04 — reBot](04-reBot-implementation/README.md),
  [05 — myCobot 280](05-mycobot-280-impl/README.md),
  [06 — AgileX PiPER](06-agile-x-piper-impl/README.md).
- **[07 — Arms comparison](07-arms-comparison.md):** which arm to
  simulate first, before buying.
- **[08 — Learning checklist](08-learning-checklist.md):** the skills to
  pick up along the way.
