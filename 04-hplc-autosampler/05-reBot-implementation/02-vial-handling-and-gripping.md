# Part 02 — Vial handling & gripping (simulation)

> **Sim goal:** Prove in open-source sim that the reBot parallel
> gripper can approach, grasp, lift, and transport a 2 mL vial from a
> known rack slot — validating grasp poses, approach/retreat, and
> timing — while being honest that real friction on glass is a
> hardware-only question.

A **parallel gripper** is a two-finger hand whose jaws close
straight toward each other. A **2 mL vial** is the small glass
cylinder an HPLC autosampler draws from — roughly ~12 mm across and
~32 mm tall. Picking something that small and smooth is the most
contact-sensitive motion in the whole cell, so it gets its own part.

## What we can prove in simulation

We can prove the **geometry and choreography** of the pick:

- **Grasp pose.** Where the gripper frame must sit relative to the
  vial (height on the body, finger opening) to enclose it cleanly.
- **Approach / retreat.** A collision-free path in to the grasp pose
  and a straight lift-out that clears neighbouring vials in the rack.
- **Transport.** Carrying the held vial across the cell to the next
  station without collisions or self-collisions.
- **Timing.** Planned durations for approach, close, lift, and move,
  feeding the Part 01 cycle-time estimate.
- **Pick/place sequencing logic.** Open/close commands interleaved
  with motion, the basis for the orchestration in Part 08.

**Honest note.** Small, smooth, rigid objects are *contact-finicky*
in Gazebo: the solver can jitter, squirt the vial out, or let it
penetrate the fingers. So we do **not** rely on simulated friction to
hold the vial. Instead we use a **grasp-fix plugin** (and/or MuJoCo
for tuning), described below. This means sim proves *which grasp pose
to use and that the motion is clean* — it does **not** prove real
grip force, slip, or whether glass squeaks out of the jaws. Those are
hardware-acceptance items: real friction, fingertip compliance, and
crush force must be measured on the bench (see
`10-hardware-platform-and-capital-model.md`).

## Open-source tools

| Tool | Role | Bottom line |
|------|------|-------------|
| Gazebo Harmonic (gz-sim) | Hosts vial + rack models, runs the pick | Primary sim; fine for poses, weak on tiny-object contact. |
| grasp-fix plugin | Attaches vial to gripper on close via a temp fixed joint | The honest workaround for unreliable contact; proves choreography. |
| MuJoCo | Contact-rich re-sim of the grasp | Optional; far better stable contacts when tuning grip detail. |
| MoveIt 2 | Plans approach/grasp/retreat motions | Generates and checks the collision-free pick path. |
| `GripperCommand` action | Commands the gripper open/close | Same interface as the reBot driver; sim/HW parity. |
| RViz2 / Foxglove | Watch the pick, debug collisions | Confirm finger placement and clearance by eye. |
| Open3D / PCL | (Later) point-cloud grasp checks | Used in Part 07 to verify the vial is actually held. |

## How to simulate it now

This part adds vials and grasp behaviour on top of the cell from
`01-scope-and-workflow.md`. The arm already spawns via
`gz_ros2_control` and answers `FollowJointTrajectory`,
`GripperCommand`, and `MoveToPose`.

**1. Model the vials and rack.** Represent each 2 mL vial as a thin
**cylinder** model (~12 mm diameter, ~32 mm tall, small mass) in
Gazebo. Place them in a **nested supply rack** model at the
`vial_supply` tf frame from Part 01, so each slot has a known pose
(e.g. `vial_supply/slot_03`). Known poses let us skip vision for now —
perception-driven grasping is layered in by Part 07; here the slot
geometry is given.

**2. Define the grasp pose.** Relative to a vial frame, fix a
**pre-grasp** pose (a few cm above, fingers open) and a **grasp**
pose (gripper frame centred on the vial body at a safe height,
fingers sized to the diameter). Store these as tf offsets so the same
numbers drive every slot.

**3. Plan and execute the pick.**

- Call MoveIt to plan from `home` (Part 01) to the **pre-grasp** pose
  over the target slot.
- Execute a short **Cartesian approach** straight down to the grasp
  pose (a straight-line move, so the fingers descend around the vial
  rather than swinging in).
- Send `GripperCommand` to close to the vial's diameter.

**4. Hold the vial (the abstraction).** On gripper close, the
**grasp-fix plugin** detects the vial within tolerance of the
gripper frame and creates a temporary **fixed joint** attaching the
vial link to the gripper link. From that instant the vial moves
rigidly with the hand — no reliance on flaky contact friction.
Releasing (open `GripperCommand`) deletes the joint and drops the
vial. For contact-detail work (finger pad deformation, minimum hold
force) re-create the same grasp in **MuJoCo**, which handles
small-object contact far more stably.

**5. Validate lift and transport.**

- Plan a **retreat**: straight lift clearing the rack and neighbours.
- Plan a transport motion toward a downstream station frame
  (`scan_station`, `decap_station`, …) and confirm no collisions and
  no self-collisions with the vial attached (MoveIt treats the
  attached vial as part of the arm for collision checking).
- Log success/failure and durations per slot; sweep several slots to
  confirm the rack geometry is reachable end to end.

**6. Grip-verification hook.** Emit a simple "holding/not-holding"
signal from the grasp-fix plugin (joint present?) so orchestration
(Part 08) can branch on a failed grasp. The richer, sensor-based
verification (point-cloud or image check that a vial is in the jaws)
is built in `07-perception-and-verification.md`.

## Additional hardware needed

- **Gripper** — ships with the reBot arm; modelled as the gripper
  links already in the URDF, commanded via `GripperCommand`.
- **Compliant elastomer fingertips** — soft fingertip pads that
  forgive small pose error and grip smooth glass; in sim they are
  just the fingertip geometry (their *real* compliance and friction
  are exactly what sim cannot prove).
- **Physical vial supply rack** — modelled as the nested rack model
  with known slot frames.

In short, every hardware item here exists in sim as a model, and the
one property that matters most physically — friction/grip on glass —
is the headline thing deferred to hardware.

## How it connects

- `01-scope-and-workflow.md` — provides the world, the arm spawn,
  MoveIt config, and the `vial_supply` frame this part populates.
- `03-decapping-and-capping.md`, `04-liquid-handling-and-sample-prep.md`,
  `05-tray-loading-and-positioning.md` — receive the vial this part
  picks up; the grasp-fix attachment carries it to those stations.
- `07-perception-and-verification.md` — upgrades the simple
  grip-verification hook into a real sensor-based held-vial check.
- High-level companion:
  `../03-high-level-solution/02-vial-handling-and-gripping.md`.
- Folder overview: `README.md`.
