# Part 07 — Perception & verification

> **Problem:** The arm cannot trust that a step worked just because it
> ran the motion — a vial can be missed, a cap left on, a fill short.
> This part gives the system eyes, and turns "looking" into a set of
> hard checkpoints the workflow is not allowed to pass without.

## The problem

In a regulated lab the expensive failures are silent ones: a vial that
never got picked, a cap still on when the dispense needle comes down, a
half-filled vial that the instrument injects anyway. A blind arm running
taught motions will happily do all of these and report success, because
nothing told it otherwise. The job of perception here is therefore two
jobs:

1. **Sense the world** — find vials, caps, slots, and liquid so the arm
   can act and so we can describe what is actually there.
2. **Verify each step** — after every action, confirm the world changed
   the way it should have *before* the next action is allowed to start.

The second job matters more than the first. Most of the time the world
is exactly where it was taught to be (fixed stations, known positions —
see `01-scope-and-workflow.md`), so we do not need clever search. We
need cheap, reliable confirmation, and the discipline to **stop when
confirmation fails** rather than press on.

A note on two camera types, because the rest of this document leans on
the distinction:

- **RGB camera** — an ordinary colour camera. It returns a flat picture
  (red/green/blue pixels). Great for reading barcodes, reading a printed
  fiducial, spotting a colour change (foam, a spill), and 2-D position.
  It does **not** directly know how far away anything is.
- **RGB-D camera** ("D" for depth) — a colour camera plus a depth
  sensor, so every pixel also carries a distance. This gives 3-D shape:
  how tall the liquid column is, whether a slot is empty, how far the
  vial rim is from the gripper. Common, inexpensive, and the natural
  choice when "is it there and how full" matters.

A **fiducial marker** is a printed pattern designed to be found and
measured by a camera — think a small high-contrast square sticker.
**AprilTags** are a widely used fiducial: each tag is a unique
black-and-white square that vision software can detect fast and turn
into an exact position and orientation (**pose**) plus an ID number.
Stick AprilTags on the supply rack, the tray, and the stations and the
arm gets a precise, self-checking reference frame almost for free.

## The solution

Use **two camera vantage points**, not one:

- **A wrist camera** mounted on the arm near the gripper. It moves with
  the arm, so it can look straight down a vial it is about to pick,
  read a barcode it is holding, or inspect a slot from directly above.
- **Fixed station cameras** that watch a station from a known angle —
  e.g. a side-on RGB-D view of the dispense station to read liquid
  level, or a top-down view of the tray to read slot occupancy across
  the whole rack at once.

The wrist camera gives close, on-demand, correctly-aligned views; the
fixed cameras give whole-scene context and a second independent witness
for verification. Two viewpoints also let one confirm the other.

**Method order — known-pose and fiducials first, learning later.** For
v1 we deliberately avoid general "find any vial in any pose" detection.
Instead:

- **Known poses** — stations are calibrated once; the arm goes to taught
  coordinates.
- **Fiducials (AprilTags)** — give exact, drift-correcting reference
  frames and unambiguous IDs.
- **Simple geometric checks** — circle/edge finding for a vial rim,
  height of a liquid column, an empty-vs-filled slot by depth.

Learned/neural detection (a trained model that recognises objects in
messy, unknown scenes) is deferred until v1's narrow, tidy world is
proven. It is more capable but harder to validate in a regulated lab —
see `09-software-compliance-and-integration.md`.

### What to sense at each step

| Step | What to sense | Camera | Method | Bottom line |
|---|---|---|---|---|
| Locate vial in supply rack | Vial present in known cell; rim centre | Wrist RGB-D | Known pose + rim find | Confirm before grip |
| Confirm pick | Vial now in gripper (gone from rack / seen in hand) | Wrist + fixed | Presence check, 2 views | Catch missed grips early |
| Cap presence / orientation | Is a cap on; is it square | Wrist RGB-D | Geometric profile | Don't dispense into a capped vial |
| Confirm decap | Open rim visible, no cap | Wrist | Edge/depth check | Gate before fill |
| Liquid level / approx volume | Height of liquid column | Fixed RGB-D side view | Depth/edge of meniscus | Approximate, not metrology-grade |
| Spill / foam / bubbles | Stray liquid, froth on top | Fixed + wrist RGB | Colour/texture anomaly | Flag, don't proceed |
| Confirm cap (re-cap) | Cap seated, flush, square | Wrist RGB-D | Profile + AprilTag frame | Seal integrity matters |
| Read barcode / label | Readable, matches worklist | Wrist RGB | Barcode decode | See `06-...tracking.md` |
| Slot occupancy (tray) | Empty vs filled per cell | Fixed top-down RGB-D | Depth per cell | Avoid placing into an occupied slot |
| Confirm seated | Vial fully down in correct slot | Fixed top-down | Depth + position | Final gate before next vial |

**Liquid-level caveat.** A camera reads an *approximate* fill — enough
to catch "empty / way short / overfilled / foaming," not a certified
volume. Accurate volume is the dispenser's job (see
`04-liquid-handling-and-sample-prep.md`); the camera is the independent
sanity check that the dispense visibly happened.

### Verification gates

The organising idea is the **verification gate**: a checkpoint between
two workflow steps that must return PASS before the next step starts. If
it returns FAIL (or UNSURE), the arm does not continue — it hands off to
error handling.

```
pick vial ──▶ [GATE: in gripper?] ──▶ decap ──▶ [GATE: open rim?]
   ──▶ dispense ──▶ [GATE: right level? no spill?] ──▶ cap
   ──▶ [GATE: cap seated?] ──▶ read barcode ──▶ [GATE: matches worklist?]
   ──▶ place in slot ──▶ [GATE: seated in correct slot?] ──▶ next vial
```

Each gate is small and cheap, but together they mean a defective vial
cannot silently reach the instrument. Every gate result (pass/fail, the
image or measurement, timestamp) is logged for the audit trail in
`09-software-compliance-and-integration.md`. A failed gate is an event
for `08-orchestration-error-handling-and-safety.md` to act on.

## v1 vs later

**v1 — keep it simple.**

- **Known fixed positions** — perception verifies taught poses; it does
  not search an unknown bench.
- **Fiducials everywhere** — AprilTags on rack, tray, and stations for
  exact, self-checking reference frames and IDs.
- **Simple liquid-level check** — one fixed RGB-D side view giving
  approximate fill, plus a basic spill/foam flag.
- **Verification gates between every step** — pass-to-proceed, fail-to-
  halt, all results logged.
- **Wrist camera + a small number of fixed cameras** — no large camera
  array.

**Deferred to later milestones:** learned/general object detection for
messy or mixed layouts; reading hand-written or damaged labels;
pose-free "find any vial anywhere" picking; precise vision-based volume
metrology; detecting subtle quality defects (particulates, colour
shifts) beyond gross spill/foam; multi-vial-in-flight tracking.

## How it connects

- **`02-vial-handling-and-gripping.md`** — perception locates the vial
  to pick and confirms it is in the gripper after the grip.
- **`03-decapping-and-capping.md`** — gates confirm the vial is actually
  decapped before fill and the cap is seated afterwards.
- **`04-liquid-handling-and-sample-prep.md`** — the approximate level /
  spill / foam checks verify the dispense visibly happened.
- **`05-tray-loading-and-positioning.md`** — slot-occupancy and seated
  checks confirm the right slot is empty and the vial is fully down.
- **`08-orchestration-error-handling-and-safety.md`** — a failed gate is
  what triggers retry, stop, or quarantine.
- Back to the index: [`README.md`](README.md).
