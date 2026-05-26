# Phase 5 — Integration, the loop, metrics & randomization

> **Goal:** tie the layers together with a Behavior Tree that runs the
> full **drive → pick → locate slot → place → verify → repeat** loop,
> add the v1 geometric perception inputs, and produce the per-unit
> success log over randomized runs that is the project's definition of
> done (`../01-requirements.md` §6, §9,
> `../03-stack/07-orchestration.md`).
>
> **Checkpoint:** one command runs a full autonomous stocking job and
> writes a per-unit success/failure log; repeated randomized runs report
> a success rate.

---

## 5.1 The v1 perception inputs (geometric / known)

Keep perception minimal for the Gazebo stage
(`../03-stack/05-perception.md`):

- **Product pose:** from the **known tray layout** — no vision needed for
  the pick in v1. (FoundationPose is the Isaac-stage upgrade.)
- **Slot location:** computed from the **planogram** (slot origin +
  offset × already-placed) plus a **planar fit of the shelf face** from
  the wrist RGB-D point cloud to refine the shelf plane and the base
  alignment from Phase 3.
- **Verify:** after the place, a quick check that a can occupies the slot
  and is upright (point-cloud occupancy at the expected slot, or the
  attach/detach + final pose).

Put these in a `shelf_perception` node publishing poses; the BT consumes
them. No learned models in this stage.

## 5.2 The planogram

A small static file (`shelf_orchestration/config/planogram.yaml`): target
shelf ID → slot origin, SKU, facing count, per-facing spacing. This is
the "known store layout" assumption (`../01-requirements.md` §3) — not a
live retail integration.

## 5.3 The Behavior Tree

Author the loop in **BehaviorTree.CPP** (monitor with **Groot2**),
reusing the same BT paradigm Nav2 already runs
(`../03-stack/07-orchestration.md`). Each leaf is a ROS 2 action from the
earlier phases:

```
Sequence: StockShelfJob
  ├─ NavigateToShelf        (Phase 3)
  ├─ AlignToShelfFace       (planar fit nudge, 5.1)
  └─ Repeat [until tray empty OR row full]
       └─ Sequence: OnePlacement
            ├─ LocateProduct      (known tray cell)
            ├─ PickProduct        (Phase 4)  ── on fail → LogAndSkip
            ├─ LocateSlot         (planogram + planar fit)
            ├─ PlaceProduct       (Phase 4)  ── on fail → LogAndSkip
            └─ VerifyPlacement    (5.1)      ── on fail → LogAndSkip
  └─ ReportJobComplete
```

Failure policy (`../01-requirements.md` §7): a failed pick/place/verify is
**logged and skipped**, not retried indefinitely; an unrecoverable state
or an obstacle (safe-stop from Phase 3) **halts** and flags a human. The
robot must never wedge itself.

## 5.4 Logging & observability

Every run writes a structured per-unit log (CSV/JSON), the
**observability** requirement (`../01-requirements.md` §7):

- per unit: outcome (placed / dropped / missed-slot / collision /
  knocked-neighbor), cycle time, failure reason;
- per job: units attempted/placed, overall success rate, total time.

This is what turns "it worked" into a **measurable success rate**. Also
record `rosbag2` for replay/debugging.

## 5.5 Randomization for the success-rate runs

Gazebo-level randomization between runs (full visual DR waits for Isaac
Sim — `../03-stack/01-simulator.md`):

- **Robot start pose** in the aisle (Nav2 must still arrive).
- **Tray cell offsets** and small **SKU spawn perturbations** (tests the
  grasp + the planar-fit alignment).
- Optionally shelf stand-off jitter.

Script N runs headless (`gz sim -s -r` server-only, no GUI) and aggregate
the logs into a success rate.

## 5.6 Definition of done (Gazebo stage)

- A single launch runs the full job autonomously: drive → stock the row
  → report, upright and collision-free.
- Over **N randomized runs** the log shows a single-unit place success
  rate trending toward the requirements target (≥95% — pushing the last
  few percent may wait for the Isaac stage), within the cycle-time budget
  (20–40 s/unit).
- Every leaf is a ROS 2 action over the standard interface, so the same
  BT and nodes run unchanged when the simulator is swapped to Isaac Sim
  or the drivers are swapped to hardware.

## Deliverables

- `shelf_perception` (geometric pose, planar fit, verify).
- `planogram.yaml` + the BehaviorTree.CPP tree + Groot2 monitoring.
- Per-unit logging + a headless N-run harness producing a success rate.

## Checkpoint & next stage

One command stocks the shelf end to end and emits a success-rate log over
randomized runs. The mechanics are proven in Gazebo. **Next stage:** move
the *perception* half to **Isaac Sim** for photoreal + domain
randomization (FoundationPose, learned slot detection) under the *same*
ROS 2 nodes — the recommended path in `../03-high-level-tech.md` §7.
