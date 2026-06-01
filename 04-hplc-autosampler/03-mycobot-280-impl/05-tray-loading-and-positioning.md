# Part 05 — Tray loading & positioning (myCobot 280 simulation)

> **Sim goal:** Prove that the **myCobot 280** can place a carried
> vial into the *correct* autosampler-tray slot — centred, fully
> seated, and without knocking its neighbours — and that the
> worklist-row → physical-slot mapping is realised exactly, all in
> Gazebo before any tray hardware exists. Because the 280 is a small
> desktop arm (~280 mm reach, `~250 g` payload — verify), this doc
> also stress-tests *how many slots are even reachable* from a fixed
> bench seat.

This mirrors the high-level
[`../01-high-level-solution/05-tray-loading-and-positioning.md`](../01-high-level-solution/05-tray-loading-and-positioning.md).
New robotics terms are defined in
[`../../03-place-items-on-shelf/02-glossary.md`](../../03-place-items-on-shelf/02-glossary.md).

## What we can prove in simulation

The **autosampler tray** (also called a rack) is a flat holder with
many small cylindrical pockets — **slots** — laid out in a regular
grid. Its key property is a **fixed pitch**: the centre-to-centre
spacing between slots is a known constant. That makes the whole tray
a predictable geometric model we can stand up in sim and address by a
simple **tf frame per slot** (`A1`, `A2`, …).

**Can prove fully in open-source sim:**

- **Reachability (the big one for the 280).** Whether the short-reach
  arm can actually reach *every* slot from its fixed bench position,
  without hitting joint limits or self-colliding. With only ~280 mm
  of reach this is not a given — see the call-out below.
- **Collision-free placement** — that MoveIt 2 can plan a path to
  each slot plus a straight-down approach that does not clip the
  **neighbouring vials** already standing in a dense grid.
- **The placement sequence** — plan-above-slot → straight-down
  approach → (optional) compliance/search → release (detach) →
  straight-up retreat — runs end to end and repeats across the tray.
- **Worklist → slot mapping** — that worklist **row N** drives the
  arm to the intended **physical slot**, with the registry in Part 06
  agreeing on which vial went where.
- **Cycle time per slot**, feeding the throughput / ROI estimate.

**Honest limits (need real hardware to settle):**

- **Real seating force.** Whether the vial actually drops all the way
  home depends on real friction, slot taper, and how hard the arm
  pushes. The 280 is a light arm with modest stiffness, so this is a
  real worry. Sim "seats" the vial by an **attach** event, not by
  feeling contact.
- **Tray tolerances.** Real trays have manufacturing slop and may not
  sit *exactly* where the model says. Sim assumes a perfectly known
  tray pose; hardware needs the teach/calibration step repeated.
- **Clean release.** Whether the gripper withdraws without dragging
  the just-placed vial back out is a friction question sim only
  approximates.

So sim proves the **logic, geometry, reachability map, sequencing,
and the no-collision-with-neighbours** claim; it de-risks but does
not finally prove **seating reliability**.

### Reach call-out — the 280 may not cover a full tray

With ~280 mm reach, the tray **must sit very close to the arm base**,
and even then the far corners of a standard autosampler tray may fall
outside the reachable workspace. Expect to either:

- place the tray so its *centre* is well inside the workspace and
  accept that some edge slots are unreachable, or
- step up to a longer-reach arm (e.g. a **myCobot 320**, ~320 mm
  reach) if a full standard tray must be covered.

Treat the sim **reachability map** (below) as the deliverable that
decides this. Confirming *true* full-tray reach with real tray
geometry and the real fixture is exactly the kind of thing the
**digital twin** is for — flag it there rather than assuming it here.

## Open-source tools

| Tool | Role | Bottom line |
|------|------|-------------|
| **Gazebo Harmonic** | Hosts the bench, the myCobot 280 (`mycobot_ros` URDF), the tray model, and the vials | The world the place-loop runs in |
| **MoveIt 2** (+ `mycobot_ros` config) | Plans the collision-free path to each slot plus the short Cartesian straight-line approach/retreat | Owns "reach the slot without hitting neighbours" |
| **`ros2_control` + `gz_ros2_control`** | Runs the 280's joint controllers in sim, same interface the real arm exposes | Drives the URDF; no `pymycobot` driver in sim |
| **Grasp-fix plugin** (Gazebo) | Models the gripper holding the vial in transit, and the "seat" on release, as attach/detach events | Stands in for real grip + seating contact |
| **MuJoCo** (optional) | Contact-rich refinement of the final straight-down insertion if Gazebo contacts look too coarse | Only if you want finer insertion physics |
| **tf2** (ROS 2) | Publishes one named transform **per slot** the arm plans to | The slot map lives here as tf frames |
| **RViz2 / Foxglove** | Visualise tray frames, the plan, the reachability map, and which slots are filled | Eyeball the sequence; catch near-misses and out-of-reach slots |

