# Layer 01 — Simulator & physics: the digital twin (only-code)

> **Job:** Stand up a virtual myCobot 280 and its workcell — vials,
> racks, tray, cameras — inside a physics simulator so the whole
> prep → load loop can be built, replayed, and de-risked in software
> alone.
>
> **Mode — only code.** No hardware is bought or wired. The simulator
> *is* the robot: a **digital twin** (a software model that mirrors the
> arm's geometry and physics) plus mock devices stand in for everything
> physical.

This layer is the foundation of the only-code folder. If the twin is
faithful, every layer above it — motion planning, perception, grasping,
orchestration — can be developed and tested against it without ever
touching the bench. The five candidates below are general-purpose robot
**simulators** (programs that model rigid-body physics, contacts,
sensors, and rendering). We judge them on fidelity, cost, hardware
needs, and how readily they already know about the myCobot 280.

## The five at a glance

| Framework | Role | Tier | One-liner |
|-----------|------|------|-----------|
| NVIDIA Isaac Sim | Photoreal GPU simulator + synthetic data | `Best-in-class` | Highest visual + sensor fidelity, but heavy and GPU-bound. |
| PyBullet | Lightweight Python physics engine | `Cheapest` | `pip install`, runs anywhere, tiny — fidelity is modest. |
| Gazebo Harmonic | ROS-native robotics simulator | `Best-practical` | Free, CPU-friendly, has myCobot/`mycobot_ros` assets. |
| MuJoCo | Contact-rich physics engine | `Alternative` | Best-in-class contacts for grasp tuning; not a full cell sim. |
| Webots | All-in-one desktop simulator | `Alternative` | Friendly, batteries-included; smaller ROS 2 ecosystem. |

## NVIDIA Isaac Sim

Isaac Sim is NVIDIA's robotics simulator built on the Omniverse
platform. It models physics with PhysX and renders with a real-time
**ray tracer** (a rendering method that traces light paths for
photoreal images). Crucially it supports **domain randomization** —
automatically varying lighting, textures, and object poses across many
runs so that perception trained or tested in sim is robust to the messy
real world. For an HPLC cell full of glossy glass vials and reflective
trays, that photoreal pipeline is genuinely useful.

Where it shines: nothing else on this list gets as close to
camera-accurate images, and its synthetic-data tooling can generate
thousands of labelled frames for the perception layer. It speaks USD
(a scene-description format) and has first-class connectors to ROS 2,
so the twin can drive the same middleware the rest of the stack uses.
For a vision-heavy task it is the most capable option here by a clear
margin.

Where it is bad versus the others: it is **heavy and proprietary**. It
effectively requires a recent NVIDIA RTX GPU (~$1,500+ of hardware) and
a large install, where **PyBullet** runs on any laptop and **Gazebo
Harmonic** runs happily on a CPU. Its licence and Omniverse dependency
make it the least portable choice, and its learning curve dwarfs
**Webots'**. For an only-code project whose goal is to *cheaply*
de-risk the loop, that weight is hard to justify unless photoreal
vision is the bottleneck — which, for a known-pose vial task, it
usually is not.

## PyBullet

PyBullet is a Python binding to the Bullet physics engine. It installs
with a single `pip install pybullet`, loads URDF models (the standard
XML format describing a robot's links and joints), and gives you a
scriptable simulation in a few lines of code. There is no project
structure to learn — you import it, spawn the arm, step the physics,
and read joint states.

Where it shines: it is the **cheapest and most frictionless** option,
full stop. It is free, has no GPU requirement, runs on a modest laptop,
and starts in seconds. That makes it ideal for fast unit-style checks —
"does this inverse-kinematics solution reach the rack nest?" — and for
reinforcement-learning loops where you need to step physics millions of
times. For early scripting of the myCobot 280's reach and joint limits
it is the quickest thing to reach for.

Where it is bad versus the others: its **fidelity is modest**. Rendering
is basic compared to **Isaac Sim**, its contact model is less refined
than **MuJoCo's** (which matters when you tune a delicate vial grasp),
and it has no native ROS 2 integration the way **Gazebo Harmonic** does
— you bridge it yourself. There is also no off-the-shelf myCobot cell;
you assemble the scene by hand. It is excellent as a throwaway physics
sandbox, weaker as the *system* twin the whole project lives in.

## Gazebo Harmonic

Gazebo Harmonic is the current long-term-support release of Gazebo, the
simulator most tightly woven into the ROS ecosystem. (Gazebo was
rewritten from "Gazebo Classic" into the modern "Ignition"/"gz" line;
Harmonic is a stable release of that line.) It models physics, sensors,
and worlds, and — most importantly here — the myCobot 280 already has
community URDF and Gazebo assets via `mycobot_ros`, so the twin is
largely a matter of loading existing files rather than modelling from
scratch.

Where it shines: it is the **best-practical** pick. It is free and
open-source, runs on a **CPU** (no expensive GPU), and integrates
natively with ROS 2 through `ros_gz`, which means the same Nav2/MoveIt
2-style middleware the upper layers use can drive the simulated arm
unchanged. Because real hardware is also typically driven through ROS 2,
a Gazebo-based twin is the smallest possible jump to the sibling
hardware mode. For a small team building a known-pose HPLC cell, it hits
the sweet spot of fidelity, cost, and ecosystem fit.

Where it is bad versus the others: its rendering is far from
**Isaac Sim's** photorealism, so it is a weaker source of training
images for vision. Its contact solver is serviceable but not as crisp
as **MuJoCo's** for fine grasp tuning. It is also heavier to install and
configure than **PyBullet** or **Webots**, and the Classic-to-Harmonic
transition means some online tutorials target the old version — a real
source of confusion. None of these outweigh the ROS-native + ready-asset
advantage for this project.

## MuJoCo

MuJoCo (Multi-Joint dynamics with Contact) is a physics engine prized
for fast, stable, accurate **contact** simulation — the physics of
things touching, gripping, and slipping. Once commercial, it is now
free and open-source under Google DeepMind, with a clean Python API and
its own MJCF model format (it can also import URDF).

Where it shines: its **contact dynamics are the best on this list**.
When the question is "will the gripper's jaws hold a smooth 2 mL glass
vial without crushing or dropping it," MuJoCo's solver gives more
trustworthy answers than **PyBullet's** or **Gazebo's**. It is also very
fast, which suits large-scale grasp search or learning. As a focused
tool for the grasping layer it is excellent.

Where it is bad versus the others: it is a **physics engine, not a full
cell simulator**. It has no built-in photoreal rendering like
**Isaac Sim**, no native ROS 2 plumbing like **Gazebo Harmonic**, and
no ready myCobot HPLC scene — you wire sensors, rendering, and
middleware yourself. That makes it a poor choice as the *system* twin
the whole only-code project runs in, even though it is the one you might
reach for to validate a single tricky grasp. Hence: Alternative, not the
backbone.

## Webots

Webots is a long-established open-source desktop simulator that bundles
physics, rendering, sensors, and a library of robot and sensor models
behind a friendly GUI. It aims to be **all-in-one**: install it, pick or
import a robot, and you have a working world without stitching pieces
together.

Where it shines: it is arguably the **gentlest on-ramp** here. The
editor, asset library, and documentation make it approachable for
newcomers, and it ships a ROS 2 interface (`webots_ros2`) so it is not
isolated from the wider stack. For getting *a* moving robot on screen
quickly — to teach the team or sketch the cell layout — it is pleasant
and low-friction.

Where it is bad versus the others: its **ROS 2 ecosystem and community
momentum are smaller** than **Gazebo Harmonic's**, which is the de-facto
ROS simulator and the one with ready `mycobot_ros` assets. Its rendering
trails **Isaac Sim**, its contacts trail **MuJoCo**, and it is heavier
than **PyBullet** for quick scripting. It does nothing badly, but on
every axis another tool here does that axis better — which is exactly
why it lands as an Alternative rather than the practical pick.

## Verdict

- **Best-in-class — NVIDIA Isaac Sim.** Unmatched photoreal rendering,
  sensor accuracy, and domain randomization for synthetic data; the
  right choice when vision fidelity is the limiting factor, accepting
  its GPU cost (~$1,500+) and proprietary weight.
- **Cheapest — PyBullet.** Free, `pip`-installable, GPU-free, and
  instant to script; ideal for fast reach/IK checks and learning loops,
  at the price of modest fidelity and no ready myCobot cell.
- **Best-practical — Gazebo Harmonic.** Free, CPU-friendly, ROS-native,
  and already supplied with myCobot/`mycobot_ros` assets, so it balances
  fidelity and cost while staying one short step from real hardware —
  the right backbone for the only-code twin.

## See also

- Folder overview: [`README.md`](README.md)
- Sibling mode (real arm in the loop):
  [`../02-code-plus-hardware/01-simulation-and-digital-twin.md`](../02-code-plus-hardware/01-simulation-and-digital-twin.md)
