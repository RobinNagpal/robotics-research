# Layer 01 — Robot bring-up & digital twin (code-plus-hardware)

> **Job:** Bring the real myCobot 280 to life — talk to its joints,
> publish its pose, and run a **digital twin** (a software model that
> mirrors the physical arm) alongside it so commands can be checked in
> software while the real hardware moves.
>
> **Mode — code plus hardware.** The physical arm is connected over a
> serial/USB link. This layer is the bridge between bench and code:
> drivers, calibration, and a twin kept **in sync** with the real arm.

Once hardware is real, "bring-up" means more than loading a model. You
must handle **serial latency** (the small, variable delay of sending
commands over a wire), **joint calibration and zeroing** (teaching the
arm where each joint's true zero is so software angles match reality),
the small arm's **physical limits** (~250 g payload, ~280 mm reach), and
**twin sync** (making sure the on-screen model reflects the real arm,
not a hopeful guess). The five tools below cover the driver, the SDK,
the controller framework, the twin, and the model/TF plumbing that ties
them together. (**TF** is ROS's system for tracking where every frame —
base, joints, gripper — sits relative to the others over time.)

## The five at a glance

| Framework | Role | Tier | One-liner |
|-----------|------|------|-----------|
| mycobot_ros + ros2_control | ROS 2 driver + controller stack | `Best-in-class` | Standards-based bring-up with twin, controllers, and TF. |
| pymycobot | Elephant's Python SDK | `Cheapest` | Direct serial control, minimal deps — but you build the rest. |
| ros2_control + hardware_interface | Controller framework, real backend | `Alternative` | The portable controller layer; needs a myCobot backend. |
| Gazebo Harmonic | Hardware-in-the-loop digital twin | `Alternative` | Mirrors the real arm for safe pre-checks; not a driver. |
| robot_state_publisher + xacro/URDF | Model + TF bring-up | `Alternative` | Publishes the arm's frames; foundation, not full control. |

## mycobot_ros + ros2_control

`mycobot_ros` is Elephant Robotics' official ROS package set for the
myCobot family: it ships the URDF/`xacro` model (an XML description of
the arm's links and joints), launch files, and a driver node that talks
to the arm. Paired with **`ros2_control`** — the standard ROS 2
framework for running controllers against hardware — it gives you a
complete, standards-based bring-up: joint-state feedback, position/
trajectory controllers, and the same interfaces the motion-planning
layer expects.

Where it shines: it is the **best-in-class** because it solves the whole
bring-up problem the *standard* way. The real arm appears to the rest of
the stack exactly as a simulated one would, so MoveIt 2 and the
orchestration layer need no special-casing. It publishes proper TF, so a
**Gazebo Harmonic** twin can mirror the live joint states for safe
pre-flight checks, and it gives a clean home for handling calibration
offsets and joint limits. For a team that wants the hardware to slot
into a ROS 2 architecture, nothing else here is as complete.

Where it is bad versus the others: it is the **heaviest to stand up**.
You need a working ROS 2 install, correct serial permissions, and
matching package/firmware versions — far more setup than a one-line
**pymycobot** script. The community packages can lag the latest ROS 2
release, and the `ros2_control` hardware interface for the 280 is
thinner than for industrial arms, so you may patch around serial-latency
quirks yourself. The payoff — standards, twin sync, reuse — is worth it
for the real build, but it is not the fastest way to make a single joint
move.

## pymycobot

`pymycobot` is Elephant Robotics' Python SDK. You `pip install
pymycobot`, open the serial port, and call methods like
`send_angles(...)` or `get_coords()` to command and read the arm
directly. There is no middleware in between — your script talks to the
firmware over the wire.

Where it shines: it is the **cheapest and most direct** path to a moving
arm. With minimal dependencies and no ROS 2 to configure, it is perfect
for the very first "is it alive?" bring-up: jog the joints, read angles,
confirm the serial link, and sanity-check **zeroing** by commanding a
known pose and eyeballing it. For quick scripts, calibration jigs, and
diagnostics it is the fastest tool on this list.

Where it is bad versus the others: it gives you **only raw control**.
There is no trajectory controller, no TF, no twin, and no clean hook
into MoveIt 2 the way **mycobot_ros + ros2_control** provides — you would
reinvent all of that yourself. Its blocking serial calls also expose
**latency** directly to your code, with no controller smoothing it out,
which is risky for coordinated motion. It is the ideal *first* tool and
a fine fallback, but a poor foundation for the full system — hence
cheapest, not best.

## ros2_control + hardware_interface

`ros2_control` is the general ROS 2 controller framework; its
**`hardware_interface`** is the abstraction layer where a specific robot
plugs in via a "system" plugin that reads joint states and writes
commands. In principle you write (or adopt) a myCobot hardware interface
that wraps the serial protocol, and then every standard controller —
joint-trajectory, position, velocity — works against the real 280
unchanged.

Where it shines: it is the **portable, future-proof controller layer**.
The same controllers run against the real arm, a **Gazebo Harmonic**
twin, or any other backend, so swapping sim for hardware is a config
change rather than a rewrite. It is the principled place to centralize
joint-limit enforcement and to absorb serial latency behind a steady
control loop, which raw **pymycobot** cannot do.

Where it is bad versus the others: by itself it is **incomplete for the
myCobot**. It is a framework, not a product — you still need a hardware
interface that speaks the 280's protocol, which in practice is exactly
what **mycobot_ros** bundles. Used alone you are building that backend;
used together with `mycobot_ros` it becomes the best-in-class pairing
above. On its own it is therefore an Alternative: necessary plumbing,
but not a turnkey bring-up.

## Gazebo Harmonic

Gazebo Harmonic is the ROS-native simulator (the modern "gz" line's
stable release). In hardware mode its role changes: instead of *being*
the robot, it runs as a **hardware-in-the-loop digital twin** beside the
real arm. Fed the live joint states the driver publishes, it shows a
synchronized model you can use to preview a planned trajectory for
collisions before it executes on glass and metal.

Where it shines: it is the **safety net for a real cell**. Because it
consumes the same TF and joint-state topics that `mycobot_ros`
publishes, keeping the twin **in sync** is mostly a matter of wiring,
and it lets you dry-run motions, visualize reach against the ~280 mm
envelope, and catch a bad plan before the real arm swings a vial into a
rack. It reuses the very same scene built in the only-code folder, so
the hardware project inherits that work.

Where it is bad versus the others: it is **not a driver** and does not
move the real arm — it only mirrors it. It cannot calibrate, zero, or
command hardware the way **mycobot_ros + ros2_control** or **pymycobot**
do, and a twin that silently drifts out of sync is worse than none. It
is an important companion to bring-up, not the bring-up itself, which is
why it sits as an Alternative here.

## robot_state_publisher + xacro/URDF

`robot_state_publisher` is the ROS 2 node that reads the arm's
`xacro`/URDF model plus its current joint angles and publishes the full
**TF** tree — the live transforms saying where the base, each link, and
the gripper are in space. `xacro` is a macro layer that keeps the URDF
maintainable. Together they are the model-and-frames foundation every
other tool here leans on.

Where it shines: it is **lightweight, universal, and indispensable**.
Without a correct URDF and a published TF tree, MoveIt 2 cannot plan,
RViz cannot draw the arm, and a **Gazebo Harmonic** twin has no geometry
to mirror. It is also where the arm's true **joint limits** and link
geometry are encoded, so getting it right underpins both calibration and
collision checking on the small 280.

Where it is bad versus the others: it is **only the skeleton**. It
publishes where the arm *says* it is but does not talk to hardware,
enforce control, run controllers, or close any loop — that is the job of
**mycobot_ros + ros2_control** or **pymycobot**. Feed it bad joint data
and it cheerfully publishes a wrong pose, so it is only as honest as the
driver behind it. Essential infrastructure, but not a bring-up solution
on its own — an Alternative that every other choice quietly depends on.

## Verdict

- **Best-in-class — mycobot_ros + ros2_control.** The standards-based
  bring-up: official driver and model joined to the standard controller
  framework, giving trajectory control, TF, twin sync, and clean reuse
  by the motion-planning layer — worth its heavier setup for the real
  build.
- **Cheapest — pymycobot.** A `pip install` and a serial port get the
  arm moving with minimal dependencies; perfect for first-light
  bring-up, jogging, and calibration checks, at the cost of doing
  controllers, TF, and twin yourself.
- **Best-practical — mycobot_ros.** Even without the full
  `ros2_control` stack, the official package gives the model, driver,
  TF, and ready twin assets in one place, balancing real-hardware
  control against effort — the pragmatic backbone for the cell.

## See also

- Folder overview: [`README.md`](README.md)
- Sibling mode (pure simulation, no hardware):
  [`../01-only-code/01-simulation-and-digital-twin.md`](../01-only-code/01-simulation-and-digital-twin.md)
