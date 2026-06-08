# Layer 02 — Middleware & control (only-code)

> **Job:** Pick the plumbing that carries messages between the parts of
> the HPLC cell and the loop that drives the joints — here proven
> **entirely in simulation, with no real arm or stations attached.**

A quick vocabulary pass, because this layer is the jargon-heavy one and
the rest of the file leans on it:

- **Middleware** is the software "post office" that lets separate
  programs (a planner, a camera node, a gripper driver) send each other
  messages without each knowing where the others run. It is the layer
  *between* your application code and the network.
- **DDS** (Data Distribution Service) is the particular post-office
  standard ROS 2 uses by default. It finds peers automatically and ships
  data over the network.
- **RMW** (ROS MiddleWare interface) is the thin adapter that lets ROS 2
  swap one DDS (or non-DDS transport) for another without you rewriting
  application code. You pick an RMW with an environment variable.
- **Real-time** means *bounded, predictable timing* — the control loop
  fires every few milliseconds, on time, every time. In pure sim this is
  a soft concern (the simulator can wait for you); on hardware it bites,
  which is the sibling file's whole story.

In "only-code" mode nothing physical is on the other end of the wire, so
we optimise for **developer speed and a clean interface** that the real
build can inherit unchanged — not for microsecond latency.

## The five at a glance

| Framework | Role | Tier | One-liner |
|-----------|------|------|-----------|
| ROS 2 + ros2_control | Middleware + standard control framework | Best-in-class | The de-facto robotics stack; everything else plugs into it. |
| Plain rclpy + topics | Minimal Python messaging, no control framework | Cheapest | Just publish/subscribe in Python — fastest to start, least structure. |
| ROS 2 + ros2_control (+ gz_ros2_control) | Same stack, wired into the simulator | Best-practical | The sim-native build that transfers to hardware with one swapped plugin. |
| CycloneDDS | Default DDS/RMW under ROS 2 | Alternative | The lightweight transport doing the actual message delivery. |
| Zenoh / zenoh-bridge-ros2dds | Modern transport / bridge | Alternative | Newer, leaner pipe that can replace or bridge DDS. |
| micro-ROS | ROS 2 on microcontrollers (here simulated) | Alternative | Brings tiny station controllers into the same graph — mocked for now. |

## ROS 2 + ros2_control

**What it is.** ROS 2 is the open-source robotics middleware: a set of
libraries (`rclcpp` for C++, `rclpy` for Python) plus tools for nodes to
talk over **topics** (continuous streams), **services** (request/reply),
and **actions** (long jobs with feedback). `ros2_control` is the
companion framework that standardises *control*: it defines a
**hardware_interface** (the boundary where joint commands go out and
joint states come back) and a set of swappable **controllers** (e.g. a
`joint_trajectory_controller` that turns a planned path into timed joint
commands). Together they are the spine of the whole cell — the planner
(Layer 03), perception (Layer 04), and orchestration (Layer 07) all
exchange messages through ROS 2, and the arm is driven through
`ros2_control`.

**How it's good.** The decisive advantage is the **ecosystem and the
abstraction boundary**. MoveIt 2, Nav2, RViz, Gazebo bridges, and the
`mycobot_ros` packages all assume ROS 2, so choosing it unlocks the rest
of the stack for free. `ros2_control`'s `hardware_interface` is the
single most valuable idea for a two-mode project like this one: your
controllers and planners talk to an *abstract* arm, and only one small
plugin underneath changes when you move from sim to a real myCobot 280.
That means the code you write in "only-code" mode is the code you keep —
you do not rebuild the control layer for hardware, you swap a plugin.

**How it's bad (vs the other four).** It is the **heaviest** option
here. Versus plain `rclpy`, you pay a real setup cost: URDFs, controller
YAML, the controller_manager, and a vocabulary (interfaces, resources,
lifecycle) you must learn before anything moves — overkill if you only
wanted to publish a few messages. Versus **CycloneDDS** or **Zenoh**,
ROS 2 is the *application* layer, not the transport — it does not itself
make delivery faster or leaner; it inherits whatever the RMW under it
does, so those alternatives complement rather than compete. Versus
**micro-ROS**, full ROS 2 is far too large to run on a microcontroller,
which is exactly the gap micro-ROS fills. So ROS 2 + ros2_control wins on
reach and structure but loses on minimalism and on tiny embedded targets.

## Plain rclpy + topics

