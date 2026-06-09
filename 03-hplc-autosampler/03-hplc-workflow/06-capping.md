# Step 6 — Capping

> **In one line:** close the vial with a lid, so the liquid cannot spill,
> evaporate, or be touched before the machine reads it.

This is the sixth of the eight steps (see the
[overview](README.md)). It follows
[Step 5 — Transfer to the vial](05-transfer-to-vial.md).

## The words you need here

- **Cap** — the **lid** that closes the vial. (As a verb, "to cap" means
  "to put the lid on.")
- **Screw cap** — a lid with a **thread** (the spiral ridge, like a
  drink-bottle top) that you **twist on**. This is the most common,
  easiest kind, and the kind we assume for our examples.
- **Crimp cap** — a metal lid that is squeezed tight with a special
  hand tool. It seals very well but is fiddlier. We mention it only so
  the word is not a surprise; our examples use the simpler screw cap.
- **Septum** — a small soft disc (usually rubber or soft plastic) inside
  the cap. The machine's needle pokes **through** this disc to draw the
  sample, and the disc reseals afterwards. So the cap is not fully
  solid — it is designed to be pierced.
- **Evaporate** — when a liquid slowly turns into vapour (gas) and
  escapes into the air, like a puddle drying up. Open vials lose liquid
  this way, which would slowly make the sample stronger and wrong.
- **Torque** — the **amount of twisting force** used to tighten the cap.
  Too little and it leaks; too much and it jams or cracks. "Just firm
  enough" is the goal.

## Why we do this

Once the sample is in the vial, it must be **sealed**:

- **Stop evaporation.** Our solvents (methanol, water) slowly evaporate
  in open air. If liquid escapes, the *amount of target stays the same
  but the liquid shrinks*, so the sample silently becomes **stronger**
  than we recorded — a hidden error.
- **Prevent spills.** The vials are about to be moved, tilted, and
  loaded into a machine. An open vial could tip and lose everything.
- **Keep it clean.** A sealed vial cannot catch dust or stray drops.
- **Let the machine work.** The autosampler's needle expects to pierce a
  capped vial through its **septum**. A capped vial is what the machine
  is built to handle.

## What you actually do (the general routine)

1. Pick up a cap (with its septum already inside).
2. Place it squarely on top of the vial — **straight, not crooked.**
3. For a screw cap: **twist** until it is **firm but not forced**.
4. Quickly check it is seated evenly and not cross-threaded (jammed on
   at a slight angle).

## Paracetamol and ketchup — the same step

By this point in the workflow, **both** examples behave identically.
Whether the vial holds clean paracetamol solution or clarified ketchup
extract, it is the **same kind of vial** with the **same kind of cap**,
and the capping motion is exactly the same. The earlier steps were where
food and drug differed; capping is one of the steps where they finally
look alike.

The only real-world difference is **count**: if the ketchup job involves
more vials (more batches and repeats), there are simply more caps to put
on — but each one is the same small action.

## What can go wrong

- **Cap too loose** → the seal leaks, the solvent evaporates, the sample
  drifts stronger, and it may even spill in the machine.
- **Cap too tight / cross-threaded** → the cap jams on crooked, can
  crack the glass, or will not seal properly.
- **Crooked placement** → an uneven seal that lets air in.
- **Wrong cap type** → a cap whose septum the machine's needle cannot
  pierce cleanly.

## For the robot arm

Capping is **medium** difficulty — it is **fiddly but highly
repeatable**. The challenges are lining the cap up squarely
(**alignment**) and twisting it to the right firmness (**torque
control**): firm enough to seal, gentle enough not to crack or jam. The
good news for automation is that, once tuned, this is the *same precise
motion every time* — exactly the kind of repetitive, well-defined task an
arm is well suited to. There is no judgement involved, just consistency.

## Objects needed in the simulation scene

Beyond the **shared workcell** (arm, gripper, table, overhead + wrist
cameras, AprilTag markers, racks), this step adds:

| Object | What it is | Mock node / topic |
|---|---|---|
| **Vial cap + septum** | The screw cap (with a pierceable septum) the capper seats | — |
| **Cap tray / dispenser** | Holds the caps at known poses for pickup | — |
| **Capper station** | A mock that ramps and reports applied torque, so the twin stops inside the seal-don't-crack band | `mock_capper` → `/mock_capper/screw`, `/capper/torque` |
| **Filled vial** | The vial from Step 5 being sealed | shared with Stage 4 |

These are **Stage 5** of the ketchup scene's
[object list](../05-mycobot-280-impl/01-only-code/01-simulation/01-ketchup-experiment-objects.md).

---

**Next step:** mark each vial so we always know what is inside it →
[Step 7 — Labeling](07-labeling.md).
