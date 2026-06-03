# Layer 02 — Middleware & control (code-plus-hardware)

> **Job:** Carry messages between the parts of the HPLC cell and drive
> the joints — now with a **real myCobot 280 and real peripheral
> stations on the wire,** where latency, timing, and the transport you
> choose stop being abstract and start mattering.

The vocabulary is the same as the sim file, but the stakes change:

- **Middleware** — the software "post office" between programs (planner,
  perception, gripper driver) so they exchange messages without knowing
  where each other runs.
- **DDS** — the post-office *standard* ROS 2 uses by default; finds peers
  and ships data over the network. Two implementations matter here:
  **CycloneDDS** and **Fast DDS**.
- **RMW** — the adapter that lets ROS 2 swap one DDS for another via an
  environment variable, without rewriting application code.
- **Real-time** — *bounded, predictable timing*. A control loop must fire
  on schedule; if a message or a serial read is late, the arm stutters or
  a deadline is missed. In sim the clock could wait for you; **a real
  motor cannot.** This is the through-line of the whole file.

This layer also **carries the real sensor data.** The cell's full sensor
suite (see [`../sensor-suite.md`](../sensor-suite.md)) reaches the graph
*through* this middleware: camera SDKs, a force-torque / IMU node, serial
sensor nodes, and GPIO for proximity, limit, and safety lines all publish
onto the **same ROS 2 topics the sim used**, so the gates above don't know
(or care) whether a reading came from Gazebo or a real device. That faith
in the topic boundary is exactly why the new hardware concerns land here:
**latency and QoS** for sensor streams (a depth stream wants low,
predictable latency, not just reliable delivery), **time-sync** across
devices so two-witness checks compare frames from the *same* instant, and
the cardinal rule that the cell must **never act on a stale frame** — a
late or dropped reading must be detected and treated as "unknown," not
trusted as current.

With hardware attached, the cheapest-to-run idea and the
best-to-live-with idea diverge — so the comparison below weighs each
option on what it costs you *at 50 Hz on a real USB serial link,* not
just what it costs to set up.

## The five at a glance

| Framework | Role | Tier | One-liner |
|-----------|------|------|-----------|
| ROS 2 + ros2_control (real hardware_interface) | Middleware + control, driving the real arm | Best-in-class | The standard stack with a clean driver boundary to the myCobot. |
| pymycobot bridge + pyserial | Wrap the vendor SDK / raw serial into ROS 2 | Cheapest | Least to set up — talk to the arm and stations with plain Python. |
| ROS 2 + ros2_control | Same standard stack | Best-practical | The maintainable middle: clean interface, transfers from sim, real-time-honest. |
| micro-ROS (real) | ROS 2 firmware on station MCUs | Alternative | Real microcontroller nodes for the decapper/dispenser stations. |
| CycloneDDS vs Fast DDS | RMW choice & tuning | Alternative | The transport knob you turn for latency and reliability. |
| pyserial / python-can | Raw device I/O for stations | Alternative | Lowest-level byte/frame plumbing to non-ROS peripherals. |

## ROS 2 + ros2_control (real hardware_interface)

**What it is.** The same ROS 2 + `ros2_control` stack as in sim, but now
the **hardware_interface** at the bottom is a *real* driver: it opens the
myCobot 280's serial connection, writes joint commands to the arm, and
reads joint states back, exposing them to the `controller_manager` and
its controllers (e.g. `joint_trajectory_controller`). Everything above —
MoveIt 2, orchestration, perception — is unchanged from the sim build;
only this bottom plugin swapped from `gz_ros2_control` to the arm's
driver. A `hardware_interface` is simply the well-defined seam where
"commanded joint positions out, measured joint states in" crosses from
software into a specific device.

**How it's good.** It gives you a **clean, swappable boundary** plus
ready-made, well-behaved controllers. The `joint_trajectory_controller`
interpolates a planned path into smoothly timed setpoints and reports
state in a standard way, so MoveIt's output flows straight to the motors.
Because the interface is identical to the simulator's, **the entire
upper stack transfers from the only-code build with no rewrite** — the
sim work pays off directly. And `ros2_control` is explicit about timing:
it runs the read→update→write cycle at a configured rate, which forces
you to confront the real control-loop question head-on rather than hiding
it inside a script.

