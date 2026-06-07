# Layer 09 — Sensing & signal acquisition (only-code)

> **Job:** Make every sensor in the cell's suite *exist* — as a ROS 2
> (Robot Operating System 2) topic publishing the same data a real
> sensor would — and read each one reliably, entirely in simulation,
> with zero hardware purchased.

In "only-code" mode there is no physical sensor anywhere. Each one is
either a **Gazebo plugin** (a piece of the simulator that renders or
computes sensor data from the synthetic world) or a **mock ROS 2 topic**
(a small program that simply publishes plausible values). Either way the
rule is the same: the simulated sensor publishes on the **exact topic
name a real sensor would** — `/overhead/image_raw`, `/light_curtain_clear`,
`/balance/mass`, and so on — so every layer above it cannot tell, and
must not care, whether the bytes came from hardware or from a plugin.
That is the whole point of this layer: it is the *seam* the rest of the
cell is built on top of, proven in software first.

"Acquisition" here means two distinct things, and this layer owns both.
First, **making the sensor exist**: standing up the plugin or the mock
publisher so the topic appears on the ROS 2 graph at all. Second,
**reading it reliably**: subscribing to that topic, handling the case
where it is stale or silent, and handing a clean, current value to the
gate logic. A camera that publishes RGB-D (a colour image where every
pixel also carries a *depth* — how far it is from the camera) frames, an
IMU (Inertial Measurement Unit — the chip that reports tilt and
vibration) that publishes orientation, an e-stop button that publishes a
single true/false — all of them become, after this layer, just topics
you can read.

The canonical list of what must exist — all **12 sensors**, their topic
names, their simulation stand-ins, and rough costs — lives in
[`../sensor-suite.md`](../sensor-suite.md), and this layer is the code
that brings that list to life. Note especially the **two-witness habit**
from that doc: wherever a fact matters, it is confirmed by *two
independent sensors* before the workflow trusts it (e.g. "vial is held" =
gripper feedback **and** a wrist-camera glance). This layer's job is only
to deliver each witness as a readable topic; the *fusing* of two
witnesses into one verdict is the next layer,
[`10-sensor-fusion-and-gating.md`](10-sensor-fusion-and-gating.md).

## The five at a glance

