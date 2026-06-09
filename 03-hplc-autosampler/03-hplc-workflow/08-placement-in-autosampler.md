# Step 8 — Placement in the autosampler

> **In one line:** put each finished, labelled vial into its exact
> numbered slot in the machine, in the right order.

This is the eighth and final step (see the
[overview](README.md)). It follows
[Step 7 — Labeling](07-labeling.md). After this, the human's hands-on
work is done and the machine takes over.

## The words you need here

- **Autosampler** — the part of the HPLC machine that **holds many vials
  and feeds them in one at a time, automatically**. "Auto" = automatic,
  "sampler" = the thing that takes a sample. Instead of a person
  injecting each vial by hand, the autosampler works its way through the
  whole tray on its own, often for hours, even overnight.
- **Tray / rack / carousel** — the holder that the vials sit in. It is a
  grid (or a circle) of **numbered slots**, each shaped to hold one
  vial. A "carousel" is just a round, rotating version of the same idea.
  Trays commonly have **96 or 120 positions**.
- **Position / slot** — one numbered hole in the tray. Position 1,
  position 2, and so on. Each vial belongs in a **specific** position.
- **Sequence / worklist** — the **ordered list** that tells the machine
  *which position holds which sample, and in what order to run them*. It
  is the machine's to-do list. The vial in position 1 must be the sample
  the worklist *says* is in position 1.
- **Run** — when the machine starts working through the sequence,
  injecting and measuring each vial in turn.

## Why we do this

The machine does not know what any vial is — it only knows **positions**.
It will draw from "position 1," then "position 2," and so on, and write
the results against those position numbers. So the vials must be placed
**in the exact positions the worklist expects**. If a vial sits in the
wrong slot, the machine will happily measure it and record the answer
under the **wrong name** — a silent, serious mistake.

Order also matters. A proper run is not just the samples; it is usually:

- a **blank** first (solvent only, to prove nothing is contaminating the
  readings),
- some **reference standards** (known strengths, so the machine "learns
  the scale"),
- then the **actual samples**, often with standards repeated partway
  through to prove the machine did not drift.

Getting this **order** right is part of placing the vials correctly.

## What you actually do (the general routine)

1. Look at the **worklist**: it says position 1 = this, position 2 =
   that, and so on.
2. Take each labelled vial and set it gently into its **matching
   numbered slot**.
3. **Double-check** that each vial's label matches the position the
   worklist assigns it.
4. Slide the tray into the machine and start the **run**.
5. Walk away — the autosampler now works through every vial by itself.

## Paracetamol example (the easy case)

A simple, sensible order for the drug comparison might be:

| Position | Vial |
|---|---|
| 1 | Blank (solvent only) |
| 2 | Standard (pure paracetamol reference) |
| 3 | In-house batch |
| 4 | Brand A |
| 5 | Brand B |
| 6 | Brand C |
| 7 | Brand D |
| 8 | Standard again (drift check) |

You place each of the ~6–8 vials into its slot, in order, confirm each
matches the worklist, and start the run. Because there are few vials,
this is quick and low-stress.

## Ketchup example (the hard case)

The **action is identical** — set each vial into its numbered slot — but
there are simply **more vials** (several supplier batches × 2–3 repeats,
plus standard and blank, perhaps ~8–12 or more). More vials in the tray
means:

- **more positions to get right**, and
- a **higher chance of a slip** — putting "Supplier-2 rep-2" where
  "Supplier-1 rep-2" should go.

So, as with the previous few steps, food is not harder to *place* — it
is harder to *keep track of*, because of the count.

## What can go wrong

- **Vial in the wrong position** → the result is recorded under the
  wrong sample. Like a mislabel, the numbers look fine but mean the
  wrong thing.
- **Wrong order** → the blank or standards are not where the method
  expects, so the run's checks fail or the data is invalid.
- **Vial not seated properly** → the machine's needle may miss it or
  jam.
- **A position skipped** → the sequence and the tray no longer match
  from that point on.

## For the robot arm

Placement is one of the **easier and most natural** steps to automate —
and a perfect showcase for an arm. The slots are at **fixed, known
positions**, the same every time, so it becomes precise **pick-and-place
into a known grid**: take vial, move to position N, set it down, repeat.
There is no messy liquid and no judgement — just exact, repeatable
positioning, which is exactly what robot arms are best at. A machine also
**never loses track of the order** the way a tired person at 11:45 p.m.
might, so automating this step can make the run *more* reliable, not just
faster.

## Objects needed in the simulation scene

Beyond the **shared workcell** (arm, gripper, table, overhead + wrist
cameras, a YOLO object detector, racks), this step adds:

| Object | What it is | Mock node / topic |
|---|---|---|
| **Autosampler tray / carousel** | The destination grid of numbered slots (~96–120) | — |
| **Scene lighting + matte backdrop** | Even, varied lighting so the overhead camera's **YOLO** detector locates the tray; slots are indexed from the tray's known geometry | domain-randomized |
| **Labelled vial** | The finished vial from Step 7 being placed | shared with Stage 4 |
| **Vial rack (source)** | Holds the finished vials before they go to the tray | shared workcell |

The autosampler tray is part of the **shared workcell** in the ketchup
scene's
[object list](../05-mycobot-280-impl/01-only-code/01-simulation/01-ketchup-experiment-objects.md)
(placement happens just after Stage 6).

---

**That is the full workflow.** From a weighed speck of powder or a spoon
of ketchup, through dissolving, diluting, filtering, vialling, capping,
labelling, and placing — the sample is now a clean liquid in a labelled
bottle sitting in the machine, ready to be read. Everything after this
point the HPLC does on its own.

Back to the [workflow overview](README.md), or up to the
[sample-prep primer](../02-lab-bench-new.md).
