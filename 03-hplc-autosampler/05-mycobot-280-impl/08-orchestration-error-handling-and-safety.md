# Part 08 — Orchestration, error handling & safety (myCobot 280 simulation)

> **Sim goal:** Build the workflow *conductor* — a Behavior Tree that
> ticks the per-vial loop and calls each part's ROS 2 action/service —
> entirely in the Gazebo sim, then use the simulator's superpower,
> **fault injection**, to deliberately break grasps, decaps, barcodes,
> and fills and *prove the recovery branches actually fire*. Add a
> `/safety_stop` signal that halts the tree as a stand-in for a real
> e-stop, while being honest that sim cannot certify safety.

A **Behavior Tree** (BT) is a way of writing a robot's logic as a tree
of small tasks and decisions that the system "ticks" through over and
over, so it always knows what to do next and can react to each step's
success or failure. It is the natural home for the verification gates
from `07-perception-and-verification.md`: a gate that returns FAIL just
routes the tree down a recovery branch instead of to the next step.

Parts 02–07 each solve one slice (grip, decap, dispense, cap, label,
place, verify). None of them decides *when* to run, *in what order*, or
*what to do when one fails mid-batch*. That is this part — and it is the
piece that decides whether the cell is *trustworthy*, which matters most
in a regulated lab. The non-negotiable rule: **never silently continue
in a way that risks sample integrity.** A halted run is visible; a
corrupted sample reaching the instrument is not.

## What we can prove in simulation

- **The conductor sequences the whole loop.** The BT drives
  pick → scan → decap → dispense → cap → place for N worklist rows, one
  vial at a time, calling each part's mock-station service/action in
  order — proving the orchestration logic end to end.
- **Recovery branches actually fire (the headline).** Because we can
  *inject* failures on demand, we can prove every branch — retry→alert,
  quarantine, skip-and-log, stop — runs when its trigger occurs, instead
  of hoping it would in a rare real failure.
- **Bounded retries and escalation.** We can confirm a retry loop stops
  after its fixed limit and escalates (alert/pause/stop) rather than
  looping forever.
- **Repeatable batch statistics.** Run hundreds of simulated batches
  with a known failure rate and measure success rate, recovery rate, and
  where the tree gets stuck — a stress test no early hardware run could
  afford.
- **Safe-stop *logic*.** A `/safety_stop` event halts the tree
  mid-loop, holds state, and forces an explicit resume — we can prove
  the *software* reacts correctly.

Honest limits — what sim **cannot** prove:

- **It cannot certify safety.** A simulated `/safety_stop` is not a
  rated emergency stop, an interlock, or a force limit. Real safety needs
  certified hardware and a risk assessment. The myCobot 280 is a
  low-force desktop arm — *collaborative by nature*, which helps — but a
  real cell still needs proper e-stop, interlocks, and quite possibly an
  enclosure, and sim proves none of that.
- **It cannot prove real failure *rates*.** We inject the faults we
  imagine; the real world invents new ones. Sim proves the *response*,
  not the *frequency*.
- **Timing is optimistic.** Tree timing ignores real settling, station
  dwell, and human reaction in the recovery loop.

## Open-source tools

| Tool | Role | Bottom line |
|------|------|-------------|
| BehaviorTree.CPP | Authors and executes the Behavior Tree | Mature, widely used in ROS 2; the conductor itself. |
| Groot2 | Live-watch and edit the tree as it ticks | See which node is active and which branch a fault took. |
| py_trees / py_trees_ros | Python BT alternative | Fine if the team prefers Python; same idea, same gates. |
| ROS 2 actions / services | How the tree calls each part | Each step is an action/service the BT node ticks. |
| Fault-injection node (ours) | Deliberately fails a chosen step | The sim superpower; turns rare faults into on-demand tests. |
| `/safety_stop` topic + latched state | Stand-in for e-stop / interlock | Halts the tree; proves stop *logic*, not certified safety. |
| SQLite + FastAPI | Records every decision for the audit trail | Ties to Part 09; recovery choices must be logged. |
| RViz2 / Foxglove | Watch the cell and current state | Cross-check the tree against what the arm is doing. |

