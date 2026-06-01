# AgileX PiPER implementation — proving each part in open-source simulation

> **The claim.** Every part of the HPLC vial-prep + tray-loading
> solution in `../01-high-level-solution/` can be **developed and proven
> in simulation first**, using the **AgileX PiPER** arm and a fully
> **open-source** stack — *before* buying the arm, the stations, or the
> instrument. This folder is the PiPER sibling of
> `../02-reBot-implementation/` and `../03-mycobot-280-impl/`: same 10
> parts, same method, different arm.

New to a term? See `../../03-place-items-on-shelf/02-glossary.md` for
robotics vocabulary; lab terms are defined in `../01-high-level-solution/`.

> **Disclaimer.** Tool versions, package maturity, reach/payload specs,
> and cost figures drift — re-verify before relying on them. Simulation
> proves *logic, geometry, and software*, not real-world physics (see
> "What sim can and can't prove").

---

## Why the AgileX PiPER

The **PiPER** (AgileX Robotics) is a **lightweight 6-DoF arm** aimed
squarely at embodied-AI and teleoperation work. It is an interesting
middle option between the two other arms covered here:

- **Low cost** — roughly **~$1.5–2.5k** (`~`, verify), in the hobby/
  research price band rather than industrial-cobot territory.
- **Useful payload and reach** — **~1.5 kg** payload and a working
  radius around **~600 mm** (`~`, verify). That is far more bench reach
  than the myCobot 280's ~280 mm, so the PiPER can serve **several
  spread-out stations** without an ultra-compact layout — a real
  advantage for this multi-station cell.
- **Native ROS / ROS 2** — AgileX ships **`piper_sdk`** (the low-level,
  CAN-bus Python/C++ SDK for the real arm) and the **`piper_ros`** ROS
  packages (GitHub `agilexrobotics`), with a **URDF** and explicit
  **Hugging Face LeRobot** compatibility for imitation learning.

For a *simulation-first* effort the relevant assets are the **URDF** and
the ROS interfaces: you drive the URDF in **Gazebo** with
`gz_ros2_control` + **MoveIt 2**; `piper_sdk` is only for the real arm.

