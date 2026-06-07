# Part 08 — Orchestration, error handling & safety (simulation)

> **Sim goal:** Build the workflow *conductor* as a Behavior Tree that
> ticks through the per-vial loop in Gazebo, calling each part's ROS 2
> action/service — and then *deliberately break* steps (fault
> injection) to prove the recovery branches and the safe-stop all work,
> without risking a single real vial or finger.

This part stitches Parts 02–07 into one running system. Each of those
solves a slice (grip, decap, dispense, cap, scan, place, verify) but
none decides *when* to run, *in what order*, or *what to do when a step
fails mid-batch*. That coordination — plus making the arm stop safely —
is the job here, and in a regulated lab it is the part that decides
whether the whole cell can be trusted.

A **Behavior Tree** (BT) is a way of writing a robot's logic as a tree
of small tasks and decisions that the system "ticks" (re-evaluates)
many times a second, so it always knows the next action and can react
to success or failure at each node. We use **BehaviorTree.CPP** to run
it and **Groot2** to watch it tick live. The non-negotiable rule it
enforces: **never silently continue in a way that risks sample
integrity** — a wrong-but-plausible vial reaching the instrument is
worse than a halted run, because a halt is visible and a corrupted
result is not.

## What we can prove in simulation

Entirely in the open-source stack, before hardware, we can prove:

- **Sequencing works.** The BT drives the full per-vial loop for N
  vials in worklist order, station by station, calling the right ROS 2
  action/service at each step and never skipping a verification gate
  (`07-perception-and-verification.md`).
- **Recovery logic works.** With **fault injection** (deliberately
  failing a step on command) we trigger every recovery branch — retry,
  alert, quarantine, skip-and-log, stop — and confirm each does the
  right thing. This is sim's single biggest advantage: we can break the
  process a thousand times for free.
- **Safe-stop behaviour works.** A `/safety_stop` signal halts the tree
  and the arm at any point, then resumes or aborts cleanly — the
  *logic* of an e-stop / interlock, tested exhaustively.
- **Batch statistics.** Running many simulated batches yields early
  success-rate, recovery-rate, and cycle-time figures (hedge with `~`;
  sim timing ignores real settling/dwell).
- **Everything is logged.** Each decision, gate result, and fault emits
  an audit record (ties to `09-software-compliance-and-integration.md`).

**Honest limits.** Sim proves *sequencing, recovery logic, and
safe-stop behaviour*. It does **not** certify functional safety. A real
e-stop, door interlock, or light curtain (a beam that detects a person
reaching in) is a certified hardware safety function that must be
validated on the physical cell — the simulated `/safety_stop` proves
the software reacts correctly, not that the safety chain meets its
standard. Treat all sim rates as optimistic upper bounds.

## Open-source tools

| Tool | Role | Bottom line |
|------|------|-------------|
| BehaviorTree.CPP | Run the workflow as a ticking Behavior Tree | The conductor; battle-tested, ROS 2-friendly. |
| Groot2 | Live monitor + editor for the BT | Watch ticks, see which node is active, debug visually. |
| py_trees (option) | Python BT alternative | Fine if the team prefers Python over C++. |
| ROS 2 actions/services | The BT's calls into Parts 02–07 | Each step is an action/service the leaf nodes invoke. |
| Fault-injection node | Deliberately fails a step on command | Sim-only; the engine for testing recovery. |
| `/safety_stop` topic/state | Stand-in for e-stop / interlock / light curtain | Halts the tree; proves safe-stop logic. |
| MoveIt 2 + `gz_ros2_control` | Executes the arm motions a leaf requests | From `01-scope-and-workflow.md`; the actuation layer. |
| SQLite + FastAPI | Persist every decision to the audit trail | Ties to `09-software-compliance-and-integration.md`. |
| RViz2 / Foxglove | Watch the cell while the BT runs | Confirm motions and stops by eye. |

## How to simulate it now

**1. Author the BT XML.** Describe the per-vial loop as a BehaviorTree.CPP
tree. The backbone is a sequence of leaves, each calling one part's
action/service, with a verification gate (Part 07) after every action:

