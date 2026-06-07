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

## Meta code

The shape of the best-practical per-vial Behavior Tree — the same tree
you would author in BehaviorTree.CPP's XML — whose condition nodes are
sensor gates that branch to retry / quarantine / stop on `Failure`:

```text
# the per-vial subtree, ticked top-to-bottom on a fixed heartbeat:
# Sequence "process one vial":
#     Condition  safe?   ← /light_curtain_clear AND /door_closed AND NOT /estop  (#10/#11)
#                          on FAILURE: stop the whole run                          (safe-stop)
#     Action     pick the vial                                                    (-> Layer 03)
#     Fallback "confirm held":                                                    (retry wrapper)
#         Condition  held?  ← gripper feedback (#4)                               (grasp success)
#         Action     re-pick once, then re-check held?                            (retry branch)
#         Action     quarantine this vial and move on                            (give-up branch)
#     Action     decap / dispense / recap / scan / place                         (-> lower layers)
# safe? is re-checked every tick, so it can pre-empt any running step
```

## Real code

A minimal but complete ROS 2 (`rclpy`) per-vial tree built with
**py_trees** — the pure-Python Behavior Tree library that expresses the
same best-practical tree you would later author in BehaviorTree.CPP.
This is **illustrative teaching code**: library and message names drift
between versions, so re-verify before relying on it. Every line carries
an inline comment.

```python
import rclpy                                    # ROS 2 Python client library (the robot framework)
from rclpy.node import Node                     # base class every ROS 2 program ("node") builds on
from std_msgs.msg import Bool                   # a true/false message: each safety topic publishes this
import py_trees                                  # the pure-Python Behavior Tree library (tree engine)


class SafeGate(py_trees.behaviour.Behaviour):    # CONDITION node: "is it safe to move right now?"
    def __init__(self, node):                    # built once, handed the ROS node so it can subscribe
        super().__init__("safe?")                # name this leaf "safe?" as it appears in the tree
        self.curtain = False                     # latest /light_curtain_clear reading (start unsafe)
        self.door = False                        # latest /door_closed reading (start unsafe)
        self.estop = True                        # latest /estop reading (start as "pressed" = unsafe)
        node.create_subscription(                # subscribe to the light curtain (sensor #10)
            Bool, "/light_curtain_clear",        # message type and topic name from the sensor suite
            lambda m: setattr(self, "curtain", m.data), 10)  # store every new reading on self.curtain
        node.create_subscription(                # subscribe to the door interlock (sensor #11)
            Bool, "/door_closed",                # message type and topic name from the sensor suite
            lambda m: setattr(self, "door", m.data), 10)     # store every new reading on self.door
        node.create_subscription(                # subscribe to the emergency stop (sensor #11)
            Bool, "/estop",                      # message type and topic name from the sensor suite
            lambda m: setattr(self, "estop", m.data), 10)    # store every new reading on self.estop

    def update(self):                            # runs on every tick; returns Success or Failure
        safe = self.curtain and self.door and not self.estop  # two-witness AND: all three must agree
        if safe:                                  # is the work zone clear, door shut, e-stop released?
            return py_trees.common.Status.SUCCESS  # yes -> let the sequence proceed to the next step
        return py_trees.common.Status.FAILURE     # no -> FAIL pre-empts the run (safe-stop branch)


class HeldGate(py_trees.behaviour.Behaviour):    # CONDITION node: "is the vial actually in the grip?"
    def __init__(self, node):                    # built once, handed the ROS node so it can subscribe
        super().__init__("held?")                # name this leaf "held?" as it appears in the tree
        self.held = False                        # latest grasp-success reading (start: nothing held)
        node.create_subscription(                # subscribe to gripper feedback (sensor #4)
            Bool, "/gripper/holding",            # message type and topic the grasp layer publishes
            lambda m: setattr(self, "held", m.data), 10)     # store every new reading on self.held

    def update(self):                            # runs on every tick; returns Success or Failure
        if self.held:                             # does the gripper report a vial is held?
            return py_trees.common.Status.SUCCESS  # yes -> grasp confirmed, sequence continues
        return py_trees.common.Status.FAILURE     # no -> FAIL drops into the retry / quarantine branch


def make_vial_tree(node):                         # assemble the per-vial subtree from the gates above
    safe = SafeGate(node)                        # the safety condition, re-ticked every heartbeat
    held = HeldGate(node)                        # the grasp-success condition for the pick step
    retry = py_trees.decorators.Retry(           # wrap "held?" so a failed pick is retried, not fatal
        name="retry pick", child=held, num_failures=2)  # allow up to 2 re-picks before giving up
    root = py_trees.composites.Sequence(         # a Sequence: every child must succeed, left to right
        name="process one vial", memory=True)    # memory=True resumes where it left off between ticks
    root.add_children([safe, retry])             # gate on safety first, then confirm (and retry) the grasp
    return py_trees.trees.BehaviourTree(root)    # wrap the root in a ticking tree the engine drives


class OrchestratorNode(Node):                      # the ROS 2 node that owns and ticks the tree
    def __init__(self):                            # set-up that runs once, when the node is created
        super().__init__("orchestrator")          # register on the ROS 2 graph as "orchestrator"
        self.tree = make_vial_tree(self)          # build the per-vial Behavior Tree, wired to our topics
        self.create_timer(0.5, self.tick)         # tick the tree on a fixed 0.5 s heartbeat (2 Hz)

    def tick(self):                               # called by the timer; advances the tree one tick
        self.tree.tick()                          # evaluate the whole tree once, top-to-bottom
        status = self.tree.root.status            # read what the root returned on this tick
        self.get_logger().info(f"tree -> {status}")  # print the result so the run is watchable


def main():                                        # the standard ROS 2 program entry point
    rclpy.init()                                    # start up the ROS 2 client library (must come first)
    node = OrchestratorNode()                       # build our node, which builds and starts the tree
    rclpy.spin(node)                                # keep ticking until you press Ctrl-C
    node.destroy_node()                             # remove the node from the graph on shutdown
    rclpy.shutdown()                                # close the ROS 2 client library cleanly


if __name__ == "__main__":                          # only run if this file is launched directly
    main()                                          # ...then start everything above
```

Each condition node above is one **sensor → gate** from the canonical
map in [`../sensor-suite.md`](../sensor-suite.md): `safe?` fuses the
safety topics (#10/#11) and `held?` reads gripper feedback (#4). In
only-code mode those topics come from mock publishers, so you can
**inject faults** — drop `/light_curtain_clear` to `false`, or fake a
slipped grip — and watch the tree fall into its safe-stop, retry, and
quarantine branches with no bench time.

## See also

- Folder overview: [`README.md`](README.md)
- Sibling mode (real arm + peripherals in the loop):
  [`../02-code-plus-hardware/07-orchestration-and-task-logic.md`](../02-code-plus-hardware/07-orchestration-and-task-logic.md)
- [`../foundation-models.md`](../foundation-models.md) — a VLA (and
  especially **Gemini Robotics-ER** as a high-level planner) can take
  over parts of this task-logic layer; the learned alternative to a
  hand-built behavior tree.
