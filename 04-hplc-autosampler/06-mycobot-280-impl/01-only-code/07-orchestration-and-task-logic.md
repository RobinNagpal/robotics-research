# Layer 07 — Orchestration & task logic (only-code)

> **Job:** Sequence the per-vial **prep → load** routine — pick a
> vial, decap, dispense, recap, scan, place it in the tray, repeat —
> and decide what happens when a step fails, all driven against
> *mock* station services inside the simulator.
>
> **Mode — only code.** No real arm or instruments. The orchestrator
> drives **mock services** (software stand-ins that fake the decapper,
> dispenser, scanner, and gripper) and we deliberately **inject faults**
> into those mocks to prove every recovery branch in software alone.

This layer is the "brain" that sits above motion planning, perception,
and grasping. It does not move joints or read cameras itself; it calls
the lower layers in the right order and reacts to their results. The
five candidates below are **task-logic frameworks** — libraries for
expressing "do this, then that; if this fails, do that instead" as a
structured, inspectable program rather than a tangle of `if`/`else`.

Two recurring bits of jargon. A **finite-state machine (FSM)** is a
model where the system is always in exactly one named *state* (e.g.
`DECAPPING`) and moves to another state on a defined *transition* (e.g.
`decap_ok → DISPENSING`). A **Behavior Tree (BT)** is a tree of tasks
that is re-evaluated top-to-bottom on a fixed heartbeat; each
re-evaluation is called a **tick**. On every tick a node returns
`Success`, `Failure`, or `Running`, and parent nodes (sequences,
fallbacks) combine those results to decide what runs next. BTs tend to
be more **reactive** (easy to abort and retry) and **composable**
(small subtrees snap together) than hand-written FSMs.

Because this is the only-code mode, the deciding factor is how easily a
framework lets us **swap real devices for mocks** and **force failures
on demand** — a scanner that returns "no read," a grip that reports
slip — so that the recovery logic is exercised without any bench time.

