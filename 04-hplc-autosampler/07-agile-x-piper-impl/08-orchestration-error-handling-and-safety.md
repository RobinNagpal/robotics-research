# Part 08 — Orchestration, error handling & safety (AgileX PiPER simulation)

> **Sim goal:** Build the workflow *conductor* as a Behavior Tree that
> ticks the per-vial loop and calls each part's ROS 2 action/service —
> then use the simulator's best trick, **fault injection**, to
> deliberately break steps and prove the recovery branches (retry,
> quarantine, skip-and-log, stop) and a `/safety_stop` actually do the
> right thing, all watched live in Groot2.

This part is the brain that ties Parts 02–07 together. Each of those
solves one slice — grip, decap, dispense, cap, label, place, verify —
but none decides *when* to run, *in what order*, or *what to do when a
step fails mid-batch*. That coordination is its own problem, and it
assumes the cell, arm, station mock nodes, and verification-gate
services from the earlier parts already run. The design here mirrors
the high-level companion
`../03-high-level-solution/08-orchestration-error-handling-and-safety.md`;
this doc shows how to *prove it in simulation*.

A **Behavior Tree (BT)** is a way of writing a robot's logic as a tree
of small tasks and decisions that the system "ticks" through
repeatedly, so it always knows what to do next and can react to
success or failure at each node. We use **BehaviorTree.CPP** (or
`py_trees`) for the tree and **Groot2** to watch and edit it live.

The non-negotiable rule that shapes everything: **never silently
continue in a way that risks sample integrity.** A wrong-but-plausible
vial reaching the instrument is worse than a halted run, because a halt
is visible and a corrupted result is not.

## What we can prove in simulation

- **The conductor sequences a whole batch.** The BT drives the per-vial
  loop from `01-scope-and-workflow.md` for N worklist rows, one vial at
  a time, calling each part's ROS 2 action/service in order with no
  skipped steps or collisions.
- **Verification gates are branch points.** The gate services from
  `07-perception-and-verification.md` are nodes in the tree; a FAIL
  routes into a recovery branch instead of the next step.
- **Recovery logic is *exercised*, not just written.** Because we can
  inject faults on demand, we can fire every recovery branch hundreds
  of times in a row and measure how often it does the right thing —
  something almost impossible to provoke reliably on hardware.
- **Safe-stop halts the tree.** A `/safety_stop` signal interrupts the
  loop, holds state, and forbids silent restart — the *logic* of an
  e-stop / interlock.
- **Everything is logged.** Each decision, retry, quarantine, pause,
  and stop is written to the audit trail of
  `09-software-compliance-and-integration.md`; we confirm the log is
  complete and ordered.

Honest limits:

- **`/safety_stop` is not certified safety.** A ROS 2 topic stopping a
  Behavior Tree proves the *reaction logic*. Real **functional safety**
  — a hardware e-stop that cuts power, rated interlocks, guaranteed
  stopping distance and force limits — must be validated on hardware
  (`10-hardware-platform-and-capital-model.md`). Sim cannot certify it.
- **Injected faults are *chosen* failures.** They prove the branch
  exists and behaves; they do not predict the real-world *rate* or the
  *surprising* failure modes hardware will invent.

## Open-source tools

| Tool | Role | Bottom line |
|------|------|-------------|
| BehaviorTree.CPP | The conductor: ticks tasks, routes on success/fail | Primary BT engine; tree is an editable XML. |
| Groot2 | Live view + editor of the running tree | Watch ticks/branches in real time; a debugging win. |
| `py_trees` (option) | Python Behavior Trees | Alternative if the team prefers Python. |
| ROS 2 actions/services | How the BT calls each part (pick, decap, gate…) | Same interfaces sim and hardware present. |
| Fault-injection node (custom) | Deliberately fails a chosen step | The core sim experiment; flips faults via params/services. |
| `/safety_stop` topic + state | Stand-in for e-stop / interlock | Halts the tree; logic only, not certified safety. |
| SQLite + FastAPI | Records every decision to the audit trail | Ties to `09-...`; proves nothing is silent. |
| RViz2 / Foxglove | Watch the arm and run state during batches | Visual confirmation alongside Groot2. |

## How to simulate it now

Assumes Parts 01–07 are running (cell, arm, station mock nodes,
verification-gate services).

**1. Author the BT XML.** Express the per-vial loop as a tree whose leaf
nodes call the existing ROS 2 actions/services:

