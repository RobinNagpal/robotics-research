# Part 05 — Tray loading & positioning (simulation)

> **Sim goal:** Prove that the reBot arm can place a carried vial
> into the *correct* autosampler-tray slot — centred, fully seated,
> and without knocking its neighbours — and that the
> worklist-row → physical-slot mapping is realised exactly, all in
> Gazebo before any tray hardware exists.

This mirrors the high-level
[`../03-high-level-solution/05-tray-loading-and-positioning.md`](../03-high-level-solution/05-tray-loading-and-positioning.md).
New robotics terms are defined in
[`../../03-place-items-on-shelf/02-glossary.md`](../../03-place-items-on-shelf/02-glossary.md).

## What we can prove in simulation

The **autosampler tray** (also called a rack) is a flat holder with
many small cylindrical pockets — **slots** — in a regular grid. Its
key property is a **fixed pitch**: the centre-to-centre spacing
between slots is a known constant. That makes the whole tray a
predictable geometric model we can stand up in sim.

**Can prove fully in open-source sim:**

- **Reachability** — that the arm can reach every slot of the tray
  from its fixed bench position, without joint limits or
  self-collision blocking any slot.
- **Collision-free placement** — that MoveIt 2 can plan a path to
  each slot and a straight-down approach that does not clip the
  **neighbouring vials** already placed in a dense grid.
- **The placement sequence** — plan-above-slot → straight-down
  approach → (optional) compliance/search → release (detach) →
  straight-up retreat — runs end to end and repeats for a full tray.
- **Worklist → slot mapping** — that worklist **row N** drives the
  arm to the intended **physical slot** (A1, A2, …), with the
  registry in Part 06 agreeing on which vial went where.
- **Cycle time per slot**, feeding the throughput / ROI estimate.

**Honest limits (need real hardware to settle):**

- **Real seating force.** Whether the vial actually drops all the
  way home depends on real friction, slot taper, and how hard the
  arm pushes. Sim "seats" the vial by an **attach** event, not by
  feeling contact.
- **Tray tolerances.** Real trays have manufacturing slop and the
  tray may not sit *exactly* where the model says. Sim assumes a
  perfectly known tray pose; real life needs the calibration/teach
  step to be repeated on hardware.
- **Clean release.** Whether the gripper withdraws without dragging
  the just-placed vial back out is a friction question sim only
  approximates.

So sim proves the **logic, geometry, reachability, sequencing, and
the no-collision-with-neighbours** claim; it de-risks but does not
finally prove **seating reliability**.

## Open-source tools

| Tool | Role | Bottom line |
|------|------|-------------|
| **Gazebo Harmonic** | Hosts the bench, the reBot arm, the tray model, and the vials | The world the whole place-loop runs in |
| **MoveIt 2** | Plans the collision-free path to each slot + the short Cartesian (straight-line) approach and retreat | Owns "reach the slot without hitting neighbours" |
| **`ros2_control` + `gz_ros2_control`** | Runs the reBot joint controllers in sim, same interface as the real arm | No hardware driver needed to move the arm |
| **Grasp-fix plugin** (Gazebo) | Models the gripper holding the vial in transit and the "seat" on release as an attach/detach event | Stands in for real grip + seating contact |
| **MuJoCo** (optional) | Contact-rich refinement of the final straight-down insertion if Gazebo contacts look too coarse | Only if you want finer insertion physics |
| **tf2** (ROS 2) | Publishes one named transform **per slot** (A1, A2, …) the arm plans to | The slot map lives here as tf frames |
| **RViz2 / Foxglove** | Visualise the tray frames, the plan, and which slots are filled | Eyeball the sequence and catch near-misses |

## How to simulate it now

**1. Build the tray model + per-slot tf frames.**

- Add a static **tray model** (SDF/URDF) to the Gazebo world at a
  fixed pose on the bench — a block with the grid of slot pockets.
