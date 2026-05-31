# Learn: MoveIt 2 — the arm motion-planning layer

> This is the hands-on companion to the stack note
> [`../04-arm-motion-planning.md`](../04-arm-motion-planning.md). That
> note explains *why* we picked MoveIt 2; this file teaches you *how*
> to use it. You will learn what arm motion planning is, the handful of
> concepts you meet every day, and then build up — from a one-line move
> to the project's real `pick_product` and `place_product` moves — using
> the MoveIt 2 Python API (`moveit_py`). Robotics terms are defined the
> first time they appear; the short reference is
> [`../../02-glossary.md`](../../02-glossary.md). This doc assumes you
> have read [`02-ros2.md`](02-ros2.md), so you already know what a ROS 2
> node, topic, and action are. When you finish here, the camera that
> tells the arm *where* to reach is the next layer:
> [`05-perception.md`](05-perception.md).

---

## 1. Introduction and basic concepts

**Arm motion planning** is the job of finding a path for a robot arm.
You know where the gripper (the hand) is now, and you know where you
want it to end up. The planner must find a sequence of in-between arm
poses that moves the gripper from here to there **without hitting
anything** — not the shelf, not a product already on the shelf, and not
the robot's own body. That sequence is called a **trajectory**: a list
of arm positions plus the timing for how fast to move through each one.

Think of it like routing in a web app. You have a start and a
destination, and a router that has to find a path that avoids walls. The
difference is that a robot arm does not move on a flat 2D map — it moves
in 3D, and it has several joints that all bend at once, so the "map" it
searches is much larger and stranger. That larger search is exactly what
a motion planner handles for you.

**MoveIt 2** is the standard open-source software for arm motion
planning. It is not one algorithm; it is a whole toolbox bundled
together: it holds a model of the robot, keeps track of obstacles, calls
a planning algorithm to find a collision-free trajectory, and then hands
that trajectory to the part of the system that drives the motors. MoveIt
2 runs **on top of ROS 2** (the messaging middleware from
[`02-middleware.md`](../02-middleware.md)). In practice that means MoveIt
2 is a set of ROS 2 nodes and we talk to it from our own ROS 2 Python
node. If you have not read [`02-ros2.md`](02-ros2.md) yet, do that
first — everything below is built out of ROS 2 nodes, topics, and
actions.

### Forward vs inverse kinematics, in plain words

A robot arm is a chain of rigid segments (**links**) connected by
**joints** that rotate. To describe the arm's pose you can list the
angle of every joint — that list is called the **joint state**.

- **Forward kinematics (FK):** given the joint angles, compute where the
  gripper ends up in space. This is easy and has exactly one answer —
  bend each joint by the given angle and see where the hand lands. It is
  like evaluating a formula: plug in the inputs, get one output.
- **Inverse kinematics (IK):** the reverse, and the hard direction. You
  say "put the gripper *here*, pointing *this way*," and IK has to solve
  for the joint angles that achieve it. There may be many solutions
  (several ways to bend the arm to reach the same spot), exactly one, or
  none (the target is out of reach). MoveIt 2 has an IK solver built in,
  so usually you just give it a target pose and let it find the joints.

A **pose** here means a position (x, y, z) plus an orientation (which
way the gripper is rotated). Position plus orientation together is six
numbers — that is why people say a gripper has "6-DoF" pose, where
**DoF** means *degrees of freedom*, the count of independent ways it can
move.

### The planning scene and the collision world

The planner cannot avoid obstacles it does not know about. MoveIt 2
keeps a model of the world called the **planning scene**: the robot
itself plus every obstacle, each represented as a simple shape (a box, a
cylinder, a mesh). The obstacles in that scene make up the **collision
world**. Before MoveIt 2 accepts a trajectory, it checks every step of
that trajectory against the collision world; if any step would overlap
an obstacle, that trajectory is rejected and the planner keeps looking.

For our project the collision world is the **shelf** and any products
**already placed** on it. Telling MoveIt 2 about them is how we keep the
arm from clipping the shelf edge or knocking over a neighbor — both of
which count as failures in [`../../01-requirements.md`](../../01-requirements.md).

### The place must be a gentle "guarded set-down"

