# Layer 03 — Arm motion planning (only-code)

> **Job:** In pure-simulation mode, compute the joint
> movements that swing the myCobot 280 arm from where it is to
> where a vial (or tray slot) needs it to be — without ever
> touching a real motor.

A quick vocabulary check before the comparison, because the rest of
this page leans on these terms (see also `../02-glossary.md` style
plain-language definitions):

- **Kinematics** — the geometry of how the arm's joints relate to
  where its hand ends up in space. No forces, just shapes and angles.
- **FK (forward kinematics)** — given the six joint angles, where is
  the gripper? This is the easy direction; there is exactly one
  answer.
- **IK (inverse kinematics)** — given a target gripper pose (a point
  in space plus an orientation), what joint angles get you there?
  Harder: there can be many answers, or none.
- **Motion planning** — finding a *whole path* of joint angles from
  start to goal that avoids collisions (with the bench, the HPLC
  rack, the arm itself).
- **Trajectory** — a planned path *with timing*: not just the
  sequence of poses but how fast to move through each, so the motors
  could in principle follow it smoothly.

In only-code mode there is no controller latency, no motor that
overshoots, no serial cable to drop packets. The simulator executes
whatever trajectory you hand it, more or less perfectly. So this
layer is really about *which library computes good, collision-free
trajectories fastest and with the least setup* for a small 6-axis
arm doing repetitive, well-defined vial moves.

## The five at a glance

| Framework | Role | Tier | One-liner |
|-----------|------|------|-----------|
| **MoveIt 2** | Full motion-planning stack | Best-in-class | Planning + collision + IK + ROS 2 ecosystem; the default everyone reaches for. |
| **KDL (orocos_kdl)** | Classic IK/FK library | Cheapest | Tiny, battle-tested kinematics chain solver with no heavyweight dependencies. |
| **Pinocchio** | Fast kinematics/dynamics | Best-practical | Blazing-fast FK/IK/dynamics you can script directly; minimal stack to stand up. |
| **Tesseract** | Industrial planning environment | Alternative | Strong collision-aware planning aimed at industrial cells; less ROS-default. |
| **Drake** | Modelling + optimization planning | Alternative | Research-grade optimization-based planning and simulation; powerful but steep. |

Tier note: MoveIt 2 wins *two* of the three named slots in this mode
(best-in-class and best-practical) because the same property — that
you can auto-generate its whole configuration from the myCobot URDF
— makes it both the most capable and the most pragmatic. The
"cheapest" slot goes to a bare kinematics library; either KDL or
Pinocchio qualifies, and we explain the trade between them below.

## MoveIt 2

**What it is.** MoveIt 2 is the standard motion-planning framework
for ROS 2 (Robot Operating System 2, the middleware these robots
talk over). You feed it a **URDF** — the XML file describing the
myCobot 280's links, joints, and limits — and it gives you IK,
forward kinematics, a self-collision and environment-collision
checker, a library of planners (OMPL sampling-based planners like
RRT and PRM, plus optional optimizers), and a trajectory smoother
that turns a raw collision-free path into a timed trajectory the arm
could follow. There is a setup assistant that reads the URDF and
generates almost all the configuration for you.

**How it's good.** For our shelf-of-vials task it is hard to beat on
*completeness*. The pick-move-place loop needs all of: solve IK to a
vial pose, check that the planned path does not clip the HPLC tray or
the bench, smooth it into a trajectory, and (later) hand that
trajectory to a controller. MoveIt 2 does every one of those out of
the box, and because it is the community default there are myCobot
280 URDFs, examples, and tutorials already floating around. In
only-code mode it pairs directly with Gazebo or Isaac Sim, so the
*exact same* planning code you debug in sim is what you later run on
hardware (covered in the sibling file). That continuity is the single
biggest reason to start here.

