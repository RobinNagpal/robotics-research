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

## See also

- Folder overview: [`README.md`](README.md)
- Sibling mode (real arm + peripherals in the loop):
  [`../02-code-plus-hardware/07-orchestration-and-task-logic.md`](../02-code-plus-hardware/07-orchestration-and-task-logic.md)