One project-specific idea matters from the start. When the robot puts a
product on the shelf, it must **not drop it from the air**. It must
lower the product until it lightly touches the shelf surface, then open
the gripper. We call this a **guarded set-down**: move down slowly,
stop on contact, release. The opposite — letting go above the shelf so
the product falls — risks the product toppling or rolling, which our
requirements forbid. Keep this picture in mind; the place code in
section 5 is built entirely around making the set-down gentle.

---

## 2. Important concepts that are used most often

These are the terms and tools you will reach for in almost every MoveIt
2 program. Skim them now; the code in later sections uses each one.

### Joints, links, and the URDF

As above, an arm is **links** (rigid segments) joined by **joints**
(rotating connections). The full description of the robot — every link's
shape and mass, every joint and its limits, and how they connect — lives
in a file called the **URDF** (Unified Robot Description Format). It is
an XML file; you can think of it as the robot's schema. MoveIt 2 reads
the URDF so it knows the exact shape and reach of the arm it is
planning for. You normally write the URDF once when you model the robot
and rarely touch it after.

### Degrees of freedom (DoF)

The number of joints that can move independently. Our arm is **6-DoF** —
six rotating joints. Six is the magic number because it is the minimum
needed to place the gripper at *any* position *and* any orientation in
3D. With six joints, IK can usually find a solution for a reachable
target.

### Joint space vs Cartesian (task) space

Two different ways to describe "where the arm is" and "where you want it
to go."

- **Joint space** is the list of joint angles. A *joint-space goal* says
  "set the joints to these exact angles." It does not care where the
  gripper ends up in the room; it only cares about the angles.
- **Cartesian space** (also called **task space**) is the gripper's pose
  in the room — the (x, y, z) position and orientation. A *pose goal*
  says "put the gripper here, oriented this way," and lets IK figure out
  the joints.

You use joint-space goals for safe, repeatable "home" or "ready"
positions. You use Cartesian pose goals when you care about *where the
hand is*, which is most of pick-and-place.

### Planning groups: `arm` and `gripper`

A robot can have several sets of joints that you plan for separately.
MoveIt 2 calls each set a **planning group**. Our robot has two:

- **`arm`** — the six arm joints that position the gripper.
- **`gripper`** — the joints that open and close the parallel jaws.

A **parallel-jaw gripper** is a two-finger hand whose flat jaws slide
together to pinch an object and apart to release it. We plan arm motions
with the `arm` group and open/close the hand with the `gripper` group.

### The planning scene and collision objects

The **planning scene** (from section 1) is the live model of the robot
plus obstacles. Each obstacle is a **collision object**: a named shape
with a pose, added to the scene so the planner avoids it. In ROS 2 a
collision object is a message of type `moveit_msgs/CollisionObject`.
You add the shelf as a box, and each already-placed product as a
cylinder. You can also **attach** a collision object to the gripper —
more on that below.

### OMPL sampling planners

MoveIt 2 does not invent paths by hand; it calls a planning library.
The default is **OMPL** (Open Motion Planning Library). OMPL uses
**sampling planners** — algorithms that work by randomly trying many
candidate arm poses, keeping the collision-free ones, and connecting
them into a path from start to goal. A well-known one is **RRTConnect**.
"Sampling" just means "try lots of random points and stitch together the
ones that work." You rarely call OMPL directly; you ask MoveIt 2 to
plan and it uses OMPL underneath.

### Inverse kinematics (IK)

Already defined in section 1: turning a target gripper pose into joint
angles. You will see IK happen implicitly — whenever you give MoveIt 2 a
pose goal, it runs IK to find the joints before it plans.

### Trajectory execution via controllers and `FollowJointTrajectory`

Planning produces a trajectory, but planning does not move the robot. A
separate program called a **controller** drives the motors to follow the
trajectory. MoveIt 2 sends the trajectory to the controller over a ROS 2
**action** (a long-running request you can monitor and cancel) named
**`FollowJointTrajectory`**. In simulation the simulator provides this
controller; on hardware the motor drivers do. The good news: `moveit_py`
hides this — you call `execute()` and it sends the action for you. The
current joint angles, meanwhile, are continuously published on the
**`/joint_states`** topic, which MoveIt 2 listens to so it always knows
where the arm is right now.

### Cartesian path planning for straight approach and retreat

