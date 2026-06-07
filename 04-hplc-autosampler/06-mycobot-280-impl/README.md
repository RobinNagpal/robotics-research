# myCobot 280 implementation — proving each part in open-source simulation

> **The claim.** Every part of the HPLC vial-prep + tray-loading
> solution in `../03-high-level-solution/` can be **developed and proven
> in simulation first**, using the **Elephant Robotics myCobot 280** and
> a fully **open-source** stack — *before* buying the arm, the stations,
> or the instrument. This folder is the myCobot 280 sibling of
> `../05-reBot-implementation/`: same 10 parts, same method, different
> arm.

New to a term? See `../../03-place-items-on-shelf/02-glossary.md` for
robotics vocabulary; lab terms are defined in `../03-high-level-solution/`.

> **Disclaimer.** Tool versions, package maturity, reach/payload specs,
> and cost figures drift — re-verify before relying on them. Simulation
> proves *logic, geometry, and software*, not real-world physics (see
> "What sim can and can't prove").

---

## Why the myCobot 280 — and its one big caveat

The **myCobot 280** is a compact 6-DoF desktop cobot from Elephant
Robotics. Its appeal for a *simulation-first* effort is **maturity and
price**: it ships an established open-source ROS package, `mycobot_ros`
(GitHub `elephantrobotics/mycobot_ros`), that already includes a
**URDF, a Gazebo simulation, and a ready-made MoveIt configuration** —
plus the `pymycobot` Python API for the real arm. So unlike a brand-new
arm, you can stand up an arm-in-MoveIt-in-Gazebo demo on day one.

> **The caveat: it is small.** The myCobot 280 has only a **~250 g
> payload** and a **~280 mm working radius** (`~` figures — verify). For
> *handling 2 mL vials* (a few grams) the payload is fine, but the
> **short reach** means a very **compact bench layout** — the supply
> rack, decapper, dispenser, scanner, and tray must all sit close
> together. For a real production cell you would likely step up to a
> **myCobot 320** (`~`500 mm reach, `~`1 kg) or larger. For a cheap,
> fast **proof-of-concept in simulation**, the 280 is ideal — and the
> reach limit is itself something the digital twin lets you discover
> before spending a cent (see Part 10).

In simulation you don't use `pymycobot` (that drives the real arm) — you
drive the **URDF** with `gz_ros2_control` + **MoveIt 2**, exactly as on
the reBot path.

---

## The open-source simulation stack (shared across all parts)

Identical to the reBot path, so the two arms are directly comparable:

| Tool | Role here | Licence |
|------|-----------|---------|
| **Gazebo Harmonic** (`gz-sim`) | Primary physics + sensor simulator; bench, stations, vials, tray | Apache-2.0 |
| **MuJoCo** (optional) | Contact-rich tuning for grasping/insertion | Apache-2.0 |
| **ROS 2** (Humble/Jazzy) | Middleware tying every node together | Apache-2.0 |
| **`ros2_control` + `gz_ros2_control`** | Joint controllers in sim | Apache-2.0 |
| **MoveIt 2** (+ `mycobot_ros` config) | Collision-free arm motion planning | BSD |
| **`mycobot_ros`** | Ready-made myCobot URDF, Gazebo + MoveIt assets | BSD |
| **OpenCV**, **apriltag_ros**, **Open3D/PCL** | Perception: detection, fiducials, level checks | BSD/Apache |
| **ZBar / pyzbar** | Barcode/QR decoding from simulated camera images | LGPL |
| **BehaviorTree.CPP** (+ **Groot2** free) / **py_trees** | Orchestration + failure handling | MIT |
| **SQLite**, **FastAPI** | Audit-trail store + mock LIMS/CDS service | Public-domain/MIT |
| **RViz2**, **Foxglove Studio** | Visualization and debugging | BSD/MPL |

---

## The sensor suite (this cell is not blind)

