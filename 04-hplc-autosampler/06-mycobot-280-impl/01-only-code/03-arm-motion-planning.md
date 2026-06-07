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

## Collision-free pick/place across a crowded bench

A lab bench is a crowded, ever-changing place — racks, beakers, a waste
bin, a colleague's tray, and the instrument itself all share the same few
square feet. A lab assistant threads a vial through that clutter without
thinking, adjusting the path on the fly to avoid knocking anything over.
This use case is the cell doing the same: planning a collision-free route
for the arm from a rack nest to a tray slot, around whatever happens to be
on the bench today.

The bigger experiment is the HPLC batch, in which every one of the tray's
60–100 vials has to be carried from its rack to its slot, with stops at the
dispenser and cap station along the way. Each of those transfers is a
chance to clip a neighbour or strike the instrument; planning around the
actual obstacle layout is what turns "move the vial" into a safe,
repeatable motion rather than a gamble.

The assistant performs this navigate-and-place motion for essentially
every vial, plus every reagent and tool they reposition — easily a few
hundred times a day. The cell plans a fresh route just as often, on every
transfer, because the bench is never guaranteed to be exactly as it was a
minute ago.

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
- **Why it's done this way:** a bench is a shared human space that gets
  rearranged; hard-coding "safe" paths would make the cell brittle to any
  change and risk an expensive crash, so the planner reasons about the
  live obstacle set on every move.
- **In the full loop:** this is the transit half of every pick-and-place —
  after Layer 04 says where a vial is and Layer 05 picks it, this carries
  it across the bench to the dispenser or its tray slot without a crash.
- **Value:** the arm adapts to a bench that changed since yesterday instead
  of demanding a frozen world.

### Meta code

This meta hands the hard problem — "find a path that doesn't hit
anything" — to a dedicated motion planner (MoveIt 2) and concentrates on
feeding it an honest picture of the world. The planner can only avoid
obstacles it knows about, so the pipeline's first job is to keep a
*planning scene* that mirrors the real bench: the rack, the instrument
body, the decapper, the tray, and any extra obstacle like the newly-added
waste bin, each represented as a simple collision shape.

Critically, that scene is not static. Perception feeds obstacle updates in
as the bench changes, so when an operator slides a bin onto the workspace
overnight, the next plan accounts for it even though it was never in the
CAD model. This is what lets the cell adapt to a bench that changed since
yesterday rather than demanding a frozen, fully-specified world.

On a pick-or-place request, the pipeline sets the goal pose for the
gripper and asks the planner for a collision-aware path from the arm's
current configuration. The planner samples and checks candidate motions
against the scene; if it can find a clean route it returns a trajectory to
execute, and if every route is blocked it returns *nothing*.

That "no plan" outcome is a feature, not a crash: it is handed back to
orchestration, which can retry, wait, or flag the vial — so a blocked path
becomes a handled decision instead of a collision. The planner in
pseudocode:

```text
# build a planning scene: add rack, instrument, decapper, tray as collision boxes
# subscribe to perception's obstacle updates -> add/move the waste bin live
# on a pick/place request (goal_pose for the gripper):
#     plan from the live joint state with a collision-aware planner   (samples + checks scene)
#     no plan found -> return FAILURE to orchestration                (retry / flag, never crash)
#     plan found    -> execute the trajectory                         (joint by joint)
```

### Real code

A **MoveItPy** planner that keeps the scene honest and plans collision-free
moves. **Illustrative teaching code** — MoveIt's Python API drifts between
releases, so re-verify before relying on it; every line is commented.