A normal OMPL plan gets the gripper from A to B by *any* collision-free
route, which may curve through the air. Sometimes you need the gripper
to move in a **straight line** — for example, lowering straight down
onto the shelf, or lifting straight up after grasping. MoveIt 2 has a
separate tool, **Cartesian path planning** (sometimes called
`compute_cartesian_path`), that produces a trajectory following a
straight line (or a series of waypoints) in Cartesian space. We use it
for the **approach** (move straight toward the object/shelf) and the
**retreat** (back straight away). Straight-line moves are predictable,
which is exactly what a gentle set-down needs.

### `tf2` frames and the gripper frame `tool0`

Positions are always measured relative to *something*. In ROS 2 those
reference points are called **frames**, and the library that tracks how
all the frames relate to each other (and how they move over time) is
**`tf2`**. Each frame has a name. Our robot's frames form a chain:

```
map → odom → base_link → arm_base_link → ... → wrist_camera_link
                                              → tool0
```

- **`map`** — the fixed world.
- **`odom`** → **`base_link`** — the mobile base's position.
- **`arm_base_link`** — where the arm bolts onto the base; the root of
  the arm chain.
- **`wrist_camera_link`** — the RGB-D camera on the wrist.
- **`tool0`** — the **gripper tip frame**, the point between the jaws.
  This is the frame we steer. When we say "move the gripper to this
  pose," we mean "move `tool0` to this pose." (`tool0`, read "tool
  zero," is the conventional name for a robot's tool tip.)

Every pose we send to MoveIt 2 carries the name of the frame it is
measured in, so MoveIt 2 can convert it into the arm's own coordinates
using `tf2`.

---

## 3. Hello world example with code

Goal: bring up MoveIt 2 from a Python node, send the arm to a safe
named "ready" position (a joint-space goal), then send the gripper tip
to a pose in space (a pose goal). This is the smallest end-to-end use of
`moveit_py`.

First, the core loop you will repeat forever in MoveIt 2: **plan, then
execute**. Planning *computes* a trajectory and checks it for
collisions but does **not** move the robot. Execution *sends* that
trajectory to the controller, which moves the robot. Separating them
means you can inspect or reject a bad plan before anything moves.

```python
#!/usr/bin/env python3
# hello_moveit.py - the smallest moveit_py program.

import rclpy                       # ROS 2 Python client library
from rclpy.node import Node
from moveit.planning import MoveItPy            # the main moveit_py entry point
from geometry_msgs.msg import PoseStamped       # a pose tagged with its frame


def plan_and_execute(robot, planning_component, label=""):
    """Ask the component to plan, and if it succeeds, execute the plan.

    This helper is the plan-then-execute pattern in one place so we can
    reuse it for every move below.
    """
    # plan() runs the planner (OMPL) and returns a result object.
    plan_result = planning_component.plan()

    if plan_result:                              # truthy only if a plan was found
        robot_trajectory = plan_result.trajectory
        # execute() sends the trajectory to the controller via the
        # FollowJointTrajectory action and blocks until it finishes.
        robot.execute(robot_trajectory, controllers=[])
        print(f"[{label}] executed")
        return True
    else:
        print(f"[{label}] planning FAILED")      # e.g. target unreachable / in collision
        return False


def main():
    rclpy.init()

    # MoveItPy launches MoveIt 2 inside this process and reads the robot
    # model (URDF) and the MoveIt config that defines our planning groups.
    robot = MoveItPy(node_name="hello_moveit")

    # Grab a handle to the "arm" planning group - the six arm joints.
    arm = robot.get_planning_component("arm")

    # --- Move 1: a joint-space goal using a named target -------------
    # "ready" is a named pose defined in the MoveIt config (a saved set
    # of joint angles). Named targets are the safest way to reach a
    # known, collision-free posture.
    arm.set_start_state_to_current_state()       # start from where the arm is now
    arm.set_goal_state(configuration_name="ready")
    plan_and_execute(robot, arm, label="go to ready")

    # --- Move 2: a Cartesian pose goal -------------------------------
    # Now move the gripper tip (tool0) to a specific pose in space.
    pose_goal = PoseStamped()
    pose_goal.header.frame_id = "arm_base_link"  # the frame these numbers are in
    pose_goal.pose.position.x = 0.30             # 30 cm forward
    pose_goal.pose.position.y = 0.00
    pose_goal.pose.position.z = 0.40             # 40 cm up
    pose_goal.pose.orientation.w = 1.0           # no rotation (identity orientation)

    arm.set_start_state_to_current_state()
    # link "tool0" is the frame we want placed at pose_goal; MoveIt runs
    # IK to find joint angles, then plans a collision-free path to them.
    arm.set_goal_state(pose_stamped_msg=pose_goal, pose_link="tool0")
    plan_and_execute(robot, arm, label="go to pose")

    rclpy.shutdown()


if __name__ == "__main__":
    main()
```

