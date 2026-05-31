# Behavior Trees — the orchestration layer

> This teaches the **top choice** for the orchestration layer:
> **Behavior Trees** built with **BehaviorTree.CPP** (the C++ library)
> and authored/monitored with the **Groot2** visual editor — the same
> engine Nav2 already runs. Orchestration is the "supervisor" that
> decides what the robot does next and what to do when a step fails.
> For the why-this-and-not-that decision, read the layer note
> [`../07-orchestration.md`](../07-orchestration.md); for any unfamiliar
> term, the [glossary](../../02-glossary.md) defines it in a sentence.
> This is the last doc in the learn series — it assumes you have read
> [`02-ros2.md`](02-ros2.md), [`03-nav2.md`](03-nav2.md), and
> [`04-moveit2.md`](04-moveit2.md), and it ends by tying the whole stack
> together.

You are a web developer. You know how to write code, call functions,
and reason about control flow, but robotics is new. So every robotics
term below is defined in one plain sentence the first time it appears.
Where a web analogy genuinely helps, you'll get one; where it would
mislead, you won't.

---

## 1. Introduction and basic concepts

### What orchestration is

Our robot does a long chain of things: drive to the shelf, look for a
product, pick it up, find the empty slot, place the product, check it
landed right, then do it again for the next can. Each of those steps is
handled by a different layer of the stack — navigation, perception, arm
motion, and so on.

**Orchestration** is the layer that decides the *order* of those steps,
and decides what to do when one of them goes wrong. It does no sensing
and no moving itself. It only **directs**. Think of it as the shift
supervisor on a stocking crew: it holds the checklist, calls each
worker in turn, and handles the "uh oh, that didn't work" moments.

In web terms, orchestration is the request handler / workflow engine
that calls each service in sequence, retries the flaky ones, and bails
out cleanly when something is unrecoverable. It is glue logic with a
strong opinion about failure.

### Why not just a finite-state machine?

The classic way to write a robot's task logic is a **finite-state
machine** (FSM) — a set of named states ("Navigating", "Picking",
"Placing") with arrows describing which state you can jump to next.
FSMs are fine for short, mostly-linear tasks.

Our task is neither short nor linear. It is **long** (nine steps),
**branchy** (every step has a failure path), and **recoverable** (a
failed pick should retry, then skip-and-log; a person in the aisle
should trigger a safe-stop from anywhere). In an FSM, every new failure
path means new arrows from many states to many other states. The arrows
multiply until the diagram is a hairball — the well-known "spaghetti of
transitions" problem.

A **Behavior Tree** (BT) is an alternative way to structure that same
logic. Instead of states-and-arrows, it is a *tree* of nodes that is
re-evaluated, top to bottom, many times per second. Recovery and
sequencing are expressed by the *shape* of the tree, not by a web of
transitions. Adding a retry or a safe-stop is a local edit — you drop in
one node — instead of rewiring the whole graph. That reactivity and
composability is exactly why BTs win for this kind of task.

### The tick and the three return states

The heartbeat of a Behavior Tree is the **tick** — a signal that flows
down from the top of the tree on a fixed clock (say, 10 or 100 times per
second), visiting nodes in order and asking each one "what's your
status?".

Every node, when ticked, returns exactly one of **three states**:

- **SUCCESS** — the node finished its job. (The robot arrived at the
  shelf.)
- **FAILURE** — the node tried and could not do its job. (The grasp
  slipped.)
- **RUNNING** — the node is still working and needs more ticks to
  finish. (The arm is mid-trajectory.) This third state is the thing an
  FSM lacks and a BT has: it lets a long action stay "in progress"
  across many ticks while the rest of the tree keeps being re-checked.

A **node** is just one box in the tree. The boxes at the very bottom,
which actually *do* or *check* something, are called **leaves** (a leaf
is a node with no children — the end of a branch). The boxes above them
are **control nodes** that route the tick to their children and combine
the children's return states into their own.

That is the entire model: a tree of nodes, ticked repeatedly, each
returning SUCCESS / FAILURE / RUNNING, with the parents deciding what
the combination means. Everything else is detail on top of this.

---

## 2. Important concepts that are used most often

### The tick, again — but where it comes from