## How to simulate it now

This part assumes the world, arm, station mocks (Parts 01–05), and
verification-gate services (Part 07) already run.

**1. Author the BT XML.** Write a BehaviorTree.CPP tree that, per
worklist row, ticks the loop as a `Sequence`, with each verification
gate as a condition node:

```
Repeat (per worklist row)
└─ Sequence "process one vial"
   ├─ ReadWorklistRow
   ├─ Pick (vial_supply)            → [GATE: in gripper?]
   ├─ Scan (scan_station)           → [GATE: matches worklist?]
   ├─ Decap (decap_station)         → [GATE: open rim?]
   ├─ Dispense (dispense_station)   → [GATE: right level? no spill?]
   ├─ Cap (decap_station)           → [GATE: cap seated?]
   └─ Place (autosampler_tray N)    → [GATE: seated in correct slot?]
```

Each leaf is a ROS 2 action/service call into the relevant part's mock
station; each `[GATE]` is a Part 07 service returning PASS / FAIL /
UNSURE. A FAIL or UNSURE falls out of the sequence into a recovery
sub-tree (a `Fallback`) that picks the defined response.

**2. Encode the defined responses** (same policy as the high-level doc):

| Failure mode | Injected how (sim) | Recovery branch | Bottom line |
|---|---|---|---|
| Missed grip | grasp-fix plugin refuses to attach | Retry pick ~2–3×, then **alert** & pause | Cheap to retry; bound it |
| Spill / breakage | dispenser sets a spill flag | **Stop, flag, hold for human** | Liquid + glass = integrity + safety event |
| Barcode mismatch | scan mock returns wrong ID | **Quarantine** that vial; pause per policy | Never load an unidentified vial |
| Decap failure | station service leaves cap link on | Retry ~1–2×, else **skip-and-log**, alert | Don't force; don't fill a capped vial |
| Cap not seated | re-cap gate returns FAIL | Retry seat; else **flag**, don't place | Unsealed vial leaks/evaporates |
| Short / over fill | fill-volume scalar set off-target | **Flag vial**, don't place | Integrity gate, not retried blindly |
| Slot occupied | tray model pre-seeded full | **Pause & alert** | Don't stack; human resolves |
| Sensor UNSURE | gate returns UNSURE | Re-image once; else treat as FAIL | "Unsure" is not "pass" |

Cross-cutting: **quarantine, don't discard** (suspect vial goes to a
known quarantine frame and is logged); **bounded retries** (fixed limit,
then escalate).

**3. Implement a fault-injection node.** A ROS 2 node exposes parameters
and services that deliberately make a step fail — refuse the grasp-fix
attach, force the decap station to leave the cap link on, make the scan
mock return a mismatched ID, raise the spill flag, or set the fill-volume
scalar short. It can fire on a schedule, at random with a set
probability, or on command. This converts rare real faults into tests we
can run on demand.

**4. Run repeated sim batches.** Launch the world headless, run the BT
over a worklist of N vials with the fault-injector at a chosen failure
rate, and repeat for many batches. Record success rate, recovery rate,
quarantine count, and any deadlocks. This is the stress test that builds
confidence before hardware.

**5. Watch it in Groot2.** Connect Groot2 to the running tree to see in
real time which node is ticking and which recovery branch a given
injected fault took — the fastest way to confirm the logic, and a clear
artifact to show reviewers.

**6. Add the safe-stop.** Publish a `/safety_stop` topic with a latched
state. A high-priority node in the tree (a `ReactiveSequence` guard at
the root) checks it every tick; when set, the tree halts the current
safe sub-step, holds worklist state, and refuses to resume until an
explicit operator action clears it — proving the **no silent restart**
rule in software. (Again: this is logic only, not a certified stop.)

