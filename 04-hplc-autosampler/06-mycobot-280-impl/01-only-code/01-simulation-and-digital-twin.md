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

## Run the full prep→load loop in the twin

A lab assistant runs the same loop all day — prepare a vial, place it,
move to the next — batch after batch. The cell has to reproduce that
entire loop, and the twin is where developers watch it happen: spin up the
simulated cell and let it work a whole tray from the first vial to the
loaded autosampler, with no hardware in the room. This use case is that
end-to-end run — the smoke-test that proves the pick-drive-place loop
still holds together after a change.

The bigger experiment is the HPLC batch itself, simulated end to end.
Every other layer — perception, motion, grasping, gating, orchestration —
only proves its worth when they run together as the loop the assistant
performs; the twin is the only place that whole loop can be exercised
before hardware exists. Running it is how the team turns ten separate
layers into one working cell.

The lab assistant runs their loop hundreds of times a day. For the
developers, running the loop in the twin is the most frequent thing they
do — many times a day, on every meaningful change — because it's the
fastest way to see whether the cell as a whole still does its job. It is
the development equivalent of the assistant's per-vial cadence.

- **The moment:** after changing a layer, a developer needs to know the
  whole pick-drive-place loop still works — so they run a full tray in the
  twin.
- **How, in depth:** the twin launches the cell world and arm, and a
  scripted worklist drives the per-vial loop through every layer, with
  mock stations standing in for devices.
- **Edge case it survives:** a regression in one layer surfaces as a
  failed run here, not as a surprise on hardware — the loop breaks in sim
  where it's cheap.
- **Walkthrough:** (1) launch the twin (world + arm + sensor plugins +
  mock stations); (2) feed a worklist; (3) let orchestration run the
  per-vial loop end to end; (4) check the tray ends correctly loaded.
- **In the scene:** on screen the simulated arm works steadily down a tray
  — pick, decap, dispense, scan, place — vial after vial, the whole cell
  exercised in fast-forward with nothing real at risk.
- **Why it's done this way:** the layers only matter when they run
  together; the twin is the one place the full loop can be exercised
  repeatedly, cheaply, before any hardware exists.
- **In the full loop:** this *is* the full loop, run in simulation — every
  other layer is exercised through it, so it's the integration point the
  whole project is built around.
- **Value:** the entire pick-drive-place loop is provable on demand, in
  software, as often as the team changes the code.

### Meta code

This meta is integration, not a single algorithm: it stands up the whole
simulated cell and lets the real orchestration drive it through a
worklist, exactly as it would on hardware. It launches the Gazebo world
(bench, stations, sensor plugins), spawns the arm, starts the controllers,
and brings up the mock station nodes — so every topic and service the
upper layers expect exists.

With the cell alive, a worklist is fed in and the Layer 07 behaviour tree
begins ticking the per-vial loop: perceive, pick, decap, dispense, scan,
verify, place, repeat. Each layer does its real work against the simulated
devices, so the run exercises perception, motion, grasping,
identification, gating, and orchestration together rather than in
isolation.

Because nothing is real, the run is fast, repeatable, and free of risk — a
vial dropped in sim costs nothing, and the same tray can be run a hundred
times. The developer watches it interactively (or replays a recording) to
see where the loop succeeds or stalls.

The run ends by checking the simulated tray against the worklist: every
vial that should be loaded is in its slot, every quarantined vial
accounted for. That end-state check is what turns "it looked like it
worked" into a definite pass or fail. The run in pseudocode:

```text
# launch the twin: Gazebo world + arm + sensor plugins + mock station nodes
# wait until every expected topic/service is up                      (the cell is "alive")
# feed a worklist (the tray to build)
# start the Layer 07 behaviour tree; for each worklist row it ticks:
#     perceive -> pick -> decap -> dispense -> recap -> scan -> verify -> place
# let it run to the end of the worklist                              (the whole loop, in sim)
# assert the simulated tray matches the worklist                     (pass / fail)
```

### Real code

The harness that feeds a worklist and checks the tray once the loop has
run it. **Illustrative teaching code** — re-verify before use; every line
is commented.

