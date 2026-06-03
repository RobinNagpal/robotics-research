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
purchase: the loop is proven before a cable is plugged in.

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

## See also

- Folder overview: [`README.md`](README.md)
- Sibling mode (hardware in the loop):
  [`../02-code-plus-hardware/02-middleware-and-control.md`](../02-code-plus-hardware/02-middleware-and-control.md)