**7. Log every decision.** Every step result, retry, quarantine, pause,
and safe-stop is written to the SQLite/FastAPI audit trail in
`09-software-compliance-and-integration.md`. In a regulated lab the
recovery logic is only trustworthy if it is fully recorded, and
compliance rules constrain which auto-recovery is even allowed. **Every
sensor reading — not just decisions — is logged the same way**, so the
audit trail can later show *which sensor value* opened or blocked each
step.

### Safety & state sensors — the gates this part owns

The verification gates in Part 07 are camera-and-physical checks on the
*sample*. This part owns the other half of the
[unified sensor suite](sensor-suite.md): the **safety and machine-state
sensors** that gate the tree as plain boolean / state inputs, regardless
of which vial is in flight. The mental model is one line:

> **Sensor → gate.** *Every* step in the per-vial loop is opened or
> blocked by a sensor reading; the BT ticks that reading as a condition
> node, and a FAIL branches to **retry / quarantine / stop**. The safety
> sensors below sit *above* the loop — they can block any step.

| # | Sensor | BT input | Tripped → | Sim stand-in |
|---|--------|----------|-----------|--------------|
| 10 | **Safety light curtain / laser scanner** | `/light_curtain_clear` (bool) | Beam broken → **safe stop** | `/light_curtain_clear` topic |
| 11 | **Door interlock + e-stop** | `/door_closed`, `/estop` (bool) | Door open or e-stop pressed → **safe stop** | `/door_closed`, `/estop` topics |
| 12 | **Base IMU / tilt** | tilt within bound? (state) | Bench knocked / not level → **safe stop** | Gazebo `imu` sensor on the base link |
| 9 | **Homing / limit switches** | at-home / within-limits (state) | Not homed or at end-stop → **block motion** | Joint-limit / home state |

These fold into the same `/safety_stop` discipline from step 6: the
high-priority `ReactiveSequence` guard at the root checks the safety
inputs (#10, #11) **and** the tilt / limit state (#12, #9) every tick.
If `/light_curtain_clear` goes false, `/door_closed` goes false, `/estop`
latches, the IMU reports the bench out of level, or a joint sits past a
limit / the arm is not homed, the guard halts the current safe sub-step,
holds worklist state, and refuses to resume until an operator explicitly
clears it. The homing/limit state also gates *start-up*: the tree will
not begin a loop until the arm reports homed and within limits.

Two-witness applies here too: a tilt event from the **IMU (#12)** plus a
limit-switch trip (#9) is stronger evidence of a real knock than either
alone. As above, every safety reading and every stop is logged to the
audit trail (Part 09).

(Honesty, repeated: in sim these are topics and state checks — they
prove the *stop logic*, not a *certified* stop. See the limits above
and `10-hardware-platform-and-capital-model.md`.)

## Additional hardware needed

Beyond the arm and gripper, the real cell needs proper safety hardware:
a rated **emergency stop**, **interlocks** / **door sensors**, and
likely a guarded **enclosure** (the 280's low force helps, but does not
remove the need). In this part *none of that is bought*:

- e-stop / interlocks / door sensors → a single `/safety_stop` topic and
  latched state the tree watches;
- enclosure → not modelled; represented only by the stop signal.

The honest gap is large here: sim proves the cell *reacts* correctly to
a stop and *recovers* correctly from a fault, but a real cell's safety
must be designed, risk-assessed, and certified on hardware — see
`10-hardware-platform-and-capital-model.md`.

## How it connects

- **`02-vial-handling-and-gripping.md`** … **`07-perception-and-
  verification.md`** — the tree drives every one of these in order and
  reacts to their results; the Part 07 verification gates are the branch
  points in the tree.
- **`07-perception-and-verification.md`** — a failed gate is the primary
  trigger for the recovery branches above.
- **`09-software-compliance-and-integration.md`** — every sequencing
  decision, retry, quarantine, pause, safety stop, **and sensor
  reading** is logged to the audit trail; compliance constrains what
  auto-recovery may do.
- **[`sensor-suite.md`](sensor-suite.md)** — the canonical sensor list;
  this part is the home of the safety / state sensors #9–#12 and the
  *sensor → gate* model that drives the whole tree.
- Folder overview: [`README.md`](README.md).