- Compute one **tf frame per slot** from the corner origin and the
  known **pitch**: e.g. `tray/A1`, `tray/A2`, … `tray/F9`. A small
  node (or a static-transform launch) broadcasts them all relative
  to a single `tray_origin` frame.
- Model the **calibration/teach step in sim**: instead of hard-coding
  the origin, run a tiny "teach" routine that records the tray-origin
  pose (in sim, read it straight from the model; on hardware this is
  where a fiducial or jogging the arm to a corner slot comes in).
  Keeping this step in the sim workflow means the hardware version
  drops in later with no code change.

**2. Implement sequential placement.**

A `tray_loader` node (or a behavior-tree subtree, see Part 08) does,
per worklist row:

- Look up the target slot frame for this row (row 1 → `tray/A1`, …;
  the **sequential** v1 rule keeps the map trivial to audit).
- Ask **MoveIt 2** for a plan to a **pre-place pose** ~3–5 cm above
  the slot frame.
- Execute a short **Cartesian straight-down approach** to the
  insertion depth.
- *(Optional)* run a small **spiral/search** wiggle or a brief
  **MuJoCo** insertion to mimic self-centring on the slot taper.
- Trigger the **grasp-fix detach** to release the vial and an
  **attach to the slot/tray** to "seat" it, so it stays put.
- Execute a **straight-up retreat**, then plan to the next row.

**3. Check no collision with neighbouring vials.**

- Represent each already-placed vial as a **collision object** in the
  MoveIt planning scene (added on each successful seat). MoveIt then
  plans around them automatically — a clumsy approach that would clip
  a neighbour fails to plan, which is exactly the signal we want.
- For a dense grid, prefer a **top-down approach corridor** so the
  carried vial descends only into its own slot column.

**4. Verify each placement** by calling the seating/occupancy check
in [`07-perception-and-verification.md`](07-perception-and-verification.md):
position check (gripper reached expected release height) plus a
sim-camera occupancy check (slot now filled, vial top flush). A vial
sitting proud means "not seated" → hand to Part 08.

**Workflow per tray:** teach tray origin → for each worklist row:
plan-above → approach → (search) → detach/seat → verify → retreat →
add neighbour as collision object → next row. Repeat until the tray
is full, then signal "tray ready for hand-off."

## Additional hardware needed

| Real hardware | Why | How mocked in sim |
|---------------|-----|-------------------|
| **HPLC autosampler + its trays/racks** | The actual device that holds vials and injects from them | A **static tray model** with one **tf frame per slot** at a fixed bench pose |
| **Tray fixture / jig** | Holds the tray repeatably at a known location so the slot map stays valid | Baked into the model pose; the in-sim teach step records the origin |
| *(later)* fiducial marker / teach pendant | Real-world calibration of the tray origin | In sim, read the model pose directly; `apriltag_ros` path is ready for hardware |

None of this blocks building the digital twin now — the tray is just
a model and a set of frames.

## How it connects

- [`02-vial-handling-and-gripping.md`](02-vial-handling-and-gripping.md)
  — carries the vial to the tray; the placement here is the end of
  that carry, and the same grasp-fix plugin does both grip and seat.
- [`06-identification-labeling-and-tracking.md`](06-identification-labeling-and-tracking.md)
  — defines the vial-ID ↔ slot mapping this doc realises physically;
  we report back the slot actually used.
- [`07-perception-and-verification.md`](07-perception-and-verification.md)
  — provides the slot-occupancy and seating verification that
  confirms each place succeeded.
- [`08-orchestration-error-handling-and-safety.md`](08-orchestration-error-handling-and-safety.md)
  — handles placement failures (jam, missed slot, tipped neighbour,
  proud vial): retry, re-search, or quarantine and alert.
- Mirrors
  [`../03-high-level-solution/05-tray-loading-and-positioning.md`](../03-high-level-solution/05-tray-loading-and-positioning.md);
  back to the overview: [`README.md`](README.md).