**How it's bad (vs the other four).** It is the **most to set up** and
the most to understand — versus the **pymycobot bridge + pyserial**
shortcut you must learn interfaces, resources, controller YAML, and the
lifecycle before the arm twitches. It also inherits a **hard physical
limit**: the myCobot 280 talks over a relatively slow **USB serial**
link, so a clean `hardware_interface` cannot conjure a fast, hard
real-time loop the hardware can't sustain (the firmware/serial path
realistically supports only a modest update rate, on the order of a few
tens of Hz — re-verify per firmware). Versus **micro-ROS** it does not
itself run on the station MCUs. Versus the **CycloneDDS-vs-Fast-DDS**
knob it is application-level — your RMW choice still decides delivery
latency underneath it. Heavier to adopt, but the only option that is both
maintainable and faithfully sim-compatible.

## pymycobot bridge + pyserial

**What it is.** Elephant Robotics ships **`pymycobot`**, a Python SDK
that talks to the 280 over serial (send angles, read angles, open/close
gripper). The **bridge** is a small ROS 2 node that wraps those SDK calls
behind ROS topics/services/actions so the rest of the graph can command
the arm. **`pyserial`** is the underlying Python library that actually
opens the USB serial port and moves bytes; the bridge uses it (directly
or via the SDK). This is the least-ceremony way onto the real hardware.

**How it's good.** It is the **cheapest to set up** — `pymycobot` is the
vendor's own SDK, so it speaks the arm's protocol out of the box, and a
bridge node is a couple of dozen lines. For a software-primary team that
wants the real arm moving *today*, this is the fastest path, all in
Python, no controller configuration. It is also the natural place to do
quick bring-up checks and to script the non-ROS peripheral stations over
plain `pyserial`.

**How it's bad (vs the other four).** It is an **ad-hoc seam, not a real
control layer**, and that is exactly the trap. Versus ROS 2 +
`ros2_control`, the bridge usually just relays position commands: you
lose the `joint_trajectory_controller`'s timed interpolation and standard
state reporting, so smooth trajectory following and proper timing become
*your* code to write and maintain. It tends to grow into a pile of
special-case serial scripts that are fragile, hard to test, and **do not
match the simulator's interface**, so your sim work no longer transfers
cleanly. Versus **micro-ROS** it offers nothing structured for the MCU
stations. Versus the **RMW** discussion it ignores transport tuning
entirely. It is the right way to *start* and the wrong thing to *keep*:
Cheapest, deliberately not Best-practical.

## ROS 2 + ros2_control

**What it is.** This is the Best-in-class stack named as the pragmatic
default once you accept its setup cost — listed separately as
**Best-practical** to make the recommendation explicit. Same
`controller_manager`, same controllers, same real `hardware_interface`
to the myCobot; the distinction is one of *stance*: this is the build you
should standardise on for the cell, with the bridge reserved for bring-up
only.

**How it's good.** It is the **best balance of effort and payoff**. You
get standard, tested controllers; a real-time-honest read/update/write
loop; and — the recurring win — an interface **identical to the
simulator's**, so the only-code work transfers untouched and the move to
hardware is a plugin swap, not a rewrite. It is also the version every
other ROS 2 tool and teammate expects, which keeps the system legible.

**How it's bad (vs the other four).** It shares the Best-in-class
entry's weight: more to learn than the **pymycobot bridge**, and still
bounded by the 280's modest serial update rate, so do not promise a
crisp kHz loop on this arm — set the controller rate to what the serial
link reliably sustains and verify it. Versus **micro-ROS** it does not
run on the station MCUs; versus the **DDS** choice it still depends on a
well-chosen RMW beneath it for latency. The cost is real but one-time;
the maintainability is permanent, which is why it is the practical pick.

## micro-ROS (real)

**What it is.** With hardware present, **micro-ROS** comes into its own:
it is ROS 2 sized for **microcontrollers**, so the MCUs that physically
drive the **decapper** and **dispenser** stations can be ROS 2 nodes
themselves. The MCU runs a tiny client; a host-side **agent** bridges it
into the main graph over serial or UDP. Orchestration then commands a
station the same way it commands the arm.

**How it's good.** It gives the peripheral stations **first-class,
deterministic embedded control** while keeping one mental model: the
decapper is just another node publishing state and accepting goals.
Time-critical, simple actuation (spin the decapper, fire the dispenser)
lives on the MCU where timing is tight and predictable, instead of being
pulled across the host's USB and scheduler. And because it shares ROS 2's
message contracts, the simulated station nodes from the only-code build
map straight onto real firmware.

**How it's bad (vs the other four).** It is **embedded engineering** —
firmware, a cross-compile toolchain, the agent process, flashing — which
is real work versus driving a station with five lines of **pyserial**.
Versus ROS 2 + `ros2_control` on the host, it is a deliberate *subset*
(tighter resources, fewer features), scoped to the MCU. It only earns its
keep for stations that genuinely need on-device timing; for a simple
relay-driven gadget, raw serial or CAN may be enough. Hence Alternative:
powerful and correct for MCU-driven stations, overkill for trivial ones.