```python
import rclpy                                            # ROS 2 Python client library
from rclpy.node import Node                             # base class for a ROS 2 program
from moveit.planning import MoveItPy                    # the Python entry point to MoveIt 2
from geometry_msgs.msg import Pose, PoseStamped         # poses for obstacles and the goal
from moveit_msgs.msg import CollisionObject             # an obstacle for the planning scene
from shape_msgs.msg import SolidPrimitive               # the box primitive for that obstacle


class CrowdedBenchPlanner(Node):                        # plans collision-free pick/place moves
    def __init__(self):                                 # one-time setup
        super().__init__("crowded_bench_planner")       # register on the ROS 2 graph
        self.moveit = MoveItPy(node_name="moveit_py")   # spin up MoveIt 2's planning components
        self.arm = self.moveit.get_planning_component("arm")  # the move group for the 6-DoF arm
        self.scene = self.moveit.get_planning_scene_monitor()  # owns the world the arm must avoid
        self._add_box("waste_bin", [0.30, -0.10, 0.95], [0.15, 0.15, 0.40])  # the new obstacle

    def _add_box(self, name, xyz, size):                # add one box obstacle to the planning scene
        obj = CollisionObject()                         # the message describing the obstacle
        obj.id = name                                   # a unique name so we can move/remove it later
        obj.header.frame_id = "base_link"               # poses are given in the arm's base frame
        box = SolidPrimitive()                          # the shape...
        box.type = SolidPrimitive.BOX                   # ...is a box
        box.dimensions = size                           # its [x, y, z] extents in metres
        pose = Pose()                                   # where the box sits
        (pose.position.x, pose.position.y, pose.position.z) = xyz  # box centre in the base frame
        obj.primitives = [box]                          # attach the shape...
        obj.primitive_poses = [pose]                    # ...at that pose
        obj.operation = CollisionObject.ADD             # ADD it into the scene (vs REMOVE / MOVE)
        with self.scene.read_write() as s:              # lock the scene for editing
            s.apply_collision_object(obj)               # the arm will now plan around this box

    def move_to(self, goal: PoseStamped) -> bool:       # plan + execute a move; True if it ran
        self.arm.set_start_state_to_current_state()     # plan from where the arm actually is
        self.arm.set_goal_state(pose_stamped_msg=goal, pose_link="gripper")  # the target pose
        plan = self.arm.plan()                          # run the collision-aware planner
        if not plan:                                    # planner found no collision-free path
            self.get_logger().warn("no plan -> back to orchestration")  # don't crash, hand back
            return False                                # orchestration will retry or flag the vial
        self.moveit.execute(plan.trajectory, controllers=[])  # follow the planned trajectory
        return True                                     # the move was executed
```

## Cartesian straight-line approach and retreat

Picking a 2 mL vial out of a packed rack is a precise, vertical motion — a
lab assistant lowers two fingers straight down into the nest, grips, and
lifts straight up, never swinging sideways into the vials packed
millimetres away. This use case captures exactly that: a controlled
straight-line descent into a nest and a straight-line lift out, kept
separate from the looser motion of carrying the vial across the bench.

The bigger experiment is the HPLC batch, where vials sit in dense racks
and in the autosampler tray with only millimetres of clearance between
them. A sideways nudge on the way in or out doesn't just risk the target
vial — it can topple a neighbour, spilling or contaminating a sample that
was already prepared. The straight-line entry and exit is what protects
the other 95 vials every time the arm services one.

The assistant makes this vertical pick-or-place motion on every vial they
handle — at least twice per vial, in and out — so hundreds of times a day.
The cell reuses the same constrained approach for every nest entry and
every tray placement, the most repeated precise motion in the loop.

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
- **Why it's done this way:** vials sit millimetres apart and a free-space
  planner is free to swing the gripper sideways on the way in;
  constraining the final approach to a straight line is what keeps the arm
  from knocking neighbours during the most delicate part of the move.
- **In the full loop:** the delicate ends of each move — the approach
  Layer 05 grasps on and the placement into a tray slot — are these
  straight-line segments, bracketing every pick and every place in the
  run.
- **Value:** tight nests are entered and exited without disturbing 95 other
  vials.

### Meta code

This meta splits a single "put the vial in the nest" motion into two very
different pieces, because they have different requirements. The long,
free-space part — carrying the vial across the bench to a point just above
the target nest — only needs to avoid obstacles, and is handled by the
ordinary collision-aware planner. The short, final part — dropping into
the nest and lifting back out — needs to be a perfectly straight vertical
line, and is handled differently.

For that final segment the pipeline asks MoveIt for a *Cartesian path*:
rather than letting the planner choose any joint motion, it specifies the
exact straight line the gripper tip must follow — same X and Y, only Z
changing — and the solver interpolates a trajectory that keeps the tool on
that line. This is what guarantees no sideways drift into the neighbouring
vials during the most delicate moment.

The Cartesian solver also reports how much of the requested line it could
actually achieve, as a fraction from zero to one. A descent that can't
reach full depth — because it would hit a joint limit or pass through a
singularity — comes back with a fraction below one, and the pipeline
treats that as a reason to abort the entry cleanly rather than force a
skewed, partial insertion.

The retreat is simply the mirror image: a straight pure-Z lift back out
before the next free-space transit begins. The entry in pseudocode:

```text
# free-space transit to the nest-top pose (just above the vial)       (collision-aware)
# build a pure-Z Cartesian path down:
#     waypoints = [nest_top, nest_top lowered by approach_z]           (no X/Y change)
#     compute_cartesian_path(waypoints, step, jump_threshold)          (follow the line)
#     fraction < 1.0 -> abort the entry (can't reach full depth)       (singularity / limit)
# grasp, then mirror the path upward for a straight retreat            (pure +Z translation)
```

