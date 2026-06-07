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

## Meta code

The shape of the best-practical layer (ROS 2 + `ros2_control`, wired
into Gazebo by the `gz_ros2_control` plugin, plus a mock station node
that exposes a device as a *service* and streams a sensor *topic*),
before any library-specific detail:

```text
# (in the URDF) declare the gz_ros2_control plugin + the arm's joints     (the sim hardware_interface)
# (in YAML) configure the controller_manager + a joint_trajectory_controller
# on start-up the controller_manager loads and activates that controller  (now the arm accepts paths)
# a mock station node (here the balance, sensor #6) does two things:
#     it offers a service "weigh"           -> request/reply: "give me a mass reading now"
#     it publishes a topic /balance/mass    -> continuous stream of the current reading
# orchestration (Layer 07) calls the service before trusting a fill        (two-witness with the level)
# everything talks ROS 2 topics/services, identical to what real HW shows
```

## Real code

The best-practical pick is **ROS 2 + `ros2_control` with
`gz_ros2_control`**; the snippet below shows the *mock station* side of
it — a `rclpy` node that exposes a device as a service and streams a
sensor topic, the pattern every simulated station follows. This is
**illustrative teaching code**: client-library and message/service
names drift between versions, so re-verify before relying on it. Every
line carries an inline comment explaining exactly what it does.

```python
import rclpy                                          # ROS 2 Python client library (the robot framework)
from rclpy.node import Node                           # base class every ROS 2 program ("node") builds on
from std_msgs.msg import Float64                      # the message type we use for a single mass reading
from std_srvs.srv import Trigger                      # a ready-made request/reply: ask, get success + text
import random                                          # used only to fake a slightly noisy mass in sim


class MockBalance(Node):                              # the simulated analytical balance (sensor #6)
    def __init__(self):                               # set-up that runs once, when the node is created
        super().__init__("mock_balance")              # register on the ROS 2 graph as "mock_balance"
        self.mass_g = 0.0                             # the current reading in grams; updated each tick
        self.pub = self.create_publisher(             # open an outgoing channel for the live mass stream
            Float64, "/balance/mass", 10)             # type, topic name others read, inbox queue depth
        self.timer = self.create_timer(               # arrange to run a function on a fixed schedule
            0.1, self.tick)                           # every 0.1 s (10 Hz) call self.tick to refresh+publish
        self.srv = self.create_service(               # offer a request/reply service others can call
            Trigger, "weigh", self.on_weigh)          # service type, its name, the handler to run per call

    def tick(self):                                    # runs ten times a second, on the timer above
        self.mass_g = 12.50 + random.uniform(-0.01, 0.01)  # fake a ~12.5 g vial with tiny sim noise
        msg = Float64()                               # make the empty message we are about to fill in
        msg.data = self.mass_g                        # put the current mass into the message
        self.pub.publish(msg)                         # send it out on /balance/mass for anyone listening

    def on_weigh(self, request, response):             # runs whenever another node calls the "weigh" service
        response.success = True                       # report that the weighing completed without error
        response.message = f"{self.mass_g:.3f} g"     # return the latest mass as text in the reply
        self.get_logger().info(                       # print a tidy, time-stamped status line
            f"weigh requested -> {response.message}")  # show what reading we just reported
        return response                               # hand the filled reply back to the caller


def main():                                            # the standard ROS 2 program entry point
    rclpy.init()                                       # start up the ROS 2 client library (must come first)
    node = MockBalance()                               # build our node, which runs its __init__ set-up
    rclpy.spin(node)                                   # keep serving the topic + service until Ctrl-C
    node.destroy_node()                                # remove the node from the graph on shutdown
    rclpy.shutdown()                                   # close the ROS 2 client library cleanly


if __name__ == "__main__":                             # only run if this file is launched directly
    main()                                             # ...then start everything above
```

The arm half of this layer is configuration, not code: the
`gz_ros2_control` plugin is declared in the myCobot URDF (so Gazebo
plays the `hardware_interface`), and a `joint_trajectory_controller` is
spelled out in a controller YAML the `controller_manager` loads at
start-up. Those files are what let a planned path become timed joint
commands; the mock-station node above shows the *other* thing this layer
carries — a device exposed as a service plus a sensor streamed as a
topic, exactly as [`../sensor-suite.md`](../sensor-suite.md) describes.

## See also

- Folder overview: [`README.md`](README.md)
- Sibling mode (hardware in the loop):
  [`../02-code-plus-hardware/02-middleware-and-control.md`](../02-code-plus-hardware/02-middleware-and-control.md)