Whichever framework wins, the tree (or state machine) is **gated by
sensor topics**, exactly as it will be on hardware. The model is
uniform: each step is a **sensor → gate; FAIL → retry / quarantine /
stop**. Safety gates read the mock topics `/light_curtain_clear`,
`/door_closed`, and `/estop` (sensors #10/#11) and can pre-empt any
running motion; a base-IMU tilt check (#12) and the limit/home state
(#9) guard that the cell is level and the arm is where it claims; and
the perception (Layer 04) and grasp-success (Layer 05) gates feed in as
ordinary condition nodes. In sim these topics come from Gazebo plugins
and mock publishers, so the whole gate structure can be exercised — and
fault-injected — with no bench time. The canonical sensor → gate map is
in [`../sensor-suite.md`](../sensor-suite.md).

## The five at a glance

| Framework | Role | Tier | One-liner |
|-----------|------|------|-----------|
| BehaviorTree.CPP (+ Groot2) | C++ Behavior Tree engine + live editor/monitor | `Best-in-class` | Fast, reactive, composable; Groot2 shows ticks live. Used by Nav2. |
| py_trees / py_trees_ros | Pure-Python Behavior Tree library | `Cheapest` | Free, `pip`-installable, easiest to script and fault-inject. |
| BehaviorTree.CPP | Same engine, judged as the pragmatic default | `Best-practical` | Mature, well-documented, ROS 2-ready; the safe long-term bet. |
| YASMIN | ROS 2 finite-state machine library | `Alternative` | Clean modern FSM for ROS 2; less reactive than a BT. |
| FlexBE | Hierarchical FSM + operator GUI | `Alternative` | Great when a human supervises/steps the flow; heavier. |
| SMACH | Classic ROS 1 finite-state machine | `Alternative` | Legacy; ROS 1 only — off the table for new work. |

(The table lists six rows because BehaviorTree.CPP earns both the
best-in-class and best-practical calls; the *five distinct frameworks*
are BehaviorTree.CPP, py_trees, YASMIN, FlexBE, and SMACH.)

## BehaviorTree.CPP (+ Groot2)

BehaviorTree.CPP is a C++ library for building and running Behavior
Trees. You describe the tree in an XML file — sequences, fallbacks, and
your own leaf nodes ("pick vial," "decap," "scan") — and the engine
ticks it. **Groot2** is its companion desktop tool: a visual editor for
drawing the tree and, crucially, a **live monitor** that highlights
which node is ticking, which returned `Success`, and which is `Running`,
in real time as the sim runs. It is the same engine the ROS 2 Nav2
navigation stack uses for its own task logic, so it is battle-tested at
scale.

How it's good here: in the only-code loop, Groot2's live view turns the
mock-driven run into something you can *watch* — when you inject a
"scanner no-read" fault into the mock, you literally see the tree fall
out of the happy-path sequence into the retry fallback. The engine is
**reactive** (a higher-priority branch can pre-empt a running one on the
next tick, so a safe-stop condition aborts the prep mid-step cleanly)
and **composable** (the per-vial subtree is written once and reused for
every vial). Trees are data (XML), so fault scenarios can be assembled
and replayed without recompiling.

How it's bad versus the other four: it is **C++**, so the
write-compile-run loop is slower and less beginner-friendly than
**py_trees'** pure Python — for a sim-only project where you are
constantly editing logic and injecting faults, that friction is real.
Its model is also a Behavior Tree, not an FSM, so if your problem is
genuinely a handful of named states with rare transitions, **YASMIN**
or **FlexBE** can read more naturally than nested ticks. And unlike
**FlexBE** it has no built-in operator GUI for a human to step the flow;
Groot2 monitors and edits, but it is not an in-the-loop supervision
console.

## py_trees / py_trees_ros

py_trees is a pure-Python Behavior Tree library; `py_trees_ros` is the
thin layer that wires it into ROS 2 (publishing the tree's state,
wrapping ROS actions/services as leaves). It installs with `pip`, has no
compiler, and lets you build a tree in a few dozen lines of readable
Python. The same tick/`Success`/`Failure`/`Running` semantics as
BehaviorTree.CPP apply — it is the same idea, expressed in Python.

How it's good here: it is the **cheapest and most frictionless** option
for the only-code mode. Because the whole tree and all the mock services
are Python, **fault injection is trivial** — a mock decapper is just a
function you can make raise an exception, return `Failure`, or sleep to
fake a timeout, and you edit-and-rerun in seconds with no build step.
For rapidly drafting the prep → load logic and hammering its recovery
branches against mocks, nothing here is faster to iterate.

How it's bad versus the other four: pure Python is **slower** and less
suited to tight real-time loops than **BehaviorTree.CPP** — invisible in
sim, but a ceiling if the same tree later runs on hardware. Its live
introspection (`py_trees_ros` viewers, `rqt` plugins) is **less polished
than Groot2's** editor/monitor. It is also a smaller, lighter-governed
ecosystem than the Nav2-backed BehaviorTree.CPP, and being a BT it
shares the "why not just an FSM" critique that **YASMIN** and
**FlexBE** can answer for simple state-based flows.

## YASMIN

YASMIN ("Yet Another State MachINe") is a modern finite-state-machine
library for ROS 2, available in both C++ and Python. You define named
states and the transitions between them; each state does its work and
returns an outcome string that selects the next state. It is, in spirit,
the contemporary ROS 2 answer to the old SMACH — a clean FSM toolkit
that targets current middleware rather than legacy ROS 1.

How it's good here: when the prep → load routine is framed as explicit
stages — `PICK → DECAP → DISPENSE → RECAP → SCAN → PLACE` — an FSM is a
very **legible** way to write it, and YASMIN keeps states small and
testable. Against mocks it is straightforward: each state calls a mock
service and branches on the returned outcome, and YASMIN ships a viewer
to watch the active state. For a team that thinks in states rather than
trees, it is a clean, modern, ROS 2-native fit.

How it's bad versus the other four: a plain FSM is **less reactive** than
a Behavior Tree. Cross-cutting concerns — "abort to safe-stop from *any*
state," "retry up to three times" — must be wired as explicit
transitions out of every state, which a BT expresses once as a
higher-priority branch. So compared with **BehaviorTree.CPP** and
**py_trees**, recovery logic tends to sprawl as states multiply. Its
tooling is also lighter than **Groot2** or **FlexBE's** operator GUI,
and its community is smaller than the Nav2-scale BT ecosystem.

## FlexBE

FlexBE (the Flexible Behavior Engine) is a **hierarchical** FSM
framework — states can nest inside higher-level states — bundled with a
real-time **operator GUI**. Its standout feature is human-in-the-loop
supervision: an operator can watch the state machine run, pause it,
step it state-by-state, or hand control between "autonomy levels," all
from the GUI. It has a ROS 2 line and is widely used where a person
oversees a long, partly-manual procedure.

How it's good here: even in sim, the FlexBE GUI is a pleasant way to
**drive and observe** the prep → load flow by hand — step into the
`DISPENSE` state, confirm the mock behaved, step on. For demos and for
designing the operator experience the eventual hardware cell will need,
that supervision console is something none of the BT tools provide out
of the box. Hierarchy also keeps a long laboratory procedure organised.

How it's bad versus the other four: for *autonomous, headless*
fault-injection testing — the heart of the only-code mode — FlexBE's
operator focus is **weight you don't need**, and it is heavier to set up
than `pip install py_trees`. As an FSM it carries the same
reactivity limits as **YASMIN** versus a Behavior Tree. And its
human-in-the-loop strength is largely wasted while there is no hardware
and no operator — it earns its keep later, in the hardware mode, not
here.

## SMACH

SMACH is the classic ROS **finite-state-machine** library — for years
the default way to script task logic in ROS 1. It offers nested
("container") state machines, concurrence, and an introspection viewer
(`smach_viewer`). A great deal of older robotics tutorial material and
many legacy lab systems are built on it, so it is worth recognising.

How it's good here: conceptually it is sound and familiar, and its
container/concurrent-state patterns directly influenced newer tools.
If you are reading or porting **existing ROS 1 lab code**, knowing SMACH
helps you understand what that code is doing before you rewrite it.

How it's bad versus the other four: it is **ROS 1 only**, and ROS 1 is
end-of-life — which makes SMACH a non-starter for new only-code work
that should target ROS 2 from day one. Everything it does, **YASMIN**
does on modern middleware, and its reactivity limits are the same FSM
limits that **BehaviorTree.CPP** and **py_trees** avoid. Its tooling
predates **Groot2** and **FlexBE's** GUIs. We list it only so the
lineage is clear; it should not be chosen for this project.

## Verdict

- **Best-in-class — BehaviorTree.CPP (+ Groot2).** The most capable,
  reactive, composable engine, proven at Nav2 scale, with a live
  Groot2 monitor that makes mock-driven, fault-injected sim runs
  visible as they happen. The strongest foundation even before
  hardware exists.
- **Cheapest — py_trees / py_trees_ros.** Free, `pip`-installable,
  pure Python; the fastest thing to script and to fault-inject against
  mocks, at the cost of raw speed and Groot2-grade tooling.
- **Best-practical — BehaviorTree.CPP.** The same mature, well-documented,
  ROS 2-ready engine taken as the default: it balances power, tooling,
  and longevity, and the only-code tree you build with it carries over
  unchanged to the hardware mode. (Reach for py_trees when speed of
  iteration matters more than runtime performance.)

## Realistic scenario & use cases

> **Why this matters for automation.** Orchestration is the cell's brain:
> it turns ten capable-but-dumb layers into a loop that runs **96 vials
> unattended overnight** and, crucially, **does the right thing when
> something goes wrong**. Its automation value is exactly the part a human
> operator provides today — sequencing, judgement, and recovery — so the
> bench can be left alone.

**The scenario.** A 96-vial worklist runs overnight. Partway through,
vial 53's **barcode mismatches** the worklist (Layer 06), vial 61's grasp
**slips twice** (Layer 05), an **e-stop fires** during vial 70's transfer,
the dispenser **times out** on vial 78 (Layer 02), and a **power blip**
reboots the controller after vial 84. By morning the tray must be
correctly loaded with only verified vials, every exception logged, and the
two genuinely bad vials flagged — not a crashed cell at vial 53.

The layer must therefore serve several **distinct use cases**:

1. **Drive the per-vial loop deterministically.** Run
   perceive → pick → decap → dispense → recap → scan → place for each
   worklist row, in order, 96 times.
   - *How the solution handles it:* a **behavior tree** iterates a per-vial
     subtree over the worklist; `Sequence` nodes enforce the order and
     each step only runs if the prior one succeeded.

2. **React to a verification failure.** Halt the *affected* vial on a
   barcode mismatch or failed fill-check, flag it, and carry on with the
   rest of the tray.
   - *How:* **condition nodes** gate each action; a failed identity check
     routes that vial to a "quarantine + log" branch instead of the place
     action, while the loop continues — vial 53 is isolated, not fatal.

3. **Bounded retry then escalate.** A slip or no-read retries a few times,
   then skips-and-flags rather than looping forever.
   - *How:* a **retry decorator** with a hard cap wraps the fragile step;
     on exhaustion a fallback branch parks the vial for human review (vial
     61).

4. **Safe-stop and resume.** An e-stop or open door mid-motion must halt
   safely; clearing it resumes from the current vial.
   - *How:* a high-priority **reactive guard** subtree watches `/estop` and
     the Layer 10 gates and preempts everything below; when the gate
     reopens the tree resumes ticking (vial 70).

5. **Crash / power-blip recovery with durable state.** After a reboot,
   resume at the right worklist row and never double-place.
   - *How:* worklist progress is **persisted** (Layer 08); on boot the cell
     reconciles the *actual* tray and gripper state via perception before
     resuming, so vial 84 isn't placed twice or skipped.

**Where the pick flexes.** BehaviorTree.CPP (best-practical) covers all
five, and its **Groot2** monitor makes the overnight run — including every
injected fault above — visible as it happens. When the priority is *speed
of iterating* the tree against mocks rather than runtime performance,
**py_trees** is the lighter pure-Python swap; the tree's logic is the same
either way.

## Deep dive: the three highest-value use cases

The five above all matter; these three carry the most weight for
orchestration — the cell's conscience for the overnight run.

## React to a verification failure (quarantine)

- **The moment:** vial 53's barcode mismatches; the loop must isolate it
  and keep going, not crash the run or place a wrong vial.
- **How, in depth:** **condition nodes** gate each action, so a failed
  identity or fill check routes that vial to a "quarantine + log" branch
  instead of the place action, while the per-vial subtree continues to
  vial 54.
- **Edge case it survives:** several failures in one tray — each is
  quarantined independently, so a bad batch yields a list of flagged vials
  and a still-valid run for the good ones.
- **Walkthrough:** (1) run the verify condition node; (2) on failure branch
  to quarantine-and-log; (3) skip the place for that vial; (4) tick on to
  the next worklist row.
- **In the scene:** vial 53 fails its check and, instead of the run
  grinding to a halt, the behaviour tree quietly routes it to a "set aside
  and log" branch and moves straight on to vial 54 — the night's work flows
  around the one bad apple.
- **Why it's done this way:** in a 96-vial run one bad vial is normal; if
  a single failure aborted the whole tray the cell would rarely finish a
  run, so isolating the bad vial and continuing is what makes overnight
  throughput real.
- **In the full loop:** this is the loop's response to any Layer-04/06/10
  failure on a vial — it decides per-vial pass-or-quarantine and keeps the
  worklist advancing, the control flow that turns ten capable layers into
  one resilient run.
- **Value:** one bad vial costs one slot, not the night.

### Meta code

The shape of the place-or-quarantine subtree, before any library detail:

```text
# Selector "place-or-quarantine" (first child to succeed wins):
#     Sequence "verified place" (all must pass):
#         Condition  identity OK?   ← Layer 06 verdict == PLACE
#         Condition  fill OK?       ← Layer 10 fill gate
#         Action     place the vial in its slot                    (-> Layer 03)
#     Sequence "quarantine" (runs only if the verified place failed):
#         Action     move the vial to the reject tray
#         Action     log an audit event {vial, reason}             (-> Layer 08)
# the outer loop iterates this subtree over every worklist row
```

### Real code

A **py_trees** place-or-quarantine subtree (the pure-Python pick; the same
shape as BehaviorTree.CPP's XML). **Illustrative teaching code** —
re-verify before use; every line is commented.

```python
import py_trees                                          # the behavior-tree library (pure Python)


class IdentityOK(py_trees.behaviour.Behaviour):         # condition: did the vial pass identity?
    def __init__(self, bb):                             # share a blackboard with the rest of the tree
        super().__init__("identity OK"); self.bb = bb   # name the node + keep the blackboard
    def update(self):                                   # ticked each cycle
        return (py_trees.common.Status.SUCCESS          # SUCCESS if Layer 06 said PLACE...
                if self.bb.get("identity") == "PLACE"   # ...for the current vial
                else py_trees.common.Status.FAILURE)    # else FAILURE -> routes to quarantine


class Place(py_trees.behaviour.Behaviour):              # action: place the vial in its slot
    def update(self):                                   # (calls Layer 03 in a real build)
        return py_trees.common.Status.SUCCESS           # assume the place succeeds in sim


class Quarantine(py_trees.behaviour.Behaviour):         # action: set the vial aside + audit it
    def __init__(self, bb):                             # share the blackboard
        super().__init__("quarantine"); self.bb = bb    # name the node + keep the blackboard
    def update(self):                                   # move to the reject tray + log the reason
        self.bb.set("audit", f"QUARANTINE {self.bb.get('vial')}")  # write a Layer-08 audit event
        return py_trees.common.Status.SUCCESS           # quarantining always "succeeds"


def per_vial_subtree(bb):                               # build the place-or-quarantine subtree
    verified = py_trees.composites.Sequence("verified place", memory=True)  # all children must pass
    verified.add_children([IdentityOK(bb), Place()])    # identity OK? then place
    root = py_trees.composites.Selector("place-or-quarantine", memory=False)  # first success wins
    root.add_children([verified, Quarantine(bb)])       # try the verified place, else quarantine
    return root                                         # the per-vial subtree the loop iterates
```

## Safe-stop and resume

- **The moment:** an e-stop fires or a door opens during vial 70's
  transfer; the arm must halt safely and resume cleanly once cleared.
- **How, in depth:** a high-priority **reactive guard** subtree watches
  `/estop` and the Layer 10 gates and preempts everything below; when the
  gate reopens the tree resumes ticking from where it paused.
- **Edge case it survives:** an e-stop *mid-grasp* — because steps are
  designed idempotent, the resume re-checks whether the vial is held and
  either completes or re-picks, never dropping or double-placing.
- **Walkthrough:** (1) the reactive guard sees `/estop`; (2) it preempts
  the running subtree; (3) the arm holds safely; (4) on clear, the tree
  re-checks state and resumes from where it paused.
- **In the scene:** a hand breaks the light curtain mid-move; a guard
  branch high in the tree instantly overrides everything below and the arm
  holds. When the curtain clears, the tree re-checks where it was and
  resumes the very vial it paused on.
- **Why it's done this way:** people will reach into a shared cell and
  safety must always win instantly; but if every safety trip meant
  scrapping the tray the cell would be unusable, so a clean
  pause-and-resume keeps it both safe and practical.
- **In the full loop:** this wraps the entire per-vial loop in a safety
  envelope — any motion from Layers 03/05 can be preempted here on a
  Layer-10 safety gate and then resumed, so safety overrides the loop
  without ending it.
- **Value:** a safety event is a pause, not a ruined tray and a manual
  reset.

### Meta code

The shape of the reactive safety guard, before any library detail:

```text
# Sequence "guarded run" (re-ticked every heartbeat, memory=False):
#     Condition  safe?  ← /light_curtain_clear AND /door_closed AND NOT /estop
#                          FAILURE -> children below STOP immediately            (safe-stop)
#     Subtree    the per-vial loop                                               (ticks only while safe)
# because the guard is re-evaluated each tick, an e-stop preempts instantly;
# when it clears, the guarded subtree resumes from where it paused (idempotent steps)
```

### Real code

A **py_trees** reactive guard that gates the whole loop on safety.
**Illustrative teaching code** — re-verify before use; every line is
commented.

```python
import py_trees                                          # the behavior-tree library


class Safe(py_trees.behaviour.Behaviour):               # reactive condition: is it safe to move?
    def __init__(self, bb):                             # read the latched safety bits...
        super().__init__("safe?"); self.bb = bb         # ...from a shared blackboard
    def update(self):                                   # re-evaluated on EVERY tick (reactive)
        ok = (self.bb.get("curtain_clear") and          # light curtain clear AND...
              self.bb.get("door_closed") and            # ...door closed AND...
              not self.bb.get("estop"))                 # ...e-stop not pressed
        return (py_trees.common.Status.SUCCESS if ok    # SUCCESS lets the loop below tick...
                else py_trees.common.Status.FAILURE)    # FAILURE preempts everything below


def guarded_loop(loop_subtree, bb):                     # wrap the per-vial loop in a safety guard
    root = py_trees.composites.Sequence("guarded run", memory=False)  # memory=False re-ticks the guard
    root.add_children([Safe(bb), loop_subtree])         # Safe must pass before the loop ticks
    return root                                         # an unsafe state instantly halts the loop


if __name__ == "__main__":                              # demo: tick the guarded tree
    bb = py_trees.blackboard.Client(name="cell")        # a shared blackboard for the safety bits
    for key in ("curtain_clear", "door_closed", "estop"):  # the keys a sensor bridge writes...
        bb.register_key(key, access=py_trees.common.Access.READ)  # ...from the safety topics
    loop = py_trees.behaviours.Running(name="per-vial loop")  # stand-in for the real loop subtree
    py_trees.trees.BehaviourTree(guarded_loop(loop, bb)).tick()  # one tick: the guard gates the loop
```

## Crash/power-blip recovery with durable state

- **The moment:** a power blip reboots the controller after vial 84; on
  restart the cell must resume at vial 85, not redo 1–84.
- **How, in depth:** worklist progress is **persisted** (Layer 08); on boot
  the cell reconciles the *actual* tray and gripper state via perception
  before resuming, so it trusts reality over its last intention.
- **Edge case it survives:** a crash *during* a place — reconciliation sees
  the vial already in the slot and advances, avoiding a double-place into
  an occupied nest.
- **Walkthrough:** (1) on boot read the persisted worklist progress; (2)
  perceive the actual tray and gripper; (3) reconcile intent against
  reality; (4) resume at the correct next vial without double-placing.
- **In the scene:** the lab wakes to find the cell rebooted overnight after
  a power blip — yet the tray is correct. On restart it read its own saved
  place, looked at the real tray to confirm, and carried on from vial 85
  rather than starting the night over.
- **Why it's done this way:** unattended means no one is there to restart
  it after a power blip; without durable state and reconciliation a hiccup
  would silently corrupt the tray, so resuming from verified reality is
  what lets the lab trust an unwatched run.
- **In the full loop:** this spans whole runs — it ties the persisted
  state from Layer 08 to the live tray via Layer 04, so the loop can be
  interrupted at any vial and still finish the tray correctly.
- **Value:** an unattended run survives an infrastructure hiccup instead of
  silently corrupting the tray.

### Meta code

The shape of the crash-safe resume, before any library detail:

```text
# after every vial: atomically persist {placed:[slots], next:row} to disk   (Layer 08)
# on boot:
#     read the persisted progress (or start fresh if none)
#     perceive the ACTUAL tray (filled slots) + gripper (holding a vial?)
#     reconcile intent vs reality:
#         "placed" + perception confirms filled -> done, skip
#         "placed" but perception sees empty    -> redo that vial
#         gripper holding a vial                 -> finish placing it first
#     resume the worklist at the first not-yet-done row                       (never double-place)
```

### Real code

A crash-safe progress store and a boot-time reconcile that trusts reality
over intention. **Illustrative teaching code** — re-verify before use;
every line is commented.

```python
import json                                              # the durable progress file format
import os                                                # for the atomic replace + existence check

PROGRESS = "progress.json"                              # {"placed": [slots], "next": row_index}


def save_progress(placed, next_row):                    # called after every vial (durable state)
    tmp = PROGRESS + ".tmp"                              # write to a temp file first...
    with open(tmp, "w") as fh:                           # ...so a crash never leaves a half file
        json.dump({"placed": sorted(placed), "next": next_row}, fh)  # the progress snapshot
    os.replace(tmp, PROGRESS)                            # atomic rename = crash-safe commit


def recover(worklist, tray_filled, gripper_has_vial):   # reconcile saved state with reality on boot
    if not os.path.exists(PROGRESS):                     # first run, nothing to recover?
        return 0, set()                                  # start at row 0 with nothing placed
    with open(PROGRESS) as fh:                           # load what we believed before the crash
        saved = json.load(fh)                            # {"placed": [...], "next": i}
    placed = set(saved["placed"])                        # slots we thought were filled
    for slot in list(placed):                            # trust reality over intention...
        if slot not in tray_filled:                      # logged placed, but the slot is actually empty
            placed.discard(slot)                         # -> it wasn't really placed; redo it
    if gripper_has_vial:                                 # crashed mid-place, vial still in hand?
        return saved["next"], placed                     # resume by finishing that very vial
    for i, row in enumerate(worklist):                   # else scan the worklist in order...
        if row["slot"] not in placed:                    # first slot not confirmed placed
            return i, placed                              # -> resume here, no double-placing
    return len(worklist), placed                         # everything done: nothing left to do
```

## See also

- Folder overview: [`README.md`](README.md)
- Sibling mode (real arm + peripherals in the loop):
  [`../02-code-plus-hardware/07-orchestration-and-task-logic.md`](../02-code-plus-hardware/07-orchestration-and-task-logic.md)
- [`../foundation-models.md`](../foundation-models.md) — a VLA (and
  especially **Gemini Robotics-ER** as a high-level planner) can take
  over parts of this task-logic layer; the learned alternative to a
  hand-built behavior tree.