```python
import rclpy                                            # ROS 2 Python client library
from rclpy.node import Node                             # base class for a ROS 2 program
from std_msgs.msg import String                         # publish the worklist; read placements
import csv, sys                                         # load the worklist; read the path argument


class WorklistRunner(Node):                             # feeds a worklist and checks the tray at the end
    def __init__(self, path):                           # path = the tray CSV to build
        super().__init__("worklist_runner")             # register on the ROS 2 graph
        self.expected = [r["slot"]                      # the slots that must end loaded...
                         for r in csv.DictReader(open(path))]  # ...one per worklist row
        self.loaded = set()                             # slots the loop reports as placed
        self.pub = self.create_publisher(String, "/worklist", 10)  # hand the tray to orchestration
        self.create_subscription(                       # the loop reports each placement...
            String, "/tray/placed", self.on_placed, 10)  # ...as a slot id
        self.started = False                            # so we publish the worklist only once
        self.create_timer(1.0, self.start_once)         # publish shortly after startup

    def start_once(self):                               # kick off the run once the graph is up
        if not self.started:                            # only on the first timer tick
            self.pub.publish(String(data=",".join(self.expected)))  # send the tray to build
            self.started = True                         # don't publish again

    def on_placed(self, msg):                           # runs each time the loop places a vial
        self.loaded.add(msg.data)                       # record the slot it just filled
        if set(self.expected) <= self.loaded:           # every expected slot now loaded?
            print("RUN PASSED: tray fully loaded")      # the end-state check succeeded
            rclpy.shutdown()                            # end the run cleanly


def main():                                             # standard ROS 2 entry point
    rclpy.init()                                         # start the client library
    rclpy.spin(WorklistRunner(sys.argv[1]))             # run until the tray is complete (or killed)


if __name__ == "__main__":                              # run directly: pass the worklist path
    main()
```

## Headless regression run in CI

A good lab doesn't just run samples — it runs controls and standards every
batch to prove the process itself is still working before trusting any
result. The cell's developers need the same assurance about their
software, and they get it from a headless regression: on every code
change, a machine runs the full prep→load loop in the twin, with no screen
and no human, and checks the tray came out right. It's the cell's "is the
process still valid?" control, run automatically.

The bigger experiment is, again, the simulated HPLC batch — but here it's
run as a gate on every commit rather than watched interactively. Because
the loop is exercised end to end automatically, a change that breaks any
layer is caught within minutes, in software, instead of weeks later on
hardware. The regression is what keeps the whole integrated loop
trustworthy as the code evolves.

A QC lab runs its controls every single batch — many times a day. The
headless regression runs even more often: on every push, every pull
request, every merge — potentially dozens of times a day across a team. It
is the most frequently-executed run of the whole loop, precisely because
it's automatic.

- **The moment:** a developer pushes a change; before it can merge, CI
  must prove the full loop still builds a correct tray.
- **How, in depth:** a CI job launches the twin headless (no GUI), runs a
  scripted worklist through the loop, and asserts the final tray, failing
  the build on any mismatch.
- **Edge case it survives:** a subtle regression that only shows up in
  integration — it fails CI here, blocking the merge, instead of reaching
  hardware.
- **Walkthrough:** (1) CI launches Gazebo headless; (2) runs the worklist
  runner; (3) the loop builds the tray; (4) the job exits non-zero if the
  tray isn't correct, failing the build.
- **In the scene:** no screen, no human — just a CI log scrolling as a
  simulated arm that no one watches loads a tray, ending in a green check
  or a red X.
- **Why it's done this way:** integration bugs are cheapest to catch
  automatically and early; gating every change on a full simulated run
  keeps the loop from silently rotting.
- **In the full loop:** this runs the entire loop, headless, as a guard on
  every change — the regression net under all the other layers.
- **Value:** every code change is proven against a full simulated run
  before it lands, so the integrated loop stays correct as it evolves.

### Meta code

This meta is the same end-to-end run as the interactive one, with two
changes that make it suitable as an automatic gate: it runs headless
(Gazebo with no GUI, so it works on a CI server) and it reports its
verdict as a process exit code (zero for pass, non-zero for fail) that CI
can act on.

A CI job checks out the change, builds the workspace, and launches the
twin headless. Once the cell is up, the same worklist runner from the
interactive case feeds a tray and drives the per-vial loop, but now with
no human watching — everything is asserted automatically.

The decisive step is the end-state assertion: the runner compares the
final simulated tray to the worklist and exits non-zero if any vial is
missing or misplaced. That non-zero exit is what fails the build and
blocks the merge.