A reliable cell is **covered in sensors**, and almost every motion is
**gated by what a sensor just reported** — the arm acts, a sensor
confirms, and only then does the next motion fire. The full, canonical
list lives in **[`sensor-suite.md`](sensor-suite.md)**; in brief the v1
suite is:

- **3 cameras** — a fixed **overhead RGB-D** (whole-tray occupancy &
  seating), a fixed **station camera** (cap on/off, liquid level, spill),
  and a **light wrist RGB** module (close alignment + barcode).
- **Gripper feedback** (jaw width + motor current) for grasp success and
  slip, a **decapper load cell** for torque, and an **analytical
  balance** for gravimetric fill — sensing pushed *off* the arm.
- **Presence/proximity** sensors per station, **homing/limit** switches,
  a **liquid-level** sensor, **safety** sensors (light curtain, door
  interlock, e-stop), and the **base IMU**.

> **The 280's one design rule:** with only ~250 g payload, the wrist
> stays light (a tiny RGB module), and everything heavy or depth-hungry
> is mounted **off the arm** — fixed cameras, station load cells, a
> balance. A *production* cell on a bigger arm (320/UR) can carry a wrist
> RGB-D and a wrist force/torque sensor instead; see
> [`sensor-suite.md`](sensor-suite.md) and Part 10.

## Beyond v1: learned generalist policies (VLAs)

The stack above is deliberately **geometric / analytical** — the right
call for one known vial. The **learned upgrade path** is
Vision-Language-Action (**VLA**) foundation models — π0/π0.5 (Physical
Intelligence), Gemini Robotics (Google DeepMind), OpenVLA, NVIDIA Isaac
GR00T, and the LeRobot/SmolVLA ecosystem — which map camera frames + a
text instruction straight to actions. They are tracked as an **option**
(centred on the grasping/manipulation layer, cutting across perception
and orchestration) for when the lab needs *generalization* across vial
types and tasks. The full comparison and the honest "why not yet for v1
/ compliance" framing is in
**[`foundation-models.md`](foundation-models.md)**.

## What simulation *can* and *can't* prove

