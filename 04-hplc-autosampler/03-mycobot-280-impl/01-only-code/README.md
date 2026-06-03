# 01 — Only code: developing each layer in simulation, no hardware

> **What this folder is.** A framework/library guide for building the
> myCobot 280 HPLC cell **entirely in code and simulation — zero hardware
> purchased.** For each of the **8 development layers** below, one file
> covers **five** frameworks or libraries that help you build that layer,
> and explicitly names the **best-in-class**, the **cheapest**, and the
> **best-practical** (the one that balances cost and performance).
>
> The sibling folder [`../02-code-plus-hardware/`](../02-code-plus-hardware/README.md)
> answers the same question for when the **real myCobot 280 + peripherals
> are in the loop**.

> **Disclaimer.** Library maturity, licences, and "best" calls drift and
> are opinions, not gospel — re-verify before committing. Figures are
> approximate (`~`).

---

## Scope: "only code"

Here you develop and prove the system with **no physical hardware**:
simulators, synthetic data, and mock device services stand in for the
arm, cameras, decapper, dispenser, scanner, and instrument. This is the
cheapest, fastest way to get the whole **prep → load** loop working and
to de-risk the eventual purchase (see
[`../10-hardware-platform-and-capital-model.md`](../10-hardware-platform-and-capital-model.md)).

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
lives in [`../sensor-suite.md`](../sensor-suite.md).

## The 8 development layers

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

> These 8 are the *framework-developable* layers. They cut across the 10
> solution parts in [`../01-scope-and-workflow.md`](../01-scope-and-workflow.md)
> onward (e.g. perception serves parts 06/07; orchestration serves part
> 08) — the parts say *what* to build, these layers say *what to build it
> with*.

## How each file is structured

- A one-glance table of the **five** options.
- One section per framework with **≥3 paragraphs**: what it is, how it's
  good, and how it's bad versus the others.
- A **Verdict** naming the **best-in-class**, the **cheapest**, and the
  **best-practical** pick (the cost/performance balance).

## The learned upgrade path (VLAs)

Beyond the per-layer frameworks, the grasping/manipulation file (Layer
05) also surveys **Vision-Language-Action foundation models** — π0/π0.5,
Gemini Robotics, OpenVLA, NVIDIA GR00T, LeRobot/SmolVLA — which in
only-code mode you can **evaluate and fine-tune in simulation with zero
hardware**. Full comparison:
[`../foundation-models.md`](../foundation-models.md).
