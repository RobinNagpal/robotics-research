# Layer 07 — Orchestration & task logic (code-plus-hardware)

> **Job:** Sequence the per-vial **prep → load** routine — pick, decap,
> dispense, recap, scan, place — and handle failures and safe-stop, now
> driving the **real myCobot 280 and real peripherals** instead of mocks.
>
> **Mode — code plus hardware.** The decapper, dispenser, barcode
> scanner, and gripper are physical devices that really fail; an **e-stop**
> (a hardware emergency-stop circuit that cuts motion) is wired in; and
> every decision must be recorded for the audit trail. The headline
> payoff: **the task-logic itself is unchanged from sim.**

This layer is the same "brain" as in the only-code mode — it calls
motion planning, perception, and grasping in order and reacts to
results — but hardware changes *what it must cope with*, not its shape.
The five candidates are identical to the sim mode; what differs is how
each one integrates a real safe-stop, how well it logs every decision,
and how it copes with **real failure modes** the mocks only pretended to
have.

Jargon, briefly. A **finite-state machine (FSM)** is always in one named
*state* and moves to another on a defined *transition*. A **Behavior
Tree (BT)** is a tree of tasks re-evaluated on a fixed heartbeat; each
re-evaluation is a **tick**, and each node returns `Success`, `Failure`,
or `Running`. The key hardware concept is **safe-stop**: bringing the
arm to a controlled, harmless halt (and honouring the hardware e-stop)
the instant anything is wrong — a person in the cell, a dropped vial, a
device timeout.

