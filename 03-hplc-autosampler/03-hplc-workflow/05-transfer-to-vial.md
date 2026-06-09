# Step 5 — Transfer to the vial

> **In one line:** move the finished clean liquid into the small glass
> bottle that the machine actually reads from.

This is the fifth of the eight steps (see the
[overview](README.md)). It follows
[Step 4 — Filtering](04-filtering.md).

## The words you need here

- **Vial** — a small glass bottle, usually holding about **2 mL** of
  liquid (less than a teaspoon). This is the *only* container the
  machine reads from. Everything we have done so far — weighing,
  dissolving, diluting, filtering — was in bigger glassware; now, at
  last, the liquid moves into its final home. The vial is about the size
  of your little finger, with a narrow opening at the top.
- **Transfer** — simply *moving liquid from one container into another*.
- **Meniscus** — the slight curve a liquid makes at its surface inside a
  narrow container. You do not need to worry about it much here; it just
  means the surface is not perfectly flat.
- **Headspace** — the empty air gap left above the liquid in the vial.
  For most samples a little air is fine; for some special tests it
  matters, but not for our two examples.

## Why we do this

The machine's **autosampler** (the part that feeds samples in
automatically) is built to reach into tiny vials in fixed positions and
draw a sip from each. It cannot reach into a beaker or a flask. So the
final, clean liquid must be placed into one of these standard little
bottles. This is the step where the sample finally takes the shape the
machine expects.

It is also a step where a careless mistake is **expensive**, because all
the earlier work is already done. Putting the liquid in the **wrong**
vial, or letting two samples mix, would waste everything that came
before.

## What you actually do (the general routine)

1. Have a clean, empty vial ready (often held upright in a small rack).
2. Take the clean filtered liquid (often the filtering in
   [Step 4](04-filtering.md) feeds **straight** into the vial — the two
   steps are usually done in one motion).
3. Aim carefully over the **narrow opening** and let the liquid flow in.
4. Fill to roughly the right level — you do not need it full; even a
   small amount (often under 2 mL) is plenty for the machine.
5. Move on to the next vial, keeping each sample strictly separate.

## Paracetamol example (the easy case)

- You have five clean paracetamol solutions (your batch + four brands),
  plus the reference standard, plus a blank.
- For each, you guide the filtered liquid into its **own** 2 mL vial.
- Because the liquid is thin and clear, it pours easily and predictably.
- The whole challenge is simply **aim**: the vial mouth is small, so you
  must line up over it without spilling or touching the rim.

## Ketchup example (the hard case)

- The clarified, filtered ketchup extract is now a thin liquid too, so
  the **pouring action is no harder** than for paracetamol.
- The extra care is about **keeping batches separate and correctly
  matched**: you may have several supplier batches, each with two or
  three repeat preparations, so there are more vials to keep straight
  and more chances to mix one up.

In other words, by this late stage the *liquids* look similar; the food
case is harder only because there are **more vials to track**, not
because the pour itself is messier.

## What can go wrong

- **Wrong vial** → the sample is mislabelled from birth; the result will
  be attributed to the wrong source.
- **Spilling or missing the opening** → lost sample, and the earlier
  work is wasted.
- **Cross-contamination** → a drop of one sample left on a tool ends up
  in another vial, blurring the results.
- **Touching the inside or rim** → introduces dirt or oils that the
  sensitive machine may pick up.

## For the robot arm

This is one of the **most important** steps for the whole automation
idea, because it is the clearest test of **precise positioning**. The
target — the vial's opening — is small, but it is a *millimetre-scale*
target, not a microscopic one. The arm does **not** need extreme
sub-millimetre precision; it needs to hit a small, fixed opening
**reliably, every single time**. That makes "transfer to vial" the ideal
**first experiment** for a proof-of-concept: a clean, consistent
paracetamol sample and one simple question — *can the arm hit the vial
opening repeatably?* Get that right and much of the rest follows.

## Objects needed in the simulation scene

Beyond the **shared workcell** (arm, gripper, table, overhead + wrist
cameras, AprilTag markers, racks), this step adds:

| Object | What it is | Mock node / topic |
|---|---|---|
| **2 mL HPLC vial** | The narrow-mouth final container — the millimetre-scale pour target | `mock_vial` → `/vial/fill_ml`, `/vial/spill` |
| **Vial rack / nest** | Holds the empty vial upright at a known pose | shared workcell |
| **Clean-liquid source** | The syringe/pipette carrying the filtered liquid (from Step 4) | — |

This is **Stage 4** of the ketchup scene's
[object list](../05-mycobot-280-impl/01-only-code/01-simulation/01-ketchup-experiment-objects.md)
— the clearest single test of the arm's positioning accuracy.

---

**Next step:** seal the vial so nothing spills or evaporates →
[Step 6 — Capping](06-capping.md).
