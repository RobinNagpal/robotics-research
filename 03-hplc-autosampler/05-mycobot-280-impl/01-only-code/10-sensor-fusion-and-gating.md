# Layer 10 — Sensor fusion, gating & full-flow integration (only-code)

> **Job:** Take the raw sensor topics published by Layer 09 and the
> camera outputs from Layer 04, **fuse** the ones that watch the same
> fact into a single trustworthy reading, turn that reading into a
> pass/fail **gate**, and wire those gates into the per-vial behaviour
> tree that Layer 07 runs — all in software, against simulated and mock
> sensor topics, with no hardware attached.

The lower layers each publish *evidence*: Layer 09 turns sensors into
ROS 2 (Robot Operating System 2) topics — gripper effort, balance mass,
load-cell torque, a fill level — and Layer 04 turns the cameras into
detections — a vial seen, a meniscus height, a cap on or off. This layer
is where that evidence is **combined and judged**. **Fusion**, in plain
terms, means taking two or more sensor readings that describe the *same*
real fact and merging them into one number or one true/false answer you
can rely on more than either alone. A single sensor can lie — glare
fools a camera, a snagged cable fakes a grip — but two independent
sensors rarely lie the same way at the same instant.

That is the **two-witness habit** from
[`../sensor-suite.md`](../sensor-suite.md): wherever a fact matters,
**two independent sensors must agree** before the workflow trusts it.
"Vial is held" is gripper feedback (#4) **and** a wrist-camera glance
(#3); "right fill" is the balance (#6) **and** the level/meniscus check
(#2/#8). This layer is where those pairings stop being a design note and
become running code.

A **gate** is the output of that judgement: a step is allowed to proceed
only if its two witnesses both read inside an expected **band** (a
low-to-high range, e.g. "grip effort between 2 and 8 newton-metres") and
**agree** with each other. The gate publishes a single true/false
answer. Those answers are exactly what the **Behaviour Tree (BT)** in
[`07-orchestration-and-task-logic.md`](07-orchestration-and-task-logic.md)
ticks as its condition nodes: the tree checks the gate *before* it fires
the guarded motion, and a `Failure` branches to retry, quarantine, or
stop. This layer therefore does not re-implement the tree — it **feeds**
it. It is the wiring between "sensors exist" (Layers 04 and 09) and
"the arm acts only when the sensors agree" (Layer 07).

## The five at a glance

| Framework | Role | Tier | One-liner |
|---|---|---|---|
| `message_filters` (ApproximateTimeSynchronizer) | Time-align two sensor streams so a two-witness check compares the *same* instant | Recommended | Pairs up messages with near-equal timestamps; the standard way to sync two witnesses. |
| `py_trees` condition / gate nodes | Express each fused gate as a BT leaf feeding the Layer 07 tree | **Best-practical** | The gate *is* a tree node; verdicts plug straight into orchestration, no glue. |
| Plain `rclpy` latest-value cache + band | Store each topic's last value, compare against a threshold band | **Cheapest** | A dictionary and an `if`; no extra libraries, trivial to fault-inject. |
| `robot_localization` (Extended Kalman Filter) | Probabilistic fusion of pose / IMU streams into one estimate | **Best-in-class** | True statistical sensor fusion; the right tool for pose+IMU — overkill for boolean gates here. |
| `diagnostic_aggregator` / Foxglove dashboards | Monitor and surface gate state to a human or a log | Alternative | Doesn't decide; rolls many gate readings into a readable health view. |

A **Kalman filter** (named in row four) is a standard maths recipe that
blends a stream of noisy measurements into one best estimate, weighting
each reading by how much it is trusted; the **Extended** version handles
non-straight-line motion. It is the gold standard for fusing *continuous
numbers* like position and velocity — not for the simple "do two
witnesses agree?" booleans this cell mostly needs.

## `message_filters` (ApproximateTimeSynchronizer)

`message_filters` is a small ROS 2 utility whose
**ApproximateTimeSynchronizer** waits until it has one message from each
of several topics with **near-equal timestamps**, then calls your code
once with all of them together. That timestamp matching is the quiet but
essential part of any two-witness check: comparing a gripper-effort
reading from one second ago against a wrist-camera glance from now would
let a stale witness vouch for a fact that has already changed. The
synchronizer makes "the same instant" precise.

How it's good versus the others: it solves the one problem the
**cheapest** latest-value cache quietly ignores — *time alignment*. The
plain cache compares whatever each topic last published, which can be
two readings taken seconds apart; `message_filters` guarantees the two
witnesses describe the same moment, which is what makes "they agree"
meaningful. It is lighter than **robot_localization** (no motion model,
no covariances) and, unlike a **Foxglove** dashboard, it actually gates
rather than merely displays. For pairing balance (#6) with level (#2/#8),
or gripper effort (#4) with a wrist glance (#3), it is the right-sized
tool.

How it's bad versus the others: it only *delivers* the synchronised
pair — it does not decide anything, so you still write the band-and-agree
logic yourself (here, that logic lives inside a **py_trees** node).
Approximate matching has tuning knobs (the allowed time slop, the queue
size) that can drop pairs if one topic is much slower than the other,
which a brute-force latest-value cache never does. And it adds a
dependency and a little ceremony over the few lines of the cheapest
option. For a fast sim-only spike you might skip it; for a gate you
intend to carry to hardware, the time alignment it buys is worth it.

## `py_trees` condition / gate nodes

`py_trees` is the pure-Python **Behaviour Tree** library Layer 07 uses
as its cheapest orchestration option. Its relevance *here* is that a
fused gate is most naturally written as a **condition node** — a tree
leaf whose `update()` returns `Success` when the two witnesses agree
inside their band and `Failure` otherwise. Because the gate is already a
tree node, it drops into the Layer 07 per-vial tree with **zero glue**:
the orchestration layer ticks it like any other condition, exactly as
its existing `safe?` and `held?` nodes already work.

How it's good versus the others: it is the only option on this list that
**ends where Layer 07 begins**. The latest-value cache and
`message_filters` both produce a value or a pair that *something else*
must still turn into a tree node; a py_trees gate *is* that node. It
inherits the tree's reactivity for free — a gate re-ticked every
heartbeat can pre-empt a running motion the instant a witness disagrees —
and it keeps every gate written in the same shape, so the fused
two-witness logic reads identically to the simple single-sensor gates
already in the tree. It is also trivial to fault-inject: feed a mock
topic a bad value and watch the gate fail.

How it's bad versus the others: a py_trees node is **judgement, not
synchronisation** — on its own it still reads "the latest value of each
topic," so for a true same-instant check it should sit *behind* a
`message_filters` sync (which is exactly the best-practical pairing).
Being pure Python it shares the speed ceiling Layer 07 already notes
versus the C++ `BehaviorTree.CPP` engine — invisible in sim, a
consideration on hardware. And it deliberately does **no probabilistic
fusion**; if a fact genuinely needs a weighted blend of noisy numbers,
that belongs in `robot_localization` upstream, with py_trees only gating
the result.

## Plain `rclpy` latest-value cache + threshold band

The cheapest possible fusion is a few lines of plain `rclpy` (the ROS 2
Python client library): subscribe to each sensor topic, store its most
recent value in a small dictionary, and whenever you need a verdict
compare those stored values against a fixed **band** with an `if`. "Held"
becomes `effort_low <= last_effort <= effort_high and last_vial_present`.
No synchroniser, no filter library, no tree — just cached values and a
comparison.

How it's good versus the others: it is **the least machinery that can
possibly work** and the fastest to stand up in only-code mode. There is
nothing to install beyond ROS 2 itself, nothing to tune, and the logic
is a single readable expression anyone can audit. Fault injection is as
easy as it gets — publish a value outside the band from a mock and the
gate flips. For an early sim spike, or for a fact whose witnesses update
at roughly the same rate, it is perfectly adequate and the quickest path
to a working pass/fail.

How it's bad versus the others: it **ignores time**. The cache holds
whatever each topic last sent, so a fast camera and a slow balance can be
compared across a several-second gap — the exact stale-witness trap
`message_filters` exists to close. It also has nowhere natural to live in
the tree: you end up calling it from a py_trees node anyway, at which
point you have most of the best-practical structure without its time
safety. And it does no real fusion in the statistical sense — it cannot
weight a trusted sensor over a flaky one the way **robot_localization**
can. It is the right *starting* point and the wrong *finishing* point.

## `robot_localization` (Extended Kalman Filter)

`robot_localization` is a mature ROS 2 package that fuses multiple
continuous sensor streams — wheel odometry, an Inertial Measurement Unit
(IMU), Global Positioning System (GPS), visual odometry — into one
smoothed pose-and-velocity estimate, using an **Extended Kalman Filter**
(EKF) or an Unscented variant. This is *fusion* in its full, textbook
sense: each sensor contributes weighted by its stated uncertainty, and
the filter outputs a single best estimate with a confidence on it.

How it's good versus the others: it is genuinely **best-in-class** at
what it does. Where a fact is a noisy continuous quantity watched by
several sensors — most obviously the base IMU (#12) plus any odometry,
fused into "is the cell level and still?" — an EKF produces a smoother,
better-justified answer than any threshold band, and it degrades
gracefully when one sensor drops out. Nothing else on this list models
sensor *uncertainty* at all; the others compare raw values, this one
reasons about how much to trust each.

How it's bad versus the others: for **this** cell it is **overkill**.
Almost every two-witness check here is a boolean — held / not held, cap
on / off, fill right / wrong — not a continuous pose, and an EKF has
nothing to estimate in a true/false question. It demands per-sensor
covariance tuning and a motion model that a static benchtop arm does not
really have, which is effort the **band-and-agree** gates simply skip.
And its output is an estimate, not a gate, so you would *still* threshold
it into a boolean for the tree. List it as the ceiling for the one
genuinely continuous fact (cell level / vibration); reach for the lighter
tools for everything else.

## `diagnostic_aggregator` / Foxglove dashboards

The last option does not fuse or gate at all — it **surfaces** gate
state. ROS 2's `diagnostic_aggregator` rolls many per-component status
messages into a single tree-shaped health summary; **Foxglove** is a
modern visualisation tool that subscribes to topics and draws live
dashboards. Pointed at the gate topics this layer publishes, either one
turns "twelve booleans flickering across the graph" into a single
readable "is the cell happy right now?" view.

How it's good versus the others: it answers a question the other four
don't — **"can a human (or a log) see what every gate is doing?"** In
only-code mode, while you inject faults, a Foxglove panel showing each
gate going red or green as you break a witness makes the whole
two-witness machine *legible* in a way reading log lines never matches.
For the audit trail and operator experience the eventual hardware cell
needs, this is where gate state becomes a record and a display rather
than a fleeting boolean.

How it's bad versus the others: it is **strictly downstream of a
decision** — it shows verdicts, it never makes them, so it can never
replace the gate logic itself. Wiring `diagnostic_aggregator` analysers
is fiddly relative to a one-line band check, and a Foxglove dashboard is
another process to run and maintain. It earns its place as monitoring
*alongside* the real gates (and feeds the compliance log in Layer 08),
but if you only built this, the arm would still be flying blind — nothing
here would ever stop a motion.

## Verdict

- **Best-in-class — `robot_localization` (EKF).** True probabilistic
  fusion: it weights each sensor by its uncertainty and produces one
  best estimate, the correct tool for the cell's one genuinely
  continuous fact (base IMU #12 + odometry → "level and still"). For the
  boolean two-witness gates that dominate this cell it is **overkill** —
  there is nothing to estimate in a true/false question.
- **Cheapest — plain `rclpy` latest-value cache + band.** Subscribe,
  store each topic's last value, compare against a low-to-high band with
  an `if`. Zero extra libraries, trivial to fault-inject, perfect for an
  early sim spike — at the cost of ignoring *time* (it can compare a
  fresh witness against a stale one).
- **Best-practical — `message_filters` to sync the two witnesses +
  `py_trees` gate nodes wired into the Layer 07 tree.** The synchronizer
  guarantees the two witnesses describe the **same instant**; the
  py_trees condition node turns "both in band **and** in agreement" into
  one `Success`/`Failure` that the
  [`07-orchestration-and-task-logic.md`](07-orchestration-and-task-logic.md)
  tree already knows how to tick. It closes the stale-witness gap the
  cheapest option leaves open and lands the gate exactly where
  orchestration consumes it — no glue, no duplication.

## Realistic scenario & use cases

> **Why this matters for automation.** This is the integration layer: it
> fuses the Layer 09 signals into the **two-witness gates** that open or
> block every motion in the per-vial loop. Its automation value is the
> cell's *conscience* — it is what lets the arm act on what it senses
> instead of blindly, and what makes "never place an unverified vial" a
> mechanical guarantee rather than a hope.

**The scenario.** At the moment of placing vial 78, four facts must each
be confirmed by **two independent witnesses**: *is a vial actually
grasped?* (gripper effort + wrist camera), *is it filled correctly?*
(level + balance), *is it safe to move?* (light curtain + door), and *is
the base level and still?* (IMU). Two traps lurk: the wrist camera says
"vial present" while the gripper effort reads "jaws fully closed" (empty)
— a **disagreement that must block the place** — and the light curtain
**cleared 2 s ago but no fresh reading has arrived**, which must *not* be
treated as safe. Getting either wrong drops a vial or moves into a hand.

The layer must therefore serve several **distinct use cases**:

1. **Two-witness grasp gate.** Allow transit/place only if the wrist
   camera **and** the gripper agree a vial is held; block on disagreement.
   - *How the solution handles it:* `message_filters` syncs the two
     witnesses to the same instant and a **py_trees gate** returns
     `Failure` unless both agree — the empty-jaws/"present" conflict stops
     the place.

2. **Fill-verification gate.** Confirm fill with level **and** balance
   before recap and place.
   - *How:* the two readings are time-synced and the gate passes only when
     **both sit in band and agree**, so a single drifting sensor can't
     wave a bad vial through.

3. **Fail-safe safety gate.** Block all motion unless light curtain **and**
   door read clear — *and* the readings are fresh.
   - *How:* latched booleans plus a **freshness deadline**; a stale or
     missing safety reading is treated as **unsafe**, closing the
     2-seconds-old-curtain trap.

4. **Continuous "level and still" estimate.** Fuse IMU and odometry into
   one trustworthy estimate that the base is stable before fine motions.
   - *How:* this is the cell's one genuinely continuous fact, so it uses
     the **`robot_localization` EKF** (best-in-class) rather than a boolean
     gate.

5. **Stale-witness rejection / time alignment.** Never pair a fresh
   witness with a stale one when forming a gate.
   - *How:* the `ApproximateTimeSynchronizer` slop window means
     out-of-window pairs produce **no decision** (the gate holds) instead
     of a false pass — the gap the cheapest latest-value cache leaves open.

**Where the pick flexes.** `message_filters` + py_trees gates
(best-practical) handle the four boolean two-witness gates that dominate
the cell (use cases 1–3, 5) and drop straight into the Layer 07 tree. The
**EKF** is reserved for the single continuous estimate of use case 4; the
plain latest-value cache stays the cheapest way to spike a gate early,
before time-correctness matters. Together these close the loop: Layers
03–09 *act and sense*, and this layer decides, vial by vial, whether each
action is allowed to proceed.

## Deep dive: the three highest-value use cases

The five above all matter; these three carry the most weight for sensor
fusion & gating — the cell's conscience, vial by vial.

## Two-witness grasp gate

Before carrying a vial across the bench, a lab assistant unconsciously
double-checks they actually have it — a glance plus the feel of it in
their fingers. Two senses agreeing is what makes "yes, I'm holding it"
certain. This use case is the cell formalizing that: it only lets the arm
move a vial when two independent witnesses — the gripper's own feel and
the wrist camera's eye — agree a vial is held.

The bigger experiment is the HPLC batch, where carrying nothing (a missed
pick) or dropping a vial in transit both corrupt the tray. The gate sits
between the pick and the carry, so it guards every single transfer in the
run. Requiring two witnesses is what makes "never carry nothing, never
drop" a mechanical guarantee instead of a hope, because no single fooled
sensor can wave an empty gripper through.

The assistant makes this is-it-held check on every pick — hundreds of
times a day, mostly without noticing. The cell runs the two-witness gate
just as often: once before every transit, on every vial, all run long. It
is the most frequently-evaluated gate in the loop.

- **The moment:** before transit, the cell must be *sure* a vial is held;
  the wrist camera says "present" but the gripper effort says "jaws fully
  closed" (empty) — a contradiction.
- **How, in depth:** `message_filters` syncs the two witnesses to the same
  instant and a **py_trees gate** returns `Success` only if both agree; the
  camera/effort disagreement returns `Failure`, blocking the place.
- **Edge case it survives:** a sensor that lies confidently — neither
  witness can pass the gate alone, so a single failed sensor can't wave an
  empty gripper through.
- **Walkthrough:** (1) sync the wrist camera and gripper `JointState`; (2)
  test both are in band; (3) test that they agree; (4) return `Success`
  only if both pass, otherwise block the place.
- **In the scene:** before the arm carries a vial away, two independent
  observers — the gripper's own feel and the wrist camera's eye — must nod
  in agreement that a vial is truly held; if one says "present" and the
  other says "empty", the gate slams shut.
- **Why it's done this way:** any single sensor can be fooled — a camera
  by a reflection, the gripper by a jammed jaw — and acting on one witness
  risks carrying nothing or dropping a vial; requiring two independent
  agreements is what makes "is it held?" trustworthy.
- **In the full loop:** this sits between Layer 05's pick and Layer 03's
  transit — it is the gate that must pass before the arm carries a vial
  anywhere, the checkpoint guarding every place in the loop.
- **Value:** "never carry nothing, never drop in transit" becomes a
  mechanical guarantee, not an assumption.

### Meta code

This meta turns a safety-critical yes/no question — "is a vial actually
held?" — into the logical AND of two independent confirmations, and
publishes the answer as a single boolean fact the rest of the cell can
trust. The first witness is the gripper's jaw width; the second is the
wrist camera's "vial present" signal.

Crucially, the two witnesses are first paired in time, so the gate reasons
about both sensors describing the same instant rather than a fresh reading
from one and a stale one from the other. Only a time-matched pair is
evaluated.

For each matched pair the gate computes two conditions: the gripper
condition (jaw width close to the expected vial diameter, meaning it
closed on glass rather than air) and the camera condition (a vial is seen
at the gripper line). The published gate value is the AND of the two —
true only when both agree.

That single boolean is what the Layer 07 behaviour tree ticks before
allowing transit; a false value blocks the place. Because the answer
requires two independent yeses, one fooled sensor — a reflection, a jammed
jaw — cannot open the gate alone. The gate in pseudocode:

```text
# subscribe to witness A: gripper jaw width (#4) and witness B: wrist /vial_present (#3)
# time-sync A and B so both describe the same instant (ApproximateTimeSynchronizer)
# on each synced pair:
#     held_by_jaw = jaw width ~ vial diameter            (A within its band)
#     held_by_cam = (B is True)                          (B's independent confirmation)
#     publish /gate/grasp = held_by_jaw AND held_by_cam  (one trustworthy boolean)
# the Layer 07 tree ticks this gate before transit; False blocks the place
```

### Real code

A node that ANDs the gripper and wrist-camera witnesses into one grasp
gate. **Illustrative teaching code** — re-verify before use; every line is
commented.

```python
import rclpy                                            # ROS 2 Python client library
from rclpy.node import Node                             # base class for a ROS 2 program
from sensor_msgs.msg import JointState                  # witness A: gripper jaw width
from std_msgs.msg import Bool                           # witness B: wrist "vial present"; + gate out
from message_filters import Subscriber, ApproximateTimeSynchronizer  # same-instant pairing

VIAL_DIA = 0.0118                                       # jaw width when truly holding a vial (m)
TOL = 0.002                                             # within 2 mm counts as "holding glass"


class GraspGate(Node):                                  # two-witness "is a vial held?" gate
    def __init__(self):                                 # one-time setup
        super().__init__("grasp_gate")                  # register on the ROS 2 graph
        self.pub = self.create_publisher(Bool, "/gate/grasp", 10)  # the single trustworthy fact
        jaw = Subscriber(self, JointState, "/joint_states")   # witness A: the gripper
        cam = Subscriber(self, Bool, "/wrist/vial_present")   # witness B: the wrist camera
        self.sync = ApproximateTimeSynchronizer(        # pair the two witnesses in time...
            [jaw, cam], queue_size=10, slop=0.05, allow_headerless=True)
        self.sync.registerCallback(self.on_pair)        # decide only on a matched pair

    def on_pair(self, js, present):                     # runs on a same-instant (gripper, camera) pair
        held_jaw = ("gripper_finger_joint" in js.name and  # witness A: jaw width near vial diameter?
                    abs(js.position[js.name.index("gripper_finger_joint")] * 2 - VIAL_DIA) <= TOL)
        agree = bool(held_jaw and present.data)         # the two-witness AND (both must confirm)
        self.pub.publish(Bool(data=agree))              # publish the gate; False blocks the place


def main():                                             # standard ROS 2 entry point
    rclpy.init(); rclpy.spin(GraspGate()); rclpy.shutdown()  # start, run, clean up


if __name__ == "__main__":                              # run directly
    main()
```

## Fail-safe safety gate

A careful lab assistant treats the absence of an "all clear" as a reason
to wait, not to proceed — if they can't confirm it's safe, they don't
move. This use case builds that conservative default into the cell as a
fail-closed safety gate: the arm is only allowed to move when the safety
sensors actively and recently confirm it's clear, and silence is treated
as unsafe.

The bigger experiment is the unattended HPLC batch in a shared lab, where
people can approach the cell at any time. The danger isn't only a seen
hazard — it's a safety sensor that has gone quiet, whose last "clear" is
now stale. Designing the gate so that a missing or out-of-date "clear"
blocks motion is what guarantees a sensor dropout can never be misread as
permission to move near a hand.

For the assistant, the safety judgment is constant — it precedes every
motion near other people. The cell evaluates this gate continuously, above
every per-vial step, so no pick, transit, or place proceeds unless the
cell is, at that very moment, freshly confirmed safe.

- **The moment:** the arm may only move if the light curtain *and* the door
  read clear — but the curtain cleared 2 s ago and no fresh reading has
  arrived.
- **How, in depth:** the safety booleans are latched/reliable but carry a
  **freshness deadline**; a stale or missing reading is treated as
  **unsafe**, so motion is blocked until a current "clear" arrives.
- **Edge case it survives:** a dead safety sensor (no messages at all) —
  silence reads as unsafe, the fail-safe default, rather than as implicit
  permission.
- **Walkthrough:** (1) subscribe to the curtain and door with a deadline;
  (2) check both read clear; (3) check the readings are fresh; (4) block
  unless current and clear, otherwise hold.
- **In the scene:** the arm asks permission to move and is refused — not
  because danger was seen, but because the safety sensor has gone quiet, and
  silence is treated as "unsafe". The gate would rather wait than guess.
- **Why it's done this way:** near a human the dangerous default is to
  move on stale or missing safety data; designing the gate so that the
  absence of a fresh "clear" means "stop" is what guarantees a sensor
  dropout can never be read as permission.
- **In the full loop:** this gates every motion in the loop on safety — it
  sits above Layer 07's per-vial steps, so no pick, transit, or place
  proceeds unless the cell is currently, freshly safe.
- **Value:** the gate fails closed, so a sensor dropout halts the arm
  instead of letting it move near a hand.

### Meta code

This meta is built around a default of "unsafe," from which the gate only
departs when it has positive, current evidence to the contrary. It
subscribes to the safety inputs — the light curtain and the door — and,
importantly, records not just their latest values but the time each was
last received.

On a fixed timer it recomputes the verdict from two requirements that must
both hold. The first is "clear": both inputs currently report a safe
state. The second is "fresh": both inputs were received within a short
deadline, so the cell is acting on current information.

Safe is published only when the readings are both clear AND fresh. This is
what closes the stale-curtain trap: a curtain that said "clear" two seconds
ago but has since gone silent fails the freshness test, so the gate
reports unsafe even though the last value was good.

The default before any message has arrived is unsafe, and a sensor that
stops publishing entirely is read as unsafe rather than as permission —
the gate fails closed in every degenerate case. The gate in pseudocode:

```text
# subscribe to /light_curtain_clear and /door_closed (latched booleans)
# track the time each was last received (freshness)
# on a fixed timer, publish /gate/safe:
#     fresh = both received within DEADLINE seconds
#     clear = curtain_clear AND door_closed
#     safe  = fresh AND clear                            (absence of a fresh "clear" => UNSAFE)
# default before any message: UNSAFE                     (fail-closed)
```

### Real code

A gate that publishes "safe" only when both safety inputs are clear AND
fresh. **Illustrative teaching code** — re-verify before use; every line
is commented.

```python
import rclpy                                            # ROS 2 Python client library
from rclpy.node import Node                             # base class for a ROS 2 program
from std_msgs.msg import Bool                           # the safety inputs + the /gate/safe output

DEADLINE = 0.5                                          # a reading older than 0.5 s counts as stale


class SafetyGate(Node):                                 # fail-closed safety gate
    def __init__(self):                                 # one-time setup
        super().__init__("safety_gate")                 # register on the ROS 2 graph
        self.state = {"curtain": (False, 0.0),          # topic -> (last_value, last_time)...
                      "door": (False, 0.0)}             # ...both start UNSAFE + never-seen
        self.pub = self.create_publisher(Bool, "/gate/safe", 10)  # the fused safety verdict
        self.create_subscription(Bool, "/light_curtain_clear",    # curtain input...
                                 lambda m: self._set("curtain", m), 10)
        self.create_subscription(Bool, "/door_closed",            # door input...
                                 lambda m: self._set("door", m), 10)
        self.create_timer(0.1, self.publish)            # re-evaluate at 10 Hz

    def now(self):                                      # current time in seconds
        return self.get_clock().now().nanoseconds * 1e-9  # ROS clock -> float seconds

    def _set(self, key, msg):                           # record a fresh reading + its arrival time
        self.state[key] = (msg.data, self.now())        # value + the time we received it

    def publish(self):                                  # runs at 10 Hz: compute + publish "safe"
        t = self.now()                                  # the time of this evaluation
        fresh = all(t - ts <= DEADLINE for _, ts in self.state.values())  # both readings recent?
        clear = all(v for v, _ in self.state.values())  # both readings say "clear"?
        self.pub.publish(Bool(data=bool(fresh and clear)))  # safe ONLY if fresh AND clear


def main():                                             # standard ROS 2 entry point
    rclpy.init(); rclpy.spin(SafetyGate()); rclpy.shutdown()  # start, run, clean up


if __name__ == "__main__":                              # run directly
    main()
```

## Stale-witness rejection

A lab assistant wouldn't act on a glance they took several seconds ago and
a touch they feel right now as if the two described the same moment —
they'd take a fresh look first. Acting on stale information is how mistakes
happen. This use case gives the cell that discipline: a gate decision is
only made from witnesses whose readings are genuinely from the same,
recent instant; a fresh reading paired with a stale one produces no
decision at all.

The bigger experiment is the HPLC batch, where every two-witness gate
(grasp, fill, safety) depends on combining sensors. A cheap shortcut —
pairing whatever each sensor reported most recently — can match a fresh
reading against a stale one and decide wrongly. Rejecting stale pairings,
and holding the gate until a properly time-matched pair arrives, is what
keeps every fused decision trustworthy in time, not just in value.

The assistant's instinct to take a fresh look applies whenever a judgment
matters — many times an hour. The cell applies the same rule under every
gate it evaluates, on every vial, throughout the run; the cost is at most
a brief hold while a matching pair arrives, never a wrong action on old
data.

- **The moment:** a gate is about to pass a *fresh* gripper reading against
  a *stale* camera frame from before the last move.
- **How, in depth:** the `ApproximateTimeSynchronizer` slop window means
  out-of-window pairs produce **no decision** (the gate holds) rather than a
  false pass on mismatched-in-time data.
- **Edge case it survives:** a momentarily lagging camera — the gate waits
  for a matching pair instead of trusting an old frame, so a transient delay
  causes a brief hold, not a wrong action.
- **Walkthrough:** (1) tag each witness with its stamp; (2) the
  synchronizer seeks a pair within slop; (3) no in-window pair means no
  decision; (4) the gate holds until a fresh matching pair arrives.
- **In the scene:** a fresh gripper reading is about to be matched against a
  camera frame that is a beat too old; the synchronizer notices the
  timestamps don't line up, declines to decide, and waits a moment for a
  properly matched pair.
- **Why it's done this way:** comparing readings without checking their
  timestamps can pass a decision built on out-of-date data; refusing to
  decide until a properly time-matched pair exists is what makes the fused
  gate trustworthy in time, not just in value.
- **In the full loop:** this underlies all the loop's gates — by ensuring
  only time-matched witnesses decide, it keeps every per-vial grasp, fill,
  and safety gate honest across the whole run.
- **Value:** closes the exact gap the cheap latest-value cache leaves open,
  making fused decisions trustworthy in time as well as value.

### Meta code

This meta closes the one gap a naive two-witness gate leaves open:
comparing readings without checking whether they are from the same time.
It treats both witnesses as stamped streams and uses an approximate time
synchronizer to deliver only pairs whose timestamps fall within a small
slop window.

Because the synchronizer never pairs an out-of-window sample, a fresh
reading from one sensor is simply never matched against a stale reading
from the other. Unmatched samples produce no callback at all — and no
callback means no decision, so the gate holds rather than deciding wrongly.

A second guard handles the case where even a time-matched pair is itself
too old: if the pair's timestamp is older than a maximum age, it is
dropped. This stops a long stall from later "unsticking" and pushing
through a decision built on data that is internally consistent but stale
overall.

Only a pair that is both mutually time-matched and recent gets to decide,
which is what makes the fused gate trustworthy in time as well as in value
— the property a cheap latest-value cache can't provide. The rejection in
pseudocode:

```text
# subscribe to the two witnesses as STAMPED streams
# feed them into ApproximateTimeSynchronizer(slop=S):
#     a pair is delivered ONLY if |stamp_A - stamp_B| <= S   (no fresh-vs-stale pairing)
#     out-of-window samples are buffered, not paired -> NO decision (the gate holds)
# also drop any matched pair older than MAX_AGE                (a long stall can't decide late)
# (contrast: a latest-value cache would pair a fresh A with a stale B and decide wrongly)
```

### Real code

A gate that decides only on a fresh, time-matched witness pair and holds
otherwise. **Illustrative teaching code** — re-verify before use; every
line is commented.

```python
import rclpy                                            # ROS 2 Python client library
from rclpy.node import Node                             # base class for a ROS 2 program
from std_msgs.msg import Bool                           # the gate output
from sensor_msgs.msg import JointState, Image           # two stamped witness streams
from message_filters import Subscriber, ApproximateTimeSynchronizer  # time-window pairing

SLOP = 0.03                                             # only pair witnesses within 30 ms
MAX_AGE = 0.2                                           # ignore even a matched pair older than 200 ms


class StaleSafeGate(Node):                              # only decides on a fresh, time-matched pair
    def __init__(self):                                 # one-time setup
        super().__init__("stale_safe_gate")             # register on the ROS 2 graph
        self.pub = self.create_publisher(Bool, "/gate/grasp", 10)  # the gate verdict
        a = Subscriber(self, JointState, "/joint_states")    # witness A (stamped)
        b = Subscriber(self, Image, "/wrist/image_raw")      # witness B (stamped)
        self.sync = ApproximateTimeSynchronizer(        # deliver a pair ONLY within SLOP...
            [a, b], queue_size=20, slop=SLOP)            # ...so out-of-window samples never pair
        self.sync.registerCallback(self.on_pair)        # ...making stale pairing impossible

    def on_pair(self, a, b):                            # runs only on a time-matched (A, B) pair
        now = self.get_clock().now().nanoseconds * 1e-9  # current time in seconds
        stamp = a.header.stamp.sec + a.header.stamp.nanosec * 1e-9  # the pair's own timestamp
        if now - stamp > MAX_AGE:                        # even a matched pair can be too OLD...
            return                                       # ...drop it: no decision -> the gate holds
        # a fresh, time-matched pair would be evaluated here (e.g. the grasp AND above):
        self.pub.publish(Bool(data=True))               # only a fresh, coherent pair gets to decide


def main():                                             # standard ROS 2 entry point
    rclpy.init(); rclpy.spin(StaleSafeGate()); rclpy.shutdown()  # start, run, clean up


if __name__ == "__main__":                              # run directly
    main()
```

## See also

- [`README.md`](README.md) — the only-code folder overview and the full
  list of development layers.
- [`../sensor-suite.md`](../sensor-suite.md) — the canonical **sensor →
  gate** map and the **two-witness** habit this layer turns into code.
- [`04-perception-and-vision.md`](04-perception-and-vision.md) — the
  camera witnesses (#1–#3) whose detections feed half of each visual
  gate.
- [`07-orchestration-and-task-logic.md`](07-orchestration-and-task-logic.md)
  — the behaviour tree that **ticks** these gates before each guarded
  motion; this layer feeds it rather than duplicating it.
- [`09-sensing-and-signal-acquisition.md`](09-sensing-and-signal-acquisition.md)
  — the layer that publishes the raw sensor topics (gripper effort,
  balance, load cell, level) this layer fuses.
```
