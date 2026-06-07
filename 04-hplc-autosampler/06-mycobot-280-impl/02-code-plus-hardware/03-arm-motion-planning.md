# Layer 03 — Arm motion planning (code-plus-hardware)

> **Job:** On the *real* myCobot 280, compute joint movements to
> reach vials and tray slots — and actually execute them on a small
> serial-driven arm, with real timing, real collisions, and real
> motor limits.

The planning math is almost identical to only-code mode, so this page
does not re-derive it. Instead it emphasises **what changes once a
physical arm is in the loop**. First, the same vocabulary (kept short;
see the only-code sibling for fuller definitions):

- **Kinematics / FK / IK** — the geometry of joints vs. gripper
  position; FK goes angles→pose, IK goes pose→angles.
- **Motion planning** — finding a collision-free path from start to
  goal.
- **Trajectory** — that path *with timing*, the thing a controller
  actually executes.

What is genuinely different on hardware:

- **Execution path.** In sim you "run" a trajectory and it just
  happens. On hardware the trajectory is streamed to a controller via
  the **`FollowJointTrajectory`** action (the standard ROS 2
  interface for "follow this timed joint path"), driven by
  **`ros2_control`** (the framework that talks to the arm's motor
  drivers). The plan must be *executable*, not just geometrically
  valid.
- **Controller latency.** The myCobot 280 is driven over a serial
  link to small hobby-grade servos. Command round-trips are slow and
  jittery (tens of milliseconds), so a trajectory that looked perfect
  in sim can lag, overshoot, or stutter. Plans should be conservative
  in speed and acceleration.
- **Real-time jogging.** Some steps (lining the gripper up over a
  vial, teleoperated nudges) want *continuous* velocity commands, not
  a fully pre-planned path. That is what **MoveIt Servo** provides.
- **Reachability & repeatability.** The 280 has a ~280 mm reach and
  modest, ~0.5–1 mm-class repeatability (re-check the spec). Poses
  that solve in IK may be near singularities or just inconsistent
  shot-to-shot, which matters when seating a vial precisely.
- **Collisions from real perception.** In sim, obstacles are known
  exactly. On hardware, the HPLC rack and tray enter the planning
  scene as **collision objects** derived from real sensors (a
  depth camera, fixtures), which are noisier and must be kept current.

## The five at a glance

| Framework | Role | Tier | One-liner |
|-----------|------|------|-----------|
| **MoveIt 2** | Full planning + execution | Best-in-class | Plans, checks collisions, and executes via ros2_control on the real arm. |
| **MoveIt Servo** | Real-time jog/teleop | Best-practical | Streams smooth velocity commands for jogging and servoing — the hardware-specific addition. |
| **KDL (orocos_kdl)** | Classic IK/FK library | Cheapest | Minimal kinematics with no stack; useful for quick IK on a constrained arm. |
| **Pinocchio** | Fast kinematics/dynamics | Alternative | Fast FK/IK/dynamics you script directly; pairs well with custom controllers. |
| **Tesseract** | Industrial planning environment | Alternative | Collision-aware industrial planning for crowded real cells. |

We swap Drake out (relative to the only-code five) for **MoveIt
Servo**, because on real hardware the ability to stream live velocity
commands matters more than research-grade offline optimization.
MoveIt 2 takes best-in-class and MoveIt Servo best-practical, since
Servo *is* MoveIt and the practical hardware win is having both
planned moves and real-time jogging from one stack.

## MoveIt 2

**What it is.** Same framework as in only-code mode — IK, collision
checking, planners, trajectory smoothing — but here its execution
side is the point. MoveIt 2 plans a timed trajectory and ships it to
the real arm through a **`FollowJointTrajectory`** action server
backed by **`ros2_control`**, which drives the myCobot 280's servo
controller.

**How it's good.** It closes the whole loop on hardware: plan around
the real (sensor-derived) HPLC rack, smooth into a trajectory, and
execute it on the physical arm with the *same code you proved in
sim*. That sim-to-hardware continuity is the biggest practical win —
you are not rewriting the planner when you move off the simulator.
MoveIt's time-parameterization also lets you cap velocity and
acceleration, which is exactly the knob you need to keep the slow
serial servos from overshooting.

**How it's bad (vs the other four).** Its planned-then-executed model
is *not* designed for continuous real-time correction — for live
jogging or teleop you reach for **MoveIt Servo** instead. It is far
heavier than **KDL** or **Pinocchio** if you only need an IK solve.
And against **Tesseract**, its default sampling planners can produce
less smooth paths in tight real-cell collision scenes. On a slow
serial arm a jerky sampling path is more noticeable than in sim, so
this is worth watching.

## MoveIt Servo

**What it is.** MoveIt Servo is a component of MoveIt 2 for
**real-time servoing**: instead of planning a whole path, it takes a
live stream of desired end-effector or joint velocities (from a
joystick, a teleop script, or a visual-servoing loop) and converts
them into smooth, collision-checked, singularity-aware joint commands
sent continuously to the controller.