What just happened, step by step:

1. `MoveItPy(...)` starts MoveIt 2 in our process, loading the robot
   model and the configuration that names our `arm` and `gripper`
   groups.
2. `get_planning_component("arm")` gives us an object that plans for the
   arm group.
3. For the first move we set the goal by **name** (`"ready"`). That is a
   joint-space goal — a saved set of angles — so no IK is needed.
4. For the second move we set the goal as a **pose** of `tool0`. MoveIt
   2 runs IK to convert that pose into joint angles, then OMPL plans a
   collision-free path.
5. `plan()` computes and checks; `execute()` moves the robot. Always in
   that order.

For comparison, the same plan-then-execute pattern in C++ uses the
`MoveGroupInterface` class. You will see this in older tutorials; the
shape is identical:

```cpp
// One-time look at the C++ API for orientation; we use Python (moveit_py).
#include <moveit/move_group_interface/move_group_interface.h>

auto move_group =
    moveit::planning_interface::MoveGroupInterface(node, "arm");

move_group.setNamedTarget("ready");               // joint-space goal

moveit::planning_interface::MoveGroupInterface::Plan plan;
bool ok = (move_group.plan(plan) ==               // plan...
           moveit::core::MoveItErrorCode::SUCCESS);
if (ok) move_group.execute(plan);                 // ...then execute
```

We use Python (`moveit_py`) for the rest of this document because the
project's orchestration glue is in Python.

To run a `moveit_py` node you launch it like any ROS 2 node, after the
MoveIt 2 configuration for the robot is on the launch path:

```bash
# Run the hello-world node (MoveIt 2 config must be installed/sourced).
ros2 run shelf_stocker hello_moveit
```

---

## 4. A bit advanced example with code

Now we make planning *aware of the world* and add **straight-line**
motion. Two new skills:

1. Add the **shelf** to the planning scene as a collision object, so the
   planner routes around it.
2. Plan a **Cartesian straight-line approach** — move the gripper down
   in a straight line toward a target pose, instead of any curving path.

We also introduce **attaching** an object to the gripper, which you need
the moment the robot is holding a product.

### Adding a collision object to the planning scene

We edit the planning scene through the **`PlanningSceneMonitor`**, the
`moveit_py` object that owns the live scene. We build a
`moveit_msgs/CollisionObject` describing the shelf as a box, then apply
it.

```python
from geometry_msgs.msg import Pose
from moveit_msgs.msg import CollisionObject
from shape_msgs.msg import SolidPrimitive          # box/cylinder/etc. shapes


def add_shelf_collision_object(robot):
    """Insert the shelf into the planning scene as a box obstacle."""
    # The PlanningSceneMonitor owns the live world model. We open it for
    # writing with a 'with' block so changes are published atomically.
    psm = robot.get_planning_scene_monitor()
    with psm.read_write() as scene:

        shelf = CollisionObject()
        shelf.header.frame_id = "map"      # place the shelf in the world frame
        shelf.id = "shelf"                 # a unique name we can update/remove later

        # Describe the geometry: a single solid box.
        box = SolidPrimitive()
        box.type = SolidPrimitive.BOX
        box.dimensions = [0.80, 0.40, 0.03]   # x,y,z in metres: a thin wide plank

        # Where the box sits, relative to frame_id ("map").
        box_pose = Pose()
        box_pose.position.x = 1.50            # 1.5 m ahead in the world
        box_pose.position.y = 0.00
        box_pose.position.z = 0.90            # shelf surface ~90 cm off the floor
        box_pose.orientation.w = 1.0

        shelf.primitives.append(box)
        shelf.primitive_poses.append(box_pose)
        shelf.operation = CollisionObject.ADD     # ADD = insert (vs REMOVE/MOVE)

        # Commit the object into the scene.
        scene.apply_collision_object(shelf)
        # Tell MoveIt the world changed so planners see it immediately.
        scene.current_state.update()
```

