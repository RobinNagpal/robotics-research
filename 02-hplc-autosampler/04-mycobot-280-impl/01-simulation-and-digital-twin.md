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
vision is the bottleneck — and Gazebo's rendering is enough to generate
the synthetic data our YOLO vial detector trains on, so for this
fixed-layout cell it usually is not.

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
hardware mode. For a small team building a fixed-layout HPLC cell, it hits
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
  the right backbone for the only-code twin. **Every use case below is
  built in Gazebo.**

## Realistic scenario & use cases

> **Why this matters for automation.** The digital twin is where each
> prep step is *proven before a cent is spent on hardware*. Every bad
> pour pose, every crushed vial, every clogged filter the twin catches
> in software is cost and risk removed from the real bench. This section
> makes that concrete by walking the **six core prep steps** — the same
> six from the [workflow primer](../03-hplc-workflow/README.md) —
> through the **Gazebo** twin, each shown on our two running samples:
> **paracetamol** (the clean, easy case) and **tomato ketchup** (the
> thick, messy case).

**The scenario.** The cell must prepare an overnight worklist that mixes
both sample types: a tray of **paracetamol** tablet solutions (an assay
of the in-house batch against four competitor brands) *and* a set of
**ketchup** extracts (several supplier batches tested for the
heat-marker chemical **5-HMF**). Paracetamol dissolves cleanly and
dilutes in one step; ketchup must be extracted, spun clear, and filtered
before it is even fit to enter a vial. Before buying a single myCobot,
the team builds and de-risks **every prep step, for both samples, in the
Gazebo twin** — the free, CPU-friendly, ROS-native backbone chosen in
the verdict above.

Each prep step becomes one **simulation use case**. The twin does not
model the *chemistry* (whether the powder truly dissolved, how much
5-HMF formed) — it models the **manipulation and choreography** around
it: reach the station, dispense the right volume, run the mock device,
honour the timing, assert the outcome. That manipulation is exactly the
part the robot must get right. Each physical device is stood in for by a
**mock station node** (`mock_dispenser`, `mock_mixer`, `mock_centrifuge`,
`mock_filter`, `mock_capper`, `mock_printer`) that publishes the same
ROS 2 topics its real counterpart would, so the loop built here transfers
to hardware unchanged.

