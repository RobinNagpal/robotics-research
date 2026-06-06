# Part 04 — Liquid handling & sample prep

> **Problem:** The real chemistry happens here — putting accurate
> volumes of sample, solvent, and standards into a vial and diluting to
> the right strength — and the volumes are tiny, the accuracy demands are
> tight, and a drop of carryover from one sample into the next can
> invalidate a whole batch.

## The problem

"Sample prep" is the wet-chemistry work a lab tech does to turn a raw
sample into something the HPLC can measure. A few terms first:

- **Diluent / solvent** — the liquid (often water, buffer, or an
  organic solvent like methanol/acetonitrile) used to dilute a sample to
  a known concentration.
- **Internal standard** — a known compound added in a fixed amount so
  the instrument can correct for small volume errors; getting its volume
  right matters as much as the sample's.
- **Dilution** — mixing a measured volume of sample with a measured
  volume of diluent to hit a **target concentration** the method expects.
- **Carryover / cross-contamination** — when traces of one sample end up
  in the next, via a dirty tip, nozzle, or needle. In a sensitive assay
  even nanograms of carryover skew results.

What makes this hard:

- **Volume accuracy across a wide range.** Methods call for anything
  from a few **microlitres** (µL, millionths of a litre — e.g. spiking
  an internal standard) up to a couple of **millilitres** (mL). One
  device rarely covers the whole span accurately, and accuracy/precision
  must be repeatable vial after vial.
- **Cross-contamination is the dominant risk.** Every fluid path that
  touches more than one sample is a carryover route. Control means
  either a fresh disposable **tip** per sample, or a defined **wash**
  (flush the path with solvent, sometimes to waste) between samples.
- **Volatile solvents.** Many diluents evaporate fast, are flammable,
  and give off fumes — so open vials should be exposed briefly, dispense
  should be quick and bubble-free, and the workspace may need fume
  extraction.
- **Mixing.** After dilution the contents must be homogeneous; a
  layered, unmixed vial reads wrong. **Vortexing** (rapid orbital
  shaking) is the usual fix.

The temptation is to have the arm "pipette" like a human. That is the
wrong instinct: a 6-DoF arm is not built to meter a 5 µL volume to
sub-percent accuracy. Metering is a job for a precision fluidics device.

## The solution

**Do not make the arm pipette freehand.** Instead pair the arm with a
proper **metering device** and let each side do what it is good at — the
device meters volume precisely; the arm positions vials and tips.

Metering-device options:

- **Lab syringe pump.** A motor-driven syringe with a valve; excellent
  accuracy and precision over a wide volume range, ideal for a fixed
  dispensing nozzle. The workhorse choice.
- **Bottle-top / peristaltic dispenser.** Simpler and cheap for
  repeated fixed volumes of one bulk diluent; peristaltic (squeezing a
  flexible tube) keeps fluid in disposable tubing, which helps with
  cleanliness, but is less precise at very small volumes.
- **OEM pipetting head.** A buyable air-displacement pipettor module
  (the kind inside liquid-handling robots) that uses disposable tips —
  best contamination control, multi-reagent capable, highest cost and
  integration effort.

Two ways to bring vial and fluid together:

- **Present-the-vial-to-a-fixed-nozzle (recommended for v1).** The
  metering device and its dispense nozzle are bolted to the bench; the
  arm brings each open vial under the nozzle. The fluid path is fixed,
  short, and easy to wash — simplest and most reliable.
- **Carry-a-pipetting-tool.** The arm picks up a pipettor via the
  tool-changer (the quick-swap interface from
  [`03-decapping-and-capping.md`](03-decapping-and-capping.md)) and
  pipettes from reservoirs into vials with disposable tips. More
  flexible (multiple reagents, serial dilutions) but more to integrate
  and to keep clean.

**Optional gravimetric verification.** Place the vial on a precision
**balance** (scale) before and after a dispense; the mass gained, with
the liquid's known density, confirms the volume actually delivered.
This turns "we commanded 500 µL" into "we measured 0.50 g delivered" —
strong evidence for a regulated record, at the cost of an extra weighing
step. See [`07-perception-and-verification.md`](07-perception-and-verification.md).

### Approaches compared

| Approach | Volume accuracy | Contamination control | Multi-reagent | Cost / integration | Bottom line |
|---|---|---|---|---|---|
| **Fixed syringe-pump nozzle, arm presents vial** | Excellent over wide range | Wash between samples | Limited (per added line) | ~Moderate, simplest | **Recommended for v1.** Best accuracy-for-effort; fixed, washable path. |
| **Bottle-top / peristaltic, fixed volume** | Good for one bulk volume | Tubing/wash | Single diluent | ~Low | Great when v1 only needs one fixed diluent volume. |
| **OEM pipetting head on tool-changer** | Excellent, very small volumes | Best — disposable tips | Yes — many reagents | ~High | The path to complex recipes; defer past v1. |
| **Arm pipettes freehand** | Poor / unrepeatable | n/a | n/a | "Cheap" | Don't — metering is not an arm's job. |

**Top choice: a fixed syringe-pump dispensing nozzle with the arm
presenting each open vial**, a defined wash between samples (or
disposable tips if a pipetting head is used), and optional gravimetric
verification on a bench balance. Mixing is handled by a fixed vortexer
station the arm presents capped vials to.

## v1 vs later

**v1 (simplest that proves the loop):**

- A **single fixed-volume dispense** of **one diluent** at **one
  dispensing station** (fixed syringe-pump nozzle).
- **One recipe**, one vial type, known fixed station positions.
- **Wash between vials** (or one disposable tip per vial) to control
  carryover.
- Optional **gravimetric check** on a balance to confirm the dispense.
- Mixing via a fixed vortexer if the recipe needs it; otherwise skipped.
- Human supervising.

**Deferred to later:**

- **Multi-reagent and serial dilutions** (dilute, then dilute again to
  reach low concentrations) and **complex, multi-step recipes**.
- Adding **internal standards** and multiple solvents in one run.
- A **tool-changer pipetting head** for very small volumes and many
  reagents.
- Automatic recipe selection and on-the-fly volume calculation beyond
  the one fixed recipe.

## How it connects

- [`02-vial-handling-and-gripping.md`](02-vial-handling-and-gripping.md)
  and [`03-decapping-and-capping.md`](03-decapping-and-capping.md) — the
  vial must be securely held and **open** before any liquid goes in;
  it is recapped afterwards.
- [`06-identification-labeling-and-tracking.md`](06-identification-labeling-and-tracking.md)
  — identity drives which sample this is and therefore which recipe and
  volumes to apply.
- [`07-perception-and-verification.md`](07-perception-and-verification.md)
  — checks liquid level / fill (and the optional gravimetric mass) to
  confirm the dispense actually happened correctly.
- [`09-software-compliance-and-integration.md`](09-software-compliance-and-integration.md)
  — the recipe (volumes, diluent, target concentration) comes from the
  worklist in the LIMS/CDS, and the delivered volumes are recorded.
- Back to the index: [`README.md`](README.md).