You don't tick nodes by hand. You build a tree, get back a `BT::Tree`
object, and call `tree.tickOnce()` (or `tree.tickWhileRunning()`) in a
loop. Each call sends one tick from the root down through the tree. Your
job is to define the leaves and describe the tree's shape; the library
does the ticking.

### Node types

There are three families of nodes. Learning these three is most of
learning Behavior Trees.

**1. Control nodes** — the branching logic. They have children and
decide how the tick flows through them:

- **Sequence** — ticks its children left to right. If a child returns
  SUCCESS, it moves to the next child. If any child returns FAILURE, the
  Sequence returns FAILURE immediately (the rest are skipped). It
  returns SUCCESS only when *all* children succeeded. This is logical
  **AND**: "do A, then B, then C — stop if any fails."
- **Fallback** (also called **Selector**) — ticks its children left to
  right, but stops at the first **SUCCESS**. If a child fails, it tries
  the next child. It returns FAILURE only if *all* children fail. This
  is logical **OR**, and it is how you express recovery: "try the normal
  thing; if it fails, try the backup thing."
- **Parallel** — ticks all its children on the same tick and succeeds or
  fails based on a threshold (e.g. "succeed when 2 of 3 children
  succeed"). Used less often; handy for "do this while also watching for
  that."

**2. Decorators** — a node with exactly **one** child that modifies the
child's result or how often it runs. (A decorator wraps one node, the
way a Python decorator wraps one function.) The ones you'll use:

- **Inverter** — flips SUCCESS to FAILURE and vice versa (logical NOT).
- **RetryUntilSuccessful** — re-ticks its child up to *N* times while it
  keeps failing; returns SUCCESS as soon as the child succeeds, or
  FAILURE after *N* tries. This is your "try the pick three times before
  giving up."
- **Timeout** — returns FAILURE if its child has not finished within a
  given number of milliseconds. Keeps a stuck action from hanging the
  robot forever.
