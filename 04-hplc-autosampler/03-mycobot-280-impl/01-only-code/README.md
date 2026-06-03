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
