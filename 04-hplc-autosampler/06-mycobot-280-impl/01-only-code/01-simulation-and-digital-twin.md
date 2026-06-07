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

## Realistic scenario & use cases

> **Why this matters for automation.** The digital twin is where the
> cell's value is *proven before a cent is spent on hardware*. Every
> mis-reached nest, every gripper crash, every bad bench layout the twin
> catches in software is cost and risk removed from the real build. This
> section makes that concrete: one complex scenario, then the distinct
> jobs this layer must do to serve it.

**The scenario.** A contract lab wants the cell to run an **overnight
96-vial worklist** that mixes **2 mL screw-cap and 11 mm crimp-cap vials**
across two rack types, with the dispenser station **12 cm further** from
the arm base than the previous layout. Two vials are deliberately
under-filled and one nest is left empty, to mimic a real tray. Before
buying a single myCobot, the team must answer: *does the arm reach every
nest, does it ever collide with the instrument, how long is the cycle,
and does the loop survive a vial that isn't where it should be?* All of
that is answered in the twin.

The twin must therefore serve several **distinct use cases**:

1. **Reach & collision validation.** Prove the arm can reach all 96 rack
   nests, the tray, the decapper, and the dispenser without
   self-collision or hitting the (static) instrument body, for *this*
   bench layout.
   - *How the solution handles it:* Gazebo Harmonic loads the myCobot
     URDF and the `hplc_cell.sdf` world, and a script commands each nest
     pose; Gazebo's collision engine flags any contact with the
     instrument mesh, so a bad layout shows up as a failed pose, not a
     bent arm.

2. **What-if layout planning.** Re-validate the whole cycle after moving
   the dispenser 12 cm — without rebuilding a physical bench.
   - *How:* the station pose is a single transform in the world SDF; edit
     it, relaunch, re-run the reach script. Iterating bench geometry
     costs seconds, not a workshop afternoon.

3. **Synthetic perception data.** Produce labelled RGB-D frames of vials
   in racks under varied lighting and fill levels to feed Layer 04.
   - *How:* the camera `<sensor>` plugins publish the same
     `/overhead/image_raw` + points topics a real camera would; for
     geometry-only labels Gazebo suffices, and when photoreal glass
     reflections matter the same scene swaps to **Isaac Sim** (the
     best-in-class pick) for domain-randomized frames.

4. **Fault-injection rehearsal.** Deliberately stage the empty nest, the
   two under-filled vials, a dropped vial mid-transfer, and an e-stop
   during a move, to prove orchestration + gates react correctly.
   - *How:* missing/under-filled vials are edits to the world's model
     list; a dropped vial is a scripted detach; the e-stop is the
     `mock_safety` node flipping `/estop`. Every fault is reproducible on
     demand — something no real bench can promise.

5. **Headless regression twin (CI).** Run the full prep → load loop
   automatically on every code change to catch breakages before they
   reach hardware.
   - *How:* Gazebo Harmonic runs **headless** (no GUI) in CI; a scripted
     worklist drives the loop and asserts the tray ends correctly loaded,
     turning the twin into a regression test the whole team relies on.

**Where the pick flexes.** The best-practical backbone (Gazebo Harmonic)
covers use cases 1, 2, 4, and 5 directly and cheaply. Only use case 3, at
its most demanding (photoreal glass), reaches for **Isaac Sim**; and the
one tricky grasp in the scenario — holding the under-filled, off-balance
vial without slip — is the moment you might validate in **MuJoCo** (best
contacts). The layering is deliberate: one free, CPU-friendly twin for
the system, two specialists swapped in only where their axis is the
bottleneck.

## Deep dive: the three highest-value use cases

The five above all matter; these three carry the most weight for the
digital twin, so each is worth unpacking.

### Reach & collision validation

- **The moment:** before a myCobot is ordered, the twin is asked to touch
  all 96 nests, the tray, the decapper, and the dispenser for *this*
  layout; nest D11 comes back unreachable and A1's approach clips the
  instrument housing.
- **How, in depth:** a script walks the worklist, solves IK and a short
  approach for each nest, and Gazebo's collision engine reports any
  contact with the static instrument/rack meshes — producing a
  reachability map of the bench, not a guess.
- **Edge case it survives:** a nest reachable empty-handed but *not* with
  a capped vial in the gripper — the test grasps a vial model first, so
  reach is checked with the payload that actually flies.
- **Walkthrough:** (1) load the world and URDF and grasp a capped-vial
  model so the payload is included; (2) for each of the 96 nest poses solve
  IK plus a short approach; (3) step physics and read the collision engine
  against the instrument and rack meshes; (4) write each nest's pass/fail
  and coordinates to a reachability map.
- **In the scene:** on screen the simulated myCobot swings from nest to
  nest across the virtual bench, a ghost-coloured collision mesh flashing
  red the instant a link grazes the instrument housing. No glass, no
  money, nothing real is at stake — it is pure geometry being
  interrogated, slot by slot, until the whole 96-nest grid is either green
  or flagged.
