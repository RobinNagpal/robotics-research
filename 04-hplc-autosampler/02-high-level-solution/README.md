# High-level solution — automating HPLC vial prep & tray loading

> **The problem in one line.** In QC, pharma, and analytical labs, the
> HPLC **injection** is already automated — but the **vial preparation**
> and **tray loading** that happen *before* injection are still done by
> hand. This folder works out how a **robotic arm** can take over that
> manual front-end.

New to a term? Plain-language definitions are inlined on first use
below; deeper robotics terms follow the same vocabulary as the
sibling project in `../../03-place-items-on-shelf/02-glossary.md`.

> **Disclaimer.** Market sizes, instrument prices, and regulatory
> details below are approximate (`~`) and drift — re-verify before
> quoting. This is a solution *design*, not a validated GxP system.

---

## What this is

A focused design note for a second, **higher-value** robotics target
than the grocery-shelf project (`../../03-place-items-on-shelf/`). The
shape is the same — take one concrete task, decompose it, and work out a
per-part solution — but the economics are stronger and the task is a
**clean fit for an arm**.

## Background: what HPLC and an "autosampler" are

**HPLC** (High-Performance Liquid Chromatography) is a standard
laboratory technique that separates a liquid mixture into its components
so they can be identified and measured — the workhorse of pharmaceutical
quality control, analytical chemistry, and environmental testing.

Samples are presented to the instrument in small **vials** (commonly
2 mL screw-cap or snap-cap vials) arranged in a **tray** (also called a
rack or carousel). An **autosampler** is the instrument module that
automatically draws a measured amount of liquid from the next vial and
**injects** it into the HPLC. That injection step is fully automated and
has been for decades.

## The gap (and why it's worth money)

Everything *before* the injection is still manual lab-tech labor:

- **Vial prep** — pipetting sample and diluent/solvent into vials,
  diluting to the right concentration, adding internal standards,
  capping, labeling.
- **Tray loading** — placing the right vials into the right tray
  positions, in the order the worklist expects.

This is repetitive, error-prone, and a bottleneck — and mistakes here
(wrong vial in wrong slot, wrong dilution, mis-labeled sample) are
expensive in a regulated lab. Meanwhile the **capital story works**:
HPLC systems and their automation run **~$50–150K+**, labs already
budget for instrument-grade capital, and an automation add-on carries a
**strong margin**. That combination — real pain, existing budget, good
margin — is why this is a better wedge than consumer/retail robotics.

## Why this is "purely an arm" problem

Unlike the shelf-stocking robot, this task needs **no mobile base**.
Everything happens within arm's reach on a single bench: vial racks, a
decapping station, a liquid-handling station, a labeler, and the
autosampler tray. That means a **fixed-mount robotic arm** (6-DoF, with
a suitable gripper and tool changer) is the whole robot. Removing
mobility removes the hardest, least reliable part of the stack and lets
the design concentrate on **dexterous manipulation, liquid handling,
perception, and lab-software/compliance integration**.

---

## How we divide the problem

We split the work into **10 parts**, read in order. The first frames the
task; the middle parts are the physical sub-tasks the arm must perform;
the last three are the perception, orchestration, software/compliance,
and hardware/business layers that make it a deployable product.

| # | Document | What it covers |
|---|----------|----------------|
| 01 | [`01-scope-and-workflow.md`](01-scope-and-workflow.md) | The manual process today, the target automated loop, the "simplest viable version," and the definition of done. |
| 02 | [`02-vial-handling-and-gripping.md`](02-vial-handling-and-gripping.md) | Reliably picking, holding, and moving small glass vials between stations without dropping or spilling. |
| 03 | [`03-decapping-and-capping.md`](03-decapping-and-capping.md) | Opening and closing vials — screw caps, snap caps, crimp/septa — the trickiest manipulation step. |
| 04 | [`04-liquid-handling-and-sample-prep.md`](04-liquid-handling-and-sample-prep.md) | Dispensing sample, diluent, and standards; dilution and mixing; integrating a pipettor or syringe pump. |
| 05 | [`05-tray-loading-and-positioning.md`](05-tray-loading-and-positioning.md) | Placing prepared vials into the autosampler tray in the exact position and order the worklist demands. |
| 06 | [`06-identification-labeling-and-tracking.md`](06-identification-labeling-and-tracking.md) | Barcodes/labels, vial→position→sample mapping, and chain-of-custody so every sample is traceable. |
| 07 | [`07-perception-and-verification.md`](07-perception-and-verification.md) | Vision to find vials/caps/slots, check liquid level and fill, and verify each step actually happened. |
| 08 | [`08-orchestration-error-handling-and-safety.md`](08-orchestration-error-handling-and-safety.md) | Sequencing the whole workflow, handling failures (missed grip, spill), retries, and safe-stop. |
| 09 | [`09-software-compliance-and-integration.md`](09-software-compliance-and-integration.md) | Talking to the LIMS/CDS worklist and meeting data-integrity rules (21 CFR Part 11, audit trail, GxP). |
| 10 | [`10-hardware-platform-and-capital-model.md`](10-hardware-platform-and-capital-model.md) | The arm/gripper/bench choice, enclosure & safety, and the cost/ROI story that closes the sale. |

Each part document follows the same shape:

1. **The problem** — what is manual or hard about this part today, and
   why it matters.
2. **The solution** — how the arm-based system automates it, the key
   design choices, and the trade-offs.
3. **v1 vs later** — what the simplest first version does, and what is
   deliberately deferred (keeping the "start simple" discipline).
4. **How it connects** — links to the neighbouring parts.

---

## Keep-it-simple framing (v1)

As in the shelf project, the first build deliberately narrows scope:
**one vial type, one tray format, one prep recipe, known fixed station
positions**, geometric/known-pose perception before anything learned,
and a human supervising. Breadth (many vial types, many recipes, full
walk-away autonomy) is a later milestone. The point of v1 is to prove
the **prep → load → inject hand-off** end to end on one real method.
