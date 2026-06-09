# Step 1 — Weighing

> **In one line:** measure out a tiny, exact amount of the sample, so we
> always start from a known quantity.

This is the first step. See the
[folder overview](README.md) for the full list of eight, and
[`../02-lab-bench-new.md`](../02-lab-bench-new.md) for the short summary
this file expands on.

## The words you need here

- **Weighing** just means *finding the weight of something* — the same
  idea as standing on a bathroom scale, but far more precise.
- **Analytical balance** — the special scale a lab uses. "Balance" is
  simply the lab word for "scale." It is extremely sensitive: it can
  measure down to **0.0001 of a gram** (that is one *tenth of a
  milligram* — far smaller than a single grain of salt). Because it is
  so sensitive, even a puff of breath would disturb it, so it sits
  inside a small **glass box** with little doors. That box is called a
  **draft shield** ("draft" = a movement of air).
- **Tare** — to "tare" the balance means to **set it back to zero** with
  an empty container already sitting on it. Then, when you add your
  sample, the scale shows *only the weight of the sample*, not the
  container. (Your kitchen scale's "zero" button does the same thing.)
- **Weighing boat / weighing paper** — a small disposable dish or square
  of glossy paper you put the powder on, so you do not pour it straight
  onto the scale.

## Why we do this

The whole test is about **amounts**. To say "this tablet contains 500
milligrams of medicine," we must compare it against a *known* amount.
And to know the strength (the **concentration**) of any liquid we make
later, we must know exactly how much solid we started with. If the
starting weight is wrong, **every number after it is wrong too** — no
later step can fix it. That is why weighing is done so carefully and
slowly.

## What you actually do (the general routine)

1. Place an empty container (a weighing boat, or the flask you will use)
   on the balance.
2. Close the little glass doors and press **tare** so the screen reads
   **0.0000**.
3. Open a door, and gently add a small amount of the sample.
4. Close the doors and wait for the number to settle.
5. Add or remove a tiny bit until you reach your target weight.
6. **Write the number down** (in a real lab the balance often sends the
   number straight to a computer so it cannot be mistyped).

## Paracetamol example (the easy case)

Paracetamol is a dry, solid powder pressed into a tablet, so it is
pleasant to weigh.

- In a full lab, you would first take **20 tablets**, weigh them
  together, and **crush them into an even powder** — this way one scoop
  represents the *average* tablet, not one lucky pill.
- Then you weigh out a small, exact amount of that powder — in our
  simple example, about **~5 milligrams** (mg) — onto a weighing boat.
- You do this once for **each** product you are comparing: your own
  batch plus the four competitor brands, so **five weighings**.
- You also separately weigh out some **certified pure paracetamol
  powder** (a trusted reference, like a "ruler" you measure the others
  against). This is the **reference standard**.

The powder is light and a little fluffy, so the main annoyances are
**static** (the powder clinging to the spoon) and breathing on it. None
of this is hard — it is just slow and precise.

## Ketchup example (the hard case)

Ketchup is not a tidy powder. It is a thick, sticky, wet paste. So
weighing changes in two ways:

- You usually weigh a **larger amount** — about **~5 grams** (g), which
  is roughly a teaspoon — because the chemical we want (5-HMF) is only
  present in tiny traces, so we need more material to find it.
- You weigh it **straight into a beaker** (a small cup-shaped glass
  container), not onto a flat boat, because the paste would smear
  everywhere. You put the empty beaker on the balance, press **tare**,
  then spoon ketchup in until you reach ~5 g.

The trouble with ketchup is that it is **sticky and clingy**: some stays
on the spoon, it does not pour cleanly, and the exact amount is harder
to hit than with a free-flowing powder. This stickiness is the first
small sign of why food samples are harder than tablets.

## What can go wrong

- **Too little or too much sample** → the final answer is off.
- **Static or stray powder** → grains jump around and the weight drifts.
- **Air movement** (a door left open, someone walking past) → the number
  will not settle.
- **Sticky residue left on the spoon** (ketchup) → you measured less
  than you think.
- **Not taring** → you accidentally include the container's weight.

## For the robot arm

Weighing is one of the **hardest** steps to fully automate. The reason
is subtle: positioning the container is easy, but *dispensing a powder a
fraction of a milligram at a time* is a delicate skill. A general arm
pinching powder would be clumsy. In practice this step is handled by a
**dedicated dosing balance** (a machine built only for this) that the
arm simply **feeds and unloads** — the arm carries containers to and
from it, rather than doing the fine powder work itself. Sticky samples
like ketchup are harder still.

## Objects needed in the simulation scene

Beyond the **shared workcell** (arm, gripper, table, overhead + wrist
cameras, a YOLO object detector, racks), this step adds:

| Object | What it is | Mock node / topic |
|---|---|---|
| **Sample source** | The tablet jar (paracetamol) or ketchup container the sample is drawn from | — |
| **Weighing boat / dish** | A small disposable dish for powder (paracetamol) | — |
| **Beaker** | Weighed *into* directly for sticky ketchup | — |
| **Scoop / spatula** | The tool the arm uses to add sample | — |
| **Analytical balance** | A mock that publishes a settled mass and a "weighed" flag | `mock_balance` → `/mock_balance/mass_g`, `/prep/weighed` |

These feed the ketchup scene's
[object list](../05-mycobot-280-impl/01-only-code/01-simulation/01-ketchup-experiment-objects.md)
(weighing happens just before Stage 1).

---

**Next step:** once we have our exact weighed amount, we need to get it
into a liquid → [Step 2 — Dissolution / extraction](02-dissolution-and-extraction.md).