**How it's bad (vs the other four).** It is the heaviest of the five.
Compared to **KDL** or **Pinocchio**, which are single libraries you
can `import` and call in a few lines, MoveIt 2 drags in a large ROS 2
stack, a parameter/config tree, and a lifecycle you must understand
before anything moves — overkill if all you want is one IK solve.
Compared to **Tesseract**, MoveIt 2's planning is more
general-purpose and arguably less tuned for tight industrial
collision scenes (Tesseract was built around exactly that). And
compared to **Drake**, MoveIt 2's default planners are sampling-based
rather than optimization-based, so it will not give you the smooth,
cost-optimal trajectories Drake can when you are willing to pay the
modelling effort. For a 6-axis tabletop arm doing repetitive moves,
none of these weaknesses bite hard — but they are real.

## KDL (orocos_kdl)

**What it is.** KDL — the Kinematics and Dynamics Library from the
Orocos project — is a small, long-lived C++ library for chain
kinematics. You build a "chain" of joints and links and it computes
forward kinematics and inverse kinematics (via numerical solvers like
the Levenberg–Marquardt method) and basic dynamics. MoveIt has
historically used KDL as one of its IK plugins, so you are often
running it even when you think you are only running MoveIt.

**How it's good.** It is the cheapest possible way to get IK/FK for
the myCobot 280: no ROS node, no config tree, almost no dependencies,
and it has been stable for well over a decade. If your only-code task
at an early milestone is "given this vial pose, what joint angles?"
and you are scripting the rest of the loop yourself, KDL answers that
in a handful of lines and almost zero compute. It is small enough to
embed anywhere.

**How it's bad (vs the other four).** It is *just* kinematics. It has
no motion planner, so unlike **MoveIt 2**, **Tesseract**, or
**Drake** it will happily hand you a target pose with no awareness
that the straight-line path to it drives the elbow through the HPLC
rack — collision avoidance is entirely your problem. Its numerical IK
solver is also slower and less robust than **Pinocchio**'s modern
implementation, and it can fail to converge near singularities or
joint limits where Pinocchio's analytic Jacobians do better. Choose
KDL only when you want the absolute minimum and you will supply
planning yourself.

## Pinocchio

**What it is.** Pinocchio is a modern, very fast rigid-body
kinematics and dynamics library (the math engine under a lot of
current robotics research, including parts of the humanoid and
quadruped world). Like KDL it loads a URDF and gives you FK, IK
(through efficient Jacobian-based solvers), Jacobians, and full
dynamics — but it is engineered for speed and for being called inside
optimization loops.

**How it's good.** In only-code mode, where you may be running
thousands of IK or FK evaluations to test reachability across a whole
tray of vial positions, Pinocchio's speed is a genuine advantage over
**KDL**. It is still lightweight — a library you script against, not
a stack you deploy — so it shares KDL's "cheap and minimal" virtue
while being faster and numerically sturdier. That is why it earns the
*best-practical* slot here for teams who want to prototype the
kinematics of the cell quickly before committing to the full MoveIt
stack: it gives you correct, fast FK/IK with almost no ceremony.

**How it's bad (vs the other four).** Same core gap as KDL: it is a
kinematics/dynamics engine, **not** a motion planner. It will not
check collisions against the bench or plan a path around the HPLC
tray the way **MoveIt 2**, **Tesseract**, or **Drake** do — you would
bolt a planner (or your own collision checks) on top. It also lacks
MoveIt's ready-made ROS 2 integration and tutorials, so wiring it
into a full pick-place loop is more do-it-yourself. It is the right
tool for fast math, the wrong tool if you want batteries-included
planning.

## Tesseract

**What it is.** Tesseract is a motion-planning environment built for
industrial robotics. It bundles a collision-aware planning framework
(including trajectory-optimization planners such as TrajOpt) with its
own scene/environment model, and it is designed to handle complex
cells with many obstacles and tight clearances.