**What it is.** This is ROS 2 stripped to its smallest useful core: you
import `rclpy` (the Python client library), create a node, and `publish`
/ `subscribe` on a few topics — no `ros2_control`, no controllers, no
hardware_interface. To "move" the simulated arm you would publish joint
commands directly to whatever the simulator listens on, or drive a sim
plugin yourself. It is messaging without the control framework.

**How it's good.** It is the **cheapest to start** and the easiest to
reason about. A newcomer can have two Python scripts talking in an
afternoon; there is no YAML, no controller lifecycle, no URDF parsing to
fight. For early experiments — does my orchestration logic call the
right things in the right order? — this minimalism is a genuine virtue,
and it stays in Python end to end, which suits a software-primary team.

**How it's bad (vs the other four).** It **does not scale into a real
control layer**. Versus ROS 2 + `ros2_control`, you get no
`hardware_interface`, so the code you write to wiggle joints in sim is
throwaway — it will not transfer to the real arm, and you will rebuild
this layer for hardware (the opposite of what the project wants). It also
lacks the off-the-shelf `joint_trajectory_controller`, so smooth, timed
trajectory following becomes your problem to hand-roll. Versus
**CycloneDDS**/**Zenoh**, it still rides on a DDS underneath, so it is no
faster — just less structured. Versus **micro-ROS**, it offers nothing
on the embedded side. Cheap and fast to begin, costly to grow.

## ROS 2 + ros2_control (+ gz_ros2_control)

**What it is.** The same Best-in-class stack, but with the
**`gz_ros2_control`** plugin loaded inside the Gazebo simulator. This
plugin *is* a `hardware_interface` implementation — except instead of
talking to a real motor it talks to the simulated joints. So the
`controller_manager`, the `joint_trajectory_controller`, and every node
above behave exactly as they will on hardware, while Gazebo plays the
part of the arm.

**How it's good.** It is the **best-practical** pick because it gives you
the full, real architecture with zero hardware cost. You write and debug
controller configs, action interfaces, and orchestration against a
faithful stand-in, and the *only* thing that changes for hardware is
swapping the `gz_ros2_control` plugin for the myCobot's real
hardware_interface — described in the sibling file. It de-risks the
purchase: the loop is proven before a cable is plugged in. The same
middleware also **carries the simulated sensor suite**: the Gazebo
camera, depth-camera, force-torque, IMU, and logical-camera plugins —
plus the mock safety topics — publish onto ordinary ROS 2 topics, the
*identical* interface a real sensor would present, so perception and
orchestration consume them with no idea whether the bytes came from a
plugin or a device (see [`../sensor-suite.md`](../sensor-suite.md)).

**How it's bad (vs the other four).** It carries **all** of
`ros2_control`'s setup weight (so heavier than plain `rclpy`) plus a
sim-specific gotcha: `gz_ros2_control` faithfully reproduces the
*interface* but **not** real timing — the sim can stretch or pause time,
so a loop that looks fine here can still miss deadlines on a real serial
link. It therefore proves *behaviour*, not *real-time performance*; that
honesty is the whole reason the hardware sibling exists. Versus
**Zenoh**/**CycloneDDS** it is again an application concern, not a
transport one. Versus **micro-ROS**, the simulated station controllers
here are just ordinary nodes, not true embedded firmware.

## CycloneDDS

**What it is.** **CycloneDDS** (Eclipse) is one of the DDS
implementations that can sit underneath ROS 2 as the **RMW** — the actual
code that discovers peers and ships bytes across the network. You select
it by setting `RMW_IMPLEMENTATION=rmw_cyclonedds_cpp`. On many ROS 2
distributions it is already the default; on others you opt in.

**How it's good.** It is **light and dependable**, with a small footprint
and sane defaults, which is why it is a popular default RMW. For a
single-machine sim cell it just works, with little tuning, and it plays
cleanly with the rest of the ROS 2 graph.

