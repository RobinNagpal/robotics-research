# Stack layer: Orchestration

> **Job:** sequence the whole task — navigate → pick → locate slot →
> place → verify → repeat — and make the failure/skip/safe-stop logic
> explicit and reusable. Each step is a ROS 2 action; the orchestrator
> is what decides order, retries, and recovery. The key tension is
> **Behavior Tree vs finite-state machine**: BTs are more reactive and
> reusable for exactly this kind of long, branchy, recoverable sequence.

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
