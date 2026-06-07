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

## Reach & collision validation

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
- **In the full loop:** the reachability map produced here fixes the bench
  layout — nest, tray, decapper, and dispenser positions — that Layers
  03–10 all assume; a nest the twin marks unreachable is one the worklist
  must never assign.
- **Value:** a bad geometry costs a relaunch, not a bent arm and a
  re-ordered fixture.

### Meta code

The shape of the reach/collision sweep, before any library detail:

```text
# load the cell world + the myCobot URDF into the physics sim          (the twin)
# attach a capped-vial model to the gripper so reach includes the payload
# for each nest/station pose in the bench layout:
#     solve inverse kinematics for the gripper to reach that pose       (joint angles)
#     if no IK solution exists -> mark the nest UNREACHABLE             (out of envelope)
#     else snap the joints there and step the physics                  (move the twin)
#         read the collision engine for arm<->instrument/rack contacts  (geometry check)
#         contact -> mark COLLISION, else -> mark OK
# write {nest: status} to a reachability map                           (feeds the worklist)
```

### Real code

A complete **PyBullet** reach-and-collision checker (PyBullet is this
layer's cheapest pick, ideal for IK/collision sweeps). **Illustrative
teaching code** — re-verify APIs before relying on it; every line is
commented.

```python
import pybullet as p                                   # the Bullet physics engine's Python API
import pybullet_data                                   # ships sample URDFs + a ground plane
import json                                            # to dump the reachability map at the end

ARM_URDF = "mycobot_280.urdf"                          # the twin's description (links + joints)
VIAL_URDF = "capped_vial.urdf"                         # a 2 mL vial model attached to the gripper
EEF_LINK = 6                                            # index of the gripper/flange link in the URDF
NESTS = {"A1": [0.18, 0.10, 0.08],                     # nest centres as [x, y, z] gripper targets...
         "D11": [0.26, -0.14, 0.08]}                   # ...(only two shown; populated for all 96)


def main():                                            # run the whole reach/collision sweep
    p.connect(p.DIRECT)                                # headless physics (no GUI) for a batch check
    p.setAdditionalSearchPath(pybullet_data.getDataPath())  # so plane.urdf etc. are findable
    p.loadURDF("plane.urdf")                           # a floor so nothing falls to infinity
    arm = p.loadURDF(ARM_URDF, [0, 0, 0.75], useFixedBase=True)   # the arm, bolted to the bench
    inst = p.loadURDF("instrument.urdf", [0.3, 0, 0.75], useFixedBase=True)  # the obstacle body
    vial = p.loadURDF(VIAL_URDF, [0, 0, 1.0])          # the payload, spawned then welded below
    p.createConstraint(arm, EEF_LINK, vial, -1,        # weld the vial to the gripper link so...
                       p.JOINT_FIXED, [0, 0, 0], [0, 0, 0.02], [0, 0, 0])  # ...reach includes it

    reach_map = {}                                     # nest -> "OK" | "UNREACHABLE" | "COLLISION"
    for name, target in NESTS.items():                 # test every nest in the layout
        joints = p.calculateInverseKinematics(arm, EEF_LINK, target)  # IK: angles to reach the nest
        if joints is None:                             # some IK backends return None on failure
            reach_map[name] = "UNREACHABLE"            # nest is outside the 280's envelope
            continue                                   # nothing to step; on to the next nest
        for j, angle in enumerate(joints):             # apply the IK solution joint by joint
            p.resetJointState(arm, j, angle)           # snap the twin into the reaching pose
        p.stepSimulation()                             # refresh contacts for the new configuration
        hits = p.getContactPoints(arm, inst)           # any arm<->instrument contact in this pose?
        reach_map[name] = "COLLISION" if hits else "OK"  # record the verdict for this nest

    with open("reach_map.json", "w") as fh:            # persist the result for the worklist builder
        json.dump(reach_map, fh, indent=2)             # human-readable map of nest -> status
    p.disconnect()                                     # tear down the physics server


if __name__ == "__main__":                             # run only when invoked directly
    main()                                             # ...do the sweep
```

## Synthetic perception data

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
- **In the full loop:** the labelled frames generated here are the
  training and test set Layer 04 uses to localize trays and verify fill,
  so this step sits upstream of every "where is the vial / is it full?"
  decision the live loop makes.
- **Value:** a dataset worth weeks of staged photography and hand-labelling
  appears overnight, covering corners real data rarely catches.

### Meta code

The shape of the synthetic-data generator, before any library detail:

```text
# for each frame we want to generate:
#     randomize the scene:
#         pick a random light direction + intensity                    (domain randomization)
#         choose which nests hold a vial and each vial's fill level     (presence + meniscus)
#         jitter the tray pose a few mm/deg                            (real racks aren't exact)
#     render an RGB image + a depth image from the overhead camera     (sensor #1 viewpoint)
#     read each spawned vial's true pose + fill from the simulator      (ground truth, free)
#     write the images + a label file {poses, fills}                    (one labelled sample)
# stop after N samples -> a labelled dataset for Layer 04               (no photography needed)
```

### Real code

A complete **PyBullet** domain-randomized dataset generator. **Illustrative
teaching code** — re-verify before use; every line is commented.

```python
import pybullet as p                                   # physics + a built-in camera renderer
import pybullet_data                                   # sample assets (plane, etc.)
import numpy as np                                     # arrays for the rendered images
import random, json, os                                # randomization, label files, paths

VIAL_URDF = "capped_vial.urdf"                         # the vial model placed into nests
NEST_XY = {"A1": (0.18, 0.10), "A2": (0.20, 0.10)}     # nest centres (x, y); ...all 96 in practice
OUT = "synthetic/"                                     # folder the dataset is written into


def render_one(i):                                     # build, render, and label a single frame
    p.resetSimulation()                                # clear the previous frame's scene
    p.loadURDF("plane.urdf")                           # neutral floor
    light = [random.uniform(-1, 1) for _ in range(3)]  # random light direction (randomization)
    labels = {}                                        # nest -> {pose, fill} ground truth
    for nest, (x, y) in NEST_XY.items():               # decide each nest independently
        if random.random() < 0.2:                      # ~20% of nests left empty (realistic tray)
            continue                                   # no vial here -> simply absent from the label
        p.loadURDF(VIAL_URDF, [x, y, 0.80])            # drop a vial into this nest
        fill = round(random.uniform(0.3, 1.0), 2)      # random fill (low = under-filled case)
        labels[nest] = {"pose": [x, y, 0.80], "fill": fill}  # record the ground truth
    view = p.computeViewMatrix([0.2, 0, 1.3], [0.2, 0, 0.8], [1, 0, 0])  # overhead camera pose
    proj = p.computeProjectionMatrixFOV(60, 1.0, 0.1, 2.0)  # 60 deg FOV, square frame
    _, _, rgb, depth, _ = p.getCameraImage(            # render the scene from that camera...
        640, 640, view, proj, lightDirection=light)    # ...640x640 RGB + depth with our light
    np.save(os.path.join(OUT, f"{i}_rgb.npy"), rgb)    # save the RGB frame (image input)
    np.save(os.path.join(OUT, f"{i}_depth.npy"), depth)  # save the depth frame (geometry input)
    with open(os.path.join(OUT, f"{i}.json"), "w") as fh:  # save the matching label file
        json.dump(labels, fh)                          # ground-truth poses + fills for this frame


def main():                                            # generate the whole dataset
    p.connect(p.DIRECT)                                # headless; we only need rendered pixels
    p.setAdditionalSearchPath(pybullet_data.getDataPath())  # find plane.urdf
    os.makedirs(OUT, exist_ok=True)                    # ensure the output folder exists
    for i in range(10000):                             # 10k labelled frames overnight
        render_one(i)                                  # ...one randomized, labelled sample each
    p.disconnect()                                     # done


if __name__ == "__main__":                             # run directly to build the dataset
    main()
```

## Fault-injection rehearsal

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
- **In the full loop:** the faults rehearsed here are exactly the
  exceptions Layer 07 must handle mid-run — dropped vial → re-pick, e-stop
  → safe-stop/resume — so this is where the overnight loop's recovery
  branches are proven before they are ever needed.
- **Value:** every recovery path is regression-locked before hardware, so
  the first real fault is one the cell has handled a hundred times.

### Meta code

The shape of the fault injector, before any library detail:

```text
# subscribe to the running loop's state (which vial, which phase)
# define a catalogue of faults, each a function that perturbs the twin:
#     drop_vial   -> delete the constraint welding vial to gripper       (a drop)
#     remove_vial -> delete a vial model from a nest                     (a missing vial)
#     stuck_cap   -> publish a high torque on /decapper/wrench           (a jammed cap)
#     trip_estop  -> publish False on /estop                             (an emergency stop)
# at a scripted (vial, phase) trigger -> fire the chosen fault           (exact, repeatable)
# observe orchestration's response, then assert the expected recovery    (a locked regression)
```

### Real code

A complete ROS 2 (`rclpy`) fault-injector node that fires scripted faults
into the running twin. **Illustrative teaching code** — re-verify before
use; every line is commented.

```python
import rclpy                                            # ROS 2 Python client library
from rclpy.node import Node                             # base class for a ROS 2 program
from std_msgs.msg import Bool, String                   # /estop (Bool) and the loop phase (String)
from geometry_msgs.msg import WrenchStamped             # the cap force-torque message type


class FaultInjector(Node):                              # fires scripted faults into the running twin
    def __init__(self):                                 # one-time setup
        super().__init__("fault_injector")              # register on the ROS 2 graph
        self.estop = self.create_publisher(Bool, "/estop", 10)   # to flip the safety line
        self.wrench = self.create_publisher(            # to fake the decapper's torque reading
            WrenchStamped, "/decapper/wrench", 10)      # same topic the real sensor would use
        self.script = {("V70", "transit"): self.trip_estop,   # e-stop mid-transfer of vial 70
                       ("V61", "decap"): self.stuck_cap}      # jammed cap while decapping vial 61
        self.fired = set()                              # triggers already fired (each fires once)
        self.create_subscription(                       # watch the loop announce its state...
            String, "/loop/phase", self.on_phase, 10)   # ..."V70:transit" style messages

    def on_phase(self, msg):                            # runs each time the loop reports its phase
        vial, phase = msg.data.split(":")               # "V70:transit" -> ("V70", "transit")
        key = (vial, phase)                             # the trigger key to look up in the script
        if key in self.script and key not in self.fired:  # a scripted, not-yet-fired fault?
            self.get_logger().warn(f"injecting fault at {key}")  # log it for the test record
            self.script[key]()                          # ...fire the matching fault function
            self.fired.add(key)                         # mark it fired so it happens only once

    def trip_estop(self):                               # the emergency-stop fault
        self.estop.publish(Bool(data=False))            # False = NOT clear -> gates must block motion

    def stuck_cap(self):                                # the jammed-cap fault
        w = WrenchStamped()                             # build an empty wrench message
        w.wrench.torque.z = 5.0                         # an abnormally high un-cap torque (N*m)
        self.wrench.publish(w)                          # publish so the grasp layer trips its limit


def main():                                             # standard ROS 2 entry point
    rclpy.init()                                         # start the client library
    rclpy.spin(FaultInjector())                         # run the injector until Ctrl-C
    rclpy.shutdown()                                     # clean shutdown


if __name__ == "__main__":                              # run directly
    main()
```

## See also

- Folder overview: [`README.md`](README.md)
- Sibling mode (real arm in the loop):
  [`../02-code-plus-hardware/01-simulation-and-digital-twin.md`](../02-code-plus-hardware/01-simulation-and-digital-twin.md)
- [`../foundation-models.md`](../foundation-models.md) — this layer is
  also where you **train and evaluate VLA policies**: sim benchmarks
  (LIBERO/SIMPLER/ManiSkill, Isaac Lab) and **synthetic-demo
  generation** (NVIDIA GR00T is sim-native).