- **Why it's done this way:** the 280 has a small (~280 mm) reach
  envelope and the cell is dense, so whether every nest is even reachable
  is the make-or-break feasibility question — and it is far cheaper to
  settle in geometry than to discover a dead corner after the bench is
  built.
- **Value:** a bad geometry costs a relaunch, not a bent arm and a
  re-ordered fixture.

### Synthetic perception data

- **The moment:** Layer 04 needs labelled images but no real photos exist
  yet; the twin renders thousands of rack frames under varied light, fill
  levels, and pose jitter, each auto-labelled with ground truth.
- **How, in depth:** the camera plugins publish the same image/point-cloud
  topics a real camera would, while a domain-randomization loop varies
  lighting and which nests are filled; the simulator already knows every
  pose, so each frame ships a perfect label for free (Isaac Sim for
  photoreal glass).
- **Edge case it survives:** meniscus glare that fools a detector —
  randomizing light angle *generates* the glare cases, training against
  the failure that would otherwise appear only on the bench.
- **Walkthrough:** (1) randomize lighting, textures, and which nests are
  filled; (2) render an RGB and depth frame from the overhead camera
  plugin; (3) read every object's ground-truth pose straight from the
  simulator; (4) save the frame with its auto-generated label and repeat
  thousands of times.
- **In the scene:** the overhead camera view flickers through hundreds of
  variations a second — lights swinging angle, vials appearing and
  vanishing from nests, the tray nudged a few millimetres — while a folder
  of perfectly labelled images piles up beside it. The "lab" here is a
  rendering loop, manufacturing experience the real camera has not yet
  lived.
- **Why it's done this way:** perception needs labelled examples of the
  exact lighting and clutter it will face; collecting and hand-labelling
  those on a real bench is slow and never covers the rare cases, whereas
  the twin knows ground truth for free and can over-represent the hard
  ones.
- **Value:** a dataset worth weeks of staged photography and hand-labelling
  appears overnight, covering corners real data rarely catches.

### Fault-injection rehearsal

- **The moment:** the team must know the loop survives a dropped vial, a
  missing vial, a stuck cap, and an e-stop mid-motion — none of which a
  real arm will do on cue.
- **How, in depth:** each fault is scripted — a missing vial is a deleted
  model, a drop is a timed detach, a stuck cap is a torque the mock
  publisher emits, an e-stop is `mock_safety` flipping `/estop` — fired at
  an exact cycle point, repeatedly and identically.
- **Edge case it survives:** the *combination* (an e-stop in the same
  200 ms a vial is released) is reproducible on demand, so Layer 07's
  recovery is proven against the rare nasty interleavings.
- **Walkthrough:** (1) start the loop on a worklist; (2) at a chosen tick
  fire the fault — delete a vial, detach one mid-lift, emit a torque spike,
  or flip `/estop`; (3) record how orchestration reacts; (4) assert the
  expected recovery and keep it as a regression test.
- **In the scene:** mid-transfer the script yanks a vial out of the
  gripper and it tumbles through the simulated air; a heartbeat later the
  same run restarts and an `/estop` snaps the arm to a halt at exactly the
  wrong moment. Disasters a real lab dreads are staged on purpose, over and
  over, just to watch how the cell flinches.
- **Why it's done this way:** the cell's value is unattended overnight
  running, which only holds if it survives the faults that *will* happen;
  you cannot safely or repeatably trigger a dropped vial or a mid-motion
  e-stop on real glass, so sim is the only place to prove the recovery
  first.
- **Value:** every recovery path is regression-locked before hardware, so
  the first real fault is one the cell has handled a hundred times.

## Meta code

The shape of the best-practical twin (Gazebo Harmonic loaded from a
world file, the myCobot URDF spawned into it, plus the sensor plugins
that make each sensor appear as a ROS 2 topic), before any
library-specific detail:

```text
# launch Gazebo Harmonic with a world file describing the cell      (bench, lighting, physics)
# in that world, place the static furniture                          (rack, tray, decap/dispense stations)
# spawn the myCobot 280 from its URDF at a known bench pose          (the digital twin of the arm)
# attach sensor plugins so each sensor publishes a ROS 2 topic:
#     overhead depth_camera plugin     -> /overhead/image_raw + points (sensor #1)
#     station camera plugin            -> /station/image_raw           (sensor #2)
#     wrist camera plugin on the flange-> /wrist/image_raw             (sensor #3)
#     force-torque plugin on cap joint -> /decapper/wrench             (sensor #5)
#     base imu plugin                  -> /imu                         (sensor #12)
# start the ros_gz bridge so those gz topics cross into ROS 2         (one bridge per topic)
# mock the safety sensors as plain ROS 2 Bool topics                  (/estop, /door_closed, /light_curtain_clear)
# from then on every upper layer talks to topics, not to the simulator
```