```
Sequence (per vial):
  read_worklist_row
  pick            (Part 02)   ──▶ Gate: in_gripper?     (Part 07)
  scan            (Part 06)   ──▶ Gate: matches_worklist?
  decap           (Part 03)   ──▶ Gate: open_rim?
  dispense        (Part 04)   ──▶ Gate: level_ok & no_spill?
  cap             (Part 03)   ──▶ Gate: cap_seated?
  place           (Part 05)   ──▶ Gate: seated_in_slot?
```

Each gate is a condition node; on FAIL the tree falls into the matching
recovery branch (below). A top-level reactive node checks
`/safety_stop` on every tick so a stop interrupts immediately.

**2. Implement a fault-injection node.** A small ROS 2 node exposes
params/services that make a chosen step deliberately fail on the next
attempt — the headline sim capability:

- **grasp miss** — the grasp-fix plugin (Part 02) is told *not* to
  attach, so the vial isn't picked up;
- **decap fail** — the decap station service (Part 03) refuses to
  release the cap link;
- **barcode mismatch** — the scan node (Part 06) returns an ID that
  does not match the worklist;
- **spill flag** — the dispenser service (Part 04) or a perception node
  raises a spill/foam flag.

**3. Prove each recovery branch.** Map each injected fault to its
defined response from the high-level doc and confirm the tree does it:

| Injected fault | Expected branch | Pass criterion |
|---|---|---|
| Grasp miss | Retry pick ~2–3×, then alert & pause | Retries bounded, then halts — never loops forever |
| Decap fail | Retry ~1–2×, else skip-and-log, alert | Never proceeds to dispense a capped vial |
| Barcode mismatch | Quarantine that vial, continue/pause per policy | Unidentified vial never reaches the tray |
| Spill flag | Stop, flag, hold for human | Run halts; nothing placed |
| Gate UNSURE | Re-image once, else treat as FAIL | "Unsure" is never treated as "pass" |

Two cross-cutting rules to verify: **quarantine, don't discard** (a
suspect vial goes to a known quarantine frame, logged — nothing thrown
away) and **bounded retries** (every retry has a fixed limit, then it
escalates).

**4. Simulate safety.** Publish a `/safety_stop` (a topic or latched
state) from a button in Foxglove or a CLI. Prove that, mid-motion, it:
halts the tree at a safe sub-step, holds run state, and **requires an
explicit operator action to resume** (no silent restart). This stands
in for the e-stop / door-interlock behaviour; the certified hardware
version is deferred.

**5. Run repeated batches and measure.** Script batches of N vials with
faults injected at random or scheduled steps, run many iterations
headless, and record: completion rate, per-fault recovery success,
retries used, quarantines, and stops. Watch a live run in **Groot2** to
see exactly which branch each tick takes.

**6. Confirm every decision is logged.** Check that each tick outcome,
retry, quarantine, pause, and safety stop lands in the audit trail of
`09-software-compliance-and-integration.md`, in order and with reason.
A decision that isn't logged is a defect.

## Additional hardware needed

Beyond the PiPER and gripper, the real cell needs an **emergency stop
(e-stop)** button that cuts/holds the arm, **interlocks / door sensors**
on a guard, and an **enclosure** (or, alternatively, certified
collaborative-robot speed/force limits to allow caged-less operation).
In this part none of these is bought:

- **e-stop / interlocks / enclosure → a `/safety_stop` signal + state**
  that halts the Behavior Tree and blocks restart.
- **Certified functional safety → not provable in sim.** Stopping
  distance, force limits, and a power-cutting e-stop must be validated
  on hardware. Sim proves only that the *software reacts correctly* to
  a stop request.

The honest split: sim validates **sequencing, recovery logic, and
safe-stop reaction**; the *certified* safety case is a hardware item in
`10-hardware-platform-and-capital-model.md`. For v1, a human supervises
the whole run — the backstop the auto-recovery logic deliberately
defers to.

## How it connects

- **`02-vial-handling-and-gripping.md`** … **`07-perception-and-
  verification.md`** — the tree drives all of these in order and reacts
  to their results; the verification gates from Part 07 are the branch
  points, and fault injection works by making each part's mock fail.
- **`07-perception-and-verification.md`** — a failed gate is the primary
  trigger for the recovery branches above.
- **`09-software-compliance-and-integration.md`** — every sequencing
  decision, retry, quarantine, pause, and safety stop is logged to the
  audit trail; compliance rules constrain what auto-recovery is even
  allowed to do.
- High-level companion:
  `../03-high-level-solution/08-orchestration-error-handling-and-safety.md`.
- Back to the index: [`README.md`](README.md).