| # | Prep step (use case) | What the Gazebo twin proves | Paracetamol vs ketchup |
|---|---|---|---|
| 1 | [Dissolution / extraction](../03-hplc-workflow/02-dissolution-and-extraction.md) | Reach the prep vessel, dispense solvent, run the mix/heat cycle, hit the dwell | Para: swirl & done; ketchup: warm, longer, then needs clarifying |
| 2 | [Dilution](../03-hplc-workflow/03-dilution.md) | Precise aliquot + top-up between vessels; dilution-factor bookkeeping | Para: one step to ~100 µg/mL; ketchup: 1:10–1:100, often two stages |
| 3 | [Filtering](../03-hplc-workflow/04-filtering.md) | Force-controlled push through the syringe filter; clog handling | Para: one clean filter; ketchup: centrifuge first, then filter |
| 4 | [Transfer to vial](../03-hplc-workflow/05-transfer-to-vial.md) | Aim over the narrow 2 mL vial mouth and dispense without a spill | Same pour; ketchup just has more vials to track |
| 5 | [Capping](../03-hplc-workflow/06-capping.md) | Align the cap and screw to the right torque (seal, don't crack) | Identical for both |
| 6 | [Labeling](../03-hplc-workflow/07-labeling.md) | Apply the barcode and log a unique Sample ID for traceability | Para: short IDs; ketchup: many supplier/batch/rep IDs |

The six sections below each unpack one use case, then give its **meta
code** (the pseudocode shape) and **real code** (illustrative ROS 2 /
Gazebo teaching code). Every mock station and topic name is shared with
the hardware mode, so what the twin proves, the bench inherits.

## 1. Dissolution & extraction in the twin

In the real lab this is the step that turns a weighed sample into a
liquid (see [Step 2 of the primer](../03-hplc-workflow/02-dissolution-and-extraction.md)).
The twin cannot decide *whether* the solid dissolved — that is chemistry
— so it proves the **manipulation**: drive the arm to the dispense
station, pour a measured volume of solvent into the prep vessel, carry
the vessel to the mock mixer/sonicator, switch on heat if the recipe
calls for it, and **wait on a flag** rather than a fixed sleep.

The two samples exercise different branches of the *same* code. For
**paracetamol**, the recipe is gentle: ~10 mL of methanol, no heat, a
short dwell, and `mock_mixer` raises `/prep/dissolved` quickly. For
**ketchup**, the recipe is harsher: a larger volume of water/acid, heat
**on**, and a much longer dwell before the flag rises — and the twin
proves that this longer warm detour still fits inside the cycle budget
and never desyncs the loop.

- **The moment:** before the bench exists, prove the arm can turn a
  weighed sample into a mixed prep liquid for *both* a clean drug and a
  messy food.
- **How:** a per-sample recipe (solvent, volume, heat, dwell) drives the
  dispense + mock mix; `/prep/dissolved` gates the handoff to dilution.
- **Edge case it survives:** ketchup's long warm extraction — the loop
  waits on the flag, so a slow extraction delays but never corrupts the
  run.
- **Value:** the pour-and-mix choreography and timing are proven per
  sample, in Gazebo, before a drop of solvent is poured for real.

### Meta code

```text
# launch the Gazebo cell: arm + prep vessels + mock_dispenser + mock_mixer
# look up the active sample's recipe:
#     paracetamol -> solvent=methanol,   volume=10 mL, heat=off, dwell=short
#     ketchup     -> solvent=water/acid, volume=25 mL, heat=on,  dwell=long
# move the arm to the dispenser; dispense `volume` into the prep vessel
# carry the vessel to mock_mixer; start the mix (with heat if the recipe says so)
# WAIT on /prep/dissolved == true   (mock_mixer raises it after the dwell)
# hand the mixed prep off to the dilution step (use case 2)
```

### Real code

Drives one sample's dissolution/extraction through the Gazebo mock
stations. **Illustrative teaching code** — re-verify before use; every
line is commented.

```python
import rclpy                                            # ROS 2 Python client library
from rclpy.node import Node                             # base class for a ROS 2 program
from std_msgs.msg import Bool, Float64, String          # device commands + the "dissolved" flag
import sys                                              # read the sample name argument

# the twin fakes the chemistry, but the *manipulation* a recipe implies is real
RECIPES = {
    "paracetamol": {"solvent": "methanol",   "volume_ml": 10.0, "heat": False},  # clean, quick
    "ketchup":     {"solvent": "water_acid", "volume_ml": 25.0, "heat": True},   # messy, warm
}


class DissolveStep(Node):                               # runs the dissolution/extraction step in sim
    def __init__(self, sample):                         # sample = "paracetamol" or "ketchup"
        super().__init__("dissolve_step")               # register on the ROS 2 graph
        self.r = RECIPES[sample]                        # pick this sample's recipe
        self.sample = sample
        self.dispense = self.create_publisher(Float64, "/mock_dispenser/volume_ml", 10)  # pour command
        self.mix = self.create_publisher(Bool, "/mock_mixer/run", 10)    # start/stop the mixer
        self.heat = self.create_publisher(Bool, "/mock_mixer/heat", 10)  # heat on/off (ketchup only)
        self.create_subscription(Bool, "/prep/dissolved", self.on_done, 10)  # the gate flag
        self.started = False                            # publish the start commands only once
        self.create_timer(1.0, self.start_once)         # give the graph a second to connect

    def start_once(self):                               # kick off the step once everything is up
        if self.started:                                # only on the first tick
            return
        self.started = True
        self.dispense.publish(Float64(data=self.r["volume_ml"]))  # arm pours solvent into the vessel
        self.heat.publish(Bool(data=self.r["heat"]))             # ketchup warms; paracetamol does not
        self.mix.publish(Bool(data=True))                        # start the mock mixer / sonicator
        self.get_logger().info(                                   # record what we asked for
            f"{self.sample}: dispensed {self.r['volume_ml']} mL {self.r['solvent']}, mixing")

    def on_done(self, msg):                             # fires when mock_mixer reports the dwell is over
        if msg.data:                                    # /prep/dissolved == true
            self.get_logger().info(f"{self.sample}: prep ready -> hand off to dilution")
            rclpy.shutdown()                            # step complete


def main():                                             # standard ROS 2 entry point
    rclpy.init()                                         # start the client library
    rclpy.spin(DissolveStep(sys.argv[1]))               # pass "paracetamol" or "ketchup"


if __name__ == "__main__":                              # run directly
    main()
```

## 2. Dilution in the twin

Dilution weakens the strong stock solution to a concentration the
detector can read, and — for the paracetamol comparison — brings every
brand to the *same* strength so the comparison is fair (see
[Step 3 of the primer](../03-hplc-workflow/03-dilution.md)). The twin
proves two things: that the arm can perform the **precise
aliquot-and-top-up** between vessels, and that the **dilution-factor
bookkeeping** is correct, because the final analysis multiplies that
factor back to recover the real amount.

**Paracetamol** needs a single, known step (the stock is brought to
~100 µg/mL). **Ketchup** is less predictable — the 5-HMF level is
unknown — so it is diluted harder (1:10 or 1:100), often in **two
stages**, which is gentler and more accurate than one big leap. The same
planner handles both: it splits any large dilution into ≤10× stages and
drives the mock liquid handler stage by stage.

- **The moment:** prove the arm can hit a target concentration for a
  known drug *and* for an unknown-strength food extract.
- **How:** a planner turns (stock, target) into a list of ≤10× stages;
  each stage commands an aliquot + a solvent top-up on the mock handler;
  the cumulative factor is logged.
- **Edge case it survives:** the 1:100 ketchup case — done as two 10×
  stages, not one error-prone 100× pour.
- **Value:** both the precise transfers and the factor record are proven
  in sim, where a mis-dilution costs nothing.

### Meta code

```text
# inputs: stock concentration, target concentration for the active sample
#     paracetamol -> target ~100 ug/mL  (one ~1:N stage)
#     ketchup     -> target lands 1:10..1:100  (split into <=10x stages)
# plan = split (stock/target) into stages each <= 10x
# for each stage:
#     command mock_handler: aliquot a small volume -> add solvent to the mark
#     multiply the running dilution_factor by this stage
# assert /prep/concentration is within tolerance of target
# record dilution_factor (the analysis multiplies it back later)
```

### Real code

Plans and runs the dilution on the Gazebo mock liquid handler.
**Illustrative teaching code** — re-verify before use; every line is
commented.

```python
import rclpy                                            # ROS 2 Python client library
from rclpy.node import Node                             # base class for a ROS 2 program
from std_msgs.msg import Float64                        # concentrations and stage factors
from std_msgs.msg import Float64MultiArray             # (aliquot_ml, solvent_ml) per stage
import sys

# realistic-ish demo targets (ug/mL); treat as illustrative, not a validated method
TARGETS = {"paracetamol": 100.0, "ketchup": 5.0}        # ketchup diluted much harder


def plan_dilution(stock, target, max_factor=10.0):      # split a big dilution into gentle <=10x stages
    stages, c = [], stock                               # c = current concentration as we step down
    while c / target > max_factor:                      # still too strong for a single stage?
        stages.append(max_factor)                       # do a 10x stage...
        c /= max_factor                                 # ...and update where we are
    stages.append(c / target)                           # final stage to land exactly on target
    return stages                                       # e.g. 500->5 ug/mL gives [10, 10]


class DiluteStep(Node):                                 # runs the dilution step in sim
    def __init__(self, sample, stock):
        super().__init__("dilute_step")
        self.target = TARGETS[sample]                   # this sample's readable target
        self.stages = plan_dilution(stock, self.target)  # the staged plan
        self.factor = 1.0                               # running dilution factor (multiply back later)
        self.cmd = self.create_publisher(Float64MultiArray, "/mock_handler/transfer", 10)  # to handler
        self.create_subscription(Float64, "/prep/concentration", self.on_conc, 10)  # handler reports
        self.create_timer(1.0, self.run_once)
        self.sample, self.started = sample, False

    def run_once(self):                                 # issue every stage once the graph is up
        if self.started:
            return
        self.started = True
        for f in self.stages:                           # walk the planned stages in order
            aliquot, total = 1.0, f                     # take 1 mL, make up to f mL -> a factor-of-f dilution
            self.cmd.publish(Float64MultiArray(data=[aliquot, total - aliquot]))  # (aliquot, solvent)
            self.factor *= f                            # accumulate the overall dilution factor
        self.get_logger().info(f"{self.sample}: dilution factor x{self.factor:.0f} -> target {self.target}")

    def on_conc(self, msg):                             # mock_handler publishes the achieved concentration
        if abs(msg.data - self.target) / self.target < 0.05:   # within 5% of target?
            self.get_logger().info(f"{self.sample}: hit {msg.data:.1f} ug/mL -> ready to filter")
            rclpy.shutdown()


def main():
    rclpy.init()
    # args: sample name, measured stock concentration (ug/mL)
    rclpy.spin(DiluteStep(sys.argv[1], float(sys.argv[2])))


if __name__ == "__main__":
    main()
```

## 3. Filtering in the twin

Filtering strains out solid bits so they cannot clog the column (see
[Step 4 of the primer](../03-hplc-workflow/04-filtering.md)). The twin
proves a **force-controlled push** through the syringe filter and, for
food, the **extra clarifying detour**. `mock_filter` publishes a rising
back-pressure on `/mock_filter/pressure` as liquid is pushed; the
controller must push hard enough to flow but stop before the pressure
exceeds the burst limit.

This is where the two samples diverge most. **Paracetamol** is already
near-clear: one filter, low steady pressure, done. **Ketchup** is full
of pulp, so the loop first sends the vessel to `mock_centrifuge` (spin,
then decant the clear top layer) and only *then* filters — and even
then, if the pressure climbs toward the limit, the twin proves the
recovery: stop, swap the filter (or re-centrifuge), and resume.

- **The moment:** prove the arm filters a clean drug in one push and
  survives a clogging food extract without bursting the filter.
- **How:** the push is force-limited against `/mock_filter/pressure`;
  ketchup gets a `mock_centrifuge` step first; a pressure spike triggers
  a filter swap.
- **Edge case it survives:** a ketchup clog mid-push — caught as a
  pressure ceiling, handled as a swap, not a burst.
- **Value:** the column-protecting step and its food-only detour are
  proven in sim before any real filter is touched.

### Meta code

```text
# if the sample is "ketchup":
#     move vessel to mock_centrifuge -> spin -> decant the clear supernatant
# attach the syringe filter; begin a force-limited push into the vial
# while pushing, watch /mock_filter/pressure:
#     pressure rising but < burst limit  -> keep pushing (normal)
#     pressure >= burst limit            -> STOP, swap filter / re-centrifuge, resume
# when the target volume has passed, the clean liquid is in the vial
```

### Real code

Force-limited filtering with a ketchup-only centrifuge detour and clog
recovery. **Illustrative teaching code** — re-verify before use; every
line is commented.

```python
import rclpy                                            # ROS 2 Python client library
from rclpy.node import Node                             # base class for a ROS 2 program
from std_msgs.msg import Bool, Float64                  # centrifuge trigger, push command, pressure
import sys

BURST_KPA = 250.0                                       # filter bursts above this back-pressure (demo)


class FilterStep(Node):                                 # runs the filtering step in sim
    def __init__(self, sample):
        super().__init__("filter_step")
        self.sample = sample
        self.spin = self.create_publisher(Bool, "/mock_centrifuge/run", 10)  # ketchup-only clarify
        self.push = self.create_publisher(Float64, "/mock_filter/push", 10)  # commanded push effort
        self.create_subscription(Float64, "/mock_filter/pressure", self.on_pressure, 10)  # feedback
        self.swaps = 0                                  # how many times we had to swap a clogged filter
        self.create_timer(1.0, self.start_once)
        self.started = False

    def start_once(self):                               # begin the step once the graph is up
        if self.started:
            return
        self.started = True
        if self.sample == "ketchup":                    # pulpy food must be clarified first
            self.spin.publish(Bool(data=True))          # spin down the solids, then decant (mock)
            self.get_logger().info("ketchup: centrifuged + decanted before filtering")
        self.push.publish(Float64(data=1.0))            # start a gentle, steady push

    def on_pressure(self, msg):                         # fires as mock_filter reports back-pressure
        if msg.data >= BURST_KPA:                       # about to burst -> this is a clog
            self.swaps += 1                             # count the recovery
            self.get_logger().warn(f"{self.sample}: clog at {msg.data:.0f} kPa -> swap filter #{self.swaps}")
            self.push.publish(Float64(data=0.0))        # stop pushing (protect the filter)
            self.push.publish(Float64(data=1.0))        # resume on the fresh filter
        elif msg.data < 0.0:                            # mock_filter uses -1 to signal "done"
            self.get_logger().info(f"{self.sample}: filtered clean (swaps={self.swaps}) -> ready to vial")
            rclpy.shutdown()


def main():
    rclpy.init()
    rclpy.spin(FilterStep(sys.argv[1]))                 # "paracetamol" filters in one push; "ketchup" may swap


if __name__ == "__main__":
    main()
```

## 4. Transfer to the vial in the twin

This is the canonical, project-defining motion: aim the clean liquid over
the **narrow 2 mL vial mouth** and dispense without spilling (see
[Step 5 of the primer](../03-hplc-workflow/05-transfer-to-vial.md)).
By this stage both samples are thin, clear liquids, so the **pour is the
same** — the difference is only that the ketchup job has more vials to
keep straight. The twin makes the vial mouth a small but **fixed,
millimetre-scale** target and asks the question the whole POC turns on:
*can the arm hit it reliably, every time?*

`mock_vial` publishes the achieved fill on `/vial/fill_ml` and a spill
flag on `/vial/spill` (raised by a simple contact check against the rim).
The twin asserts the fill reaches the target *and* the spill flag stays
false — across every vial in the tray.

- **The moment:** prove the arm can land liquid in the vial mouth
  repeatably — the single clearest test of positioning accuracy.
- **How:** command the pour pose over `mock_vial`; assert `/vial/fill_ml`
  reaches target and `/vial/spill` never goes true.
- **Edge case it survives:** a near-rim pour — the spill flag catches a
  miss in sim, where it costs nothing.
- **Value:** the positioning question is answered cheaply, on the clean
  paracetamol case first, before the messier food batches scale it up.

### Meta code

```text
# move the arm to the pour pose directly above mock_vial's mouth
# dispense toward the target fill (e.g. ~1.5 mL)
# while dispensing, watch:
#     /vial/fill_ml  -> climbing toward target  (good)
#     /vial/spill    -> must stay false         (a miss raises it)
# success = fill reached target AND spill never went true
# repeat for every vial in the tray (paracetamol: a handful; ketchup: many)
```

### Real code

Pours into the vial and asserts fill-without-spill. **Illustrative
teaching code** — re-verify before use; every line is commented.

```python
import rclpy                                            # ROS 2 Python client library
from rclpy.node import Node                             # base class for a ROS 2 program
from std_msgs.msg import Float64, Bool                  # pour command, fill feedback, spill flag
import sys

TARGET_ML = 1.5                                         # how full the vial should end (demo value)


class TransferStep(Node):                               # runs the transfer-to-vial step in sim
    def __init__(self, sample):
        super().__init__("transfer_step")
        self.sample = sample
        self.pour = self.create_publisher(Float64, "/mock_vial/pour_ml", 10)  # commanded pour volume
        self.create_subscription(Float64, "/vial/fill_ml", self.on_fill, 10)  # achieved fill level
        self.create_subscription(Bool, "/vial/spill", self.on_spill, 10)      # rim-miss detector
        self.spilled = False
        self.create_timer(1.0, self.start_once)
        self.started = False

    def start_once(self):                               # begin the pour once the graph is up
        if self.started:
            return
        self.started = True
        self.pour.publish(Float64(data=TARGET_ML))      # arm pours toward the target fill
        self.get_logger().info(f"{self.sample}: pouring {TARGET_ML} mL into the vial")

    def on_spill(self, msg):                            # raised if liquid contacts the rim, not the mouth
        if msg.data:
            self.spilled = True
            self.get_logger().error(f"{self.sample}: SPILL — pour pose missed the vial mouth")
            rclpy.shutdown()                            # fail fast: positioning needs fixing

    def on_fill(self, msg):                             # climbs as liquid enters the vial
        if not self.spilled and msg.data >= TARGET_ML - 0.05:   # reached target, no spill?
            self.get_logger().info(f"{self.sample}: filled {msg.data:.2f} mL cleanly -> ready to cap")
            rclpy.shutdown()


def main():
    rclpy.init()
    rclpy.spin(TransferStep(sys.argv[1]))


if __name__ == "__main__":
    main()
```

## 5. Capping in the twin

Capping seals the vial so it cannot spill or evaporate, and so the
machine's needle can later pierce the septum (see
[Step 6 of the primer](../03-hplc-workflow/06-capping.md)). This step
is **identical for paracetamol and ketchup** — same vial, same cap, same
motion — so the twin's job is to prove the **alignment and torque
control**: place the cap squarely, then screw to a torque that is *firm
enough to seal but gentle enough not to crack the glass or cross-thread*.

