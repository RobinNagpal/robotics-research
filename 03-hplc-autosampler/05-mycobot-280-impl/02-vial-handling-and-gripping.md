# Part 02 — Vial handling & gripping (myCobot 280 simulation)

> **Sim goal:** Prove in open-source sim that the myCobot 280's
> gripper can approach, grasp, lift, and transport a 2 mL vial from a
> known rack nest — validating grasp poses, approach/retreat, and
> timing — while being honest that real friction on glass is a
> hardware-only question.

A **gripper** here is the small hand on the arm's end. Elephant offers
an **adaptive/parallel gripper** (two jaws that close straight toward
each other, with a little give to self-centre on the object) and, as
an alternative, a **suction pump** option. A **2 mL vial** is the
small glass cylinder an HPLC autosampler draws from — roughly ~12 mm
across and ~32 mm tall. Picking something that small and smooth is the
most contact-sensitive motion in the whole cell, so it gets its own
part.

A note on the 280's limits up front: its ~250 g payload is *ample* for
a vial weighing a few grams — payload is a non-issue. The real
constraint the 280 imposes is **reach** (~280 mm), and it lands on
this part as a placement rule: the supply rack must sit well inside
the reach bubble established in `01-scope-and-workflow.md`, not at its
ragged edge where IK solutions get scarce and approach angles awkward.

## What we can prove in simulation

We can prove the **geometry and choreography** of the pick:

- **Grasp pose.** Where the gripper frame must sit relative to the
  vial (height on the body, finger opening) to enclose it cleanly.
- **Approach / retreat.** A collision-free path in to the grasp pose
  and a straight lift-out that clears neighbouring vials in the rack.
- **Transport.** Carrying the held vial across the (compact) cell to
  the next station without collisions or self-collisions.
- **Reach-aware rack placement.** That the chosen rack location yields
  good IK and clean approach for *every* nest — important on a small
  arm where the workspace edge is close.
- **Timing.** Planned durations for approach, close, lift, and move,
  feeding the Part 01 cycle-time estimate.
- **Pick/place sequencing logic.** Open/close commands interleaved
  with motion, the basis for the orchestration in Part 08.

**Honest note.** Small, smooth, rigid objects are *contact-finicky*
in Gazebo: the solver can jitter, squirt the vial out, or let it
penetrate the fingers. So we do **not** rely on simulated friction to
hold the vial. Instead we use a **grasp-fix plugin** (and/or MuJoCo
for tuning), described below. This means sim proves *which grasp pose
to use and that the motion is clean* — it does **not** prove real grip
force, slip, or whether glass squeaks out of the jaws. Those are
hardware-acceptance items: real friction, fingertip compliance, and
crush force must be measured on the bench (see
`10-hardware-platform-and-capital-model.md`).

## Open-source tools

| Tool | Role | Bottom line |
|------|------|-------------|
| Gazebo Harmonic (gz-sim) | Hosts vial + rack models, runs the pick | Primary sim; fine for poses, weak on tiny-object contact. |
| `mycobot_ros` gripper model | Gripper links/joint in the 280 URDF | Reuse the shipped description; command via the gripper action. |
| grasp-fix plugin | Attaches vial to gripper on close via a temp fixed joint | The honest workaround for unreliable contact; proves choreography. |
| MuJoCo | Contact-rich re-sim of the grasp | Optional; far better stable contacts when tuning grip detail. |
| MoveIt 2 | Plans approach/grasp/retreat motions | Generates and checks the collision-free pick path. |
| `GripperCommand` action | Commands the gripper open/close | Same interface concept the real driver presents; sim/HW parity. |
| RViz2 / Foxglove | Watch the pick, debug collisions | Confirm finger placement and clearance by eye. |
| Open3D / PCL | (Later) point-cloud grasp checks | Used in Part 07 to verify the vial is actually held. |

## How to simulate it now

This part adds vials and grasp behaviour on top of the cell from
`01-scope-and-workflow.md`. The arm already spawns via
`gz_ros2_control` and answers `FollowJointTrajectory`, and the
gripper is driven through a `GripperCommand`-style action.

**1. Model the vials and rack.** Represent each 2 mL vial as a thin
**cylinder** model (~12 mm diameter, ~32 mm tall, small mass) in
Gazebo. Place them in a **nested supply rack** model at the
`vial_supply` tf frame from Part 01, choosing a location that sat
comfortably inside the 280's reach bubble during the Part 01
reachability check — so each nest (e.g. `vial_supply/slot_03`) has a
known pose with a healthy IK margin. For this first geometry pass the
slot pose is given by the rack model; the **YOLO detector** that locates
the real vials and rack from the camera (and lifts each to 3-D via the
RGB-D depth) is layered in by Part 07.

**2. Define the grasp pose.** Relative to a vial frame, fix a
**pre-grasp** pose (a few cm above, fingers open) and a **grasp** pose
(gripper frame centred on the vial body at a safe height, fingers
sized to the diameter). The adaptive gripper's self-centring is
forgiving of small lateral error — model the jaw geometry so the
fingers wrap the ~12 mm body, not the cap. Store these as tf offsets
so the same numbers drive every nest.

**3. Plan and execute the pick.**

- Call MoveIt to plan from `home` (Part 01) to the **pre-grasp** pose
  over the target nest.