### Real code

A node that asks MoveIt's Cartesian-path service for a pure-vertical
descent and refuses to force a partial one. **Illustrative teaching
code** — re-verify before use; every line is commented.

```python
import rclpy                                            # ROS 2 Python client library
from rclpy.node import Node                             # base class for a ROS 2 program
from geometry_msgs.msg import Pose                      # waypoints for the straight-line path
from moveit_msgs.srv import GetCartesianPath            # MoveIt's straight-line path service

APPROACH_Z = 0.05                                       # how far straight down to descend (metres)


class CartesianEntry(Node):                             # builds straight-down approach/retreat paths
    def __init__(self):                                 # one-time setup
        super().__init__("cartesian_entry")             # register on the ROS 2 graph
        self.cli = self.create_client(                  # client to MoveIt's Cartesian-path service
            GetCartesianPath, "/compute_cartesian_path")
        self.cli.wait_for_service()                     # block until MoveIt is up

    def straight_line(self, start: Pose, dz: float):    # request a pure-Z move of dz from start
        end = Pose()                                    # the single waypoint at the end of the line
        end.position.x = start.position.x               # same X (no sideways drift)...
        end.position.y = start.position.y               # ...same Y...
        end.position.z = start.position.z + dz          # ...only Z changes (down when dz < 0)
        end.orientation = start.orientation             # keep the gripper orientation fixed
        req = GetCartesianPath.Request()                # build the service request
        req.group_name = "arm"                          # plan for the arm move group
        req.link_name = "gripper"                       # the link that must follow the line
        req.waypoints = [start, end]                    # the two points defining the straight segment
        req.max_step = 0.005                            # interpolate every 5 mm along the line
        req.jump_threshold = 0.0                        # 0 = disable jump checking (teaching default)
        future = self.cli.call_async(req)               # send the request without blocking
        rclpy.spin_until_future_complete(self, future)  # wait for the computed path
        res = future.result()                           # response carries the trajectory + fraction
        return res.solution, res.fraction               # how much of the line MoveIt could follow

    def enter_nest(self, nest_top: Pose):               # descend into a nest only if fully reachable
        traj, frac = self.straight_line(nest_top, -APPROACH_Z)  # try a straight-down approach
        if frac < 0.99:                                 # MoveIt couldn't follow the whole line
            self.get_logger().warn(f"approach only {frac:.0%}; aborting entry")  # don't force it
            return None                                 # abort -> orchestration re-plans / flags
        return traj                                     # the full straight-down trajectory to run
```

## Replanning on a perception correction

A lab assistant constantly makes tiny corrections without noticing —
reaching for a vial, seeing it sits a little off from where they expected,
and adjusting their hand mid-reach to land on it cleanly. This use case is
the cell's version of that live correction: when the camera reports a vial
is a few millimetres from where the plan assumed, the arm bends its path
to the new position mid-motion instead of committing to the stale one and
missing the grip.

The bigger experiment is the HPLC batch, prepared from racks that humans
place by hand and that shift slightly over a long run. Those small
misalignments are normal, not errors; a cell that could only reach
exactly-predicted positions would fumble constantly. Tracking the camera's
latest estimate is what lets the arm grip a real, slightly-moved vial as
reliably as a perfectly-placed one.

For the assistant, these micro-adjustments happen on a large fraction of
reaches — many times an hour, all day. The cell replans on a correction
whenever perception refines a target, which over a full tray is routine
rather than exceptional, so the motion has to absorb the change smoothly
every time.

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
- **Why it's done this way:** perception keeps refining where things
  actually are, and a plan made a second ago can already be stale;
  replanning to the newest pose is how the arm stays accurate instead of
  committing to an out-of-date target and missing the grasp.
- **In the full loop:** this closes the loop with Layer 04 — perception's
  live corrections become motion here, so the arm tracks the real vial
  through the pick rather than the nominal one.
- **Value:** small real-world misalignments are absorbed live, not turned
  into missed grasps.

### Meta code

The re-planner's meta is about always acting on the freshest truth without
thrashing. It keeps two things in hand: the pose it is currently driving
the arm toward, and a handle on the trajectory the arm is actively
executing. When perception publishes a corrected target, the pipeline
compares it to the current goal.