`mock_capper` reports the applied torque on `/capper/torque`. The twin
asserts the final seated torque lands inside an acceptance band: below
the band leaks, above it cracks. It is a small, repeatable, judgement-free
motion — exactly what an arm is best at — which is why the same code
serves both samples without a branch.

- **The moment:** prove the arm can seat a cap to the right firmness,
  every time, on every vial.
- **How:** ramp the mock-capper torque and stop inside the acceptance
  band `[lo, hi]`; assert the seated torque is in-band.
- **Edge case it survives:** an over-torque attempt — caught against the
  upper bound in sim, not as cracked glass on the bench.
- **Value:** a forgiving seal window is verified before hardware, so the
  first real cap is already a solved motion.

### Meta code

```text
# pick up a cap (septum already inside); place it squarely on the vial mouth
# screw down while watching /capper/torque ramp up
# stop the moment torque enters the acceptance band [TORQUE_LO, TORQUE_HI]
# assert seated torque is in-band:
#     < TORQUE_LO -> leaks (under-tight)
#     > TORQUE_HI -> cracks / cross-threads (over-tight)
# same routine for paracetamol and ketchup (identical vials + caps)
```

### Real code

Torque-banded capping shared by both samples. **Illustrative teaching
code** — re-verify before use; every line is commented.