**How it's good.** Where it shines is exactly the hard-collision,
production-cell scenario: dense workspaces, tight tolerances, and
optimization-based planners that produce smooth, short trajectories.
For an HPLC cell that grew crowded — many racks, fixtures, and a
gantry around the arm — Tesseract's planning can outperform **MoveIt
2**'s default sampling planners on path quality, and it is more
purpose-built for that than the lightweight **KDL**/**Pinocchio**
libraries (which do no planning at all).

**How it's bad (vs the other four).** It is *Alternative*, not
default, because it is more niche and has a smaller community than
**MoveIt 2** — fewer tutorials, fewer myCobot examples, more setup to
get going. For our deliberately simple v1 (one arm, a sparse
benchtop, repetitive vial moves) its industrial strengths are mostly
unused, so it adds learning cost without much payoff. Versus
**Pinocchio**/**KDL** it is far heavier; versus **Drake** it is more
planning-focused but less of a full modelling/optimization
playground.

## Drake

**What it is.** Drake is a robotics toolbox (from the MIT/Toyota
lineage) centered on *model-based* design: high-fidelity multibody
modelling, simulation, and optimization-based motion planning and
control. It treats trajectory generation as a mathematical
optimization problem you can pose and solve precisely.

**How it's good.** When you genuinely need optimal, smooth, dynamics-
aware trajectories — say you later want the arm to move a full vial
of liquid without sloshing, expressed as constraints in an optimizer
— Drake is the most capable of the five. Its optimization-based
planning can express goals and constraints that **MoveIt 2**'s
sampling planners cannot easily, and its modelling is more rigorous
than anything in **KDL** or **Pinocchio** alone.

**How it's bad (vs the other four).** The learning curve is the
steepest here. Drake is research-grade: to get value you must frame
your problem in its optimization formalism, which is a lot of effort
for moving vials between known positions on a clean bench. It is less
plug-and-play with the ROS 2 / myCobot ecosystem than **MoveIt 2**,
heavier than **Pinocchio** or **KDL**, and less specialized for dense
industrial collision scenes than **Tesseract**. For v1 it is
overkill; we keep it as an *Alternative* to revisit only if the task
grows into something that needs true trajectory optimization.

## Verdict

- **Best-in-class — MoveIt 2.** It does the entire job (IK,
  collision-aware planning, trajectory smoothing) inside the ROS 2
  ecosystem everyone else uses, and the code carries straight over to
  hardware.
- **Cheapest — KDL (or Pinocchio).** A bare kinematics library gives
  you IK/FK for the 280 with almost no dependencies and almost no
  compute. Pick KDL for the absolute minimum; pick Pinocchio if you
  want the same minimalism but faster, sturdier math.
- **Best-practical — MoveIt 2.** Its whole configuration can be
  auto-generated from the myCobot 280 URDF, so the most capable
  option is also the fastest to stand up. (If you only need
  kinematics, not planning, Pinocchio is the practical sweet spot.)

Keep the v1 "keep it simple" framing: start with MoveIt 2 driving
sampling-based plans against a sparse scene, and defer Tesseract or
Drake's heavier optimization until the cell actually demands it.

> Note: tool maturity, speed claims, and ecosystem support drift over
> time — re-check before quoting any of the above as fact.

## Realistic scenario & use cases

> **Why this matters for automation.** Motion planning is where "move the
> vial" becomes a safe, collision-free, repeatable trajectory. Its
> automation value is that the arm reaches **every** nest and station
> **without being hand-taught each pose** and **without crashing** when
> the bench is crowded or a target shifts — the difference between a demo
> and an unattended overnight run.

**The scenario.** The arm must carry a capped 2 mL vial from **rack nest
A7**, past a **newly added decapper fixture** and a **tall waste bin** an
operator slid in overnight, to the dispenser, and finally into **tray
slot 12**. One nest sits near the edge of the 280's reach, so the only
valid arm configuration is close to a joint limit; the descent into each
nest must be **straight down** so the gripper doesn't clip neighbouring
vials; and once the vial is filled, the move must be **gentle enough not
to slosh**. Then perception (Layer 04) reports the vial is actually 8 mm
off the expected nest centre, and the plan must adapt. All of this is the
planner's job.