Because the whole thing is scripted and deterministic, it can run on every
push, giving fast, repeatable feedback; a flaky or slow loop would
undermine the gate, so the run is kept lean. The regression in pseudocode:

```text
# (CI) check out the change + build the workspace
# launch the twin HEADLESS (Gazebo server only, no GUI)
# run the worklist runner on a fixed demo tray:
#     it drives the full per-vial loop through every layer
#     it asserts the final tray == the worklist
# exit code: 0 if the tray is correct, non-zero otherwise
# CI fails the build (blocks the merge) on a non-zero exit
```

### Real code

A CI test that runs the headless loop and fails the build if the tray is
wrong. **Illustrative teaching code** — re-verify before use; every line
is commented.

```python
import subprocess                                       # run the headless sim + runner as a process
import sys                                              # propagate the pass/fail exit code

WORKLIST = "trays/ci_demo.csv"                          # the fixed demo tray CI always builds


def test_full_loop_builds_tray():                       # the CI regression: run the loop, check the tray
    proc = subprocess.run(                              # launch the twin headless AND the runner...
        ["ros2", "launch", "hplc_sim", "ci_run.launch.py",  # a launch file that starts both...
         f"worklist:={WORKLIST}", "headless:=true"],    # ...with no GUI, on the CI demo tray
        timeout=600,                                    # cap the run so a hang fails rather than blocks
        capture_output=True, text=True)                 # collect logs for the CI report
    # the launch is configured to exit non-zero if the runner's tray assertion fails:
    assert proc.returncode == 0, (                      # a non-zero code means the tray was wrong...
        f"full-loop regression FAILED\n{proc.stdout}\n{proc.stderr}")  # ...fail the build, with logs


if __name__ == "__main__":                              # allow running it directly (not just pytest)
    test_full_loop_builds_tray()                        # raises AssertionError -> non-zero exit on fail
    sys.exit(0)                                         # explicit success exit for CI
```

## Fault-injection rehearsal

Every experienced lab assistant has a set of reflexes for when things go
wrong: a vial slips and they catch it or re-pour it, a cap won't budge and
they set that vial aside, someone walks into the bay and they stop what
they're doing. Those recoveries are second nature to a person but have to
be deliberately engineered into the cell. This use case is where that
happens — the twin stages dropped vials, missing vials, stuck caps, and
emergency stops *on purpose*, so the cell's recovery logic can be built
and proven against them.

The bigger experiment is the unattended overnight HPLC batch: the entire
value of automating prep is that the tray gets built correctly while no
one is watching. That only holds if the cell handles the mishaps the
assistant would otherwise catch by hand. Rehearsing each fault in
simulation is how the team makes sure a dropped vial becomes a re-pick and
an e-stop becomes a safe pause — rather than a corrupted tray discovered
in the morning.

For the lab assistant these mishaps are occasional but routine — a stuck
cap or a fumbled vial perhaps a few times a day across a busy bench, an
interruption now and then. The fault-injection rehearsal itself is run
repeatedly during development and regression-tested on every code change,
precisely so the cell is ready for the handful of real faults each day
will bring.

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

This pipeline is deliberately the inverse of normal control code: instead
of trying to make the cell succeed, it sets out to make it *fail*, on cue
and identically every time. It watches the running per-vial loop announce
its state — which vial, which phase — so that a fault can be fired at an
exact, repeatable moment rather than whenever a real mishap happens to
occur.

Behind it sits a small catalogue of fault functions, each of which
perturbs the twin in a way that mirrors a real failure: deleting the
constraint that holds a vial to the gripper reproduces a *drop*; removing
a vial model reproduces a *missing vial*; publishing an abnormally high
torque on the decapper's force-torque topic reproduces a *stuck cap*;
flipping the safety boolean reproduces an *emergency stop*. Each one drives
the very same topics a real sensor or event would, so nothing downstream
can tell the fault is staged.

A script maps "(vial, phase)" triggers to those fault functions, and the
injector fires each trigger exactly once when the loop reaches it. Because
the timing is exact, the nastiest cases — an e-stop in the same 200 ms a
vial is being released — become reproducible on demand, which no physical
bench can promise.

The payoff is that orchestration's recovery branches (re-pick a dropped
vial, safe-stop-and-resume on an e-stop, quarantine a bad vial) can be
exercised, observed, and locked in as regression tests before any hardware
exists — so the first time a real fault occurs, the cell has already
handled it a hundred times in simulation.

The injector in pseudocode:

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
