# 02 — Code plus hardware: developing each layer with the real myCobot

> **What this folder is.** The same framework/library guide as
> [`../01-only-code/`](../01-only-code/README.md), but for when the
> **physical myCobot 280 and real peripherals are in the loop** —
> cameras, decapper, dispenser, barcode scanner, and (eventually) the
> instrument. For each of the **8 development layers** below, one file
> covers **five** frameworks or libraries, naming the **best-in-class**,
> the **cheapest**, and the **best-practical** (cost/performance balance).

> **Disclaimer.** Library maturity, driver support, licences, and "best"
> calls drift and are opinions — re-verify before committing. Figures are
> approximate (`~`).

---

## Scope: "code plus hardware"

Here the real **myCobot 280** runs alongside your code, and real devices
replace the mocks. That changes the toolbox at the lower layers: you now
need **hardware drivers and SDKs** (e.g. `pymycobot`, `mycobot_ros`, a
`ros2_control` hardware interface), **real camera SDKs** (RealSense /
OAK / Orbbec), **real scanner** integration, and **instrument protocols**
(SiLA 2 / OPC UA) — plus everything that hardware forces you to care
about: latency, calibration, real-time control, and safety.

Upper layers that are hardware-agnostic (motion planning, orchestration)
reuse the *same* frameworks as the only-code folder — but each file notes
**what changes once hardware is real** (e.g. MoveIt Servo, controller
latency, gripper drivers, hand-eye calibration).

## The 8 development layers

| # | Layer | File |
|---|-------|------|
| 01 | Robot bring-up & digital twin | [`01-simulation-and-digital-twin.md`](01-simulation-and-digital-twin.md) |
| 02 | Middleware & real-time control | [`02-middleware-and-control.md`](02-middleware-and-control.md) |
| 03 | Arm motion planning | [`03-arm-motion-planning.md`](03-arm-motion-planning.md) |
| 04 | Perception & 3D vision (real cameras) | [`04-perception-and-vision.md`](04-perception-and-vision.md) |
| 05 | Grasping & manipulation | [`05-grasping-and-manipulation.md`](05-grasping-and-manipulation.md) |
| 06 | Identification & barcode (real scanners) | [`06-identification-and-barcode.md`](06-identification-and-barcode.md) |
| 07 | Orchestration & task logic | [`07-orchestration-and-task-logic.md`](07-orchestration-and-task-logic.md) |
| 08 | Software, worklist & compliance (real LIMS/CDS) | [`08-software-worklist-and-compliance.md`](08-software-worklist-and-compliance.md) |

> Same 8 layers as [`../01-only-code/`](../01-only-code/README.md) so the
> two folders line up file-for-file — only the **mode** (and therefore
> some of the framework choices) differs.

## How each file is structured

- A one-glance table of the **five** options.
- One section per framework with **≥3 paragraphs**: what it is, how it's
  good, and how it's bad versus the others.
- A **Verdict** naming the **best-in-class**, the **cheapest**, and the
  **best-practical** pick (the cost/performance balance).