If the correction is tiny — within a few millimetres — it is ignored,
because replanning for every sub-millimetre jitter would make the arm
hesitant and waste compute. Only a meaningful change triggers action,
which keeps the motion smooth while still honouring real corrections.

For a meaningful correction, the pipeline preempts rather than stops: it
cancels the in-flight trajectory goal and immediately plans a new one
*from the arm's live joint state* to the corrected pose. Planning from
where the arm actually is — not from where the old plan assumed it would
be — is what makes the new motion continue seamlessly instead of jerking
back to a start.

The new trajectory is then sent as the active goal, superseding the old
one through the controller's action interface, so the newest estimate
always wins; corrections arriving faster than plans complete simply chain,
each new goal replacing the last. The re-planner in pseudocode:

```text
# track the current target pose + the in-flight trajectory goal handle
# on a corrected target pose from perception:
#     if it differs from the current target by < epsilon -> ignore     (avoid churn)
#     else:
#         cancel the in-flight trajectory goal                         (preempt, no stop-start)
#         plan from the LIVE joint state to the corrected pose         (fresh + accurate)
#         send the new trajectory as the new active goal               (newest wins)
```

### Real code

A node that preempts the running motion onto perception's newest target.
**Illustrative teaching code** — re-verify before use; every line is
commented.

```python
import rclpy                                            # ROS 2 Python client library
from rclpy.node import Node                             # base class for a ROS 2 program
from rclpy.action import ActionClient                   # to send and cancel trajectory goals
from geometry_msgs.msg import PoseStamped               # perception's corrected target pose
from control_msgs.action import FollowJointTrajectory   # the arm controller's action interface
from moveit.planning import MoveItPy                    # to replan from the live joint state

EPS = 0.003                                             # ignore corrections smaller than 3 mm


class ReplanOnCorrection(Node):                         # preempts the arm onto the newest target
    def __init__(self):                                 # one-time setup
        super().__init__("replan_on_correction")        # register on the ROS 2 graph
        self.moveit = MoveItPy(node_name="replanner")   # MoveIt 2 planning components
        self.arm = self.moveit.get_planning_component("arm")  # the arm move group
        self.client = ActionClient(                     # action client to the trajectory controller
            self, FollowJointTrajectory,
            "/joint_trajectory_controller/follow_joint_trajectory")
        self.goal_handle = None                         # the in-flight goal we may need to cancel
        self.target = None                              # the pose we are currently driving toward
        self.create_subscription(                       # listen for perception's corrected poses
            PoseStamped, "/vial/corrected_pose", self.on_correction, 10)

    def on_correction(self, pose: PoseStamped):         # runs each time perception refines the target
        if self.target and self._close(pose, self.target):  # correction smaller than EPS?
            return                                      # ignore it -> avoid needless replanning
        self.target = pose                              # adopt the newer, more accurate target
        if self.goal_handle:                            # is a trajectory already running?
            self.goal_handle.cancel_goal_async()        # preempt it (newest goal wins)
        self.arm.set_start_state_to_current_state()     # plan from where the arm actually is now
        self.arm.set_goal_state(pose_stamped_msg=pose, pose_link="gripper")  # the corrected goal
        plan = self.arm.plan()                          # replan to the new pose
        if plan:                                        # a valid path exists
            goal = FollowJointTrajectory.Goal(          # wrap the joint trajectory as an action goal
                trajectory=plan.trajectory.joint_trajectory)
            self.goal_handle = self.client.send_goal_async(goal).result()  # make it the active goal

    def _close(self, a: PoseStamped, b: PoseStamped):   # are two target poses within EPS in XYZ?
        da, db = a.pose.position, b.pose.position       # shorthand for the two positions
        return (abs(da.x - db.x) < EPS and             # X within tolerance, and...
                abs(da.y - db.y) < EPS and             # ...Y within tolerance, and...
                abs(da.z - db.z) < EPS)                # ...Z within tolerance


def main():                                             # standard ROS 2 entry point
    rclpy.init()                                         # start the client library
    rclpy.spin(ReplanOnCorrection())                    # run the re-planner until Ctrl-C
    rclpy.shutdown()                                     # clean shutdown


if __name__ == "__main__":                              # run directly
    main()
```

## See also

- Folder overview: [`README.md`](README.md)
- Sibling mode (real hardware):
  [`../02-code-plus-hardware/03-arm-motion-planning.md`](../02-code-plus-hardware/03-arm-motion-planning.md)
- [`../foundation-models.md`](../foundation-models.md) — a VLA can emit
  **motions directly**, competing with explicit MoveIt planning here (or
  layered *under* MoveIt for collision safety); the learned alternative
  to this layer.