```python
import rclpy                                            # ROS 2 Python client library
from rclpy.node import Node                             # base class for a ROS 2 program
from std_msgs.msg import Float64, Bool                  # screw command, torque feedback
import sys

TORQUE_LO, TORQUE_HI = 0.4, 0.7                         # acceptance band in N*m (demo values)


class CapStep(Node):                                    # runs the capping step in sim
    def __init__(self, sample):
        super().__init__("cap_step")
        self.sample = sample
        self.screw = self.create_publisher(Bool, "/mock_capper/screw", 10)   # start/stop screwing
        self.create_subscription(Float64, "/capper/torque", self.on_torque, 10)  # live torque
        self.create_timer(1.0, self.start_once)
        self.started = False

    def start_once(self):                               # place + begin screwing once the graph is up
        if self.started:
            return
        self.started = True
        self.screw.publish(Bool(data=True))             # arm seats the cap and screws down
        self.get_logger().info(f"{self.sample}: seating cap, ramping torque")

    def on_torque(self, msg):                           # fires as torque ramps up
        if msg.data >= TORQUE_HI:                       # over-tight -> would crack the glass
            self.screw.publish(Bool(data=False))        # stop immediately
            self.get_logger().error(f"{self.sample}: OVER-TORQUE {msg.data:.2f} N*m — crack risk")
            rclpy.shutdown()
        elif msg.data >= TORQUE_LO:                     # inside the band -> a good seal
            self.screw.publish(Bool(data=False))        # stop screwing, sealed
            self.get_logger().info(f"{self.sample}: capped at {msg.data:.2f} N*m -> ready to label")
            rclpy.shutdown()


def main():
    rclpy.init()
    rclpy.spin(CapStep(sys.argv[1]))


if __name__ == "__main__":
    main()
```

