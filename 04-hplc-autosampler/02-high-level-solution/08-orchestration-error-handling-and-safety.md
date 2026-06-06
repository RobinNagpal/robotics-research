# Part 08 — Orchestration, error handling & safety

> **Problem:** Preparing and loading a batch of vials is a long chain of
> small steps that can each go wrong, run by a strong machine near
> people. This part is the conductor that sequences the batch, decides
> what to do when a step fails, and makes sure the arm cannot hurt
> anyone or quietly ruin a sample.

## The problem

Parts 02–07 each solve one slice of the job: grip a vial, decap it,
dispense, cap, label, place, verify. None of them decides *when* to run,
*in what order*, or *what to do when one of them fails mid-batch*. That
coordination is its own problem, and in a regulated lab it is the part
that decides whether the system is trustworthy.

Three things have to be handled together:

1. **Sequencing** — drive the per-vial loop for N vials in worklist
   order, station by station, without collisions or skipped steps.
2. **Failure handling** — every step can fail (a missed grip, a spill, a
   barcode that does not match). The system must respond in a way that
   never risks sample integrity and never "silently continues."
3. **Safety** — a 6-DoF arm has reach and force; people share the bench.
   It must stop safely when a person is present and on any emergency.

The non-negotiable rule that shapes all of this: **never silently
continue in a way that risks sample integrity.** A wrong-but-plausible
vial reaching the instrument is worse than a halted run, because a
halted run is visible and a corrupted result is not.

## The solution

**The conductor: a Behavior Tree.** A **Behavior Tree** is a way of
describing a robot's logic as a tree of small tasks and decisions that
the system "ticks" through repeatedly, so it always knows what to do
next and can react to success or failure at each node. (A **state
machine** — a fixed set of states with rules for moving between them —
is a reasonable alternative; Behavior Trees are preferred here because
adding a new check or recovery branch is a local edit, not a rewrite of
all the transitions.)

The tree sequences the per-vial loop from `01-scope-and-workflow.md`:
read worklist row, pick, decap, dispense, cap, label/read, verify,
place. Critically, the **verification gates** from
`07-perception-and-verification.md` are nodes in this tree — a gate that
returns FAIL routes the tree into a recovery branch instead of the next
step.

**Scheduling / batching.** The natural unit is one worklist of N
vials, processed one vial at a time (v1). Batching choices:

| Approach | What it means | Bottom line |
|---|---|---|
| One vial fully, then next | Pick→…→place each vial before starting the next | **Best v1** — simplest, easiest to verify and recover |
| Pipeline stations | Several vials in flight at different stations | Faster but needs multi-vial tracking; defer |
| Reorder within batch | Group by recipe/station to cut motion | Optimisation; defer, and never reorder across worklist constraints silently |

### Failure handling

Each failure has a *defined* response. The principle: retry only the
cheap, obviously-recoverable errors a small number of times; otherwise
stop or quarantine, and **always log** (audit trail in
`09-software-compliance-and-integration.md`).

| Failure mode | Likely cause | Response | Bottom line |
|---|---|---|---|
| Missed grip | Vial not where expected / slipped | Retry pick ~2–3×, then **alert** & pause | Cheap to retry; don't loop forever |
| Spill / breakage | Knocked vial, cracked glass | **Stop, flag, hold for human** | Glass + liquid = safety + integrity event |
| Barcode mismatch | Wrong/unreadable vial vs worklist | **Quarantine** that vial; continue or pause per policy | Never load an unidentified vial |
| Decap failure | Cap stuck / cross-threaded | Retry ~1–2×, else **skip-and-log**, alert | Don't force; don't fill a capped vial |
| Cap-not-seated | Re-cap didn't seat | Retry seat; else **flag vial**, don't place | Unsealed vial can leak/evaporate |
| Short / over fill | Dispenser fault | **Flag vial**, don't place; pause if repeated | Integrity gate, not retried blindly |
| Slot occupied | Tray not empty as expected | **Pause & alert** | Don't stack; human resolves |
| Sensor UNSURE | Verification can't confirm | Re-image once; else treat as FAIL | "Unsure" is not "pass" |

Two cross-cutting rules:

- **Quarantine, don't discard.** A suspect vial is set aside to a known
  quarantine position and logged, so a human can inspect it. Nothing is
  thrown away by the machine in v1.
- **Bounded retries.** Every retry has a small fixed limit; on exhaustion
  the system escalates (alert/pause/stop), it does not retry forever.

### Pause / resume

A run can be **paused** (finish the current safe sub-step, stop, hold
state) and **resumed** (continue from the same worklist position) — by an
operator, or automatically on a recoverable alert. State is held so the
batch is not restarted from scratch. The full run state and the reason
for any pause are logged.

### Safety

The arm shares a bench with people, so safety is designed in two broad
styles (v1 can use either or both):

- **Collaborative-robot ("cobot") limits** — the arm runs at reduced
  speed and with force/torque limits so that contact with a person is
  detected and the arm stops gently. Lets humans work nearby without a
  cage, at the cost of speed.
- **Guarded enclosure** — the work cell is fenced/boxed with
  **interlocks** (sensors that detect the guard's state) and **door
  sensors**; opening the enclosure during a run triggers a **safe stop**.
  Faster motion is allowed because people are kept out while it moves.

Always present, regardless of style:

- **Emergency stop (e-stop)** — a hardware button that cuts/holds the
  arm immediately; a deliberate, supervised reset is required to
  continue.
- **Safe-stop on human entry** — any door-open / presence event during
  motion stops the arm in a controlled way; the run pauses, not crashes.
- **No silent restart** — after any safety stop, resuming is an explicit
  human action, and the event is logged.

For v1, **a human is supervising the whole run**, which is itself a
safety and integrity layer: the supervisor is the backstop the
auto-recovery logic deliberately defers to.

## v1 vs later

**v1 — keep it simple.**

- **Behavior Tree** sequencing one worklist, **one vial at a time**.
- **Verification gates as tree nodes** — fail routes to recovery.
- **Stop-and-alert on most errors**, with **limited, bounded auto-retry**
  only for the cheap, clearly-recoverable ones (missed grip, decap).
- **Quarantine** for suspect vials; nothing discarded automatically.
- **Pause / resume** of a run with held state.
- **Safety**: cobot limits and/or a guarded enclosure, e-stop, door
  sensors, safe-stop on entry — **with a human supervising throughout**.

**Deferred to later milestones:** rich autonomous recovery (e.g. the
arm clearing its own spill, re-prepping a failed vial unattended);
pipelined multi-vial scheduling and reordering; **lights-out /
walk-away operation** with no supervisor; predictive fault detection;
multi-instrument / multi-tray orchestration.

## How it connects

- **`02-vial-handling-and-gripping.md`** … **`07-perception-and-
  verification.md`** — orchestration drives all of these in order and
  reacts to their results; the verification gates from Part 07 are the
  branch points in the tree.
- **`07-perception-and-verification.md`** — a failed gate is the primary
  trigger for the failure responses above.
- **`09-software-compliance-and-integration.md`** — every sequencing
  decision, retry, quarantine, pause, and safety stop is written to the
  audit trail; compliance rules constrain what auto-recovery is even
  allowed to do.
- Back to the index: [`README.md`](README.md).
