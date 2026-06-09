# myCobot 280 implementation — building each layer in open-source simulation

> **The claim.** Every part of the HPLC vial-prep + tray-loading
> solution can be **developed and proven in simulation first**, using
> the **Elephant Robotics myCobot 280** and a fully **open-source**
> stack — *before* buying the arm, the stations, or the instrument. The
> **10 development layers** below work the solution out one concern at a
> time, each built **in code and simulation with zero hardware
> purchased.**

New to a term? Lab terms are defined on first use in the
[sample-prep primer](../02-lab-bench-new.md) and the
[HPLC workflow](../03-hplc-workflow/README.md).

> **Disclaimer.** Tool versions, package maturity, licences, reach/payload
> specs, and cost figures drift, and "best" calls are opinions, not
> gospel — re-verify before relying on them. Figures are approximate
> (`~`). Simulation proves *logic, geometry, and software*, not
> real-world physics (see "What simulation can and can't prove").

---

## Scope: "only code"

Here you develop and prove the system with **no physical hardware**:
simulators, synthetic data, and mock device services stand in for the
arm, cameras, decapper, dispenser, scanner, and instrument. This is the
cheapest, fastest way to get the whole **prep → load** loop working and
to de-risk the eventual purchase.

Everything here is **open-source-first**. Where a commercial tool is the
true best-in-class, we say so, but the cheapest/best-practical picks stay
open.

In only-code, the **full sensor suite** is simulated for `~$0`: Gazebo
camera / depth-camera / IMU / force-torque / logical-camera plugins
stand in for the cameras, base IMU, decapper torque, and station
presence, while safety and level sensors are **mock topics**
(`/light_curtain_clear`, `/door_closed`, `/estop`, a fill-level reading).
Each one publishes the **same ROS 2 topics a real sensor would**, so the
gate logic and the off-arm sensor layout can be proven before anything is
bought. The canonical list of sensors, sim stand-ins, and rough costs
lives in [`sensor-suite.md`](sensor-suite.md).

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
> before spending a cent.

In simulation you don't use `pymycobot` (that drives the real arm) — you
drive the **URDF** with `gz_ros2_control` + **MoveIt 2**.

---

## The open-source simulation stack

The shared stack across every layer:

| Tool | Role here | Licence |
|------|-----------|---------|
| **Gazebo Harmonic** (`gz-sim`) | Primary physics + sensor simulator; bench, stations, vials, tray | Apache-2.0 |
| **MuJoCo** (optional) | Contact-rich tuning for grasping/insertion | Apache-2.0 |
| **ROS 2** (Humble/Jazzy) | Middleware tying every node together | Apache-2.0 |
| **`ros2_control` + `gz_ros2_control`** | Joint controllers in sim | Apache-2.0 |
| **MoveIt 2** (+ `mycobot_ros` config) | Collision-free arm motion planning | BSD |
| **`mycobot_ros`** | Ready-made myCobot URDF, Gazebo + MoveIt assets | BSD |
| **Ultralytics YOLO**, **OpenCV**, **Open3D/PCL** | Perception: object detection (vials/rack/tray) + RGB-D depth lift, level checks | AGPL/BSD/Apache |
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
> [`sensor-suite.md`](sensor-suite.md).

---

## The 10 development layers

| # | Layer | File |
|---|-------|------|
| 01 | Simulator & physics (digital twin) | [`01-simulation-and-digital-twin.md`](01-simulation-and-digital-twin.md) |
| 02 | Middleware & control | [`02-middleware-and-control.md`](02-middleware-and-control.md) |
| 03 | Arm motion planning | [`03-arm-motion-planning.md`](03-arm-motion-planning.md) |
| 04 | Perception & 3D vision | [`04-perception-and-vision.md`](04-perception-and-vision.md) |
| 05 | Grasping & manipulation | [`05-grasping-and-manipulation.md`](05-grasping-and-manipulation.md) |
| 06 | Identification & barcode | [`06-identification-and-barcode.md`](06-identification-and-barcode.md) |
| 07 | Orchestration & task logic | [`07-orchestration-and-task-logic.md`](07-orchestration-and-task-logic.md) |
| 08 | Software, worklist & compliance | [`08-software-worklist-and-compliance.md`](08-software-worklist-and-compliance.md) |
| 09 | Sensing & signal acquisition | [`09-sensing-and-signal-acquisition.md`](09-sensing-and-signal-acquisition.md) |
| 10 | Sensor fusion, gating & full-flow integration | [`10-sensor-fusion-and-gating.md`](10-sensor-fusion-and-gating.md) |

> **Sensing (09–10) ties the rest together.** Layer 09 makes every
> sensor in [`sensor-suite.md`](sensor-suite.md) exist as a ROS 2 topic
> in simulation; Layer 10 fuses those readings into the two-witness
> **gates** that open or block each motion in the per-vial flow. The
> earlier layers *act*; these two make the cell *sense and verify*
> before it acts.