## 6. Labeling in the twin

Labeling marks each vial with a unique Sample ID so a result can always
be traced back to the right sample (see
[Step 7 of the primer](../03-hplc-workflow/07-labeling.md)). The
physical motion — pressing a sticky barcode roughly straight onto a vial
— is **forgiving**, so the twin's real focus is the **information**: that
every vial gets a *unique* ID, applied via `mock_printer`, and logged to
a `/traceability/log` topic the way a robot naturally keeps a perfect
record.

The two samples differ only in **bookkeeping load**. **Paracetamol** has
a handful of short IDs (`InHouse`, `BrandA`…`BrandD`, `Standard`,
`Blank`). **Ketchup** has many, structured IDs
(`Supplier1/batchA/rep1`…), so the risk of a duplicate or mismatch is
higher — exactly why the twin asserts **uniqueness** across the whole
tray before the run is allowed to proceed.

- **The moment:** prove every vial leaves the bench with a unique,
  logged ID — no duplicates, no mismatches.
- **How:** for each vial, command `mock_printer` to apply the barcode and
  publish the ID to `/traceability/log`; assert the set of logged IDs has
  no repeats and matches the worklist.
- **Edge case it survives:** the many-ID ketchup batch — a duplicate ID
  is caught in sim as a failed uniqueness assertion.