The layer must therefore serve several **distinct use cases**:

1. **Collision-free pick/place across a crowded bench.** Reach every nest
   and station without striking the racks, the instrument body, the
   decapper, or the new waste bin.
   - *How the solution handles it:* MoveIt 2 keeps a **planning scene**
     of those obstacles and runs a collision-aware sampling planner, so a
     blocked path returns *no plan* (handed to orchestration) instead of
     a collision.

2. **Cartesian straight-line approach and retreat.** Descend vertically
   into a tight nest and lift straight up — no lateral swing that knocks
   neighbours.
   - *How:* MoveIt 2's **Cartesian path** (`compute_cartesian_path`)
     produces a pure-translation segment for the final approach/retreat,
     separate from the free-space transit move.

3. **Replanning on a perception correction.** When the target shifts
   8 mm, plan again from the *current* state, fast, and supersede the old
   motion.
   - *How:* the corrected pose is a new planning goal; MoveIt plans from
     the live joint state and the new trajectory **preempts** the old one
     through the Layer 02 action interface — no stop-start jerk.

4. **Joint-limit and singularity-aware reach.** For the edge-of-workspace
   nest, choose an IK solution that stays within limits and avoids a
   near-singular pose.
   - *How:* MoveIt's IK respects the URDF joint limits and can seed/filter
     solutions; if none is valid it fails cleanly to orchestration rather
     than forcing a bad configuration.

5. **Slosh-aware, speed-limited transfer of a filled vial.** Once a vial
   holds liquid, cap velocity and acceleration so it doesn't spill.
   - *How:* MoveIt's **velocity/acceleration scaling** throttles the
     filled-vial moves; if true slosh constraints are ever needed, this is
     the one use case that would reach for **Drake**'s optimization.

**Where the pick flexes.** MoveIt 2 (best-practical) covers all five and
auto-configures from the myCobot URDF. If only kinematics were needed
(use case 4 in isolation), **Pinocchio/KDL** would do; if the bench grew
into a dense industrial cell (use case 1 at extreme clearances),
**Tesseract**'s optimization planners would earn their keep; and slosh-
constrained transfer (use case 5) is the trigger for **Drake**. The v1
cell needs none of those escalations — MoveIt 2 on a sparse scene is the
right tool.

## Deep dive: the three highest-value use cases

The five above all matter; these three carry the most weight for arm
motion planning.

### Collision-free pick/place across a crowded bench

- **The moment:** an operator slid a tall waste bin onto the bench
  overnight; the planner must still move vial A7 to slot 12 without
  striking it, the racks, the instrument, or the decapper.
- **How, in depth:** MoveIt 2 holds a **planning scene** of those obstacles
  and runs a collision-aware sampling planner; a path that can't clear the
  bin returns *no plan*, handed to orchestration to retry or flag rather
  than executed into a crash.
- **Edge case it survives:** an obstacle that *appears* mid-run — the scene
  is updated from perception, so the next plan accounts for the bin even
  though it wasn't in the CAD.
- **Walkthrough:** (1) perception adds the waste bin to the planning
  scene; (2) request a plan from A7 to slot 12; (3) the planner returns a
  collision-free path or none; (4) execute it, or hand a no-plan back to
  orchestration to retry or flag.
- **In the scene:** the planner mentally rehearses dozens of arm paths
  around the freshly-added waste bin before a single joint moves,
  discarding any that clip an obstacle; only a clean route from nest A7 to
  slot 12 is handed to the arm to actually fly.
- **Value:** the arm adapts to a bench that changed since yesterday instead
  of demanding a frozen world.

### Cartesian straight-line approach and retreat

- **The moment:** the gripper must drop vertically into a 16 mm-clearance
  nest and lift straight out; any lateral swing knocks the neighbours.
- **How, in depth:** `compute_cartesian_path` generates a pure-translation
  segment for the final approach and retreat, kept separate from the
  free-space transit move so only the delicate part is constrained.