The **base problem** every layer builds toward is the **tomato-ketchup
→ 5-HMF** run — the messy food-matrix case the whole cell is designed
around. Its full object and workcell scene is in
[`01-simulation/01-ketchup-experiment-objects.md`](01-simulation/01-ketchup-experiment-objects.md),
and each development layer below proves one piece of it.

## How each file is structured

- A one-glance table of the **five** options.
- One section per framework with **≥3 paragraphs**: what it is, how it's
  good, and how it's bad versus the others.
- A **Verdict** naming the **best-in-class**, the **cheapest**, and the
  **best-practical** pick (the cost/performance balance).
- **Meta code** — the best-practical pipeline's shape in short pseudocode.
- **Real code** — a complete, runnable-shaped implementation of that pick,
  with an inline comment on **every line** explaining what it does. It is
  illustrative teaching code; library and message names drift between
  versions, so re-verify before relying on it.

## Beyond v1: the learned upgrade path (VLAs)

The stack above is deliberately **analytical / geometric** — the right
call for one known vial. The **learned upgrade path** is
Vision-Language-Action (**VLA**) foundation models — π0/π0.5 (Physical
Intelligence), Gemini Robotics (Google DeepMind), OpenVLA, NVIDIA Isaac
GR00T, and the LeRobot/SmolVLA ecosystem — which map camera frames + a
text instruction straight to actions. They are surveyed in the
grasping/manipulation file (Layer 05) and, in only-code mode, can be
**evaluated and fine-tuned in simulation with zero hardware**. The full
comparison and the honest "why not yet for v1 / compliance" framing is in
**[`foundation-models.md`](foundation-models.md)**.

## What simulation *can* and *can't* prove

**Can prove fully in open-source sim:** bench layout and **reachability**
(especially important given the 280's short reach), collision-free
**motion planning**, the **sequencing / state machine**, the
**perception pipelines**, the **vial→slot→worklist mapping**, the entire
**software + audit-trail** application, and **cycle-time** estimates.

**Cannot be fully proven in sim (needs hardware):** real **grasp
friction/slip on glass**, **decap torque**, **dispense accuracy**, and
**regulatory validation** (IQ/OQ/PQ). The key **abstractions** are a
grasp-fix plugin for grasping, cap-as-a-breakable-joint toggled by a
station service for decap, a scalar **fill-volume state** for liquids,
and ROS 2 **mock-station** nodes for the decapper / dispenser / balance /
scanner / autosampler.

---

## Additional real-world hardware — rollup

Beyond the **myCobot 280 + a gripper** (Elephant's adaptive/parallel
gripper, or the suction pump), the full system eventually needs the
hardware below; the stations are arm-agnostic. In simulation each is a
model or a mock-station node.

| Hardware | For step(s) | Mocked in sim as |
|----------|-------------|------------------|
| End-effector(s): parallel/adaptive gripper (+ suction option) | grasp, dispense | Gripper model + grasp-fix plugin |
| Decapper/capper station | decap | `/decap` `/cap` service node |
| Syringe pump / dispenser / pipetting head, tips, wash station | dispense | `/dispense` service + fill-volume state |
| Analytical balance (optional gravimetric check) | dispense | Reads the simulated fill state |
| Barcode scanner (+ optional label printer/applicator) | identify | Sim camera + ZBar, or `/scan` mock |
| **Cameras ×3**: overhead RGB-D + station RGB-D + light wrist RGB | perception | Gazebo `camera`/`depth_camera` sensors |
| **Gripper feedback** (jaw width + motor current) | grasp | `ros2_control` joint pos+effort + grasp-fix |
| **Decapper load cell / torque sense** | decap | Force-torque sensor on the cap joint |
| **Analytical balance** (gravimetric fill check) | dispense | Reads the fill-volume scalar as mass |
| **Proximity/presence** sensors per station; **liquid-level** sensor | dispense, tray | Logical-camera/contact sensors; level from fill state |
| **Base IMU / tilt**; **homing/limit** switches | orchestration | Gazebo `imu` sensor; joint-limit state |
| Controlled **lighting** (LED panel + matte backdrop) | perception | Gazebo scene lights (clean — glare can't be proven) |
| HPLC autosampler + trays/racks; vial supply racks; bench, jigs | place, tray | Static models with named tf frames |
| Enclosure/guarding, e-stop, interlocks, **light curtain** | orchestration, safety | `/safety_stop`, `/door_closed`, `/light_curtain_clear` |
| Compute (the myCobot's Pi/Jetson, or a controller PC) | software | The dev machine running ROS 2 |

> **myCobot-specific hardware note.** Because the 280's reach is short,
> the real bench needs **tightly clustered stations** (or a small linear
> rail/turntable to bring stations to the arm). The digital twin is the
> right place to decide whether the 280 reaches everything or whether you
> must upgrade to a myCobot 320.

---

## Which arm to simulate first

The myCobot 280 wins on **ready-made open-source sim assets today**
(`mycobot_ros` ships Gazebo + MoveIt) and **low cost**, but is
**reach/payload limited**. The candidate arms are scored on 30 parameters
in [`../05-arms-comparison.md`](../05-arms-comparison.md).
