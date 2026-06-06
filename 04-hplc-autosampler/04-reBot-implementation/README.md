# reBot implementation — proving each part in open-source simulation

> **The claim.** Every part of the HPLC vial-prep + tray-loading
> solution in `../02-high-level-solution/` can be **developed and proven
> in simulation first**, using the **reBot Arm B601-DM** and a fully
> **open-source** stack — *before* buying the arm, the stations, or the
> instrument. This folder shows how, part by part, and lists the extra
> hardware each part will eventually need on the real bench.

New to a term? See `../../03-place-items-on-shelf/02-glossary.md` for the
robotics vocabulary; lab terms are defined in
`../02-high-level-solution/`.

> **Disclaimer.** Tool versions, reBot's driver maturity, and cost
> figures drift — re-verify before relying on them. Simulation proves
> *logic, geometry, and software*; it does **not** by itself prove
> real-world physics (see "What sim can and can't prove").

---

## Why simulation-first, and why it works for this project

This is a **fixed-arm, bench-top** task — no mobile base, no driving
around. That makes it unusually friendly to simulation: the whole world
is one table, a known set of stations, and known vial/tray geometry. You
can stand the entire cell up as a digital twin and exercise the full
**prep → load → hand-off** loop in software.

It also directly answers the common objection that "there's no point
simulating an arm like reBot because everything needs hardware." Not
true: reBot ships an **open URDF** and a ROS 2 workspace
(`rebotarm_ros2`) exposing standard interfaces — `/joint_states`,
`FollowJointTrajectory`, `GripperCommand`, `MoveToPose` — plus a
**Pinocchio** kinematics adaptation. In simulation you don't even need
the hardware driver: you drive the same URDF with `gz_ros2_control` +
**MoveIt 2**.