> **Caveat (early 2026).** Confirm the maturity of PiPER's official
> **MoveIt 2 config and Gazebo assets** before relying on them — if the
> vendor config isn't ready, generate a MoveIt config from the URDF with
> the **MoveIt Setup Assistant**, exactly as on the reBot path. (We
> default to **Gazebo**/**MuJoCo** to stay fully open-source.)

---

## The open-source simulation stack (shared across all parts)

Identical to the reBot and myCobot paths, so all three arms are directly
comparable:

| Tool | Role here | Licence |
|------|-----------|---------|
| **Gazebo Harmonic** (`gz-sim`) | Primary physics + sensor simulator; bench, stations, vials, tray | Apache-2.0 |
| **MuJoCo** (optional) | Contact-rich tuning for grasping/insertion | Apache-2.0 |
| **ROS 2** (Humble/Jazzy) | Middleware tying every node together | Apache-2.0 |
| **`ros2_control` + `gz_ros2_control`** | Joint controllers in sim | Apache-2.0 |
| **MoveIt 2** (config from PiPER URDF) | Collision-free arm motion planning | BSD |
| **`piper_ros`** / **`piper_sdk`** | PiPER URDF + ROS interfaces (SDK is for the real arm) | open (verify) |
| **OpenCV**, **apriltag_ros**, **Open3D/PCL** | Perception: detection, fiducials, level checks | BSD/Apache |
| **ZBar / pyzbar** | Barcode/QR decoding from simulated camera images | LGPL |
| **BehaviorTree.CPP** (+ **Groot2** free) / **py_trees** | Orchestration + failure handling | MIT |
| **SQLite**, **FastAPI** | Audit-trail store + mock LIMS/CDS service | Public-domain/MIT |
| **RViz2**, **Foxglove Studio** | Visualization and debugging | BSD/MPL |

---

## What simulation *can* and *can't* prove

**Can prove fully in open-source sim:** bench layout and
**reachability** (the PiPER's ~600 mm reach makes multi-station layouts
realistic), collision-free **motion planning**, the **sequencing /
state machine**, the **perception pipelines**, the
**vial→slot→worklist mapping**, the entire **software + audit-trail**
application, and **cycle-time** estimates.

**Cannot be fully proven in sim (needs hardware):** real **grasp
friction/slip on glass**, **decap torque**, **dispense accuracy**, and
**regulatory validation** (IQ/OQ/PQ). The same **abstractions** apply as
on the other arms — grasp-fix plugin for grasping, cap-as-a-breakable-
joint toggled by a station service for decap, a scalar **fill-volume
state** for liquids, and ROS 2 **mock-station** nodes for the decapper /
dispenser / balance / scanner / autosampler.

---

## The parts (each mirrors the same-numbered high-level doc)

| # | Document | Mirrors |
|---|----------|---------|
| 01 | [`01-scope-and-workflow.md`](01-scope-and-workflow.md) | [scope & workflow](../01-high-level-solution/01-scope-and-workflow.md) |
| 02 | [`02-vial-handling-and-gripping.md`](02-vial-handling-and-gripping.md) | [vial handling](../01-high-level-solution/02-vial-handling-and-gripping.md) |
| 03 | [`03-decapping-and-capping.md`](03-decapping-and-capping.md) | [decapping](../01-high-level-solution/03-decapping-and-capping.md) |
| 04 | [`04-liquid-handling-and-sample-prep.md`](04-liquid-handling-and-sample-prep.md) | [liquid handling](../01-high-level-solution/04-liquid-handling-and-sample-prep.md) |
| 05 | [`05-tray-loading-and-positioning.md`](05-tray-loading-and-positioning.md) | [tray loading](../01-high-level-solution/05-tray-loading-and-positioning.md) |
| 06 | [`06-identification-labeling-and-tracking.md`](06-identification-labeling-and-tracking.md) | [identification](../01-high-level-solution/06-identification-labeling-and-tracking.md) |
| 07 | [`07-perception-and-verification.md`](07-perception-and-verification.md) | [perception](../01-high-level-solution/07-perception-and-verification.md) |
| 08 | [`08-orchestration-error-handling-and-safety.md`](08-orchestration-error-handling-and-safety.md) | [orchestration](../01-high-level-solution/08-orchestration-error-handling-and-safety.md) |
| 09 | [`09-software-compliance-and-integration.md`](09-software-compliance-and-integration.md) | [software & compliance](../01-high-level-solution/09-software-compliance-and-integration.md) |
| 10 | [`10-hardware-platform-and-capital-model.md`](10-hardware-platform-and-capital-model.md) | [hardware & capital](../01-high-level-solution/10-hardware-platform-and-capital-model.md) |

Each part doc follows the same shape: **What we can prove in
simulation** → **Open-source tools** → **How to simulate it now** →
**Additional hardware needed** → **How it connects**.

---

## Additional real-world hardware — rollup

Beyond the **PiPER arm + a gripper** (PiPER ships with a parallel
gripper; a suction or custom end-effector is an option), the full system
eventually needs the hardware below — identical to the other arms, since
the stations are arm-agnostic. In simulation each is a model or a
mock-station node.

| Hardware | For part(s) | Mocked in sim as |
|----------|-------------|------------------|
| End-effector(s): PiPER parallel gripper (+ suction/custom option) | 02, 04 | Gripper model + grasp-fix plugin |
| Decapper/capper station | 03 | `/decap` `/cap` service node |
| Syringe pump / dispenser / pipetting head, tips, wash station | 04 | `/dispense` service + fill-volume state |
| Analytical balance (optional gravimetric check) | 04 | Reads the simulated fill state |
| Barcode scanner (+ optional label printer/applicator) | 06 | Sim camera + ZBar, or `/scan` mock |
| RGB-D cameras (wrist + fixed) + lighting | 07 | Gazebo depth-camera sensors |
| HPLC autosampler + trays/racks; vial supply racks; bench, jigs | 01, 05 | Static models with named tf frames |
| Enclosure/guarding, e-stop, interlocks | 08, 10 | `/safety_stop` topic + state |
| Compute (a controller PC; PiPER is CAN-bus driven) | 09, 10 | The dev machine running ROS 2 |

---

## How PiPER compares (reBot vs myCobot 280 vs PiPER)

All three are covered so you can choose. In short:

- **myCobot 280** — cheapest, most ready-made open-source sim assets
  today, but **short reach (~280 mm)** forces a cramped layout.
- **AgileX PiPER** — **low cost** *and* a **useful ~600 mm reach /
  ~1.5 kg payload** with native ROS 2 + LeRobot, making it a strong
  **sim-to-bench PoC** arm for a multi-station cell; verify its MoveIt/
  Gazebo asset maturity.
- **reBot B601-DM** — longest reach / higher payload, but its official
  MoveIt/sim tooling was still maturing as of early 2026.

Because the *world, stations, perception, orchestration, and software
layers are identical*, only the arm URDF changes — so you can build the
cell once and swap arms to compare reach, cycle time, and cost (see
Part 10 in each folder).