- Execute a short **Cartesian approach** straight down to the grasp
  pose (a straight-line move, so the fingers descend around the vial
  rather than swinging in — easy to foul on a compact bench).
- Send the gripper close command to the vial's diameter.

**4. Hold the vial (the abstraction).** On gripper close, the
**grasp-fix plugin** detects the vial within tolerance of the gripper
frame and creates a temporary **fixed joint** attaching the vial link
to the gripper link. From that instant the vial moves rigidly with
the hand — no reliance on flaky contact friction. Releasing (open
command) deletes the joint and drops the vial. For contact-detail work
(finger pad deformation, minimum hold force) re-create the same grasp
in **MuJoCo**, which handles small-object contact far more stably.

**5. Validate lift and transport.**

- Plan a **retreat**: straight lift clearing the rack and neighbours.
- Plan a transport motion toward a downstream station frame
  (`scan_station`, `decap_station`, …) and confirm no collisions and
  no self-collisions with the vial attached (MoveIt treats the
  attached vial as part of the arm for collision checking). On the
  280's tight layout, watch especially for the held vial clipping
  adjacent station models.
- Log success/failure and durations per nest; sweep several nests to
  confirm the rack geometry is reachable and graspable end to end.

**6. Grip-verification hook.** Emit a simple "holding/not-holding"
signal from the grasp-fix plugin (joint present?) so orchestration
(Part 08) can branch on a failed grasp. The richer, sensor-based
verification (point-cloud or image check that a vial is in the jaws)
is built in `07-perception-and-verification.md`.

## Sensing that makes a grasp on smooth glass trustworthy

A taught grasp on a small, smooth, rigid vial is exactly where a
"blind" arm fails silently — the jaws close on nothing, or the vial
slips, and the arm carries air to the next station. The full cell is
sensor-gated; see the canonical [`sensor-suite.md`](sensor-suite.md)
for the whole list. Three sensors matter most here:

- **Gripper servo feedback (#4) — the primary grasp sensor.** The
  Elephant gripper's servo reports **jaw width** and **motor
  current**, with no extra hardware. Jaw width at the end of a close
  tells you *something is between the fingers* and roughly its
  diameter (a vial vs empty air vs a doubled-up pick), and motor
  current stands in for **grip force** — too low means a slipping or
  missed grasp, a sudden drop mid-transport flags **slip**. This is
  what makes a grasp on borosilicate trustworthy without joint F/T
  sensing the 280 lacks. *Sim stand-in:* `ros2_control` publishes the
  gripper joint **position + effort**; pair it with the **grasp-fix
  contact** so "joint present + width-in-band + effort-in-band" is the
  held signal.
- **Wrist camera (#3) — the second witness.** A light eye-in-hand RGB
  module on the flange takes a close glance after the close to confirm
  a **vial is actually in the gripper** (and reads its barcode/QR at
  the vial). Depth is deliberately left to the fixed cameras so the
  wrist stays within the 280's tiny payload. *Sim stand-in:* a Gazebo
  `camera` on a fixed joint at the flange. Per the **two-witness
  habit**, "vial is held" is trusted only when gripper feedback (#4)
  **and** the wrist glance (#3) agree — a single sensor can lie about a
  shiny vial; two rarely lie the same way.
- **Station presence / proximity (#7) — before the pick.** A
  photoelectric/inductive sensor at the supply rack confirms a **vial
  is staged** in the target nest *before* the arm commits to the pick,
  so it never grasps an empty slot. *Sim stand-in:* a Gazebo
  logical-camera / contact sensor at the nest.

These signals feed the same "holding/not-holding" gate above; the
richer image/point-cloud check is layered in
`07-perception-and-verification.md`, and the gates themselves are
ticked by the behavior tree in Part 08.

## Additional hardware needed

- **Gripper** — Elephant's **adaptive/parallel gripper** for the 280
  (or the **suction pump** option as an alternative for a vial cap or
  body); modelled as the gripper links in the `mycobot_ros` URDF and
  commanded via the gripper action.
- **Compliant elastomer fingertips** — soft fingertip pads that
  forgive small pose error and grip smooth glass; in sim they are just
  the fingertip geometry (their *real* compliance and friction are
  exactly what sim cannot prove, and matter more on a less-precise
  desktop arm).
- **Physical vial supply rack** — modelled as the nested rack model
  with known slot frames, placed inside the 280's reach.

In short, every hardware item here exists in sim as a model, and the
one property that matters most physically — friction/grip on glass —
is the headline thing deferred to hardware.

## How it connects

- `01-scope-and-workflow.md` — provides the world, the arm spawn,
  MoveIt config, the reach bubble, and the `vial_supply` frame this
  part populates.
- `03-decapping-and-capping.md`, `04-liquid-handling-and-sample-prep.md`,
  `05-tray-loading-and-positioning.md` — receive the vial this part
  picks up; the grasp-fix attachment carries it to those stations.
- [`sensor-suite.md`](sensor-suite.md) — the canonical sensor list;
  the gripper feedback (#4), wrist camera (#3), and station presence
  (#7) used here are defined there with costs and sim stand-ins.
- `07-perception-and-verification.md` — upgrades the simple
  grip-verification hook into a real sensor-based held-vial check.
- Folder overview: `README.md`.