**Can prove fully in open-source sim:** bench layout and **reachability**
(especially important given the 280's short reach), collision-free
**motion planning**, the **sequencing / state machine**, the
**perception pipelines**, the **vial→slot→worklist mapping**, the entire
**software + audit-trail** application, and **cycle-time** estimates.

**Cannot be fully proven in sim (needs hardware):** real **grasp
friction/slip on glass**, **decap torque**, **dispense accuracy**, and
**regulatory validation** (IQ/OQ/PQ). The same **abstractions** as the
reBot path apply — grasp-fix plugin for grasping, cap-as-a-breakable-
joint toggled by a station service for decap, a scalar **fill-volume
state** for liquids, and ROS 2 **mock-station** nodes for the decapper /
dispenser / balance / scanner / autosampler.

---

## The parts (each mirrors the same-numbered high-level doc)

| # | Document | Mirrors |
|---|----------|---------|
| 01 | [`01-scope-and-workflow.md`](01-scope-and-workflow.md) | [scope & workflow](../03-high-level-solution/01-scope-and-workflow.md) |
| 02 | [`02-vial-handling-and-gripping.md`](02-vial-handling-and-gripping.md) | [vial handling](../03-high-level-solution/02-vial-handling-and-gripping.md) |
| 03 | [`03-decapping-and-capping.md`](03-decapping-and-capping.md) | [decapping](../03-high-level-solution/03-decapping-and-capping.md) |
| 04 | [`04-liquid-handling-and-sample-prep.md`](04-liquid-handling-and-sample-prep.md) | [liquid handling](../03-high-level-solution/04-liquid-handling-and-sample-prep.md) |
| 05 | [`05-tray-loading-and-positioning.md`](05-tray-loading-and-positioning.md) | [tray loading](../03-high-level-solution/05-tray-loading-and-positioning.md) |
| 06 | [`06-identification-labeling-and-tracking.md`](06-identification-labeling-and-tracking.md) | [identification](../03-high-level-solution/06-identification-labeling-and-tracking.md) |
| 07 | [`07-perception-and-verification.md`](07-perception-and-verification.md) | [perception](../03-high-level-solution/07-perception-and-verification.md) |
| 08 | [`08-orchestration-error-handling-and-safety.md`](08-orchestration-error-handling-and-safety.md) | [orchestration](../03-high-level-solution/08-orchestration-error-handling-and-safety.md) |
| 09 | [`09-software-compliance-and-integration.md`](09-software-compliance-and-integration.md) | [software & compliance](../03-high-level-solution/09-software-compliance-and-integration.md) |
| 10 | [`10-hardware-platform-and-capital-model.md`](10-hardware-platform-and-capital-model.md) | [hardware & capital](../03-high-level-solution/10-hardware-platform-and-capital-model.md) |

Each part doc follows the same shape: **What we can prove in
simulation** → **Open-source tools** → **How to simulate it now** →
**Additional hardware needed** → **How it connects**.

---

## Additional real-world hardware — rollup

Beyond the **myCobot 280 + a gripper** (Elephant's adaptive/parallel
gripper, or the suction pump), the full system eventually needs the
hardware below — identical to the reBot rollup, since the stations are
arm-agnostic. In simulation each is a model or a mock-station node.

| Hardware | For part(s) | Mocked in sim as |
|----------|-------------|------------------|
| End-effector(s): parallel/adaptive gripper (+ suction option) | 02, 04 | Gripper model + grasp-fix plugin |
| Decapper/capper station | 03 | `/decap` `/cap` service node |
| Syringe pump / dispenser / pipetting head, tips, wash station | 04 | `/dispense` service + fill-volume state |
| Analytical balance (optional gravimetric check) | 04 | Reads the simulated fill state |
| Barcode scanner (+ optional label printer/applicator) | 06 | Sim camera + ZBar, or `/scan` mock |
| **Cameras ×3**: overhead RGB-D + station RGB-D + light wrist RGB | 07 | Gazebo `camera`/`depth_camera` sensors |
| **Gripper feedback** (jaw width + motor current) | 02 | `ros2_control` joint pos+effort + grasp-fix |
| **Decapper load cell / torque sense** | 03 | Force-torque sensor on the cap joint |
| **Analytical balance** (gravimetric fill check) | 04 | Reads the fill-volume scalar as mass |
| **Proximity/presence** sensors per station; **liquid-level** sensor | 04, 05 | Logical-camera/contact sensors; level from fill state |
| **Base IMU / tilt**; **homing/limit** switches | 08 | Gazebo `imu` sensor; joint-limit state |
| Controlled **lighting** (LED panel + matte backdrop) | 07 | Gazebo scene lights (clean — glare can't be proven) |
| HPLC autosampler + trays/racks; vial supply racks; bench, jigs | 01, 05 | Static models with named tf frames |
| Enclosure/guarding, e-stop, interlocks, **light curtain** | 08, 10 | `/safety_stop`, `/door_closed`, `/light_curtain_clear` |
| Compute (the myCobot's Pi/Jetson, or a controller PC) | 09, 10 | The dev machine running ROS 2 |

> **myCobot-specific hardware note.** Because the 280's reach is short,
> the real bench needs **tightly clustered stations** (or a small linear
> rail/turntable to bring stations to the arm). The digital twin is the
> right place to decide whether the 280 reaches everything or whether you
> must upgrade to a myCobot 320 — see Part 10.

---

## reBot vs myCobot 280 — which to simulate?

Both are covered so you can compare. In short: the **myCobot 280** wins
on **ready-made open-source sim assets today** (`mycobot_ros` ships
Gazebo + MoveIt) and **low cost**, but is **reach/payload limited**; the
**reBot** has a longer reach and higher payload but its official MoveIt/
sim tooling was still maturing as of early 2026. Either way the *world,
stations, perception, orchestration, and software layers are identical* —
only the arm URDF changes — so you can build once and swap arms (Part 10
explains the swap experiment).