| Framework | Role | Tier | One-liner |
|---|---|---|---|
| Gazebo sensor plugins (camera / depth / imu / force_torque / contact / logical_camera) | Render sensor data from the synthetic world | **Best-practical** | Free, physics-accurate sim sensors for cameras, base IMU, decap torque, presence — the bulk of the suite for `~$0`. |
| ros2_control (joint state + effort interfaces) | Joint feedback for gripper #4 and limit switches #9 | Recommended | The standard way to read joint position/effort; gives grip width, motor current, and home/end-stop state straight from the model. |
| Custom rclpy mock publishers (safety #10/#11, level #8, balance #6) | Fake the sensors that have no natural plugin | **Cheapest** | A few lines of Python publishing plausible values on the real topic names — for safety, level, and balance. |
| micro-ROS | Bridge a real microcontroller's sensors onto topics | **Best-in-class** | The genuine real-hardware acquisition path for tiny sensors; in only-code you stub it, but it is what you grow into. |
| ros_gz_bridge / sensor_msgs standard types | Carry sim sensor data into ROS 2 in standard message types | Alternative | The plumbing under everything else — translates Gazebo topics into ROS 2 `sensor_msgs` the rest of the stack expects. |

A **topic** is a named channel on the ROS 2 graph that one program
publishes to and any number read from; a **message type** (e.g.
`sensor_msgs/Image`, `std_msgs/Bool`) is the agreed shape of the data on
that channel. Sensing is, in the end, just choosing the right channel
name and message type for each of the twelve and filling it.

## Gazebo sensor plugins (camera / depth / imu / force_torque / contact / logical_camera)

Gazebo ships built-in **sensor plugins** that compute realistic sensor
output from the simulated world: a `camera` and `depth_camera` plugin
render RGB and RGB-D frames, an `imu` plugin reports the base link's
orientation and acceleration, a `force_torque` plugin reports the
wrench (force + torque) across a joint, a `contact` plugin fires when two
bodies touch, and a `logical_camera` reports which named models fall in a
view frustum. These cover, with no extra code, the *physical* sensors of
the suite — cameras **#1–#3**, the decapper torque sense **#5**, station
presence **#7**, the gripper grasp-contact half of **#4**, and the base
IMU **#12**.

Their strength over the other four options is **fidelity for free**.
Because the plugin reads the actual simulated geometry and physics, the
depth image genuinely reflects the modelled scene, the force-torque
reading genuinely reflects the modelled decap resistance, and the
logical-camera genuinely reflects whether a vial model is staged. A mock
rclpy publisher can only emit numbers you scripted; a Gazebo plugin emits
numbers the *world* produced, so it can surprise you in useful ways
(occlusion, a tipped vial, a missed contact) — exactly the cross-checks
the two-witness gates need. And it is `~$0`: every one is part of the
open-source simulator already chosen in Layer 01.

Its weakness, versus the others, is that a plugin only exists for sensors
that have a *physical analogue the simulator models*. There is no Gazebo
plugin for "is the safety light curtain clear?", "is the enclosure door
shut?", "is the e-stop pressed?", or "what mass does the analytical
balance read?" — those (#8, #10, #11, and the gravimetric side of #6)
have no natural geometry to render, so they fall to mock publishers
instead. Plugins are also bound to the simulator's update loop and
message conventions, so you still need the `ros_gz_bridge` plumbing below
to get their output into clean ROS 2 `sensor_msgs`. They are the
backbone of this layer, but not the whole skeleton.

## ros2_control (joint state + effort interfaces)

`ros2_control` is the standard ROS 2 framework for talking to a robot's
joints through a uniform set of **interfaces** — `position`, `velocity`,
and `effort` (the torque or current at a joint). In simulation it runs
against the model's joints exactly as it would against real servos,
publishing a `JointState` message that reports, per joint, where it is
and how much effort it is exerting. For sensing, that single stream is
what turns the **gripper** into a sensor: the jaw-width joint gives grasp
width, and the effort interface gives motor current — together the
"grasp success / grip force / slip" signal that is sensor **#4**.

Its strength here is that it reads feedback **the arm is already
producing**, with no separate sensor model to build. The same
`ros2_control` stack that *commands* the arm in Layer 02 also *reports*
joint state, so gripper feedback and the **homing / limit-switch** state
of sensor **#9** (is the arm at home? is a rail at its end-stop?) come
for free as joint-limit readings off the same bus. It is also the most
faithful of the five to how the real cell will work: on hardware this is
genuinely how you would read the gripper and the limit switches, so the
only-code code transfers almost unchanged.

Its weakness, against the Gazebo plugins, is that it only sees **joints**
— it knows nothing about cameras, the safety perimeter, liquid level, or
the balance, so it covers just two of the twelve sensors. And against a
plain mock publisher it is heavier: you must configure a controller
manager, a hardware (or simulation) interface, and a controller, which is
more moving parts than a six-line script that publishes a number. It is
the right tool for the joint-derived sensors and the wrong tool for
everything else — a precise, recommended *component*, not the backbone.

## Custom rclpy mock publishers (safety #10/#11, level #8, balance #6)

A custom **mock publisher** is the simplest possible sensor: a small
`rclpy` (the ROS 2 Python client library) node that, on a timer,
publishes a chosen value on the real sensor's topic. There is no plugin,
no physics, no model — just `create_publisher`, a timer, and a value.
This is how the sensors with *no natural simulator analogue* are stood
up: the safety **light curtain** and **laser scanner** (`/light_curtain_clear`,
sensor **#10**), the **door interlock + e-stop** (`/door_closed`,
`/estop`, sensor **#11**), the **liquid-level** reading (`/level`, sensor
**#8**), and the gravimetric **balance** mass (`/balance/mass`, sensor
**#6**, which the suite says reads the Part 04 fill-volume scalar as a
mass).

Its strength is being the **cheapest** and most controllable option by a
wide margin. A mock publisher is a few lines anyone can write and read,
costs `~$0`, runs on any machine, and — crucially for testing — lets you
*script the exact scenario* you want to prove: drop `/estop` to true at a
chosen moment and watch the gate logic halt; ramp `/level` past its limit
and watch the overfill branch fire; set `/balance/mass` to a wrong value
and confirm the two-witness fill check catches it. No plugin gives you
that on-demand control over a fault you want to rehearse.

Its weakness, versus the Gazebo plugins, is that the values are exactly
as smart as the script behind them — a mock publisher cannot *discover*
that a vial is tipped or that a hand crossed the perimeter, because it
has no view of the world; it only repeats what you told it. So for any
sensor that *does* have a physical analogue (the cameras, the IMU, the
force-torque), a plugin is strictly more honest and a mock is a
regression. Mock publishers are the right answer **only** for the four
sensors with no geometry to render, and lean on the discipline of also
feeding them ground truth from the sim where possible (e.g. driving
`/level` from the real fill scalar rather than a hand-typed constant).

## micro-ROS

**micro-ROS** is a port of ROS 2 that runs on **microcontrollers** — the
small, cheap chips (an ESP32, an STM32, a Teensy) that sit next to a
physical sensor and read its raw electrical signal. It lets such a chip
join the ROS 2 graph directly and **publish its sensor as a topic**, with
the same message types the rest of the stack uses, over a thin serial or
network link through a host-side **agent**. In the real cell this is the
genuine acquisition path for the small, off-the-shelf sensors — the
capacitive liquid-level probe, the photoelectric proximity switches, the
load-cell amplifier behind the decapper torque sense, an e-stop line.

It is **best-in-class** because it is the *real thing*, not a stand-in:
where a mock publisher only pretends sensor #8 or #11 exists, micro-ROS
is how that sensor will *actually* reach a topic once hardware arrives,
turning a millivolt off a capacitive probe into a `Float64` on `/level`
with proper timing and no PC in the tight loop. Designing the only-code
topics to match what a micro-ROS node will eventually publish means the
fusion and gate logic above never has to change when the stub becomes
silicon — the seam holds.

Its weakness in *only-code* is simply that there is no microcontroller to
run it on, so here it can only be **stubbed**: you mimic the topic a
micro-ROS node would publish (which is just a mock publisher again, under
a different banner) or run a software micro-ROS node with no real sensor
behind it. It also carries real-world fiddliness — agent setup, serial
transports, constrained memory on the chip — that buys you nothing until
hardware exists. So in this folder micro-ROS is the **direction**, not
the day-one tool: you build the mocks to *look like* its output, and swap
in the actual chips in the code-plus-hardware sibling.

## ros_gz_bridge / sensor_msgs standard types

`ros_gz_bridge` is the **bridge** that connects the Gazebo simulator's
internal transport to the ROS 2 graph: it translates a Gazebo sensor
topic into a standard ROS 2 topic carrying a standard **`sensor_msgs`**
message — `sensor_msgs/Image` for a camera, `sensor_msgs/Imu` for the
IMU, `sensor_msgs/PointCloud2` for depth, `geometry_msgs/WrenchStamped`
for force-torque. It is less a *source* of sensing than the *plumbing*
that carries the Gazebo plugins' output into the form the rest of the
stack expects to read.

Its strength is that it makes the whole layer **honest about message
types**. Because everything arrives as a standard `sensor_msgs` (or
`std_msgs`/`geometry_msgs`) type, the perception code in
[`04-perception-and-vision.md`](04-perception-and-vision.md), the fusion
in Layer 10, and the eventual hardware drivers all speak the same
language — a `sensor_msgs/Image` from a Gazebo camera and from a real
RealSense are the same shape, so code written against the sim runs
against the camera unchanged. It is the piece that lets only-code work
*transfer*.

Its weakness is that it is **only plumbing**: on its own it produces no
sensor data at all — point it at nothing and nothing flows. It also adds
a configuration surface (a YAML list of which topics to bridge, and in
which direction) and a small latency and naming-mismatch hazard: a
mistyped topic or message type here silently starves a gate upstream. So
it is an **Alternative** in the sense that it is not an acquisition
*strategy* you choose between — it is the connective tissue the Gazebo
plugins require and the mock publishers (which already speak native ROS
2) do not. Necessary, but never the answer by itself.

## Verdict

- **Best-in-class:** **micro-ROS** — the real acquisition path that turns
  a physical sensor on a microcontroller into a ROS 2 topic. In only-code
  you can only stub it, but every topic you design should match what it
  will eventually publish, so the swap to hardware is seamless.
- **Cheapest:** **pure rclpy mock publishers** — a handful of lines per
  sensor, `~$0`, and they let you script the exact fault you want to
  rehearse. The right tool for the four sensors (safety #10/#11, level
  #8, balance #6) that have no natural simulator analogue.
- **Best-practical:** **Gazebo sensor plugins + ros2_control + a few
  rclpy mock publishers** — plugins render the cameras (#1–#3), IMU
  (#12), torque (#5), presence (#7) and grasp contact for free;
  `ros2_control` reads the gripper (#4) and limit switches (#9) off the
  joints; and a small set of mock publishers fills the safety, level, and
  balance gaps. Bridged into standard `sensor_msgs`, this stands up all
  twelve for `~$0` and transfers cleanly to hardware later.

## Realistic scenario & use cases

> **Why this matters for automation.** This layer is the cell's nervous
> system: it makes every sensor *exist* as a faithful, timestamped ROS 2
> topic so the gates above (Layer 10) have something to trust. Its
> automation value is making the cell **observable** — and, in only-code,
> making every fault **reproducible on demand**, which no real bench can.

**The scenario.** During an overnight run the cell faces a set of faults
no single sensor catches alone: the dispenser is **gradually
under-filling** (the level reading drifts low over several vials), the
decapper hits a **stuck cap** (a torque spike), an operator's hand trips
the **light curtain for ~200 ms**, the gripper effort creeps **high**
(about to over-squeeze the glass), and the balance reports a vial **0.3 g
lighter** than its worklist expectation (wrong or empty vial). Every one
of those signals must be acquired faithfully, at the right rate, on a
common clock, so Layer 10 can fuse them into a decision.

The layer must therefore serve several **distinct use cases**:

1. **Acquire heterogeneous sensors as standard, timestamped topics.**
   Cameras, IMU, force-torque, gripper, limit switches, presence, plus the
   mock safety/level/balance signals — all as standard messages.
   - *How the solution handles it:* Gazebo plugins render the simulatable
     sensors, `ros2_control` reads the joints, and rclpy mocks fill the
     rest, all **bridged into `sensor_msgs`** so consumers see one
     uniform interface.

2. **Right-rate streaming with sane QoS.** Stream cameras at 10–30 Hz,
   torque fast, and the safety booleans as **latched** state — without
   flooding the graph.
   - *How:* a per-sensor publish rate and QoS profile; safety topics are
     reliable/latched so a late subscriber still sees the current state.

3. **Scriptable fault rehearsal.** Inject the under-fill drift, the torque
   spike, the 200 ms curtain blip, and the high gripper effort to exercise
   the gates before any hardware exists.
   - *How:* the **rclpy mock publishers** drive exact value timelines —
     which is precisely why the four non-simulatable sensors (safety #10/
     #11, level #8, balance #6) are mocks by design.

4. **Time synchronization across sensors.** Stamp readings on a common
   clock so the torque spike and the gripper-effort creep can be lined up
   at the same instant.
   - *How:* every message carries a stamp from the shared ROS clock
     (sim `/clock`), ready for `message_filters` time-alignment in Layer 10.

5. **Hardware-faithful contracts.** Every topic matches what the real
   device will publish, so nothing above changes at bring-up.
   - *How:* topics are designed now to the **micro-ROS / `sensor_msgs`**
     shape the real acquisition path will use.

**Where the pick flexes.** The best-practical mix (Gazebo plugins +
ros2_control + a few rclpy mocks) stands up all twelve sensors for `~$0`
and covers every use case in only-code. The best-in-class **micro-ROS** is
the *real* acquisition path for use case 5 — stubbed here, swapped in at
hardware — while the pure-mock route stays the cheapest way to rehearse
the exact faults of use case 3.

## Deep dive: the three highest-value use cases

The five above all matter; these three carry the most weight for sensing
& signal acquisition — the cell's nervous system.

## Scriptable fault rehearsal

- **The moment:** the gates in Layer 10 must be tested against a gradual
  under-fill, a torque spike, a curtain blip, and creeping gripper effort —
  none of which a clean sim produces on its own.
- **How, in depth:** the **rclpy mock publishers** drive exact value
  timelines for the four non-simulatable sensors (safety #10/#11, level #8,
  balance #6), so any fault is reproduced precisely and repeatably.
- **Edge case it survives:** a *slow drift* rather than a sharp fault — the
  mock can ramp the level reading down over many vials, exercising the
  trend logic a single bad reading wouldn't trigger.
- **Walkthrough:** (1) script a value timeline in the mock publisher; (2)
  publish it on the sensor's topic; (3) let the Layer 10 gate consume it;
  (4) assert the gate trips or holds exactly as intended.
- **In the scene:** a mock sensor obediently plays out a scripted lie — a
  fill level sagging vial by vial, a torque spike at a chosen instant — so
  the gates downstream can be caught reacting, or failing to, long before a
  real sensor exists.
- **Why it's done this way:** the gates are only trustworthy once they've
  been seen to trip on the real failure signatures, and several of those
  sensors have no natural simulator; scripting their signals is the only
  way to exercise the gate logic before the hardware exists.
- **In the full loop:** this provides the signals Layer 10's gates consume
  during every cycle — by exercising those gates here, it ensures the
  sensing-to-gating path the live loop relies on actually fires.
- **Value:** every gate is proven against the exact signal that should trip
  it, before any sensor is bought.

### Meta code

The shape of the fault player, before any library detail:

```text
# define a fault timeline: segments (t_start, t_end, topic, type, v_start, v_end)
# on a fixed timer (e.g. 10 Hz), advance a playback clock:
#     for each active segment -> linearly interpolate v_start -> v_end over its window
#     publish the value on the sensor's real topic                 (ramp = drift, step = blip)
# so a gradual under-fill, a torque spike, and a 200 ms curtain blip play out
#     exactly + repeatably -> the Layer 10 gates see them and react
```

### Real code

A node that plays a scripted fault timeline (ramps and steps) onto the
real sensor topics. **Illustrative teaching code** — re-verify before use;
every line is commented.

```python
import rclpy                                            # ROS 2 Python client library
from rclpy.node import Node                             # base class for a ROS 2 program
from std_msgs.msg import Float64, Bool                  # level/balance values + safety booleans

# (t_start, t_end, topic, kind, v_start, v_end): ramp v_start->v_end over [t_start, t_end]
TIMELINE = [(0.0, 12.0, "/level", "f", 1.00, 0.40),     # fill level drifts low over 12 s (under-fill)
            (5.0, 5.2, "/light_curtain_clear", "b", 1, 0),   # 200 ms curtain blip at t = 5 s
            (5.2, 99.0, "/light_curtain_clear", "b", 1, 1)]  # curtain clear again afterwards


class FaultPlayer(Node):                                # plays a scripted fault timeline onto topics
    def __init__(self):                                 # one-time setup
        super().__init__("fault_player")                # register on the ROS 2 graph
        self.pubs = {}                                  # cache one publisher per topic
        self.t = 0.0                                    # elapsed playback time (seconds)
        self.dt = 0.1                                   # tick period -> 10 Hz playback
        self.create_timer(self.dt, self.tick)           # advance + publish every dt

    def _pub(self, topic, kind):                        # get (or lazily make) a publisher for a topic
        if topic not in self.pubs:                      # first time we touch this topic?
            msg_t = Float64 if kind == "f" else Bool    # float value vs boolean state
            self.pubs[topic] = self.create_publisher(msg_t, topic, 10)  # create + cache it
        return self.pubs[topic]                         # the cached publisher

    def tick(self):                                     # runs at 10 Hz: publish the scheduled values
        for t0, t1, topic, kind, a, b in TIMELINE:      # consider every scheduled segment
            if t0 <= self.t <= t1:                       # is this segment active right now?
                frac = (self.t - t0) / max(t1 - t0, 1e-6)  # how far through the segment (0..1)
                val = a + (b - a) * frac                  # linearly interpolate a -> b (ramp or step)
                if kind == "f":                          # a float sensor (level / balance)...
                    self._pub(topic, "f").publish(Float64(data=float(val)))  # ...publish the value
                else:                                    # a boolean sensor (curtain / door)...
                    self._pub(topic, "b").publish(Bool(data=bool(round(val))))  # ...publish state
        self.t += self.dt                                # advance our playback clock


def main():                                             # standard ROS 2 entry point
    rclpy.init(); rclpy.spin(FaultPlayer()); rclpy.shutdown()  # start, run, clean up


if __name__ == "__main__":                              # run directly
    main()
```

## Cross-sensor time synchronization

- **The moment:** Layer 10 must line up the decapper torque spike with the
  gripper-effort creep at the *same instant* to decide they're one event.
- **How, in depth:** every message carries a stamp from the shared ROS clock
  (sim `/clock`), so `message_filters` can align readings within a slop
  window rather than comparing a fresh value to a stale one.
- **Edge case it survives:** sensors publishing at different rates (camera
  10 Hz, torque fast) — time-stamping, not arrival order, governs pairing,
  so the slow camera frame is matched to the right torque sample.
- **Walkthrough:** (1) stamp every message with the sim `/clock`; (2) feed
  two streams into `message_filters`; (3) pair readings within the slop
  window; (4) hand the matched pair to the gate.
- **In the scene:** two streams of readings, arriving at different speeds,
  are stamped against one shared clock and lined up instant-for-instant, so
  the torque spike and the gripper strain that happened together are seen
  together, not smeared apart.
- **Why it's done this way:** two readings only mean "the same event" if
  they describe the same instant, and sensors publish at different rates;
  stamping and aligning them is what prevents the cell from fusing a fresh
  reading with a stale one and deciding wrongly.
- **In the full loop:** this serves Layer 10 directly — every two-witness
  gate in the loop depends on the aligned readings produced here, so it
  underlies the grasp, fill, and safety checks at each vial.
- **Value:** fused decisions rest on a coherent snapshot of the cell, not a
  smear across time.

### Meta code

The shape of the time-aligner, before any library detail:

```text
# subscribe to two stamped streams, e.g. /decapper/wrench + /joint_states (gripper effort)
# feed them into an ApproximateTimeSynchronizer with a slop window (e.g. 20 ms)
# the synchronizer calls back only with samples whose stamps fall within slop
#     -> the callback gets a coherent (torque, effort) pair from the SAME instant
# hand the matched pair to the Layer 10 gate
```

### Real code

A node that pairs the cap torque and the gripper effort by timestamp.
**Illustrative teaching code** — re-verify before use; every line is
commented.

```python
import rclpy                                            # ROS 2 Python client library
from rclpy.node import Node                             # base class for a ROS 2 program
from geometry_msgs.msg import WrenchStamped             # the decapper torque (stamped)
from sensor_msgs.msg import JointState                  # the gripper effort (stamped)
from message_filters import Subscriber, ApproximateTimeSynchronizer  # align the two streams in time


class TorqueEffortSync(Node):                           # pairs torque + gripper effort by timestamp
    def __init__(self):                                 # one-time setup
        super().__init__("torque_effort_sync")          # register on the ROS 2 graph
        wrench = Subscriber(self, WrenchStamped, "/decapper/wrench")  # stream 1: cap torque
        joints = Subscriber(self, JointState, "/joint_states")       # stream 2: gripper effort
        self.sync = ApproximateTimeSynchronizer(        # align the two streams in time...
            [wrench, joints], queue_size=30, slop=0.02)  # ...within a 20 ms slop window
        self.sync.registerCallback(self.on_pair)        # fire only on a time-matched pair

    def on_pair(self, wrench, joints):                  # runs with a coherent same-instant pair
        tz = abs(wrench.wrench.torque.z)                # the un-cap torque at that instant
        eff = 0.0                                       # the gripper effort at that same instant...
        if "gripper_finger_joint" in joints.name:       # find the finger joint, if present
            eff = abs(joints.effort[joints.name.index("gripper_finger_joint")])  # its effort
        self.get_logger().info(f"t={tz:.2f} Nm  eff={eff:.2f}  (same instant)")  # one fused sample


def main():                                             # standard ROS 2 entry point
    rclpy.init(); rclpy.spin(TorqueEffortSync()); rclpy.shutdown()  # start, run, clean up


if __name__ == "__main__":                              # run directly
    main()
```

## Hardware-faithful contracts

- **The moment:** the day real sensors arrive, nothing above this layer
  should change.
- **How, in depth:** every topic is designed now to the **micro-ROS /
  `sensor_msgs`** shape the real device will publish, so a mock and a real
  sensor are interchangeable from the consumer's side.
- **Edge case it survives:** a real sensor with extra fields or different
  units — pinning to the standard message type forces the conversion into
  the driver, keeping perception and gating untouched.
- **Walkthrough:** (1) define the topic to the `sensor_msgs` / micro-ROS
  shape; (2) back it with a mock now; (3) on hardware swap in the real
  driver; (4) consumers above see no change at all.
- **In the scene:** a mock publisher and a future real sensor are made to
  speak in exactly the same words on exactly the same channel, so that on
  the day the hardware arrives the swap is silent and nothing upstream even
  notices.
- **Why it's done this way:** the only-code work is wasted if real sensors
  force changes up the stack; pinning every topic to the shape the real
  device will publish is what keeps bring-up to a driver swap instead of a
  rewrite.
- **In the full loop:** this spans the whole project's transfer — because
  every per-vial sensor read uses these contracts, the entire
  sensing-and-gating chain moves to hardware untouched.
- **Value:** sensor bring-up swaps a publisher; it doesn't ripple a rewrite
  through the stack.

### Meta code

The shape of the sensor contract, before any library detail:

```text
# pick the STANDARD message type the real device will publish (sensor_msgs / micro-ROS shape)
# back the topic with a mock now that fills exactly those fields, same topic name + QoS + rate
# define a conforms() contract: required frame_id, a non-zero stamp, expected units
# on hardware: a real driver publishes the SAME type on the SAME topic
#     -> any unit/field difference is converted INSIDE the driver
#     -> perception + gating subscribers are byte-for-byte unchanged
```

### Real code

A mock that publishes the exact standard message a real sensor would, with
a contract assertion. **Illustrative teaching code** — re-verify before
use; every line is commented.

```python
import rclpy                                            # ROS 2 Python client library
from rclpy.node import Node                             # base class for a ROS 2 program
from geometry_msgs.msg import WrenchStamped             # the STANDARD type the real sensor will use

CONTRACT_FRAME = "cap_joint"                            # the frame_id every publisher MUST set
CONTRACT_RATE_HZ = 50                                   # the rate the gate logic above expects


def conforms(msg: WrenchStamped) -> bool:               # the contract a real driver must ALSO satisfy
    return (msg.header.frame_id == CONTRACT_FRAME and   # correct frame_id, and...
            msg.header.stamp.sec != 0)                  # ...a real (non-zero) timestamp present


class MockTorque(Node):                                 # stands in for the real cap force-torque sensor
    def __init__(self):                                 # one-time setup
        super().__init__("mock_torque")                 # register on the ROS 2 graph
        self.pub = self.create_publisher(               # publish on the SAME topic the real one uses
            WrenchStamped, "/decapper/wrench", 10)
        self.create_timer(1.0 / CONTRACT_RATE_HZ, self.tick)  # at the contracted rate

    def tick(self):                                     # emit one fully-populated, stamped message
        msg = WrenchStamped()                           # the standard message type
        msg.header.stamp = self.get_clock().now().to_msg()  # a real timestamp (contract requirement)
        msg.header.frame_id = CONTRACT_FRAME            # the contracted frame_id
        msg.wrench.torque.z = 0.1                       # a benign idle torque (N*m)
        assert conforms(msg), "mock violates the sensor contract"  # fail loudly if we ever drift
        self.pub.publish(msg)                           # publish; consumers can't tell mock from real


def main():                                             # standard ROS 2 entry point
    rclpy.init(); rclpy.spin(MockTorque()); rclpy.shutdown()  # start, run, clean up


if __name__ == "__main__":                              # run directly
    main()
```

## See also

- [`README.md`](README.md) — the only-code folder overview and the full
  list of development layers.
- [`../sensor-suite.md`](../sensor-suite.md) — the canonical 12-sensor
  list, topic names, sim stand-ins, costs, and the two-witness habit this
  layer brings to life.
- [`04-perception-and-vision.md`](04-perception-and-vision.md) — the
  camera sensors (#1–#3) turned into poses; the perception half of what
  this acquisition layer feeds.
- [`10-sensor-fusion-and-gating.md`](10-sensor-fusion-and-gating.md) —
  the next layer, which *fuses* the topics stood up here into the
  two-witness gates that open or block each motion.
- [`../02-code-plus-hardware/02-middleware-and-control.md`](../02-code-plus-hardware/02-middleware-and-control.md)
  — the same plumbing once **real sensors** (via micro-ROS, camera SDKs,
  load-cell amplifiers) publish these topics from hardware.