**How it's bad (vs the other four).** It is **invisible plumbing**, not a
thing you build features on — versus ROS 2 + `ros2_control` it provides
no control concepts at all, only delivery. Versus **Zenoh** it is the
older design: in environments with lots of nodes or flaky networks,
DDS's automatic discovery can get chatty, which is one motivation for
Zenoh. In "only-code" mode none of this matters much — everything is on
one host — so CycloneDDS is correctly an **Alternative**: good to know
it is there, rarely something you touch until hardware and latency enter
the picture (see the sibling file's CycloneDDS-vs-Fast-DDS discussion).

## Zenoh / zenoh-bridge-ros2dds

**What it is.** **Zenoh** is a newer open-source data-transport protocol
(pub/sub plus query and storage) designed to be lean from tiny devices
up to the cloud. `zenoh-bridge-ros2dds` lets a ROS 2 system speak Zenoh —
either bridging a DDS graph across an awkward network, or (via the
`rmw_zenoh` RMW) replacing DDS as the transport altogether.

**How it's good.** It shines where DDS struggles: **across networks,
through firewalls, or over weak links**, where its routed model avoids
DDS's noisy auto-discovery. It is increasingly first-class in the ROS 2
world and is a sensible future-proofing bet for distributed or remote
setups.

**How it's bad (vs the other four).** For a **one-host simulation** it is
**solving a problem you don't have** — versus CycloneDDS it adds a moving
part (a bridge or a less-defaulted RMW) for benefits that only appear
once messages cross machines. Versus ROS 2 + `ros2_control` it is, again,
transport not control. Versus **micro-ROS** it does not target bare
microcontrollers. Hence Alternative: worth a note for the day a remote
operator console or a multi-machine layout appears, premature today.

## micro-ROS

**What it is.** **micro-ROS** is a port of ROS 2 sized for
**microcontrollers** (MCUs) — the small chips that would, on real
hardware, drive peripheral stations like the decapper or the dispenser.
It speaks the same topics/services/actions as full ROS 2 via a tiny
client plus a host-side **agent**, so an MCU appears as just another node
in the graph. In "only-code" mode there is no MCU, so these station
controllers are **simulated** — ordinary nodes faking the firmware.

**How it's good.** It keeps **one mental model**: even the lowest-level
device controllers are ROS 2 nodes, so orchestration talks to the
decapper the same way it talks to the arm. Mocking them now means the
real micro-ROS firmware can drop in later without changing the message
contracts — the same transfer-friendly story as `gz_ros2_control`.

**How it's bad (vs the other four).** Its whole reason for existing —
running on constrained MCUs — is **moot without hardware**, so in sim it
buys nothing the plain nodes don't, and it adds the agent and a
cross-compile toolchain you don't need yet. Versus full ROS 2 +
`ros2_control` it is deliberately a *subset* (fewer features, tighter
limits). Versus **CycloneDDS**/**Zenoh** it is an application-side
client, not a general transport. So today it is an Alternative — a
placeholder for the hardware build, where it becomes genuinely useful.

## How the sensor suite rides this layer

Every sensor in [`../sensor-suite.md`](../sensor-suite.md) reaches the
rest of the cell as a standard ROS 2 topic carried by this layer —
identical to what a real device would publish, so nothing above changes
at hardware bring-up:

- Cameras #1–#3 → `sensor_msgs/Image` (+ `CameraInfo`, and
  `PointCloud2` for the depth cameras).
- Gripper feedback #4 → `sensor_msgs/JointState` (jaw position +
  effort), via `ros2_control` and a grasp-fix contact.
- Decapper torque #5 → `geometry_msgs/WrenchStamped` from the Gazebo
  force-torque sensor on the cap joint.
- Balance #6 / level #8 → the fill-volume scalar exposed as a small
  custom or `std_msgs` reading.
- Station presence #7 → a logical-camera / contact message per station.
- Limit/home #9 → joint-limit state on `JointState`.
- Base IMU #12 → `sensor_msgs/Imu`.
- Safety #10/#11 → mock `std_msgs/Bool` topics `/light_curtain_clear`,
  `/door_closed`, `/estop`.

## Verdict

- **Best-in-class: ROS 2 + ros2_control.** The de-facto standard with the
  ecosystem (MoveIt, Gazebo, `mycobot_ros`) and, crucially, the
  `hardware_interface` boundary that lets sim code transfer to hardware
  untouched.
- **Cheapest: plain rclpy + topics.** Pure-Python publish/subscribe with
  no control framework — quickest to stand up, but the control code is
  throwaway and won't carry to the real arm.
- **Best-practical: ROS 2 + ros2_control with gz_ros2_control.** The full
  real architecture proven in Gazebo at zero hardware cost; moving to
  hardware swaps a single plugin and nothing above it changes.

## Realistic scenario & use cases

> **Why this matters for automation.** Middleware is invisible when it
> works and catastrophic when it doesn't: it is what keeps the arm,
> cameras, decapper, dispenser, balance, and safety chain talking without
> any one of them knowing about the others. Its automation value is
> **decoupling** — you can add, swap, mock, or lose a part without
> rewriting the rest — and a **clean boundary** so today's sim code is
> tomorrow's hardware code.

**The scenario.** Mid-run, the cell is transferring vial 47 while the
overhead camera streams point clouds at 10 Hz and orchestration waits on
a weigh result. At that instant the **dispenser station controller (a
mocked micro-ROS node) goes silent for ~2 seconds**, a developer **adds a
second wrist camera** to the graph, and the lab asks to **swap the
transport from CycloneDDS to Zenoh** for an upcoming remote-console
trial. The cell must not deadlock, the arm must finish or safely hold its
trajectory, the new camera must appear without touching planner code, and
the transport swap must change nothing above it. Every one of those is a
middleware/control job.

The layer must therefore serve several **distinct use cases**:

1. **Hot add / replace of a node.** Bring the second wrist camera online,
   or swap a mock station for a better one, with zero edits to
   orchestration or planning.
   - *How the solution handles it:* everything publishes/subscribes on
     **named topics**, so a new `/wrist2/points` publisher is simply one
     more topic; subscribers that don't care never notice.

2. **Sim-to-hardware transfer with one plugin swap.** The same
   controllers, actions, and YAML that drive Gazebo today must drive the
   real myCobot later.
   - *How:* the `ros2_control` **hardware_interface** boundary means
     `gz_ros2_control` (sim) and the myCobot driver (hardware) are
     interchangeable underneath an unchanged `joint_trajectory_controller`.

3. **Timed trajectory execution with preemption.** Turn a planned path
   into smooth, on-time joint commands — and cleanly replace it if Layer
   03 issues a new plan mid-motion (e.g. a re-grasp).
   - *How:* the `joint_trajectory_controller` consumes a
     `FollowJointTrajectory` **action**, which supports goal preemption,
     so a new goal cancels and supersedes the old without a stop-start jerk.

4. **Device-as-service, sensor-as-topic — with timeouts.** Orchestration
   calls `weigh` / `decap` services and reads `/balance/mass`; if the
   station is unresponsive it must get a **timeout**, never a hang.
   - *How:* services carry call timeouts and topics carry **QoS deadlines**,
     so the silent dispenser surfaces as a failed call the gate logic can
     act on (retry, pause, alarm) rather than a frozen graph.

5. **Graceful degradation on a lost node or e-stop.** If a station node
   dies or `/estop` fires mid-trajectory, controllers must hold/stop
   safely and the graph must recover when the node returns.
   - *How:* **lifecycle-managed** nodes plus the `controller_manager` let
     a controller be deactivated/held on fault and reactivated on
     recovery, while DDS auto-discovery re-attaches the returning node.

**Where the pick flexes.** The best-practical stack (ROS 2 + ros2_control
+ gz_ros2_control) covers all five directly. The transport swap in the
scenario is exactly where **CycloneDDS → Zenoh** matters — and because
that is an **RMW** choice (an environment variable), use case 1's "change
nothing above it" promise holds. The silent dispenser is the stand-in for
real **micro-ROS** station firmware, mocked now so the contract is proven
before any MCU exists.

## Deep dive: the three highest-value use cases

The five above all matter; these three carry the most weight for
middleware & control.

## Timed trajectory execution with preemption

Watch a lab assistant move a vial and you see one continuous, smooth
motion — pick, carry, place — not a series of jerks. And if something
changes mid-reach (the vial shifts, they need to adjust), the motion flows
into the correction rather than stopping and restarting. This use case is
the cell producing that same smooth, on-time motion: turning a planned
path into precisely-timed joint commands, and cleanly replacing the motion
if a new plan arrives partway through.

The bigger experiment is the HPLC batch, every vial of which requires
several arm moves — to the nest, to the decapper, to the dispenser, to the
tray. Each of those moves must be executed smoothly and land on time, and
any of them might be superseded mid-flight by a corrected target from
perception. This layer is what actually drives the joints to follow the
plan, and what lets a new plan take over without a stop-start jerk.

The assistant makes smooth, adjustable motions continuously — it underlies
every reach and place, hundreds of times a day. The cell executes a timed
trajectory for every single arm motion in the loop — several per vial — so
this is one of the most frequently-exercised paths in the whole system,
running thousands of times across an overnight batch.

- **The moment:** a planned path arrives for the arm; halfway through,
  Layer 03 issues a corrected plan, and the motion must switch to it
  smoothly.
- **How, in depth:** the `joint_trajectory_controller` consumes a
  `FollowJointTrajectory` action, interpolating the waypoints into timed
  joint commands and accepting a new goal that preempts the old one.
- **Edge case it survives:** a new goal arriving while the previous one is
  still executing — preemption cancels the old and blends into the new
  from the live state, with no stop-start jerk.
- **Walkthrough:** (1) receive a planned trajectory as an action goal; (2)
  the controller drives the joints along it on time; (3) a new goal
  arrives and preempts the current one; (4) the arm continues onto the new
  trajectory from where it is.
- **In the scene:** the arm sweeps smoothly toward a nest; mid-sweep a
  corrected target arrives and the motion bends into it without pausing,
  the way a hand adjusts mid-reach.
- **Why it's done this way:** vials must be moved smoothly — jerks slosh
  liquid — and motions must adapt to live corrections; a controller that
  couldn't preempt would force a stop-and-restart on every correction.
- **In the full loop:** this is the execution half of every move Layer 03
  plans — the actual driving of the joints — so it runs for each of the
  several arm motions per vial.
- **Value:** every arm motion is smooth and on-time, and a correction is
  absorbed mid-flight instead of forcing a stop-start.

### Meta code

This meta lives in a standard controller — the `joint_trajectory_controller`
from `ros2_control` — whose job is to turn a discrete planned path into a
continuous stream of timed joint commands. A planned trajectory is a list
of waypoints, each with target joint positions and a time; the controller
interpolates between them so the arm passes through each waypoint on
schedule.

The path is delivered as an action goal (`FollowJointTrajectory`), which
matters because actions are preemptable. While a trajectory is executing, a
new goal can arrive — for instance, Layer 03 replanned because perception
corrected the target — and the controller accepts it as the new active
goal.

On preemption the controller cancels the in-flight trajectory and begins
the new one from the arm's current state, blending the motion rather than
stopping dead and starting over. This is what makes a live correction look
like a smooth adjustment instead of a stutter.

Velocity and acceleration limits in the controller keep the motion within
safe bounds — gentle enough not to slosh a filled vial — while still
tracking the schedule. The execution in pseudocode:

```text
# the joint_trajectory_controller is loaded + active (see middleware)
# on a new FollowJointTrajectory goal (a planned path):
#     if a trajectory is already executing -> preempt it          (cancel the old goal)
#     start following the new path from the arm's CURRENT state   (smooth blend, no restart)
#     interpolate waypoints into timed joint commands             (on-schedule motion)
#     respect velocity / acceleration limits                      (gentle: no slosh)
#     report success when the final waypoint is reached           (-> the next layer may grasp)
```

### Real code

A client that sends a planned path as an action goal and preempts a
previous one. **Illustrative teaching code** — re-verify before use; every
line is commented.

```python
import rclpy                                            # ROS 2 Python client library
from rclpy.node import Node                             # base class for a ROS 2 program
from rclpy.action import ActionClient                   # to send and preempt trajectory goals
from control_msgs.action import FollowJointTrajectory   # the controller's trajectory action
from trajectory_msgs.msg import JointTrajectory         # the planned path (waypoints) to follow

JOINTS = ["joint1", "joint2", "joint3", "joint4", "joint5", "joint6"]  # the six myCobot joints


class TrajectoryRunner(Node):                           # sends planned paths, preempting on a new one
    def __init__(self):                                 # one-time setup
        super().__init__("trajectory_runner")           # register on the ROS 2 graph
        self.client = ActionClient(                     # client to the trajectory controller
            self, FollowJointTrajectory,
            "/joint_trajectory_controller/follow_joint_trajectory")
        self.active = None                              # handle to the goal currently executing

    def run(self, path: JointTrajectory):               # execute a path, preempting any current one
        self.client.wait_for_server()                   # ensure the controller is up
        if self.active is not None:                     # a trajectory is already running?
            self.active.cancel_goal_async()             # preempt it (the new path supersedes it)
        goal = FollowJointTrajectory.Goal()             # build the action goal
        goal.trajectory = path                          # the waypoints + their times to follow
        goal.trajectory.joint_names = JOINTS            # which joints the positions apply to
        send = self.client.send_goal_async(goal)        # send it without blocking
        send.add_done_callback(self._accepted)          # remember the handle once accepted

    def _accepted(self, future):                        # runs when the controller accepts the goal
        self.active = future.result()                   # keep the handle so we can preempt later
        self.active.get_result_async().add_done_callback(self._done)  # watch for completion

    def _done(self, _future):                           # runs when the trajectory finishes
        self.active = None                              # clear the handle; the arm is idle again


def main():                                             # standard ROS 2 entry point
    rclpy.init(); rclpy.spin(TrajectoryRunner()); rclpy.shutdown()  # start, run, clean up


if __name__ == "__main__":                              # run directly
    main()
```

## Device-as-service with timeouts

A lab assistant is constantly asking the bench's instruments for something
and waiting on the answer — placing a vial on the balance and waiting for
a stable mass, triggering the dispenser and waiting for it to finish. But
a person never waits forever: if the balance won't settle or the dispenser
jams, they notice, set the sample aside, and keep the batch moving. This
use case gives the cell that same instinct — it calls a station (weigh,
dispense, decap) and, if the station goes silent, gets a clean timeout
instead of freezing.

The bigger experiment is the HPLC batch, where every single vial passes
through several of these station interactions before it reaches the tray.
A weigh that never returns, on a cell that waits forever, would stall the
entire overnight run on one bad device. Bounding every station call is
what keeps the run flowing — a silent dispenser costs one vial's retry,
not the night.

The assistant leans on these stations for essentially every vial they
prepare — weighing, diluting, dispensing — so the underlying "ask a
station and wait for it" happens dozens to a few hundred times a day. The
cell makes the same calls at the same cadence, which is exactly why each
one has to fail gracefully rather than hang.

- **The moment:** orchestration calls `weigh` and reads `/balance/mass`;
  mid-run the dispenser controller goes silent for 2 s and the loop must
  not freeze.
- **How, in depth:** each station exposes a **service** (request/reply) for
  actions and a **topic** for its stream; calls carry timeouts and topics
  carry **QoS deadlines**, so a silent station returns a failed call, not a
  hang.
- **Edge case it survives:** a station that answers *slowly* rather than
  not at all — the deadline still fires, and the gate logic treats a late
  reply as a miss instead of trusting stale data.
- **Walkthrough:** (1) orchestration calls `weigh` with a timeout; (2) the
  dispenser node goes silent; (3) the call returns a timeout error rather
  than blocking; (4) the gate logic retries, pauses, or alarms on that
  failed call.
- **In the scene:** orchestration politely asks the balance "what do you
  weigh?" and waits; the dispenser, meanwhile, has gone dark. A countdown
  ticks, expires, and the request comes back marked "failed" rather than
  hanging the whole cell on a station that simply stopped answering.
- **Why it's done this way:** real lab devices stall, reboot, and drop
  messages; a cell that hangs on the first silent station cannot run
  unattended, so every cross-device call must have a bounded failure
  rather than an open-ended wait.
- **In the full loop:** each per-vial step that calls a station — weigh,
  dispense, decap — goes through this; a timeout here is what lets Layer
  07's gate decide to retry or quarantine that vial instead of stalling
  the run.
- **Value:** one flaky device degrades to a handled exception, never a
  deadlocked cell.

### Meta code

The meta for a bounded station call is about never trusting a remote
device to answer. A station like the balance is exposed two ways: a
*service* for actions you ask it to perform ("weigh now, and reply") and a
*topic* for the continuous stream it produces ("here is the mass, ten
times a second"). The pipeline uses both, but it treats every interaction
as something that might silently fail.

When orchestration needs a fresh mass, it sends the weigh request
asynchronously and then waits — but only up to a fixed timeout. If the
reply arrives in time, it returns the value; if the timeout expires first,
it raises a specific error rather than blocking. That single design choice
is what turns a dead station from a frozen cell into a handled exception
the gate logic can act on (retry, pause, alarm).

The streaming side gets the same treatment through QoS deadlines: the
subscription expects a sample at least every so often, so a stream that
goes quiet — a station that is technically alive but no longer producing —
is detected as stale rather than assumed good. A slow station and a dead
one both surface, instead of one of them sneaking through.

The net effect is that no single cross-device call can ever hang the loop.
The call in pseudocode:

```text
# create a service client for "weigh" + a subscriber for /balance/mass (QoS with a deadline)
# when orchestration needs a mass:
#     send the weigh request with a bounded timeout
#     pump callbacks up to that timeout:
#         reply arrives -> return the mass                           (happy path)
#         timeout fires -> raise StationTimeout the gate can act on  (retry / pause / alarm)
# the /balance/mass deadline event flags a stream that went stale    (slow, not silent)
```

### Real code

A client that calls the `weigh` service with a bounded timeout and watches
`/balance/mass` for a stale stream. **Illustrative teaching code** —
re-verify before use; every line is commented.

```python
import rclpy                                            # ROS 2 Python client library
from rclpy.node import Node                             # base class for a ROS 2 program
from rclpy.qos import QoSProfile, QoSReliabilityPolicy  # to attach a deadline to the stream
from rclpy.duration import Duration                     # express the deadline as a time span
from std_srvs.srv import Trigger                        # the "weigh" request/reply service type
from std_msgs.msg import Float64                        # the /balance/mass stream message type


class StationTimeout(Exception):                        # raised when a station doesn't answer in time
    pass                                                # the gate logic catches this to retry/pause


class WeighClient(Node):                                # calls a station service without ever hanging
    def __init__(self):                                 # one-time setup
        super().__init__("weigh_client")                # register on the ROS 2 graph
        self.cli = self.create_client(Trigger, "weigh")  # a client for the balance's weigh service
        qos = QoSProfile(depth=10,                      # a small inbox...
                         reliability=QoSReliabilityPolicy.BEST_EFFORT,  # sensor streams: best-effort
                         deadline=Duration(seconds=1))  # expect a sample at least once a second
        self.create_subscription(                       # watch the live mass stream...
            Float64, "/balance/mass", self.on_mass, qos)  # ...so we can tell if it goes stale
        self.last_mass = None                           # the most recent reading we trusted

    def on_mass(self, msg):                             # runs on each /balance/mass sample
        self.last_mass = msg.data                       # cache the latest mass for quick reads

    def weigh(self, timeout_s=2.0):                     # ask for a fresh mass, but never block forever
        if not self.cli.wait_for_service(timeout_sec=timeout_s):  # is the service even up?
            raise StationTimeout("weigh service absent")  # no -> a handled failure, not a hang
        future = self.cli.call_async(Trigger.Request())  # send the request without blocking
        rclpy.spin_until_future_complete(               # pump callbacks until the reply or...
            self, future, timeout_sec=timeout_s)        # ...the timeout, whichever comes first
        if not future.done():                           # the deadline fired before a reply arrived
            raise StationTimeout("weigh timed out")     # -> the gate retries / pauses / alarms
        return future.result().message                  # the reply text (the mass) on success
```

## Graceful degradation on a lost node or e-stop

When a piece of bench equipment hiccups mid-batch — a balance reboots, a
dispenser locks up for a moment — an experienced lab assistant doesn't
scrap the whole tray. They pause, let the device recover or switch to a
spare, and pick up where they left off. This use case engineers that
resilience into the cell: if one of the cell's software stations crashes,
the arm holds safely rather than lurching, and the loop resumes once the
station comes back.

The bigger experiment is the unattended overnight HPLC batch, which can
run for many hours across dozens of vials. Over that long a stretch, some
component will inevitably stumble. If a single crashed station forced the
whole run to abort, the cell would rarely finish a tray; treating a lost
station as a recoverable pause rather than a fatal error is what makes
leaving it unattended realistic.

For the lab assistant, an equipment hiccup is occasional but normal —
perhaps a few times a week across a busy bench, more on aging instruments.
The cell faces the software equivalent (a node crash, a dropped
connection) on a similar scale over long runs, so the recovery path here
is built to be exercised routinely, not treated as a once-a-year
emergency.

- **The moment:** a station node crashes or `/estop` fires mid-trajectory;
  the arm must hold/stop safely and the graph must recover when the node
  returns.
- **How, in depth:** **lifecycle-managed** nodes plus the
  `controller_manager` let a controller be deactivated/held on fault and
  reactivated on recovery, while DDS auto-discovery re-attaches the
  returning node without a restart.
- **Edge case it survives:** the node returning *mid-cycle* — because the
  topic/service contracts are unchanged, orchestration resumes from its own
  state rather than re-initialising the whole graph.
- **Walkthrough:** (1) a station node crashes mid-cycle; (2) the
  `controller_manager` holds/deactivates its controller; (3) the node
  relaunches and DDS auto-discovery re-attaches it; (4) orchestration
  resumes from its own persisted state, no full restart.
- **In the scene:** a station process dies and a corner of the graph goes
  quiet; the arm freezes its controller rather than lurching. Seconds later
  the process is back, the network quietly re-introduces it, and the loop
  picks up its thread as if nothing happened.
- **Why it's done this way:** over a multi-hour run some process will
  crash; if a single dead node forced a full restart the cell would lose
  the night's work, so the architecture treats node loss as a recoverable
  event, not a fatal one.
- **In the full loop:** across a 96-vial run any station may drop; this
  layer's recovery is what keeps the graph alive between Layer 07's
  per-vial steps, so one crash doesn't end the night.
- **Value:** a single dead process is survivable and self-healing, not a
  night's run lost.

### Meta code

The watchdog's meta is built around *liveliness*: rather than waiting for
a station to actively report a failure, it watches for the station to go
quiet. Each station emits a heartbeat on a topic, and the watchdog
subscribes with a deadline QoS that fires an event the moment a heartbeat
is overdue.

On that missed-deadline event — the station has died — the watchdog acts
immediately on the one thing that matters for safety: it asks the
`controller_manager` to deactivate (hold) the arm's trajectory controller,
so the arm stops cleanly instead of continuing a motion that depended on
the now-dead station. It also marks the station down so orchestration can
pause the affected step.

Recovery is the mirror image. When the crashed node relaunches, the
middleware's automatic peer discovery re-attaches it and its heartbeats
resume; the watchdog sees the stream return and asks the
`controller_manager` to reactivate the controller, letting the arm move
again. Because the topic and service contracts never changed, the rest of
the graph resumes from its own state with no restart.

The result is a cell that treats a lost station as a brief, self-healing
pause. The watchdog in pseudocode:

```text
# watch each station's heartbeat topic with a deadline QoS           (liveliness)
# on a missed deadline (node died):
#     call controller_manager /switch_controller -> deactivate/hold   (arm stops safely)
#     mark the station DOWN                                           (orchestration pauses it)
# on the heartbeat returning (node relaunched, DDS re-discovers it):
#     call /switch_controller -> reactivate the controller            (arm resumes)
#     mark the station UP                                             (loop continues)
```

### Real code

A watchdog that holds the arm's controller when a station's heartbeat
stops and resumes it when the node returns. **Illustrative teaching
code** — re-verify before use; every line is commented.

```python
import rclpy                                            # ROS 2 Python client library
from rclpy.node import Node                             # base class for a ROS 2 program
from rclpy.qos import QoSProfile, QoSReliabilityPolicy  # for a deadline on the heartbeat stream
from rclpy.qos_event import SubscriptionEventCallbacks  # lets us react to a missed deadline
from rclpy.duration import Duration                     # express the deadline as a time span
from std_msgs.msg import Header                         # the station heartbeat message type
from controller_manager_msgs.srv import SwitchController  # to activate/deactivate controllers

ARM_CTRL = "joint_trajectory_controller"               # the controller that drives the arm


class StationWatchdog(Node):                            # holds/resumes the arm on station loss/recovery
    def __init__(self):                                 # one-time setup
        super().__init__("station_watchdog")            # register on the ROS 2 graph
        self.up = True                                  # current belief about the station's health
        self.switch = self.create_client(               # client to the controller_manager's switcher
            SwitchController, "/controller_manager/switch_controller")
        qos = QoSProfile(depth=1,                       # only the newest heartbeat matters...
                         reliability=QoSReliabilityPolicy.RELIABLE,  # heartbeats must arrive
                         deadline=Duration(seconds=1))  # ...at least once per second
        events = SubscriptionEventCallbacks(            # hook QoS events on this subscription
            deadline=lambda info: self.on_missed())     # a missed deadline => heartbeat overdue
        self.create_subscription(                       # subscribe to the dispenser's heartbeat
            Header, "/dispenser/heartbeat",             # the topic the station pings on
            self.on_beat, qos, event_callbacks=events)  # on_beat = recovery, deadline = loss

    def on_beat(self, _msg):                            # a heartbeat arrived -> station is alive
        if not self.up:                                 # only act on the up-edge (once)
            self.up = True                              # mark the station UP again
            self._switch(activate=[ARM_CTRL])           # let the arm move again

    def on_missed(self):                                # a heartbeat deadline was missed -> node dead
        if self.up:                                     # only act on the down-edge (once)
            self.up = False                             # mark the station DOWN
            self._switch(deactivate=[ARM_CTRL])         # hold the arm safely

    def _switch(self, activate=(), deactivate=()):      # ask controller_manager to flip controllers
        req = SwitchController.Request()                # build the switch request
        req.activate_controllers = list(activate)       # controllers to start (empty if none)
        req.deactivate_controllers = list(deactivate)   # controllers to stop (empty if none)
        req.strictness = SwitchController.Request.BEST_EFFORT  # tolerate a partial switch
        self.switch.call_async(req)                     # fire it without blocking the watchdog


def main():                                             # standard ROS 2 entry point
    rclpy.init()                                         # start the client library
    rclpy.spin(StationWatchdog())                       # run the watchdog until Ctrl-C
    rclpy.shutdown()                                     # clean shutdown


if __name__ == "__main__":                              # run directly
    main()
```

## See also

- Folder overview: [`README.md`](README.md)