- **Edge case it survives:** a Cartesian path that can't reach full depth
  (singularity/limit) returns a fraction-completed flag, so the cell aborts
  the entry cleanly rather than forcing a skewed insert.
- **Walkthrough:** (1) plan a free-space transit to just above the nest;
  (2) compute a pure-Z Cartesian approach down; (3) grasp the vial; (4)
  compute a pure-Z retreat back up before the next transit move.
- **In the scene:** the gripper hovers a few centimetres above a vial
  wedged among its neighbours, then descends dead straight down into the
  nest, fingers closing, and rises dead straight back out — no sideways
  drift that would clink the bottles packed beside it.
- **Value:** tight nests are entered and exited without disturbing 95 other
  vials.

### Replanning on a perception correction

- **The moment:** perception reports vial A7 is actually 8 mm off the nest
  centre after the rack shifted; the in-flight motion must adapt.
- **How, in depth:** the corrected pose becomes a new planning goal; MoveIt
  plans from the *live* joint state and the new trajectory **preempts** the
  old one through the Layer 02 action interface — no stop-start jerk.
- **Edge case it survives:** corrections arriving faster than plans
  complete — preemption means the newest goal always wins, so the arm
  tracks the latest estimate instead of chasing a stale one.
- **Walkthrough:** (1) perception publishes a corrected pose 8 mm over;
  (2) orchestration issues it as a new goal; (3) MoveIt plans from the live
  joint state; (4) the new trajectory preempts the old one through the
  Layer 02 action interface.
- **In the scene:** halfway to a nest a corrected target blinks in 8 mm to
  the side; the arm does not stop and restart — its path smoothly bends to
  the new goal mid-flight, chasing the latest truth the cameras just
  reported.
- **Value:** small real-world misalignments are absorbed live, not turned
  into missed grasps.

## Meta code

The shape of the best-practical pick (MoveIt 2, driven from Python
through `pymoveit2`): keep the planning scene honest about obstacles,
then plan and execute a collision-free move to a target pose.

```text
# subscribe to the target pose for the gripper            (e.g. a vial from Layer 04)
# tell MoveIt about the world the arm must avoid:
#     add the bench, the HPLC rack, and the tray as obstacles  (planning-scene boxes)
#     keep these updated as fixtures move or appear            (scene stays honest)
# on a new target pose:
#     ask MoveIt to plan a path from "here" to the target  (IK + collision-aware planner)
#     if no collision-free path is found:                  (planner returned nothing)
#         report failure and stop                           (-> orchestration retries)
#     otherwise execute the planned trajectory             (sim follows it, joint by joint)
#     wait until the motion reports done                   (then the next layer may grasp)
```

## Real code

A minimal but complete ROS 2 (`rclpy`) node using **MoveIt 2** via the
**`pymoveit2`** helper. This is **illustrative teaching code**: library
and message names drift between versions, so re-verify before relying on
it. Every line carries an inline comment explaining what it does.