- **RateController** — limits how often its child is ticked (e.g. "tick
  at most once per second"), so an expensive check doesn't run on every
  10ms tick.

**3. Leaf nodes** — the boxes that actually do work. Two kinds:

- **Action** — *does* something and can take time, so it may return
  RUNNING for many ticks before SUCCESS or FAILURE. (Driving to the
  shelf, moving the arm.) In code this is usually a `BT::SyncActionNode`
  (finishes in one tick) or a `BT::StatefulActionNode` (spans many
  ticks, the right base class for wrapping a long-running ROS 2 action).
- **Condition** — *checks* something and returns SUCCESS or FAILURE
  instantly, never RUNNING. (Is the aisle clear? Is the tray empty?) In
  code this is a `BT::ConditionNode`.

### The blackboard and ports

Nodes need to share data — the navigation leaf produces a target, the
pick leaf needs a product pose, the place leaf needs a slot pose. They
share it through the **blackboard**: a shared key/value store that lives
alongside the tree, like a small in-memory context object passed around
the whole workflow. One node writes `product_pose`; a later node reads
`product_pose`.

A node declares which blackboard keys it touches through **ports**. A
port is a named, typed input or output on a node — an **input port** is
data the node reads, an **output port** is data the node writes. You
declare them in C++ with `providedPorts()` and bind them to blackboard
keys in the XML using the `{curly_braces}` syntax. Ports are how a leaf
stays reusable: the same `LocateSlot` node can read its `shelf_id` from
the blackboard instead of hard-coding it.

### The XML tree format

You *could* build the tree entirely in C++, but the idiomatic way is to
write the tree's **shape** in XML and keep only the leaf *behavior* in
C++. The XML is data, not code — you can reload it without recompiling,
and Groot2 reads and writes it. A minimal file looks like:

```xml
<root BTCPP_format="4">
  <BehaviorTree ID="MainTree">
    <Sequence>
      <SaySomething message="hello"/>
    </Sequence>
  </BehaviorTree>
</root>
```

`BTCPP_format="4"` declares the BehaviorTree.CPP v4 file format. Inside
`<BehaviorTree>` you nest control nodes and leaves to describe the tree.

### Groot2

**Groot2** is the companion desktop app for BehaviorTree.CPP. It does
two jobs: it is a **visual editor** (drag nodes around, and it writes
the XML for you) and a **live monitor** (connect to a running tree and
watch ticks light up each node green/red/blue in real time). For a
branchy stocking tree, watching the live tick is the fastest way to see
*why* a run took the recovery path. The free tier covers authoring and
monitoring for this project.

### How a BT leaf wraps a ROS 2 action

This is the bridge to the rest of the stack. Recall from
[`02-ros2.md`](02-ros2.md) that a ROS 2 **action** is the request type
for long-running goals (drive there, plan and execute this motion) with
feedback and the ability to cancel — exactly the navigation
([`03-nav2.md`](03-nav2.md)) and arm-motion
([`04-moveit2.md`](04-moveit2.md)) calls we need.

A BT **Action leaf** wraps one ROS 2 action like this: the *first* tick
sends the goal to the action server and returns **RUNNING**; every
*later* tick checks whether the server has finished and returns RUNNING
until it does, then SUCCESS or FAILURE based on the result. If the leaf
gets halted (because a higher-priority branch took over — see the
safe-stop below), it cancels the ROS 2 goal. You rarely write this glue
by hand: the **BehaviorTree.ROS2** package (and the `nav2_behavior_tree`
nodes Nav2 ships) provide base classes that handle the send-goal /
poll-result / cancel-on-halt lifecycle for you. You subclass one,
declare your ports, and fill in "build the goal" and "read the result."

> The Python alternative to all of this is **`py_trees_ros`**, which
> gives you the same Behavior Tree concepts in Python instead of C++;
> pick it only if the team is Python-first.

---

## 3. Hello world example with code

Let's build the smallest real tree: a **Sequence** with one **Condition**
("is the tray loaded?") and one **Action** ("say a message"). No ROS yet
— just the BT engine, so the mechanics are clear.

### The C++ leaves

```cpp
#include "behaviortree_cpp/bt_factory.h"
#include <iostream>

// A CONDITION leaf: checks something, returns SUCCESS or FAILURE
// instantly (never RUNNING). Here it just reports a hard-coded fact.
class TrayLoaded : public BT::ConditionNode
{
public:
  TrayLoaded(const std::string& name, const BT::NodeConfig& config)
    : BT::ConditionNode(name, config) {}

  // No ports needed for this toy condition.
  static BT::PortsList providedPorts() { return {}; }

  // tick() is called every time the tree visits this node.
  BT::NodeStatus tick() override
  {
    bool tray_has_items = true;            // pretend we checked a sensor
    return tray_has_items ? BT::NodeStatus::SUCCESS
                          : BT::NodeStatus::FAILURE;
  }
};

// An ACTION leaf. SyncActionNode = it finishes within a single tick,
// so it returns SUCCESS/FAILURE immediately (no RUNNING). It reads one
// input port called "message".
class SaySomething : public BT::SyncActionNode
{
public:
  SaySomething(const std::string& name, const BT::NodeConfig& config)
    : BT::SyncActionNode(name, config) {}

  // Declare the ports this node uses. InputPort<T>("name") = a typed
  // value this node reads from the blackboard or the XML.
  static BT::PortsList providedPorts()
  {
    return { BT::InputPort<std::string>("message") };
  }

  BT::NodeStatus tick() override
  {
    // Read the input port. getInput returns an Expected<T>; check it.
    BT::Expected<std::string> msg = getInput<std::string>("message");
    if (!msg) {
      // Port missing or wrong type -> this is a real failure.
      throw BT::RuntimeError("missing required input [message]: ",
                             msg.error());
    }
    std::cout << "[SaySomething] " << msg.value() << std::endl;
    return BT::NodeStatus::SUCCESS;
  }
};
```

### The XML tree

```xml
<root BTCPP_format="4">
  <BehaviorTree ID="MainTree">
    <!-- Sequence = logical AND: run children left to right, stop on
         the first FAILURE, succeed only if all succeed. -->
    <Sequence name="root_sequence">
      <TrayLoaded   name="check_tray"/>
      <SaySomething name="greet" message="tray is loaded, starting"/>
    </Sequence>
  </BehaviorTree>
</root>
```

### Registering and ticking

```cpp
int main()
{
  // The factory knows every node type by name and builds the tree
  // from XML.
  BT::BehaviorTreeFactory factory;

  // Tell the factory the C++ class behind each XML tag name.
  factory.registerNodeType<TrayLoaded>("TrayLoaded");
  factory.registerNodeType<SaySomething>("SaySomething");

  // Build the tree from the XML file.
  auto tree = factory.createTreeFromFile("./hello.xml");

  // Tick from the root until it stops returning RUNNING. For this
  // synchronous tree that is a single tick.
  tree.tickWhileRunning();
  return 0;
}
```

### How the three states flow up the tree

Follow one tick from the root:

1. The root **Sequence** is ticked. It ticks its first child,
   `check_tray`.
2. `TrayLoaded::tick()` runs and returns **SUCCESS**. Because a Sequence
   continues on SUCCESS, the Sequence ticks its next child, `greet`.
3. `SaySomething::tick()` prints and returns **SUCCESS**.
4. The Sequence has no more children and all succeeded, so the Sequence
   returns **SUCCESS** to the root. The run is done.

Now imagine `TrayLoaded` returned **FAILURE** instead. The Sequence
would stop right there, never tick `greet`, and return **FAILURE**
upward. That short-circuiting is the whole point of a Sequence: failure
propagates up and stops the line. (And if an action returned
**RUNNING**, the Sequence would itself return RUNNING and resume from
that child on the next tick — the engine remembers where it was.)

---

## 4. A bit advanced example with code

Now add the three things that make BTs useful for a real robot:
**recovery** (Fallback), **retrying** (RetryUntilSuccessful), and
**passing data between nodes** (the blackboard). We'll model a tiny
pick: detect a product (writes its pose), then grasp it (reads that
pose), with a recovery path if grasping fails.

### Two leaves that share data through ports

```cpp
#include "behaviortree_cpp/bt_factory.h"
#include <iostream>

// A simple 3D pose we pass on the blackboard. Any copyable type works.
struct Pose { double x, y, z; };

// DETECT: writes a Pose to an OUTPUT port. Other nodes can read it.
class DetectProduct : public BT::SyncActionNode
{
public:
  DetectProduct(const std::string& name, const BT::NodeConfig& cfg)
    : BT::SyncActionNode(name, cfg) {}

  static BT::PortsList providedPorts()
  {
    // OutputPort = a value this node WRITES to the blackboard.
    return { BT::OutputPort<Pose>("product_pose") };
  }

  BT::NodeStatus tick() override
  {
    Pose p{0.42, -0.10, 0.85};            // pretend perception found it
    setOutput("product_pose", p);          // publish to the blackboard
    std::cout << "[DetectProduct] wrote product_pose\n";
    return BT::NodeStatus::SUCCESS;
  }
};

// GRASP: reads the Pose from an INPUT port and tries to grasp.
// It fails the first two times, then succeeds, to demo the retry.
class GraspProduct : public BT::SyncActionNode
{
public:
  GraspProduct(const std::string& name, const BT::NodeConfig& cfg)
    : BT::SyncActionNode(name, cfg) {}

  static BT::PortsList providedPorts()
  {
    return { BT::InputPort<Pose>("product_pose") };
  }

  BT::NodeStatus tick() override
  {
    auto pose = getInput<Pose>("product_pose");
    if (!pose) {
      throw BT::RuntimeError("GraspProduct missing product_pose");
    }
    static int attempts = 0;
    attempts++;
    std::cout << "[GraspProduct] attempt " << attempts
              << " at (" << pose->x << ", " << pose->y << ")\n";
    if (attempts < 3) {
      return BT::NodeStatus::FAILURE;      // slipped — caller may retry
    }
    return BT::NodeStatus::SUCCESS;
  }
};
```

### The XML — Fallback + Retry + blackboard wiring

```xml
<root BTCPP_format="4">
  <BehaviorTree ID="MainTree">
    <Sequence name="pick_one">

      <!-- Output port {product_pose} writes the key "product_pose"
           onto the blackboard. -->
      <DetectProduct product_pose="{product_pose}"/>

      <!-- Fallback = logical OR / recovery: try the first child; if it
           FAILS, try the next. Succeeds at the first SUCCESS. -->
      <Fallback name="grasp_with_recovery">

        <!-- RetryUntilSuccessful re-ticks its ONE child up to
             num_attempts times while it keeps failing. -->
        <RetryUntilSuccessful num_attempts="3">
          <!-- Input port {product_pose} reads the same blackboard key
               DetectProduct wrote. This is how data flows between
               nodes. -->
          <GraspProduct product_pose="{product_pose}"/>
        </RetryUntilSuccessful>

        <!-- Recovery branch: only reached if all 3 grasp attempts
             failed. In the real robot this would skip-and-log. -->
        <AlwaysSuccess name="log_and_skip"/>

      </Fallback>

    </Sequence>
  </BehaviorTree>
</root>
```

`AlwaysSuccess` is a built-in node that does nothing and returns
SUCCESS — a stand-in here for "log the failure and move on."

### What happens, and what "reactive re-ticking" means

`DetectProduct` runs once and writes `product_pose`. Then the
`RetryUntilSuccessful` ticks `GraspProduct`: it fails (attempt 1), the
decorator re-ticks it (attempt 2, fails), re-ticks again (attempt 3,
succeeds). Because the inner branch ended in SUCCESS, the Fallback is
satisfied and never touches the `log_and_skip` recovery branch. The
Sequence then returns SUCCESS. If grasping had failed all three times,
the Retry would return FAILURE, the Fallback would move on to
`log_and_skip`, that would return SUCCESS, and so the whole pick would
end "handled, but skipped."

**Reactive re-ticking** is the BT property underneath this. Because the
tree is ticked repeatedly rather than run once, a condition placed high
in the tree is checked again on every tick. If that condition flips
(say, the aisle stops being clear), the higher-priority branch wins on
the very next tick and the engine **halts** whatever was RUNNING below
— cancelling the in-flight ROS 2 goal. That is how a BT reacts to the
world *during* a long action, not only between steps. We rely on this
for the safe-stop in the next section.

---

## 5. Explanation of place-on-shelf code

Now the real thing: the full stocking tree for **this** project. It
implements the nine-step loop from
[`../../01-requirements.md`](../../01-requirements.md) §6 — navigate,
then loop pick/place/verify until the tray is empty or the row is full,
with retry-then-skip on a bad pick and an always-watching safe-stop —
and each leaf maps to one ROS 2 action exposed by another layer.

### The leaf-to-ROS-2 mapping

These are the leaves and what each one wraps. Names match the rest of
the stack docs exactly:

| BT leaf | Kind | Wraps (ROS 2) | Reads / writes (blackboard) |
|---------|------|---------------|------------------------------|
| `navigate_to_shelf` | Action | Nav2 `NavigateToPose` | reads `shelf_id` |
| `locate_product` | Action | perception (RGB-D on `/wrist_camera/depth/points`) | writes `product_pose` |
| `pick_product` | Action | MoveIt 2 pick | reads `product_pose` |
| `locate_slot` | Action | perception (planar fit of shelf face) | reads `shelf_id`,`units_placed`; writes `slot_pose` |
| `place_product` | Action | MoveIt 2 guarded set-down | reads `slot_pose` |
| `verify_placement` | Action | perception re-check | reads `slot_pose`; writes per-unit log |
| `aisle_clear` | Condition | reads `/scan` (lidar) | reads `aisle_clear` |
| `safe_stop` | Action | cancel motion + `/cmd_vel` zero | — |
| `units_remaining` | Condition | tray-empty / row-full check | reads `units_remaining` |

All of these run in the `map`→`odom`→`base_link`→…→`wrist_camera_link`,
`tool0` transform tree (tf2) you saw in the earlier docs; the poses on
the blackboard are stamped in those frames.

### The full XML tree

```xml
<root BTCPP_format="4" main_tree_to_execute="StockShelf">

  <BehaviorTree ID="StockShelf">

    <!-- TOP-LEVEL REACTIVE FALLBACK (safe-stop guard).
         A ReactiveFallback re-ticks ALL its children on every tick,
         left to right, and returns the first non-FAILURE. We use it so
         the safety check is re-evaluated continuously, even while the
         stocking job below is RUNNING. -->
    <ReactiveFallback name="safety_guard">

      <!-- BRANCH 1: highest priority. If the aisle is NOT clear, this
           branch runs and triggers SAFE-STOP. Inverter flips the
           aisle_clear condition: when the aisle is blocked,
           "NOT clear" = SUCCESS, so this branch wins and halts the job
           branch below (cancelling any in-flight Nav2/MoveIt goal). -->
      <Sequence name="handle_intrusion">
        <Inverter>
          <AisleClear name="aisle_clear" clear="{aisle_clear}"/>
        </Inverter>
        <SafeStop name="safe_stop"/>
      </Sequence>

      <!-- BRANCH 2: the actual stocking job. Only ticked while the
           aisle is clear (branch 1 returns FAILURE -> fall through). -->
      <Sequence name="stocking_job">

        <!-- Step 1: drive to the target shelf and align to its face.
             Wraps Nav2; returns RUNNING until "arrived". -->
        <NavigateToShelf name="navigate_to_shelf"
                         shelf_id="{shelf_id}"/>

        <!-- Steps 3-8: loop over each facing/unit. The Sequence's
             child here is re-entered each tick; the units_remaining
             condition guards the loop body so the Sequence ends with
             SUCCESS once the tray is empty or the row is full. -->
        <KeepRunningUntilFailure>
          <Sequence name="place_one_unit">

            <!-- Loop guard. FAILURE when units_remaining == 0 OR row is
                 full -> KeepRunningUntilFailure stops the loop with
                 SUCCESS. -->
            <UnitsRemaining name="units_remaining"
                            remaining="{units_remaining}"/>

            <!-- PICK, with retry-then-skip recovery. Fallback: try the
                 pick branch; if it ultimately fails, fall to the
                 skip-and-log branch (which returns SUCCESS so the loop
                 continues to the next unit). -->
            <Fallback name="pick_with_recovery">
              <RetryUntilSuccessful num_attempts="3">
                <Sequence name="locate_then_pick">
                  <LocateProduct name="locate_product"
                                 product_pose="{product_pose}"/>
                  <PickProduct   name="pick_product"
                                 product_pose="{product_pose}"/>
                </Sequence>
              </RetryUntilSuccessful>
              <LogSkip name="log_failed_pick"
                       sku="{sku}" reason="pick_failed"/>
            </Fallback>

            <!-- PLACE. Find the slot from planogram + units already
                 placed, then guarded set-down, then verify. If verify
                 fails, log it but keep the run going. -->
            <Fallback name="place_with_recovery">
              <Sequence name="locate_place_verify">
                <LocateSlot name="locate_slot"
                            shelf_id="{shelf_id}"
                            units_placed="{units_placed}"
                            slot_pose="{slot_pose}"/>
                <PlaceProduct name="place_product"
                              slot_pose="{slot_pose}"/>
                <VerifyPlacement name="verify_placement"
                                 slot_pose="{slot_pose}"/>
              </Sequence>
              <LogSkip name="log_failed_place"
                       sku="{sku}" reason="place_failed"/>
            </Fallback>

          </Sequence>
        </KeepRunningUntilFailure>

        <!-- Step 9: job done -> write the per-unit success log. -->
        <Report name="report" units_placed="{units_placed}"/>

      </Sequence>

    </ReactiveFallback>

  </BehaviorTree>
</root>
```

### Reading the tree block by block

- **`<root … main_tree_to_execute="StockShelf">`** — declares the v4 XML
  format and which tree to run (a project can hold several).

- **`ReactiveFallback name="safety_guard"`** — the outermost node and
  the heart of the safety design. *Reactive* means it re-ticks every
  child on every tick rather than remembering where it stopped. So
  branch 1 (the safety check) is re-evaluated continuously, even while
  the stocking job in branch 2 is mid-action. A plain Fallback would
  only check branch 1 once and then sit inside branch 2 — too late to
  react to a shopper walking in.

- **Branch 1, `handle_intrusion`** — `AisleClear` is a Condition leaf
  that reads the lidar topic `/scan` and returns SUCCESS when the aisle
  is empty. The `Inverter` flips it, so "aisle blocked" becomes SUCCESS
  for this branch. When that happens, the branch runs `SafeStop`, which
  cancels any active motion and publishes zero velocity to `/cmd_vel`.
  Because this branch is now non-FAILURE, the ReactiveFallback stops
  here and **halts** branch 2 — and halting a RUNNING action leaf
  cancels its underlying ROS 2 goal, so a Nav2 drive or MoveIt motion
  stops cleanly. This is the reactive re-ticking from section 4 doing
  real safety work. While the aisle stays clear, `AisleClear` returns
  SUCCESS, the Inverter turns it to FAILURE, branch 1 falls through, and
  the job continues.

- **Branch 2, `stocking_job`** — a Sequence (logical AND): each step
  must succeed before the next, and any unhandled FAILURE ends the job.

- **`NavigateToShelf`** — step 2 of the requirements. Wraps the Nav2
  `NavigateToPose` action ([`03-nav2.md`](03-nav2.md)). It returns
  RUNNING while driving and SUCCESS once the robot is parked and aligned
  to the shelf face. It reads `shelf_id` from the blackboard to know
  where to go.

- **`KeepRunningUntilFailure`** — a decorator that re-ticks its one
  child until that child returns FAILURE, then returns SUCCESS. This is
  our **loop**: keep placing units until the loop body fails on purpose.

- **`UnitsRemaining`** — the loop guard and first node of the body. It
  returns SUCCESS while there is still a unit on the tray and an empty
  facing in the row, and FAILURE when the tray is empty or the row is
  full. That FAILURE is what tells `KeepRunningUntilFailure` to stop the
  loop (with SUCCESS) and move on to the report. This is steps 3 and 8
  of the requirements expressed as a single condition.

- **`pick_with_recovery` (Fallback)** — the retry-then-skip logic for
  step 4. Its first child is a `RetryUntilSuccessful` with
  `num_attempts="3"` wrapping a small Sequence: `LocateProduct` (writes
  `product_pose` from the wrist camera point cloud,
  `/wrist_camera/depth/points`) then `PickProduct` (MoveIt 2 grasp,
  reads `product_pose`). If either step fails, the Sequence fails, the
  Retry re-ticks the whole locate-then-pick up to three times. If all
  three fail, the Retry returns FAILURE and the Fallback moves to
  `LogSkip`, which records the failed unit and returns SUCCESS so the
  loop keeps going to the next unit. This is requirement §7's
  "logged and skipped rather than retried indefinitely."

- **`place_with_recovery` (Fallback)** — steps 5, 6, 7. `LocateSlot`
  reads `shelf_id` and `units_placed` and computes the next facing
  position from the planogram (slot origin + offset for cans already
  placed), writing `slot_pose`. `PlaceProduct` is the MoveIt 2
  **guarded set-down** ([`04-moveit2.md`](04-moveit2.md)): approach,
  light contact with the shelf, release — not a free-space drop.
  `VerifyPlacement` re-checks with the camera that the can landed
  upright in the slot. If any of these fail, `LogSkip` records it and
  the run continues. (A real build would also increment `units_placed`
  on a verified success; that bookkeeping lives in the
  `VerifyPlacement` / `Report` leaves.)

- **`Report`** — step 9. Once the loop ends, this writes the per-unit
  success log the requirements demand for measuring success rate.

### Sketch of the ROS 2 action-leaf wrappers

Most leaves above are thin wrappers over a ROS 2 action server. You
don't write the send-goal/poll/cancel plumbing by hand — the
**BehaviorTree.ROS2** base classes do it. The shape of one wrapper:

```cpp
#include "behaviortree_ros2/bt_action_node.hpp"
#include "nav2_msgs/action/navigate_to_pose.hpp"

// RosActionNode<T> is the BehaviorTree.ROS2 base that turns a ROS 2
// action into a BT leaf: first tick sends the goal, later ticks return
// RUNNING until the result arrives, and a halt cancels the goal.
class NavigateToShelf
  : public BT::RosActionNode<nav2_msgs::action::NavigateToPose>
{
public:
  NavigateToShelf(const std::string& name,
                  const BT::NodeConfig& conf,
                  const BT::RosNodeParams& params)
    : RosActionNode(name, conf, params) {}

  // This leaf reads shelf_id from the blackboard.
  static BT::PortsList providedPorts()
  {
    return providedBasicPorts(
      { BT::InputPort<std::string>("shelf_id") });
  }

  // Called once when the leaf starts: build and return the ROS 2 goal.
  bool setGoal(Goal& goal) override
  {
    std::string shelf_id;
    getInput("shelf_id", shelf_id);
    goal.pose = poseForShelf(shelf_id);   // planogram lookup -> map frame
    return true;                           // send it
  }

  // Called when the action server returns a result.
  BT::NodeStatus onResultReceived(const WrappedResult& wr) override
  {
    return wr.code == rclcpp_action::ResultCode::SUCCEEDED
             ? BT::NodeStatus::SUCCESS
             : BT::NodeStatus::FAILURE;
  }

  // Called if the server is unreachable or errors.
  BT::NodeStatus onFailure(BT::ActionNodeErrorEnum) override
  {
    return BT::NodeStatus::FAILURE;
  }
};
```

`PickProduct`, `LocateSlot`, `PlaceProduct`, and `VerifyPlacement`
follow the identical pattern against their own MoveIt 2 / perception
action servers; only the goal type, the ports they read/write, and the
result interpretation change. `AisleClear` and `UnitsRemaining` are
lighter — plain `BT::ConditionNode`s that read a cached topic value
(`/scan`, or the tray counter) and return SUCCESS/FAILURE with no goal.
`SafeStop` cancels active goals and zeroes `/cmd_vel`.

Registration mirrors the hello-world `main`, plus a ROS node handle for
the action wrappers:

```cpp
BT::BehaviorTreeFactory factory;
BT::RosNodeParams params;
params.nh = node;                          // your rclcpp::Node

factory.registerNodeType<NavigateToShelf>("NavigateToShelf", params);
factory.registerNodeType<PickProduct>("PickProduct", params);
// ...register LocateSlot, PlaceProduct, VerifyPlacement, AisleClear,
//    UnitsRemaining, SafeStop, LocateProduct, LogSkip, Report...

auto tree = factory.createTreeFromFile("stock_shelf.xml");
while (rclcpp::ok()) {
  tree.tickOnce();                         // one tick per loop iteration
  rclcpp::spin_some(node);                 // service ROS callbacks
  // sleep to hold ~10-100 Hz tick rate
}
```

You point Groot2 at this running process to watch the tree tick live —
green for SUCCESS, red for FAILURE, blue for RUNNING — which makes "why
did it take the skip branch on unit 4?" obvious at a glance.

---

## Recap — and how the whole stack ties together

This is the last layer, so step back and see the full picture. The
orchestration Behavior Tree is the **supervisor** sitting on top, and
every leaf in its tree calls down into a layer you've already learned:

- **[`02-ros2.md`](02-ros2.md)** — the middleware. Every BT action leaf
  is a ROS 2 action client; the blackboard poses are stamped in tf2
  frames; the whole thing runs as ROS 2 nodes, identical in sim and on
  hardware.
- **[`03-nav2.md`](03-nav2.md)** — navigation. `navigate_to_shelf` wraps
  Nav2. (And note: Nav2 *itself* is a Behavior Tree built on this same
  BehaviorTree.CPP engine — so the navigation layer and the task layer
  share one paradigm and one tool, Groot2.)
- **[`04-moveit2.md`](04-moveit2.md)** — arm motion. `pick_product` and
  the guarded `place_product` wrap MoveIt 2.
- **Perception and grasping** — `locate_product`, `locate_slot`, and
  `verify_placement` wrap the RGB-D perception layer, reading the wrist
  camera and the planogram.

The Behavior Tree is what turns these separate capabilities into a
single, recoverable job. Its three return states (SUCCESS / FAILURE /
RUNNING), its control nodes (Sequence for "and", Fallback for "or /
recovery"), its decorators (Retry, Inverter, Timeout, RateController),
its blackboard for shared data, and its reactive re-ticking for the
safe-stop are *all* you need to express the nine-step stocking loop as a
tree you can read top to bottom — and the exact same tree runs in the
simulator and on the real robot.

That completes the stack: **Isaac Sim** (with Gazebo first) for the
world, **ROS 2** to connect everything, **Nav2** to drive, **MoveIt 2**
to move the arm, **RGB-D perception** to find products and slots,
**analytical → AnyGrasp** grasping to grab them, and **Behavior Trees**
(BehaviorTree.CPP + Groot2) to run the show. Build it simulation-first,
prove the loop, then transfer.