## How to simulate it now

**1. Build the tray model + per-slot tf frames (via a sim teach
step).**

- Add a static **tray model** (SDF/URDF) to the Gazebo world at a
  fixed pose on the bench — a block carrying the grid of slot
  pockets. Place it **close to the 280's base** given the short
  reach.
- Compute one **tf frame per slot** from a corner origin and the
  known **pitch**: e.g. `tray/A1`, `tray/A2`, … A small node (or a
  static-transform launch) broadcasts them all relative to a single
  `tray_origin` frame.
- Model the **teach step in sim**: rather than hard-coding the
  origin, run a tiny "teach" routine that records the `tray_origin`
  pose (in sim, read it straight from the model; on hardware this is
  where jogging the arm to a corner slot, or an AprilTag, comes in).
  Keeping the step in the workflow means the hardware version drops
  in later with no code change.
- **Generate the reachability map first.** Before placing anything,
  loop over every slot frame and ask MoveIt 2 for an IK + plan to a
  pre-place pose above it. Colour each slot reachable / unreachable
  in RViz2. This is the artifact that answers the reach call-out.

**2. Implement sequential placement.**

A `tray_loader` node (or a behavior-tree subtree, see Part 08) does,
per worklist row:

- Look up the target slot frame for this row (row 1 → `tray/A1`, …;
  the **sequential** v1 rule keeps the map trivial to audit, and lets
  you skip any slot the reachability map marked unreachable).
- Ask **MoveIt 2** for a plan to a **pre-place pose** ~3–5 cm above
  the slot frame.
- Execute a short **Cartesian straight-down approach** to insertion
  depth.
- *(Optional)* run a small **spiral/search** wiggle, or a brief
  **MuJoCo** insertion, to mimic self-centring on the slot taper.
- Trigger the **grasp-fix detach** to release the vial and an
  **attach to the slot/tray** to "seat" it so it stays put.
- Execute a **straight-up retreat**, then plan to the next row.

**3. Check no collision with neighbouring vials.**

- Represent each already-placed vial as a **collision object** in the
  MoveIt planning scene (added on each successful seat). MoveIt then
  plans around them automatically — a clumsy approach that would clip
  a neighbour fails to plan, which is exactly the signal we want.
- For a dense grid, prefer a **top-down approach corridor** so the
  carried vial descends only into its own slot column. With the
  280's limited dexterity, a near-vertical approach is also the most
  reliable for the IK.

**4. Verify each placement** by calling the seating/occupancy check in
[`07-perception-and-verification.md`](07-perception-and-verification.md):
a position check (gripper reached expected release height) plus a
sim-camera occupancy check (slot now filled, vial top flush). A vial
sitting proud means "not seated" → hand to Part 08.

**Workflow per tray:** teach `tray_origin` → build reachability map →
for each worklist row mapped to a *reachable* slot: plan-above →
approach → (search) → detach/seat → verify → retreat → add neighbour
as collision object → next row. Repeat until the tray is full (or all
reachable slots are used), then signal "tray ready for hand-off."

## Additional hardware needed

| Real hardware | Why | How mocked in sim |
|---------------|-----|-------------------|
| **HPLC autosampler + its trays/racks** | The actual device that holds vials and injects from them | A **static tray model** with one **tf frame per slot** at a fixed bench pose |
| **Tray fixture / jig** | Holds the tray repeatably at a known location so the slot map (and reach map) stays valid | Baked into the model pose; the in-sim teach step records the origin |
| *(later)* AprilTag / teach pendant | Real-world calibration of the tray origin | In sim, read the model pose directly; `apriltag_ros` path is ready for hardware |

None of this blocks building the digital twin now — the tray is just
a model plus a set of frames. **Real seating force, slot tolerances,
and the true reachable-slot count** are the items that genuinely need
the arm + tray on the bench.

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
  proud vial, or "no reachable slot"): retry, re-search, or quarantine
  and alert.
- Mirrors
  [`../01-high-level-solution/05-tray-loading-and-positioning.md`](../01-high-level-solution/05-tray-loading-and-positioning.md);
  back to the overview: [`README.md`](README.md).