```
Repeat (per vial in worklist)
  └─ Sequence
       ├─ Pick vial            (02)  → Gate: in gripper?      (07)
       ├─ Scan barcode         (06)  → Gate: matches worklist? (07)
       ├─ Decap                (03)  → Gate: open rim?         (07)
       ├─ Dispense             (04)  → Gate: level ok? no spill? (07)
       ├─ Cap                  (03)  → Gate: cap seated?       (07)
       └─ Place in slot N      (05)  → Gate: seated correctly? (07)
```

Each leaf is a ROS 2 action/service client. A **Fallback** node wraps
each gated step so that a FAIL drops into a recovery sub-tree instead
of crashing the run.

**2. Define the recovery branches.** Map each failure to a response:

- **Retry** — re-attempt the action up to a small limit (e.g. a missed
  grip: re-plan and re-grip ~2–3 times).
- **Alert** — if retries are exhausted, raise an operator alert and
  pause.
- **Quarantine** — a sample-integrity failure (barcode mismatch, spill)
  → set the vial aside to a quarantine slot and log it; do not let it
  reach the instrument.
- **Skip-and-log** — a non-critical, non-integrity issue → record and
  move to the next vial.
- **Stop** — any unrecoverable or safety event → halt the whole batch.

**3. Implement the fault-injection node.** A sim-only ROS 2 node
exposes parameters/services that make a chosen step fail on demand, by
intercepting or corrupting the relevant mock-station behaviour:

- *grasp miss* — the grasp-fix plugin (Part 02) declines to attach;
- *decap fail* — the decap station service (Part 03) leaves the cap
  link on its breakable joint;
- *barcode mismatch* — the scan node (Part 06) returns the wrong ID;
- *short fill / spill* — the dispenser service (Part 04) sets a wrong
  fill-volume or raises a spill flag.

Drive it from a test script so each fault fires on a known vial, and
assert that the BT took the intended branch.

**4. Simulate safety.** Implement a `/safety_stop` topic (or latched
state). A high-priority node at the **root** of the BT checks it every
tick: when asserted, it pre-empts the running leaf, commands the arm to
a controlled stop via the controllers from
`01-scope-and-workflow.md`, and holds until cleared. This stands in for
the e-stop / interlock / light curtain and lets us test stop-and-resume
from every point in the loop.

**5. Run repeated batches and measure.** Script many simulated batches
(clean runs and runs seeded with injected faults), and record
per-batch success rate, recovery rate by fault type, and approximate
cycle time. Watch a representative run in **Groot2** to see exactly
which node is ticking and which branch a fault takes.

**6. Confirm everything is logged.** Each leaf result, gate
pass/fail, recovery decision, injected fault, and safety event must
write an audit record (timestamp, vial ID, step, outcome) via the
logging interface of `09-software-compliance-and-integration.md`. A run
where every decision is reconstructable from the log is the evidence
that the conductor is trustworthy.

## Additional hardware needed

On the real cell, safety is **hardware**: a physical **e-stop** button,
**safety interlocks** / a **light curtain** wired into a certified
safety controller, and an **enclosure** or guarding around the arm's
reach. None of this is bought for sim:

- e-stop / interlock / light curtain → a single `/safety_stop` signal
  and BT state that proves the *software* reacts correctly;
- enclosure → not modelled beyond the bench geometry of
  `01-scope-and-workflow.md`.

The conductor (BT), the recovery branches, and the audit logging are
genuinely the same software that will run on hardware; only the safety
*chain* and its certification are deferred.

## How it connects

- `02-vial-handling-and-gripping.md` … `06-identification-labeling-and-tracking.md`
  — the BT *drives* each of these as a ROS 2 action/service and reacts
  to its result.
- `07-perception-and-verification.md` — supplies the gates; a failed
  gate is the event that triggers a recovery branch here.
- `09-software-compliance-and-integration.md` — every decision,
  recovery, and safety event is written to the audit trail; compliance
  rules constrain which recovery is allowed (e.g. integrity failures
  must quarantine, never silently skip).
- High-level companion:
  `../03-high-level-solution/08-orchestration-error-handling-and-safety.md`.
- Folder overview: [`README.md`](README.md).
