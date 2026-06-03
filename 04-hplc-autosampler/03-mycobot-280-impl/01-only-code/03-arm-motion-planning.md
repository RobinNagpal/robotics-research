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

## See also

- Folder overview: [`README.md`](README.md)
- Sibling mode (real hardware):
  [`../02-code-plus-hardware/03-arm-motion-planning.md`](../02-code-plus-hardware/03-arm-motion-planning.md)