> **reBot status caveat (early 2026).** reBot's *official* MoveIt 2
> drivers, NVIDIA Isaac Sim USD import, and LeRobot integration were
> announced as "in development." For an **open-source** sim you don't
> wait on any of that — if the official MoveIt config isn't ready,
> generate one from the URDF with the **MoveIt Setup Assistant**. (Isaac
> Sim is free but proprietary; we default to **Gazebo**/**MuJoCo** to
> stay fully open.) Assets live at `Seeed-Projects/reBot-DevArm`.

---

## The open-source simulation stack (shared across all parts)

| Tool | Role here | Licence |
|------|-----------|---------|
| **Gazebo Harmonic** (`gz-sim`) | Primary physics + sensor simulator; the bench, stations, vials, tray | Apache-2.0 |
| **MuJoCo** (optional) | Contact-rich tuning for grasping/insertion when Gazebo contacts are too coarse | Apache-2.0 |
| **ROS 2** (Humble/Jazzy) | Middleware tying every node together (same as on real hardware) | Apache-2.0 |
| **`ros2_control` + `gz_ros2_control`** | Joint controllers in sim; identical interface to the real arm | Apache-2.0 |
| **MoveIt 2** | Collision-free arm motion planning (config from the reBot URDF) | BSD |
| **Pinocchio** / **MeshCat** | Fast kinematics/dynamics + lightweight browser viz (reBot supports this today) | BSD |
| **OpenCV**, **apriltag_ros**, **Open3D/PCL** | Perception: detection, fiducials, point clouds, level checks | BSD/Apache |
| **ZBar / pyzbar** | Barcode/QR decoding from simulated camera images | LGPL |
| **BehaviorTree.CPP** (+ **Groot2** free) / **py_trees** | Orchestration: sequence the workflow, handle failures | MIT |
| **SQLite**, **FastAPI** | Audit-trail store + a mock LIMS/CDS service for the software layer | Public-domain/MIT |
| **RViz2**, **Foxglove Studio** | Visualization and debugging | BSD/MPL |

---

## What simulation *can* and *can't* prove

**Can prove fully in open-source sim:** bench layout and arm
**reachability**, collision-free **motion planning**, the **sequencing /
state machine**, the **perception pipelines** (detection, fiducials,
level checks, barcode decode), the **vial→slot→worklist mapping**, the
entire **software + audit-trail** application, and **cycle-time**
estimates that feed the ROI model.

**Cannot be fully proven in sim (needs eventual hardware):** real
**grasp friction/slip on glass**, **decap torque** and cross-threading,
**dispense volume accuracy** and carryover, and **regulatory
validation** (IQ/OQ/PQ). Simulation still *de-risks* all of these by
abstracting them (see below), so the hardware phase is shorter.

**Key abstractions we use** (so don't expect physical fidelity here):

- **Grasping a vial** → a "grasp-fix" plugin attaches the vial to the
  gripper on contact (and/or MuJoCo for stable contacts). Proves poses
  and timing, not real friction.
- **Decap/cap** → the cap is a separate link on a breakable/fixed joint;
  a station **service** detaches/reattaches it. No threads simulated.
- **Liquids** → a scalar **fill-volume state** per vial (+ optional
  visual cylinder); a dispenser **service** mutates it. No fluid CFD.
- **Stations** (decapper, dispenser, balance, scanner, autosampler) →
  ROS 2 **mock-station** service/action nodes at fixed frames.

---

## The parts (each mirrors the same-numbered high-level doc)

| # | Document | Mirrors |
|---|----------|---------|
| 01 | [`01-scope-and-workflow.md`](01-scope-and-workflow.md) | [scope & workflow](../02-high-level-solution/01-scope-and-workflow.md) |
| 02 | [`02-vial-handling-and-gripping.md`](02-vial-handling-and-gripping.md) | [vial handling](../02-high-level-solution/02-vial-handling-and-gripping.md) |
| 03 | [`03-decapping-and-capping.md`](03-decapping-and-capping.md) | [decapping](../02-high-level-solution/03-decapping-and-capping.md) |
| 04 | [`04-liquid-handling-and-sample-prep.md`](04-liquid-handling-and-sample-prep.md) | [liquid handling](../02-high-level-solution/04-liquid-handling-and-sample-prep.md) |
| 05 | [`05-tray-loading-and-positioning.md`](05-tray-loading-and-positioning.md) | [tray loading](../02-high-level-solution/05-tray-loading-and-positioning.md) |
| 06 | [`06-identification-labeling-and-tracking.md`](06-identification-labeling-and-tracking.md) | [identification](../02-high-level-solution/06-identification-labeling-and-tracking.md) |
| 07 | [`07-perception-and-verification.md`](07-perception-and-verification.md) | [perception](../02-high-level-solution/07-perception-and-verification.md) |
| 08 | [`08-orchestration-error-handling-and-safety.md`](08-orchestration-error-handling-and-safety.md) | [orchestration](../02-high-level-solution/08-orchestration-error-handling-and-safety.md) |
| 09 | [`09-software-compliance-and-integration.md`](09-software-compliance-and-integration.md) | [software & compliance](../02-high-level-solution/09-software-compliance-and-integration.md) |
| 10 | [`10-hardware-platform-and-capital-model.md`](10-hardware-platform-and-capital-model.md) | [hardware & capital](../02-high-level-solution/10-hardware-platform-and-capital-model.md) |

Each part doc follows the same shape: **What we can prove in
simulation** → **Open-source tools** → **How to simulate it now**
(concrete steps) → **Additional hardware needed** (real-world, and how
it's mocked in sim) → **How it connects**.

---

## Additional real-world hardware — rollup

Beyond the **reBot arm + its parallel gripper**, the full system will
eventually need the hardware below. In simulation each is a model or a
mock-station node (see the per-part docs); none of it blocks building
the digital twin now.

| Hardware | For part(s) | Mocked in sim as |
|----------|-------------|------------------|
| Tool changer + extra end-effectors (decapper, pipetting tool) | 03, 04, 10 | Attach/detach end-effector models |
| Decapper/capper station | 03 | `/decap` `/cap` service node |
| Syringe pump / dispenser / OEM pipetting head, tips, wash station | 04 | `/dispense` service + fill-volume state |
| Analytical balance (optional gravimetric check) | 04 | Reads the simulated fill state |
| Barcode scanner (+ optional label printer/applicator) | 06 | Sim camera + ZBar, or `/scan` mock |
| RGB-D cameras (wrist + fixed) + lighting | 07 | Gazebo depth-camera sensors |
| HPLC autosampler + trays/racks; vial supply racks; bench, jigs | 01, 05 | Static models with named tf frames |
| Enclosure/guarding, e-stop, interlocks/light curtain | 08, 10 | `/safety_stop` topic + state |
| Industrial PC (controller/compute) | 09, 10 | The dev machine running ROS 2 |

---

## Suggested order to actually build it

1. Stand up the **world + reBot + MoveIt** (Part 01) so the arm can
   reach every station.
2. Add **vial handling** with a grasp-fix plugin (Part 02).
3. Wire the **mock stations** — decap (03), dispense (04), tray (05),
   scan (06) — as services the arm drives between.
4. Add **simulated cameras + perception/verification** (07).
5. Tie it together with a **behavior tree + fault injection** (08).
6. Build the **worklist/audit/compliance app** around it (09) and use
   the twin to compare **platforms and cycle time** (10).
