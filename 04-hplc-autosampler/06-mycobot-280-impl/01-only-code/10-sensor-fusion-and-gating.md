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

### Two-witness grasp gate

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
- **Value:** "never carry nothing, never drop in transit" becomes a
  mechanical guarantee, not an assumption.

### Fail-safe safety gate

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
- **Value:** the gate fails closed, so a sensor dropout halts the arm
  instead of letting it move near a hand.

### Stale-witness rejection

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
- **Value:** closes the exact gap the cheap latest-value cache leaves open,
  making fused decisions trustworthy in time as well as value.

## Meta code

The shape of one best-practical two-witness gate, before any
library-specific detail:

```text
# subscribe to witness A for a fact   (e.g. gripper effort #4)
# subscribe to witness B for the same fact (e.g. wrist /vial_present #3)
# time-sync A and B so both describe the same instant   (ApproximateTimeSynchronizer)
# on each synced (A, B) pair:
#     in_band_A = effort_low <= A <= effort_high          (A within its expected band)
#     witness_B = (B is True)                              (B's independent confirmation)
#     agree     = in_band_A AND witness_B                  (the two-witness AND)
#     publish one boolean gate topic = agree               (-> a single trustworthy fact)
# the Layer 07 behaviour tree ticks this gate BEFORE the guarded motion:
#     gate True  -> proceed to the next step               (act only on agreement)
#     gate False -> retry the step, else quarantine, else stop   (FAIL branch)
```

## Real code

A minimal but complete ROS 2 (`rclpy`) **two-witness gate node**, using
the best-practical pick — `message_filters` to synchronise the witnesses
and a single fused boolean out. This is **illustrative teaching code**:
library and message names drift between versions, so re-verify before
relying on it. Every line carries an inline comment.

```python
import rclpy                                      # ROS 2 Python client library (the robot framework)
from rclpy.node import Node                       # base class every ROS 2 program ("node") builds on
from std_msgs.msg import Float64, Bool            # Float64 = grip effort number; Bool = a true/false fact
import message_filters                            # utility that time-aligns two topics into one callback

# --- fixed, known band for the "held" fact (re-verify against the real gripper) ---
EFFORT_LOW_NM = 2.0                               # below this, the jaws are basically empty (no vial)
EFFORT_HIGH_NM = 8.0                              # above this, the jaws are crushing or jammed (bad grip)


class HeldGateNode(Node):                          # fuses two witnesses into the single /gate/held fact
    def __init__(self):                            # set-up that runs once, when the node is created
        super().__init__("held_gate")             # register on the ROS 2 graph under the name "held_gate"
        effort_sub = message_filters.Subscriber(   # witness A: how hard the gripper is squeezing (#4)
            self, Float64, "/grip/effort")        # a Float64 in newton-metres, published by Layer 09
        present_sub = message_filters.Subscriber(  # witness B: does the wrist camera see a vial (#3)
            self, Bool, "/vial_present")          # a Bool, published by the Layer 04 perception node
        self.sync = message_filters.ApproximateTimeSynchronizer(  # pair the two by near-equal timestamp
            [effort_sub, present_sub],            # the two witness streams to line up in time
            queue_size=10,                        # how many recent messages each stream may buffer
            slop=0.1,                             # max seconds apart two messages may be and still pair
            allow_headerless=True)                # std_msgs carry no header, so stamp them on arrival
        self.sync.registerCallback(self.on_pair)  # call self.on_pair once per matched (effort, present)
        self.pub = self.create_publisher(         # open the outgoing channel for the fused verdict
            Bool, "/gate/held", 10)               # type, topic the Layer 07 tree subscribes to, queue depth

    def on_pair(self, effort_msg, present_msg):    # runs when a same-instant (effort, present) pair arrives
        in_band = EFFORT_LOW_NM <= effort_msg.data <= EFFORT_HIGH_NM  # witness A: grip force looks right
        sees_vial = bool(present_msg.data)        # witness B: the wrist camera confirms a vial is there
        held = in_band and sees_vial              # the two-witness AND: both must agree to trust "held"
        out = Bool()                              # make the empty boolean message we are about to publish
        out.data = held                           # the single fused verdict, true only if both witnesses agree
        self.pub.publish(out)                     # send it out on /gate/held for the behaviour tree to tick
        self.get_logger().info(                   # print a tidy, watchable status line for the sim run
            f"held={held} (effort={effort_msg.data:.1f} Nm, sees_vial={sees_vial})")  # show both witnesses


def main():                                        # the standard ROS 2 program entry point
    rclpy.init()                                    # start up the ROS 2 client library (must come first)
    node = HeldGateNode()                           # build our node, which runs its __init__ set-up
    rclpy.spin(node)                                # keep fusing witness pairs until you press Ctrl-C
    node.destroy_node()                             # remove the node from the graph on shutdown
    rclpy.shutdown()                                # close the ROS 2 client library cleanly


if __name__ == "__main__":                          # only run if this file is launched directly
    main()                                          # ...then start everything above
```

The `/gate/held` topic this node publishes is the **same** `held?`
condition the Layer 07 per-vial tree already ticks — see the `HeldGate`
leaf in
[`07-orchestration-and-task-logic.md`](07-orchestration-and-task-logic.md).
The only change there is that its single subscription becomes a
subscription to `/gate/held`, so the tree now consumes a **fused,
two-witness** verdict instead of one raw sensor. In only-code mode both
witness topics come from mock publishers, so you can **inject faults** —
publish an out-of-band effort, or flip `/vial_present` to `false` — and
watch the gate go `False` and the tree fall into its retry / quarantine /
stop branch, with no bench time.

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
- [`../02-code-plus-hardware/07-orchestration-and-task-logic.md`](../02-code-plus-hardware/07-orchestration-and-task-logic.md)
  — the same orchestration once **real sensors** feed the gates, where
  noise, latency, and calibration make fusion and bands earn their keep.
```