## Real code

The best-practical pick is **Gazebo Harmonic** driven from a ROS 2
launch file via `ros_gz`. This is **illustrative teaching code**:
launch APIs, plugin names, and message names drift between versions, so
re-verify before relying on it. Every line carries an inline comment
explaining exactly what it does.

```python
import os                                            # read environment + build file paths to assets
from launch import LaunchDescription                 # the object a ROS 2 launch file must return
from launch.actions import IncludeLaunchDescription  # lets us start Gazebo's own launch file inside ours
from launch.launch_description_sources import PythonLaunchDescriptionSource  # how to load that .launch file
from launch_ros.actions import Node                  # an action that starts one ROS 2 node (a program)
from ament_index_python.packages import get_package_share_directory  # finds an installed package's files

# --- fixed, known facts about the cell and where its files live ---
WORLD = "hplc_cell.sdf"                               # the world file describing bench, lights, stations
ROBOT_URDF = "mycobot_280.urdf"                       # the arm description Gazebo spawns as the twin
SPAWN_XYZ = ["0", "0", "0.75"]                        # where on the bench to place the arm base (metres)


def generate_launch_description():                    # the function ROS 2 calls to get what to start
    pkg = get_package_share_directory("hplc_sim")     # locate our simulation package's installed files
    world_path = os.path.join(pkg, "worlds", WORLD)   # full path to the world file inside that package
    urdf_path = os.path.join(pkg, "urdf", ROBOT_URDF) # full path to the arm's URDF inside that package

    ros_gz = get_package_share_directory("ros_gz_sim")  # locate the ros_gz bridge/launch helper package
    gazebo = IncludeLaunchDescription(                # start Gazebo Harmonic by including its own launcher
        PythonLaunchDescriptionSource(                # tell ROS 2 the included file is a Python launch file
            os.path.join(ros_gz, "launch", "gz_sim.launch.py")),  # path to that stock launcher
        launch_arguments={"gz_args": f"-r {world_path}"}.items())  # -r = run immediately, with our world

    spawn = Node(                                      # a node that injects the arm into the running world
        package="ros_gz_sim", executable="create",    # ros_gz's "create" tool spawns a model into Gazebo
        arguments=["-file", urdf_path,                # the URDF file describing the model to spawn
                   "-name", "mycobot_280",            # the name the spawned arm will have in the world
                   "-x", SPAWN_XYZ[0],                # x position on the bench, in metres
                   "-y", SPAWN_XYZ[1],                # y position on the bench, in metres
                   "-z", SPAWN_XYZ[2]],               # z height (bench top), in metres
        output="screen")                              # print this node's logs to the terminal

    bridge = Node(                                     # the ros_gz bridge: copies gz topics into ROS 2
        package="ros_gz_bridge", executable="parameter_bridge",  # the standard topic-bridge executable
        arguments=[                                    # one entry per topic, with gz<->ros type mapping:
            "/overhead/image_raw@sensor_msgs/msg/Image[gz.msgs.Image",      # overhead camera (sensor #1)
            "/station/image_raw@sensor_msgs/msg/Image[gz.msgs.Image",       # station camera (sensor #2)
            "/wrist/image_raw@sensor_msgs/msg/Image[gz.msgs.Image",         # wrist camera (sensor #3)
            "/decapper/wrench@geometry_msgs/msg/WrenchStamped[gz.msgs.Wrench",  # cap force-torque (#5)
            "/imu@sensor_msgs/msg/Imu[gz.msgs.IMU"],   # base IMU reading (sensor #12)
        output="screen")                              # print the bridge's logs to the terminal

    # mock the safety sensors: plain Bool topics no real device backs yet (sensors #10/#11)
    estop = Node(package="hplc_sim", executable="mock_safety",  # a tiny node we wrote to fake safety state
                 name="mock_safety", output="screen")           # name it and show its logs on screen

    return LaunchDescription([gazebo, spawn, bridge, estop])  # hand ROS 2 the full list of things to start
```

The world file (`hplc_cell.sdf`) is where the sensor plugins actually
live — each camera, the force-torque sensor on the cap joint, and the
base IMU are `<sensor>` blocks in that SDF, which is what makes the
topics above exist. It is left out here to keep the launch file
readable, but it is the other half of the twin: the launch file *runs*
the world, the world *defines* the sensors that
[`../sensor-suite.md`](../sensor-suite.md) lists.

## See also

- Folder overview: [`README.md`](README.md)
- Sibling mode (real arm in the loop):
  [`../02-code-plus-hardware/01-simulation-and-digital-twin.md`](../02-code-plus-hardware/01-simulation-and-digital-twin.md)
- [`../foundation-models.md`](../foundation-models.md) — this layer is
  also where you **train and evaluate VLA policies**: sim benchmarks
  (LIBERO/SIMPLER/ManiSkill, Isaac Lab) and **synthetic-demo
  generation** (NVIDIA GR00T is sim-native).