- **Value:** the traceability guarantee — the whole point of labeling —
  is verified automatically, turning a forgiving motion into a reliable
  record.

### Meta code

```text
# for each vial in the worklist (paracetamol: short IDs; ketchup: structured IDs):
#     command mock_printer to print + apply the barcode for that Sample ID
#     publish the Sample ID to /traceability/log
# collect every logged ID into a set
# assert: no duplicate IDs AND the set == the worklist's IDs
# only then is the tray cleared to load (use case in Layer 07)
```

### Real code

Applies labels and asserts unique, complete traceability. **Illustrative
teaching code** — re-verify before use; every line is commented.

```python
import rclpy                                            # ROS 2 Python client library
from rclpy.node import Node                             # base class for a ROS 2 program
from std_msgs.msg import String                         # the Sample ID to print and to log
import csv, sys                                          # read the worklist of IDs

# demo worklists: paracetamol's are short; ketchup's are structured and many
WORKLISTS = {
    "paracetamol": ["InHouse", "BrandA", "BrandB", "BrandC", "BrandD", "Standard", "Blank"],
    "ketchup":     ["Sup1/batchA/rep1", "Sup1/batchA/rep2", "Sup2/batchB/rep1",
                    "Sup2/batchB/rep2", "Standard", "Blank"],
}


class LabelStep(Node):                                  # runs the labeling step in sim
    def __init__(self, sample):
        super().__init__("label_step")
        self.ids = WORKLISTS[sample]                    # the IDs this tray must carry
        self.sample = sample
        self.printer = self.create_publisher(String, "/mock_printer/apply", 10)  # print + stick label
        self.log = self.create_publisher(String, "/traceability/log", 10)        # the audit record
        self.create_timer(1.0, self.run_once)
        self.started = False

    def run_once(self):                                 # label every vial once the graph is up
        if self.started:
            return
        self.started = True
        for sid in self.ids:                            # one label per vial
            self.printer.publish(String(data=sid))      # arm applies the barcode for this ID
            self.log.publish(String(data=sid))          # and logs it for traceability
        # the all-important checks: every ID unique, and the whole worklist covered
        unique = len(set(self.ids)) == len(self.ids)    # no duplicate Sample IDs?
        assert unique, f"{self.sample}: DUPLICATE Sample ID in worklist — traceability broken"
        self.get_logger().info(f"{self.sample}: {len(self.ids)} vials labelled, all IDs unique")
        rclpy.shutdown()


def main():
    rclpy.init()
    rclpy.spin(LabelStep(sys.argv[1]))                  # "paracetamol" or "ketchup"


if __name__ == "__main__":
    main()
```

## See also

- Folder overview: [`README.md`](README.md)
- The eight prep steps these use cases are built from:
  [`../03-hplc-workflow/README.md`](../03-hplc-workflow/README.md)
- [`foundation-models.md`](foundation-models.md) — this layer is
  also where you **train and evaluate VLA policies**: sim benchmarks
  (LIBERO/SIMPLER/ManiSkill, Isaac Lab) and **synthetic-demo
  generation** (NVIDIA GR00T is sim-native).
