# Part 01 — Scope & workflow

> **Problem:** Before an HPLC instrument can run, a lab tech must
> hand-prepare and hand-load every vial in the exact order the
> instrument expects — slow, repetitive, and error-prone. This part
> fixes the boundary of what we automate and the loop the arm runs.

## The problem

In a QC, pharma, or analytical lab, an HPLC run does not start with the
instrument. It starts with a person at a bench doing a fixed sequence of
manual steps. Defining that sequence precisely is the whole job of this
document, because the arm has to reproduce it move for move.

First, a word that everything hangs on. A **worklist** (also called a
**sequence**) is the ordered list of samples the instrument will run,
one row per injection. Each row says, in effect, "tray position 7 is
sample ABC-123, run method M, expect this dilution." The autosampler
walks that list top to bottom and injects from the matching tray
position. If a vial is in the wrong slot, or prepared the wrong way, the
instrument has no way to know — it just injects whatever is physically
there. So the manual front-end is not only tedious, it is the step where
an undetected mistake silently corrupts the result.

The manual end-to-end process today looks like this:

1. **Receive samples + the worklist.** The tech gets a set of incoming
   samples (in tubes, bottles, or primary containers) and the worklist
   that says what to make and in what order.
2. **Measure / weigh.** For each sample, measure out the required amount
   — by volume (pipette) or by mass (balance), depending on the method.
3. **Dilute / add diluent + internal standard.** Add **diluent** (the
   solvent that brings the sample to the right concentration) and, where
   the method calls for it, an **internal standard** (a known reference
   compound spiked into every sample so the instrument can correct for
   small variations).
4. **Transfer into vial.** Move the prepared liquid into a clean 2 mL
   vial — the small glass container the autosampler draws from.
5. **Cap.** Close the vial (screw, snap, or crimp cap) so it does not
   evaporate or spill, and so the autosampler needle can pierce or the
   cap can be handled cleanly.
6. **Label.** Apply a human- and machine-readable label (often a
   barcode) so the vial is traceable to its sample identity.
7. **Arrange vials in the tray in worklist order.** Place each capped,
   labeled vial into the tray position its worklist row names.
8. **Load tray into the autosampler.** Slide or seat the full tray into
   the instrument's autosampler module.
9. **Start the run.** Hand off to the instrument software and begin
   injection.

Why it matters: steps 2–7 are repetitive lab-tech labor on the critical
path of every analysis, and the failure modes (wrong dilution, wrong
vial in wrong slot, mis-labeled sample, a vial left uncapped) are
exactly the ones a regulated lab spends the most money detecting and
investigating after the fact.

## The solution

We automate steps 2–8 with a single fixed-mount 6-DoF arm working a
bench of fixed stations, and we let the instrument keep doing step 9.
The arm does not move around the room; everything is within reach.

**Bench layout (target).** Stations are at known, fixed positions so the
arm can reach each with a calibrated pose:

```
            [ liquid-handling / dispense station ]
                          |
 [ vial-supply rack ] --- ARM --- [ decapping / capping station ]
                          |
        [ labeler / barcode station ]   [ autosampler tray ]
```

- **Vial-supply rack** — a nest of empty, capped 2 mL vials in known
  positions the arm picks from (see `02-vial-handling-and-gripping.md`).
- **Decapping / capping station** — holds and turns the cap while the
  arm presents the vial (see `03-decapping-and-capping.md`).
- **Liquid-handling / dispense station** — a pipettor or syringe pump
  that delivers sample, diluent, and standard into the open vial (see
  `04-liquid-handling-and-sample-prep.md`).
- **Labeler / barcode station** — applies and/or reads the vial label
  (see `06-identification-labeling-and-tracking.md`).
- **Autosampler tray** — the destination; the arm seats each finished
  vial in its worklist position (see `05-tray-loading-and-positioning.md`).

**The target automated loop** the arm performs, per vial, driven by the
worklist:

1. Read the next worklist row (which sample, which recipe, which slot).
2. Pick an empty vial from the supply rack.
3. Present it to the decapping station; uncap.
4. Move to the dispense station; add sample + diluent (+ standard).
5. Re-present to the capping station; cap.
6. Label and/or read the barcode; record vial → sample → slot.
7. Verify (level, cap seated, label readable) before committing.
8. Place the vial in the correct tray slot.
9. When the batch is done, hand the loaded tray to the autosampler.

**A design choice worth flagging early** — order of label vs. fill.

| Choice | Pros | Cons | Bottom line |
|---|---|---|---|
| Label empty vials first | Simple; label flat dry glass | Must track which blank label maps to which sample | Fine if mapping is logged |
| Fill, then label | Label reflects real contents | Handle a full vial near a labeler | Safer for traceability |
| Pre-barcoded vials | No labeler needed in v1 | Needs barcoded consumables | **Best v1**: read, don't print |

For v1 we prefer **pre-barcoded vials we only read**, which removes a
whole station and a whole failure mode while keeping traceability.

## v1 vs later

**v1 — the simplest viable version.** Deliberately narrow:

- **One vial type** — a single 2 mL screw-cap vial, one cap style.
- **One tray format** — a single autosampler rack geometry.
- **One prep recipe** — e.g. a single fixed-volume dilution (fixed
  sample volume + fixed diluent volume, no internal standard yet).
- **Known fixed station positions** — every station calibrated once;
  no on-the-fly discovery of where things are.
- **Geometric / known-pose perception** — the arm trusts taught poses
  and uses vision only to *verify*, not to search (see
  `07-perception-and-verification.md`).
- **Human refills reagents and consumables** — diluent bottles, empty
  vials, caps — and **a human supervises** the whole run.

**Deferred to later milestones:** multiple vial sizes and cap styles;
multiple tray formats; multiple/parameterized recipes including internal
standards and serial dilutions; on-board label *printing*; learned
perception for messy or unknown layouts; unattended walk-away operation;
tool-changer swaps between gripper and pipettor.

**Definition of done (v1).** The system can: take a worklist of N
samples; prepare N vials per the single recipe; load them into the tray
in the exact worklist order; perform **per-vial verification** (correct
fill level, cap seated, barcode readable, right slot); produce an
**audit log** that records what happened to each vial (timestamps, pose,
verification results, operator); and hand off the loaded tray so the
autosampler can start — all with a human supervising and no manual
intervention during the batch.

**Explicit non-goals (v1).** No mobile base (this is a pure-arm
problem). No running the HPLC method itself or interpreting
chromatograms. No weighing/gravimetric prep (volume only). No handling
of hazardous/biohazard samples requiring containment beyond a basic
enclosure. No multi-instrument scheduling. No claim of a validated GxP
system — compliance design lives in
`09-software-compliance-and-integration.md` and must be re-verified.

## How it connects

- **`02-vial-handling-and-gripping.md`** — every step above starts and
  ends with the arm holding a vial; that part defines how.
- **`05-tray-loading-and-positioning.md`** — step 8 (worklist-order
  placement) is the payoff this scope exists to deliver.
- **`08-orchestration-error-handling-and-safety.md`** — the per-vial
  loop and verify-before-commit gates are sequenced and recovered there.
- **`09-software-compliance-and-integration.md`** — the worklist comes
  from, and the audit log goes to, the lab's software (LIMS/CDS).
- Back to the index: [`README.md`](README.md).