On hardware the tree is **gated by real safety and state sensors** (see
[`../sensor-suite.md`](../sensor-suite.md)), not by mock topics: the
safety light curtain / laser scanner (**#10**) and the door interlock +
e-stop (**#11**) feed the top-priority safe-stop branch; the base IMU /
tilt (**#12**) flags a knocked bench; and the homing / limit switches
(**#9**) confirm the arm and any rail/turntable are where the logic
assumes. These fuse with the perception and grasp gates (Layers 04–05) in
the same pattern throughout — **sensor → gate; FAIL → retry / quarantine
/ safe-stop.** One caveat the BT cannot wave away: a **safety-rated**
light curtain or interlock often needs safety-rated wiring and a
hardware/safety-PLC stop path, *not* just a ROS 2 topic the tree reads —
the topic mirrors the state for the logic, but the certified stop must
exist below the software.

What changes once hardware is real, in one paragraph: (1) **safe-stop
becomes a top-priority branch** that can pre-empt any step on the next
tick and must also react to the physical e-stop line; (2) **every tick
and decision is logged** to the audit trail — see Layer 08
([`08-software-worklist-and-compliance.md`](08-software-worklist-and-compliance.md))
— so a regulator can reconstruct exactly what the cell did to each vial;
and (3) **failures are real and varied** — a **missed grip** (the
gripper closes but the vial slipped or was never there) and a **scanner
no-read** (the barcode camera returns nothing) are the two most common,
and the tree must detect and recover from both. The tree *logic* you
proved in sim does not change — only the leaves now call real drivers,
and the recovery branches you already tested now fire for real reasons.

## The five at a glance

| Framework | Role | Tier | One-liner |
|-----------|------|------|-----------|
| BehaviorTree.CPP (+ Groot2) | C++ Behavior Tree engine + live editor/monitor | `Best-in-class` | Reactive safe-stop branch + live Groot2 monitor on the real cell. Used by Nav2. |
| py_trees / py_trees_ros | Pure-Python Behavior Tree library | `Cheapest` | Free, easy; same tree as sim, but Python is the weak link for real-time. |
| BehaviorTree.CPP | Same engine, judged as the pragmatic default | `Best-practical` | Mature, ROS 2-ready, audit-loggable; safest long-term bet on hardware. |
| YASMIN | ROS 2 finite-state machine library | `Alternative` | Clean ROS 2 FSM; safe-stop must be wired into every state. |
| FlexBE | Hierarchical FSM + operator GUI | `Alternative` | Operator GUI shines now — a human can supervise the real cell. |
| SMACH | Classic ROS 1 finite-state machine | `Alternative` | Legacy; ROS 1 only — off the table for new hardware work. |

(Six rows because BehaviorTree.CPP earns both the best-in-class and
best-practical calls; the *five distinct frameworks* are
BehaviorTree.CPP, py_trees, YASMIN, FlexBE, and SMACH.)

## BehaviorTree.CPP (+ Groot2)

BehaviorTree.CPP is a C++ Behavior Tree engine: you describe sequences,
fallbacks, and custom leaves ("pick vial," "decap," "scan") in XML and
the engine ticks them. **Groot2** is its editor and **live monitor**,
highlighting which node is ticking and what it returned in real time. It
is the engine behind ROS 2 Nav2, so it is proven on real robots, not
just in simulation.

How it's good on hardware: its **reactivity** is exactly what a safe-stop
needs. A high-priority condition node — "is the e-stop pressed? is a
person detected? did a device time out?" — sits above the prep sequence,
and because the tree is re-ticked continuously, that branch **pre-empts a
running step on the very next tick** and routes the arm to a controlled
halt. Real failure modes map cleanly onto node results: a **missed grip**
makes the grasp leaf return `Failure`, dropping into a re-grasp fallback;
a **scanner no-read** does the same into a re-scan-then-quarantine
branch. And because every tick already flows through the engine, it is a
natural place to **emit an audit record per decision** — node, result,
timestamp, vial ID — feeding Layer 08; Groot2 lets you *watch* the real
cell make those decisions live.

How it's bad versus the other four: it is **C++**, so iterating on logic
at the bench is slower than **py_trees'** Python — though on hardware
the C++ runtime performance is an asset, not a cost. Being a BT, it is
arguably overkill if your real procedure truly is a few states with rare
transitions, where **YASMIN's** FSM reads more directly. And it lacks a
built-in human-supervision console: Groot2 monitors and edits, but for
an operator who must *step* a real, partly-manual lab procedure,
**FlexBE's** GUI is purpose-built and BehaviorTree.CPP is not.

## py_trees / py_trees_ros

py_trees is a pure-Python Behavior Tree library; `py_trees_ros` bridges
it to ROS 2, wrapping real ROS actions and services as tree leaves. The
big hardware payoff lands here too: **the tree you built and
fault-tested in the only-code mode runs unchanged** — you only repoint
its leaves from mock services to the real `pymycobot`/`ros2_control`
gripper, the real scanner node, and the real dispenser driver.

How it's good on hardware: it is the **cheapest** path, and because it is
Python it is quick to extend — adding an audit-logging decorator that
records every tick to the Layer 08 trail is a few lines. The recovery
branches for missed grip and scanner no-read that you exercised against
mocks now fire against real hardware with no rewrite, which is the whole
point of having proved them in sim.

How it's bad versus the other four: pure Python is the **weak link for
real-time** safe-stop. Under load, Python's timing is less predictable
than **BehaviorTree.CPP's** C++, so for the hard guarantee that a
safe-stop branch ticks promptly you generally want the e-stop enforced in
a lower, faster layer (controller / `ros2_control`) with py_trees
commanding the *graceful* stop above it. Its live introspection is also
**less polished than Groot2** for monitoring a real cell, and it is a
lighter-governed ecosystem than the Nav2-backed C++ engine.

## YASMIN

YASMIN is a modern finite-state-machine library for ROS 2 (C++ and
Python): named states, outcome-string transitions, a state viewer. On
hardware it expresses the prep → load stages —
`PICK → DECAP → DISPENSE → RECAP → SCAN → PLACE` — as explicit states,
each calling a real device and branching on its real result.

How it's good on hardware: the explicit-state model is **easy to audit**
— logging "entered state X at time T with outcome Y" maps one-to-one
onto the Layer 08 trail, and an inspector can read the state log as a
plain narrative of what happened to each vial. For a procedure that is
genuinely stage-by-stage, that legibility is a real virtue, and it is
fully ROS 2-native.

How it's bad versus the other four: a plain FSM is **less reactive**,
which bites hardest exactly where hardware needs it most — safe-stop. To
abort from *any* state you must add an explicit transition out of *every*
state, where **BehaviorTree.CPP** and **py_trees** express the safe-stop
once as a higher-priority branch. As real failure modes multiply (missed
grip, no-read, device timeout), those per-state transitions sprawl. Its
tooling is also lighter than **Groot2** or **FlexBE's** operator GUI.

## FlexBE

FlexBE is a **hierarchical** FSM framework with a real-time **operator
GUI** built for human-in-the-loop supervision: an operator can watch the
machine run, pause, step state-by-state, and shift between autonomy
levels. It has a ROS 2 line and is at home in settings where a person
oversees a long, partly-manual procedure.

How it's good on hardware: this is where FlexBE finally pays off. In a
real HPLC cell a human is often present and may need to **take over** —
confirm a recap, clear a jam, approve a quarantined vial — and FlexBE's
GUI makes that supervision and step-through first-class, which none of
the BT tools offer out of the box. Its autonomy-level switching is a
clean way to run mostly-autonomous with human checkpoints, and its state
log feeds the audit trail.

How it's bad versus the other four: it is **heavier** to set up and
operate than the alternatives, and as an FSM it inherits the same
reactivity limits as **YASMIN** — safe-stop transitions must be wired
per state rather than expressed once as in a Behavior Tree. For a cell
intended to run **autonomously and headless** most of the time, the
operator-console weight is mostly idle. It is the right pick *only* when
operator-in-the-loop supervision is a genuine requirement; otherwise the
BTs are leaner.

## SMACH

SMACH is the classic ROS 1 finite-state-machine library — for years the
default ROS task-logic tool, with nested state machines, concurrence,
and the `smach_viewer`. Much legacy lab automation still runs on it.

How it's good on hardware: it is conceptually solid and familiar, and if
your real cell must interoperate with an **existing ROS 1 system**,
recognising SMACH helps you understand and bridge that legacy code
before replacing it.

How it's bad versus the other four: it is **ROS 1 only**, and ROS 1 is
end-of-life — a non-starter for a new hardware build that needs current
drivers, `ros2_control`, and long-term support. It has **no modern
safe-stop or audit story** beyond what you bolt on, its FSM reactivity
limits match **YASMIN's**, and its tooling predates **Groot2** and
**FlexBE's** GUIs. **YASMIN** supersedes it on ROS 2. Listed for lineage
only; do not choose it for this project.

## Verdict

- **Best-in-class — BehaviorTree.CPP (+ Groot2).** Its reactivity makes
  safe-stop a clean top-priority pre-emption, every tick is a natural
  audit-log point for Layer 08, and Groot2 monitors the real cell live.
  Proven on real robots via Nav2. The tree is the *same one you built in
  sim* — only the leaves now call real drivers.
- **Cheapest — py_trees / py_trees_ros.** Free and easy, and it runs the
  unchanged sim tree against real devices; just enforce the hard e-stop
  in a faster lower layer, since Python timing is the weak point for
  real-time safe-stop.
- **Best-practical — BehaviorTree.CPP.** Mature, ROS 2-ready, fast enough
  for real-time, and audit-loggable: the safest long-term bet on
  hardware, and the one whose sim-proven logic transfers with zero
  rewrite. (Add **FlexBE** alongside it only if a human operator must
  supervise and step the real cell.)

## See also

- Folder overview: [`README.md`](README.md)
- Sibling mode (sim only, mocks + fault injection):
  [`../01-only-code/07-orchestration-and-task-logic.md`](../01-only-code/07-orchestration-and-task-logic.md)
