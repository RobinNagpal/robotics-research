# Stack layer: Orchestration

> **Job:** sequence the whole task — navigate → pick → locate slot →
> place → verify → repeat — and make the failure/skip/safe-stop logic
> explicit and reusable. Each step is a ROS 2 action; the orchestrator
> is what decides order, retries, and recovery. The key tension is
> **Behavior Tree vs finite-state machine**: BTs are more reactive and
> reusable for exactly this kind of long, branchy, recoverable sequence.

## How this layer fits into the architecture

Orchestration is the **shift supervisor** of the whole system — the
brain that decides what happens next, in what order, and what to do when
something goes wrong. Unlike every other layer, it does no sensing and
no moving itself; it only **directs**.

It sits at the **top** and drives every other layer. Holding the job
("stock shelf #4 with N cans"), it works down its checklist and calls
each layer in turn: tell navigation (`03-mobile-base-navigation.md`) to
drive to the shelf and wait for "arrived"; ask perception
(`05-perception.md`) for the product pose; ask grasping
(`06-grasping.md`) for a grasp; tell arm motion
(`04-arm-motion-planning.md`) to execute the pick; ask perception for
the slot; tell arm motion to place; ask perception to verify; then loop
for the next unit until the tray is empty or the row is full.

Crucially, it owns all the **decisions around failure**: if a pick
fails, it decides whether to retry or skip-and-log; if a person enters
the aisle, it triggers the safe-stop; if something is unrecoverable, it
halts and flags a human. Each step it calls is a ROS 2 action exposed by
another layer (`02-middleware.md`), so the supervisor stays a thin,
readable tree of "do this, then that, and on failure do this" — and the
exact same tree runs in the simulator (`01-simulator.md`) and on the
real robot.

## Comparison

| Framework | Paradigm | ROS 2 support | Reactivity | Visualization / tooling | Reusability / scalability | Language | Bottom line |
|-----------|----------|---------------|------------|-------------------------|---------------------------|----------|-------------|
| **BehaviorTree.CPP** (+ Groot2) | Behavior Tree | First-class (used by Nav2) | High (ticks re-evaluate) | **Groot2** live editor/monitor | High (composable subtrees) | C++ (+ scripting) | The standard for ROS 2 task logic; same engine Nav2 already runs |
| **py_trees / py_trees_ros** | Behavior Tree | Good | High | Render to dot/ASCII | High | Python | Pythonic BTs; great if the team prefers Python over C++ |
| **YASMIN** | Finite-state machine | Yes (ROS 2) | Lower (state transitions) | Viewer available | Moderate | C++ / Python | Clean modern FSM for ROS 2; simpler mental model, less reactive |
| **SMACH** | Finite-state machine | **ROS 1 only** | Lower | smach_viewer | Moderate | Python | The classic FSM — but ROS 1, so off the table for new work |
| **FlexBE** | Hierarchical FSM + GUI | Yes (ROS 2 port) | Moderate | Strong GUI (operator-in-loop) | Moderate–high | Python | Good when a human operator supervises/steps the state machine |

## Top choice

**BehaviorTree.CPP with Groot2** (or **py_trees_ros** if the team is
Python-first).

A Behavior Tree fits this task better than a state machine: the
pick-drive-place loop is long and branchy, every step can fail and needs
a clean skip/retry/safe-stop, and BTs express that reactively with
composable, reusable subtrees. Choosing **BehaviorTree.CPP** also means
reusing the *exact* engine Nav2 already runs (see
`03-stack/03-mobile-base-navigation.md`), so navigation and task logic
share one paradigm and one tool — **Groot2** — for authoring and live
monitoring. Pick **py_trees_ros** instead only to stay in Python; reach
for **FlexBE** only if a human operator needs to supervise the sequence
step by step. Avoid SMACH (ROS 1).

## Cost, hardware & where it runs

| Tier | Pick | Where it runs | Machine requirements | Cost |
|------|------|---------------|----------------------|------|
| **Best in class** | BehaviorTree.CPP + Groot2 | Onboard CPU, alongside the other nodes | Negligible — a thread on any CPU; **no GPU** | BehaviorTree.CPP free (MIT); Groot2 has a free tier + a paid Pro license for advanced monitoring |
| **Good enough & cheapest** | py_trees / py_trees_ros (Python) | Onboard CPU | Negligible CPU; no GPU | Free / open source |
| **Best cost-for-performance** | BehaviorTree.CPP + Groot2 (free tier) | Onboard CPU | Negligible | Free — the free Groot2 tier covers authoring/monitoring for this project |

Orchestration adds essentially **no hardware cost**: it's a lightweight
decision tree that ticks alongside everything else on the same onboard
CPU. The only money question is Groot2's optional Pro tier, and the free
tier is plenty for a v1 build.