From now on, every plan the `arm` group produces will avoid the box
named `"shelf"`. Adding the already-placed neighbor products works the
same way — a `SolidPrimitive.CYLINDER` per product, each with a unique
`id` like `"placed_0"`, `"placed_1"`, and so on.

### Planning a Cartesian straight-line approach

For a controlled approach we want the gripper to travel in a straight
line to a target pose. `moveit_py` exposes this through the planning
component's Cartesian path option. Conceptually: give it the goal pose,
and it returns a trajectory that follows a straight line, plus a
**fraction** telling you how much of that line it managed to plan before
hitting a joint limit or an obstacle (1.0 means the whole line).

```python
def cartesian_move_to(robot, arm, target_pose, label=""):
    """Move tool0 in a straight line to target_pose (a PoseStamped)."""
    arm.set_start_state_to_current_state()

    # Plan a Cartesian (straight-line) path for the tool0 link to the
    # target. max_step is how finely the line is sampled (1 cm here);
    # smaller = smoother but slower to compute.
    plan_result, fraction = arm.compute_cartesian_path(
        waypoints=[target_pose.pose],   # one waypoint = a straight segment
        max_step=0.01,                  # 1 cm resolution along the line
        jump_threshold=0.0,             # 0.0 disables the jump check (sim-safe)
    )

    # fraction is how much of the straight line was achievable (1.0 = all).
    if fraction > 0.95:
        robot.execute(plan_result, controllers=[])
        print(f"[{label}] straight-line move done ({fraction:.0%})")
        return True
    print(f"[{label}] only {fraction:.0%} of the path was reachable")
    return False
```

We require `fraction > 0.95` so we only execute if almost the entire
straight line is reachable; a short fraction means something is blocking
the way and we should not move.

### Attaching the grasped object to the gripper

Once the gripper closes on a product, MoveIt 2 should treat that product
as **part of the arm** — so the planner accounts for the can sticking
out of the hand and does not drive it into the shelf. That is an
**attached collision object**: the same shape, but parented to the
`tool0` frame so it moves with the gripper. When you let go, you
**detach** it (turn it back into a normal world object) and then, if it
has left the scene, remove it.

```python
def attach_object(robot, object_id="soup_can_400g"):
    """Tell MoveIt the gripper is now holding object_id, so the
    planner moves the held can along with the arm and avoids hitting
    things with it."""
    psm = robot.get_planning_scene_monitor()
    with psm.read_write() as scene:
        # link = the frame to attach to; touch_links = parts allowed to
        # touch the object without counting as a collision (the jaws).
        scene.process_attached_collision_object(
            link_name="tool0",
            object_id=object_id,
            touch_links=["gripper_left_finger", "gripper_right_finger"],
        )
        scene.current_state.update()
```

(The exact `moveit_py` call for attaching evolves between releases;
conceptually you always do the same thing — reparent the object to
`tool0` and list the gripper fingers as allowed-to-touch.)

Putting these together — obstacle-aware planning plus straight-line
approach plus attach — is everything the real pick and place need.
Section 5 assembles them.

---

## 5. Explanation of place-on-shelf code

This is the payoff: the project's two motion actions, `pick_product` and
`place_product`. The orchestration layer (Behavior Tree, see
[`../07-orchestration.md`](../07-orchestration.md)) calls these after
`navigate_to_shelf` has parked the base and `locate_slot` has found the
target slot; `verify_placement` checks the result afterward. Our job
here is only the arm motion.

Recall the inputs:

- The **grasp pose** (where to put `tool0` to grab the can) comes from
  the grasping layer ([`../06-grasping.md`](../06-grasping.md)).
- The **slot pose** (where on the shelf the can goes) comes from
  perception + the planogram ([`05-perception.md`](05-perception.md)).
- The SKU is **`soup_can_400g`**: a rigid cylinder of known size,
  grabbed by a side pinch of the parallel jaws.

We assume helper functions from sections 3 and 4 are available
(`plan_and_execute`, `cartesian_move_to`, `add_shelf_collision_object`,
`attach_object`) plus two obvious gripper helpers:

```python
def open_gripper(robot):
    """Plan+execute the gripper group to its 'open' named pose."""
    g = robot.get_planning_component("gripper")
    g.set_start_state_to_current_state()
    g.set_goal_state(configuration_name="open")
    plan_and_execute(robot, g, label="open gripper")

def close_gripper(robot):
    """Plan+execute the gripper group to its 'closed' named pose."""
    g = robot.get_planning_component("gripper")
    g.set_start_state_to_current_state()
    g.set_goal_state(configuration_name="closed")
    plan_and_execute(robot, g, label="close gripper")
```

### PICK = approach, grasp, attach, retreat

```python
from copy import deepcopy

def pick_product(robot, grasp_pose):
    """Pick one soup_can_400g from the tray.

    grasp_pose: a PoseStamped for tool0 at the grasp (from grasping layer).
    Returns True on success.
    """
    arm = robot.get_planning_component("arm")

    # 1. Make sure the hand is open before we approach.
    open_gripper(robot)

    # 2. Compute a "pre-grasp" pose: the grasp pose lifted 10 cm up, so
    #    we first move to a safe spot directly above the can, then come
    #    straight down. Approaching from above avoids clipping the tray.
    pre_grasp = deepcopy(grasp_pose)
    pre_grasp.pose.position.z += 0.10            # 10 cm above the grasp

    # 3. Free-space (OMPL) move to the pre-grasp pose. The planner is
    #    free to take any collision-free path here.
    arm.set_start_state_to_current_state()
    arm.set_goal_state(pose_stamped_msg=pre_grasp, pose_link="tool0")
    if not plan_and_execute(robot, arm, label="pick: to pre-grasp"):
        return False

    # 4. Cartesian straight-line APPROACH down to the grasp pose. A
    #    straight descent is predictable and won't swing into the tray.
    if not cartesian_move_to(robot, arm, grasp_pose, label="pick: approach"):
        return False

    # 5. Close the jaws on the can.
    close_gripper(robot)

    # 6. Attach the can to tool0 so the planner now carries it with the
    #    arm and avoids hitting things with the can.
    attach_object(robot, object_id="soup_can_400g")

    # 7. Cartesian straight-line RETREAT: lift straight back up to the
    #    pre-grasp height, clearing the tray before any wide motion.
    if not cartesian_move_to(robot, arm, pre_grasp, label="pick: retreat"):
        return False

    return True
```

Line by line:

- **Step 1** opens the gripper first. You never approach a grasp with a
  closed hand.
- **Step 2** builds a **pre-grasp** pose 10 cm above the grasp. The
  pattern "go above, then straight down" keeps the approach clean.
- **Step 3** is an ordinary OMPL plan to the pre-grasp pose — any
  collision-free path is fine because we are still well clear of the
  product.
- **Step 4** switches to a **Cartesian** move so the final descent onto
  the can is a straight line, not a curve.
- **Step 5** closes the jaws to grip.
- **Step 6** **attaches** the can to `tool0`. From here on, MoveIt 2
  plans as if the can is part of the arm, so it will not, say, drag the
  can through the shelf.
- **Step 7** retreats straight up to the pre-grasp height. Lifting
  straight out before any large motion avoids snagging the tray.

### PLACE = pre-place, guarded set-down, release, detach, retreat

The place is the careful half. The shelf and every already-placed
neighbor are in the collision world, and the descent must be a **guarded
set-down** — lower until the can lightly touches the shelf, then let go.