**How it's good.** This is the piece that only earns its keep on real
hardware. For fine alignment — easing the gripper down onto a vial
cap, or nudging it over a tray slot — you want to command "move 2 mm
left, slower" in real time, not re-plan. Servo handles the IK,
clamps near singularities, and respects joint limits while doing it,
which protects the fragile 280 from commands that would stall or jerk
it. It complements **MoveIt 2**'s planned moves: plan the big
transit, servo the final approach.

**How it's bad (vs the other four).** It is *not* a planner — it will
not route the arm around the HPLC rack the way **MoveIt 2**,
**Tesseract** do; it only follows velocity commands locally and stops
if it would collide. It is more complex to set up and tune than the
plain kinematics of **KDL** or **Pinocchio**, and on the laggy serial
link its real-time guarantees are softened (latency eats into the
control loop). Use it for the last few centimetres, not for whole-
task planning.

## KDL (orocos_kdl)

**What it is.** The same small Orocos kinematics library described in
the only-code file: FK and numerical IK for a joint chain, almost no
dependencies, very mature.

**How it's good.** On hardware it remains the cheapest route to a
quick IK answer when you are writing a custom control script and do
not want the full MoveIt stack — for example, a tiny utility that
computes joint targets for a few fixed vial poses and feeds them
straight to **`ros2_control`**. Minimal footprint, well understood.

**How it's bad (vs the other four).** It does no planning and no
collision checking, so on a real cell it will cheerfully command a
path that rams the elbow into the rack — unlike **MoveIt 2**,
**Tesseract**. It has no execution glue of its own and no real-time
servoing like **MoveIt Servo**. Its numerical IK is slower and less
robust near singularities than **Pinocchio**, which matters more on
hardware where a failed or near-singular solve can stall a real
motor. Fine as a helper, not as the backbone.

## Pinocchio

**What it is.** The fast modern kinematics/dynamics library from the
only-code file — quick FK/IK/Jacobians/dynamics from a URDF, built to
run inside tight loops.

**How it's good.** On hardware its speed and clean dynamics make it a
strong match for *custom* control loops: if you are writing your own
velocity controller or a lightweight visual-servoing routine, calling
Pinocchio for IK and Jacobians every cycle is fast and numerically
sturdy — sturdier near singularities than **KDL**. It is the best of
the bare libraries when you are rolling your own real-time math
rather than using **MoveIt Servo**.

**How it's bad (vs the other four).** Like KDL, it is kinematics and
dynamics only — no planner, no collision avoidance, no ready-made
execution. You get none of **MoveIt 2**'s ros2_control integration or
**MoveIt Servo**'s ready-tuned real-time servoing for free; you build
that scaffolding yourself. For a small team that just wants the arm
moving safely on hardware, that DIY burden is why it sits at
*Alternative* rather than a recommended pick.

## Tesseract

**What it is.** The industrial motion-planning environment from the
only-code file: collision-aware, optimization-capable planning built
for crowded production cells, with its own scene model.

**How it's good.** If the *real* HPLC cell becomes tight and cluttered
— several racks, a wash station, fixtures crowding the 280's small
workspace — Tesseract's collision-aware, optimization-based planning
can produce smoother, safer real-world paths than **MoveIt 2**'s
default sampling planners. On a low-repeatability arm in a busy cell,
that path quality has real safety value.

**How it's bad (vs the other four).** It is *Alternative* because of
adoption cost: smaller community than **MoveIt 2**, fewer myCobot
examples, and execution wiring you must assemble yourself rather than
leaning on MoveIt's ros2_control path. It offers no real-time jogging
equivalent to **MoveIt Servo**, and it is far heavier than the
**KDL**/**Pinocchio** helper libraries. For our simple v1 bench its
industrial strengths are largely idle.

## Verdict

- **Best-in-class — MoveIt 2 (+ MoveIt Servo).** MoveIt 2 plans and
  executes the full loop on the real arm through
  `FollowJointTrajectory`/`ros2_control`, and Servo adds the
  real-time jogging that hardware actually needs. Together they cover
  both planned transit and fine approach.
- **Cheapest — KDL (or Pinocchio).** A bare kinematics library gives
  IK/FK for the 280 with almost no dependencies; pick Pinocchio when
  you want faster, sturdier math inside a custom control loop.
- **Best-practical — MoveIt 2.** Its configuration generates from the
  myCobot 280 URDF and it carries straight over from the only-code
  sim, so the same stack that planned in simulation now drives the
  hardware — with Servo handling the last-centimetre alignment.

Keep v1 simple: cap velocity/acceleration hard to respect serial-link
latency, drive planned moves with MoveIt 2, servo the final approach,
and defer Tesseract until the real cell is genuinely crowded.

> Note: reach (~280 mm), repeatability (~0.5–1 mm), and latency
> figures are approximate and arm-specific — re-check the myCobot 280
> datasheet before quoting them.

## See also

- Folder overview: [`README.md`](README.md)
- Sibling mode (pure simulation):
  [`../01-only-code/03-arm-motion-planning.md`](../01-only-code/03-arm-motion-planning.md)
- [`../foundation-models.md`](../foundation-models.md) — a VLA can emit
  **motions directly** on the real arm, competing with explicit MoveIt
  planning (or layered *under* MoveIt for collision safety); the learned
  alternative to this layer.