## CycloneDDS vs Fast DDS

**What it is.** This is the **RMW knob.** ROS 2 ships with two main DDS
implementations — **Fast DDS** (eProsima) and **CycloneDDS** (Eclipse) —
either selectable via `RMW_IMPLEMENTATION`. Both deliver the same
ROS 2 messages; they differ in defaults, tuning surface, and behaviour
under load. With real motion-control traffic flowing, *which* one and
*how* it is tuned (reliability mode, history depth, transport settings)
affects end-to-end latency and how gracefully the system degrades.

**How it's good.** Choosing and tuning the RMW is the **lever for
latency and reliability** at the transport level — the part the
application layers can't fix. For control and state traffic you tune
toward low, predictable latency; for occasional commands you favour
reliable delivery. The same knob governs the **sensor streams** from
[`../sensor-suite.md`](../sensor-suite.md): a depth or wrist-camera feed
wants best-effort, shallow-history QoS so the gates always see the
*newest* frame and a backlog can never push a stale one through, whereas
a safety or interlock signal wants reliable, latched delivery. CycloneDDS is light with sane defaults; Fast DDS is
highly configurable and supports modes (e.g. shared-memory for
same-host nodes) that cut latency between co-located processes — handy
when arm driver, controllers, and orchestration share one PC.

**How it's bad (vs the other four).** It is **invisible plumbing you
tune, not a feature you build** — versus ROS 2 + `ros2_control` it adds
no control capability, only delivery characteristics, and a bad choice or
mis-tuning can quietly inject jitter. The tuning knobs (QoS, transport
config) are finicky and easy to get subtly wrong. Versus **micro-ROS**
and **pyserial** it operates one level down from the device entirely. For
a single-PC cell the defaults are usually fine, so this is an Alternative
— the thing you reach for only if profiling shows transport latency is
actually your bottleneck. Re-measure before changing it; `~`don't tune
on a hunch.

## pyserial / python-can

**What it is.** The **lowest-level device I/O.** `pyserial` opens a USB
serial port and reads/writes raw bytes; `python-can` does the same for
**CAN bus** (a robust two-wire bus common in motors and industrial
peripherals), reading/writing message frames. These talk to devices that
have **no ROS 2 interface at all** — a basic decapper board, a pump
controller, a barcode gadget — by speaking their native protocol
directly.

**How it's good.** It is **universal and minimal**: if a station exposes
a serial or CAN protocol, these libraries can drive it immediately, no
firmware to write and no framework to satisfy. For one-off or very simple
peripherals, wrapping a few `pyserial` writes in a small ROS 2 node is
the pragmatic, lowest-cost way to bring a device into the cell.

**How it's bad (vs the other four).** It is **raw and unstructured**, and
that is its danger at scale. Versus **micro-ROS**, you get no node model,
no standard messages, no on-device timing — just bytes, with framing,
retries, and error handling left to you. Versus ROS 2 + `ros2_control`
it offers nothing for the *arm*: hand-rolling joint control over raw
serial is exactly the ad-hoc-script trap a clean `hardware_interface`
exists to prevent — fragile, untestable, and out of step with the
simulator. Versus the **DDS** choice it is below the transport layer
entirely. So it is an Alternative: the right tool for dumb peripherals,
the wrong tool for the arm or for anything you'll maintain for long.

## Verdict

- **Best-in-class: ROS 2 + ros2_control with a real hardware_interface.**
  The standard stack with tested controllers and a clean, swappable
  driver seam to the myCobot — and the upper stack carries over from sim
  untouched. It also makes the real-time question explicit, which on this
  small arm means setting the loop to the modest rate the serial link can
  sustain.
- **Cheapest: pymycobot bridge + pyserial.** The vendor SDK wrapped in a
  thin ROS 2 node, plus raw serial for the stations — least to set up and
  quickest to first motion, but ad-hoc, off the standard, and best kept
  to bring-up only.
- **Best-practical: ROS 2 + ros2_control.** The same standard stack as
  the default to standardise on: more to learn than the bridge, but the
  one option that is maintainable, real-time-honest, and a clean swap
  away from the simulator build.

## See also

- Folder overview: [`README.md`](README.md)
- Sibling mode (pure sim, no hardware):
  [`../01-only-code/02-middleware-and-control.md`](../01-only-code/02-middleware-and-control.md)