```python
def detach_object(robot, object_id="soup_can_400g"):
    """Release the can in MoveIt's model: turn it from an attached
    object back into a free world object, then leave it in the scene as
    a placed neighbor (so future plans avoid it)."""
    psm = robot.get_planning_scene_monitor()
    with psm.read_write() as scene:
        scene.process_attached_collision_object(
            link_name="tool0",
            object_id=object_id,
            detach=True,          # detach instead of attach
        )
        scene.current_state.update()


def place_product(robot, slot_pose):
    """Place the held soup_can_400g into its shelf slot.

    slot_pose: a PoseStamped for tool0 such that the can rests upright in
    the slot (from perception + planogram). Returns True on success.
    """
    arm = robot.get_planning_component("arm")

    # 0. The shelf and neighbors must already be in the scene. Ensure the
    #    shelf is present (idempotent ADD); locate_slot adds neighbors.
    add_shelf_collision_object(robot)

    # 1. Compute a "pre-place" pose: the slot pose lifted 12 cm up, a
    #    safe staging point above the target before the set-down.
    pre_place = deepcopy(slot_pose)
    pre_place.pose.position.z += 0.12            # 12 cm above the slot

    # 2. Free-space (OMPL) move to the pre-place pose. Because the can is
    #    attached and the shelf+neighbors are collision objects, the
    #    planner routes the whole arm-plus-can around them.
    arm.set_start_state_to_current_state()
    arm.set_goal_state(pose_stamped_msg=pre_place, pose_link="tool0")
    if not plan_and_execute(robot, arm, label="place: to pre-place"):
        return False

    # 3. Guarded set-down: Cartesian straight-line DOWN toward a pose
    #    just barely touching the shelf. We aim ~1 cm below the nominal
    #    slot pose so the can makes light contact rather than stopping in
    #    mid-air; the controller's force limit stops it on contact.
    set_down = deepcopy(slot_pose)
    set_down.pose.position.z -= 0.01             # 1 cm into the surface = light contact
    if not cartesian_move_to(robot, arm, set_down, label="place: set-down"):
        return False

    # 4. Open the jaws to release the can onto the shelf.
    open_gripper(robot)

    # 5. Detach the can in MoveIt's world model. It stays in the scene as
    #    a free object so it becomes a neighbor obstacle for the next can.
    detach_object(robot, object_id="soup_can_400g")

    # 6. Cartesian straight-line RETREAT back up to pre-place, lifting
    #    the empty gripper straight out without brushing the placed can.
    if not cartesian_move_to(robot, arm, pre_place, label="place: retreat"):
        return False

    return True
```

Line by line:

- **Step 0** makes sure the **shelf** is a collision object. `ADD` with
  the same `id` is safe to repeat — it just refreshes the box. The
  neighbors were added by `locate_slot` as it counted how many cans are
  already placed.
- **Step 1** builds the **pre-place** pose 12 cm above the slot — the
  staging point we descend from.
- **Step 2** is an OMPL plan to pre-place. This is the move that most
  needs the collision world: the arm is carrying the can (attached in
  the pick) and must thread it to a point above the slot **without**
  clipping the shelf edge or a neighbor. Because everything is in the
  scene, MoveIt 2 plans the whole arm-plus-can around the obstacles.
- **Step 3** is the **guarded set-down**. We target a pose ~1 cm
  *below* the nominal slot surface and descend in a straight Cartesian
  line. We do not actually expect to reach 1 cm down: the controller's
  force/effort limit makes the arm stop as soon as the can touches the
  shelf. Aiming slightly into the surface guarantees real contact
  instead of releasing in mid-air. This is the "light, controlled
  contact" the requirements demand.
- **Step 4** opens the jaws, releasing the can onto the shelf.
- **Step 5** **detaches** the can. Crucially we *leave it in the scene*
  as a free object, so when the next can is placed it is already a
  neighbor obstacle — that is how the robot avoids knocking over the
  cans it just placed.
- **Step 6** retreats straight up to pre-place, so the empty gripper
  lifts cleanly away without brushing the can it just set down. After
  this the Behavior Tree calls `verify_placement`, and the loop repeats
  for the next can.

### Why this shape, and what's next

Notice the symmetry: both moves are **OMPL to a staging pose →
straight-line Cartesian approach → gripper action → attach/detach →
straight-line Cartesian retreat**. Free-space planning covers the big,
unconstrained motion; straight-line Cartesian moves cover the delicate
final centimetres where predictability matters. The collision world —
shelf plus placed neighbors plus the attached can — is what keeps every
plan safe.

This whole layer is CPU-only and plans in seconds, which is fine for the
v1 cycle-time budget. If planning latency ever dominates, **cuRobo /
cuMotion** drops in as a GPU planner behind the same MoveIt 2 calls
(see [`../04-arm-motion-planning.md`](../04-arm-motion-planning.md)) —
no rewrite of the code above.

The one thing this layer does not do is decide *where* the can and slot
actually are; it trusts the poses handed in. Producing those poses — the
can's pick pose and the shelf slot — is the camera's job. Continue to
[`05-perception.md`](05-perception.md).
