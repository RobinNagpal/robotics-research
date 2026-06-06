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

## The part we automate

Before the autosampler can do its job, a lab tech stands at a bench and,
for every single sample, does a fixed manual routine: measure or weigh
the sample, add diluent and internal standard, transfer it into a clean
vial, cap it, label it with a barcode, and place it in the correct tray
slot in worklist order. Only then does the tray go into the instrument.

That front-end is slow, repetitive, and exactly where silent mistakes
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