```python
import rclpy                                      # ROS 2 Python client library (the robot framework)
from rclpy.node import Node                       # base class every ROS 2 program ("node") builds on
from geometry_msgs.msg import PoseStamped         # a 6-DoF pose + which frame + what time it is for
from pymoveit2 import MoveIt2                     # thin Python wrapper that drives MoveIt 2 planning
from pymoveit2.robots import mycobot280           # joint + link names for the myCobot 280 arm

# --- fixed, known facts about the cell the arm must not hit ---
RACK_BOX = ([0.20, 0.0, 0.10], [0.10, 0.30, 0.20])  # HPLC rack: centre (x,y,z) then size (dx,dy,dz), metres
BENCH_BOX = ([0.0, 0.0, -0.02], [1.00, 1.00, 0.04])  # the benchtop the arm stands on: centre then size, metres


class ArmMover(Node):                              # our motion-planning node, built on the ROS 2 Node class
    def __init__(self):                            # set-up that runs once, when the node is created
        super().__init__("arm_mover")              # register on the ROS 2 graph under the name "arm_mover"
        self.moveit2 = MoveIt2(                    # build the MoveIt 2 driver we will plan and execute with
            node=self,                             # let it publish/subscribe on this node's behalf
            joint_names=mycobot280.joint_names(),  # the six joints of the 280, in MoveIt's expected order
            base_link_name=mycobot280.base_link_name(),   # the fixed frame the arm is measured from
            end_effector_name=mycobot280.end_effector_name(),  # the gripper frame we want to place at a pose
            group_name=mycobot280.MOVE_GROUP_ARM)  # the planning group = just the arm (not the gripper)
        self.add_obstacle("rack", *RACK_BOX)       # tell MoveIt about the rack so plans steer clear of it
        self.add_obstacle("bench", *BENCH_BOX)     # tell MoveIt about the bench so plans steer clear of it
        self.sub = self.create_subscription(       # listen for a target gripper pose to move to
            PoseStamped, "/arm/target_pose",       # message type, then the topic Layer 04 publishes on
            self.on_target, 10)                     # call self.on_target per pose; 10 = inbox queue depth

    def add_obstacle(self, name, centre, size):    # register one box in MoveIt's planning scene
        self.moveit2.add_collision_box(            # push a collision box the planner must avoid
            id=name,                               # a unique name so we can move or remove it later
            position=centre,                       # where the box centre sits, in the base frame, metres
            size=size)                             # the box's full width/depth/height, in metres
        self.get_logger().info(f"scene: added {name}")  # log that the scene now knows about this obstacle

    def on_target(self, msg):                       # runs automatically each time a target pose arrives
        self.get_logger().info("planning to target")  # announce that we are about to plan a move
        self.moveit2.move_to_pose(                  # ask MoveIt to plan AND execute a path to this pose
            position=[msg.pose.position.x,         # target gripper position: left-right, metres
                      msg.pose.position.y,         # target gripper position: forward-back, metres
                      msg.pose.position.z],        # target gripper position: up-down, metres
            quat_xyzw=[msg.pose.orientation.x,     # target gripper orientation, as a quaternion (x...
                       msg.pose.orientation.y,     # ...y...
                       msg.pose.orientation.z,     # ...z...
                       msg.pose.orientation.w])    # ...w): which way the hand should point
        success = self.moveit2.wait_until_executed()  # block until the trajectory finishes; True if it ran
        if success:                                 # did MoveIt find a collision-free path and run it?
            self.get_logger().info("reached target")  # yes -> report success (Layer 05 may now grasp)
        else:                                       # no path, or execution was rejected
            self.get_logger().warn("plan/exec failed")  # warn so orchestration can retry or stop


def main():                                        # the standard ROS 2 program entry point
    rclpy.init()                                    # start up the ROS 2 client library (must come first)
    node = ArmMover()                               # build our node, which runs its __init__ set-up
    rclpy.spin(node)                                # keep handling target poses until you press Ctrl-C
    node.destroy_node()                             # remove the node from the graph on shutdown
    rclpy.shutdown()                                # close the ROS 2 client library cleanly


if __name__ == "__main__":                          # only run if this file is launched directly
    main()                                          # ...then start everything above
```

The single planning-scene box added above is the minimum; a real cell
keeps adding and updating boxes (tray, decapper, neighbouring vials) as
fixtures move, so every plan is checked against the *current* world. When
Layer 05 attaches a vial to the gripper it also updates this same scene,
so later moves know the arm is now carrying something.

## See also

- Folder overview: [`README.md`](README.md)
- Sibling mode (real hardware):
  [`../02-code-plus-hardware/03-arm-motion-planning.md`](../02-code-plus-hardware/03-arm-motion-planning.md)
- [`../foundation-models.md`](../foundation-models.md) — a VLA can emit
  **motions directly**, competing with explicit MoveIt planning here (or
  layered *under* MoveIt for collision safety); the learned alternative
  to this layer.
