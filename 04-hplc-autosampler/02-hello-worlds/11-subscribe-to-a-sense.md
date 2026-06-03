# 11 — Subscribe to a sense (Sensors)

> Checklist exercise: **Layer S — "subscribe to a sense."**
> See [`../07-learning-checklist.md`](../07-learning-checklist.md).

## What this program proves

A robot that cannot read its own senses is blind: it can only *hope* its
moves worked. This exercise builds the smallest possible cure — a program
that **listens to a stream of numbers from a sensor** and turns each
number into a plain yes-or-no answer. That is the whole idea, and it is
the atom from which every safety check and every verification step in this
project is built.

The sensor we listen to here is a **force reading at the wrist** of the
arm — how hard the robot's wrist is being pushed or pulled, measured in
**newtons** (the standard unit of push or pull; one newton is roughly the
weight of a small apple). In the full robot this same kind of reading
tells you whether the gripper is actually holding the vial, or whether the
arm has bumped into something it should not have. While you are still in
simulation, a stand-in program broadcasts pretend force numbers — exactly
the mock-station pattern from exercise 02 — and our job is simply to
**catch each one and judge it**.

The judging rule is deliberately tiny: a number is **good** if it sits
inside an expected band, and **bad** if it strays outside. We print
`PASS` for good and `FAIL` for bad. Turning a number into a pass/fail is
called a **gate** — like a turnstile that only opens for the right
readings — and it is the core of all "sensor-driven" behaviour. A robot
that *acts on* what its sensors say, rather than acting blind, is doing
nothing more than running gates like this one, over and over.

Two new words you will meet here, because this program **listens** instead
of broadcasting:

- To **publish** is to *send* readings out onto a named channel (what the
  mock station in exercise 02 did with the weight).
- To **subscribe** is to *receive* readings from a named channel (what we
  do here). For every publisher there can be many subscribers, all
  hearing the same stream.

## What you need first

You need **the Robot Operating System, version 2** installed (the free
toolkit that lets the small programs on a robot find each other and pass
messages; its common written name is "ROS 2," and we will keep calling it
"the robot framework"). Load its commands in your terminal with:

```bash
source /opt/ros/jazzy/setup.bash
```

You also need *something publishing numbers* on the channel we listen to,
called `/wrist_force`. You do **not** need the whole robot for that: the
robot framework ships a one-line command that fakes a publisher, shown in
the "How to run it" section below. So this exercise stands entirely on its
own — no simulator, no arm, just a stream of numbers and our gate.

> Teaching note: a real force sensor needs calibration, smoothing, and
> careful thresholds; the band below is picked to be obvious, so the
> *shape* of the gate is clear. Treat the numbers as illustration, not as
> tuned settings.

## The whole program

Save this as a file named `sense_gate.py`:

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64


# The band of force readings we consider healthy, in newtons.
LOW_LIMIT = 1.0    # below this: too little contact
HIGH_LIMIT = 8.0   # above this: pressing too hard


class SenseGate(Node):
    def __init__(self):
        super().__init__("sense_gate")
        self.subscription = self.create_subscription(
            Float64, "/wrist_force", self.on_reading, 10)
        self.get_logger().info("Sense gate is listening.")

    def on_reading(self, message):
        value = message.data
        in_band = LOW_LIMIT <= value <= HIGH_LIMIT
        verdict = "PASS" if in_band else "FAIL"
        self.get_logger().info(
            f"wrist force = {value:.2f} N -> {verdict}")


def main():
    rclpy.init()
    gate = SenseGate()
    rclpy.spin(gate)
    gate.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
```

## Every line explained

**`import rclpy`**
The word `import` means "bring in a library of ready-made code so I can
use it." `rclpy` is the name of the robot framework's Python library; the
name is short for "Robot Client Library for Python." This single line
gives your program the ability to join the robot's network of programs.

**`from rclpy.node import Node`**
This brings in one specific tool from that library, called `Node`. A
**node** is the framework's word for "one small program that does one
job." By bringing in `Node`, we can build our own node on top of it.

**`from std_msgs.msg import Float64`**
This brings in a ready-made **message shape** called `Float64`. The robot
framework requires that everyone agree on the shape of the readings on a
channel. `Float64` is the simplest such shape: it holds **one decimal
number** (the "64" refers to how much computer memory it uses, which gives
it plenty of precision). Every force reading we receive arrives wrapped in
one of these. `std_msgs` means "standard messages," a collection of common
shapes that ships with the framework.

**`LOW_LIMIT = 1.0`** and **`HIGH_LIMIT = 8.0`**
These set the two edges of the healthy band, in newtons: a reading is good
only if it is at least 1.0 and at most 8.0. Below 1.0 the wrist is barely
being touched (perhaps the grip caught nothing); above 8.0 it is being
pushed dangerously hard. Writing the names in capital letters is a common
signal that these are **constants** — fixed values we set once and never
change while running.

**`class SenseGate(Node):`**
The word `class` starts the definition of our own node. Think of a class
as a blueprint. We name our blueprint `SenseGate`. The `(Node)` part means
"build this blueprint on top of the framework's `Node` blueprint," so our
gate automatically inherits the ability to talk on the network.

**`def __init__(self):`**
`def` begins a named block of instructions (a "function"). The special
name `__init__` means "the set-up steps that run once, automatically, the
moment this gate is created." The word `self` is how the code refers to
*this particular gate* while setting it up; every line inside uses it.

**`super().__init__("sense_gate")`**
This runs the framework's own set-up first and, while doing so, registers
our gate on the network under the human-readable name `"sense_gate"`.
After this line, the rest of the robot can see that a program by that name
exists.

**`self.subscription = self.create_subscription(Float64, "/wrist_force", self.on_reading, 10)`**
This is the heart of the program: it creates the **subscription** — the
act of tuning in to a channel. We hand `create_subscription` four things:
the message shape to expect (`Float64`), the public name of the channel to
listen on (`"/wrist_force"`), the name of the function to run for every
reading that arrives (`self.on_reading`, defined just below), and the
number `10`. That `10` is the size of a small holding queue: if readings
arrive faster than we handle them, up to ten will wait in line rather than
being lost. We keep the subscription in `self.subscription` so it stays
alive for as long as the gate runs.

**`self.get_logger().info("Sense gate is listening.")`**
This prints a friendly status line to the terminal. `get_logger()` is the
framework's built-in way of printing tidy, time-stamped messages;
`.info(...)` marks this one as ordinary information (as opposed to a
warning or an error). Seeing this line tells you the set-up finished and
the gate is waiting for readings.

**`def on_reading(self, message):`**
This begins the **callback function** — the function the framework runs
automatically every single time a new reading lands on the channel. (A
*callback* is simply "a function you hand to the framework so it can call
you back when something happens.") You never call this yourself; the
framework calls it for you, once per reading. The arriving reading is
handed in as `message`.

**`value = message.data`**
The `Float64` shape carries its number in a slot named `data`. This line
copies that number out into a plainly-named variable, `value`, so the rest
of the function reads clearly. This is the single number the sensor sent.

**`in_band = LOW_LIMIT <= value <= HIGH_LIMIT`**
This is the **gate** itself. It asks one question: is `value` at least
`LOW_LIMIT` **and** at most `HIGH_LIMIT`? Python lets us write that as a
single chained comparison. The answer is a plain yes-or-no value (the
framework's words for those are `True` and `False`), stored in `in_band`.
Turning the decimal number into this yes-or-no is the whole point of the
exercise — the moment a *measurement* becomes a *decision*.

**`verdict = "PASS" if in_band else "FAIL"`**
This turns the yes-or-no into a word a human can read. It means "set
`verdict` to `"PASS"` when `in_band` is true, otherwise to `"FAIL"`."

**`self.get_logger().info(f"wrist force = {value:.2f} N -> {verdict}")`**
This prints one tidy line per reading: the measured force and the verdict.
The `f"..."` is an *f-string*, a Python way to drop values into the middle
of text; `{value:.2f}` shows the number trimmed to two decimal places, and
`{verdict}` drops in `PASS` or `FAIL`. Watching these lines scroll past is
how you *see* the gate working.

**`def main():`**
This begins the program's main starting routine — the steps that run when
you launch the file.

**`rclpy.init()`**
This starts up the connection to the robot framework. Nothing can talk on
the network until this has run, so it always comes first.

**`gate = SenseGate()`**
This builds one copy of our gate from the blueprint. Building it
automatically runs the `__init__` set-up steps described above, so as soon
as this line finishes, the subscription is live and listening.

**`rclpy.spin(gate)`**
The word **spin** means "keep this program alive and responsive, handing
it each reading as it arrives, until it is told to stop." This is what
makes the callback actually fire: without `spin`, the program would set up
the subscription and then immediately end, hearing nothing. Execution
stays on this line, looping, until you press the keys to stop it.

**`gate.destroy_node()`**
After you stop the program, this politely removes the gate from the
network, freeing up its name and resources.

**`rclpy.shutdown()`**
This closes the connection to the robot framework cleanly — the mirror
image of `rclpy.init()`.

**`if __name__ == "__main__":`**
This is a standard Python guard meaning "only run the next line if this
file was launched directly (rather than being imported by another file)."
It prevents the program from starting itself unexpectedly when reused.

**`main()`**
This finally calls the starting routine, setting everything above in
motion.

## How to run it, and how you know it worked

Open **two** terminal windows. In each, first load the robot framework's
commands with `source /opt/ros/jazzy/setup.bash`.

- **Terminal one** — start the gate:
  ```bash
  python3 sense_gate.py
  ```
  You should see `Sense gate is listening.` and then nothing more — it is
  waiting for readings.

- **Terminal two** — fake a sensor by publishing numbers onto the channel.
  The framework's command-line tool can do this in one line. First send a
  *healthy* reading:
  ```bash
  ros2 topic pub /wrist_force std_msgs/msg/Float64 "{data: 4.0}"
  ```
  Here `ros2` is the framework's command-line tool, `topic pub` means
  "publish onto this channel," `/wrist_force` is the channel name,
  `std_msgs/msg/Float64` is the message shape, and `{data: 4.0}` fills its
  one slot with the number 4.0. In terminal one you should see lines like
  `wrist force = 4.00 N -> PASS` appearing. Stop this command with the
  keys that interrupt it, then send a reading *outside* the band:
  ```bash
  ros2 topic pub /wrist_force std_msgs/msg/Float64 "{data: 12.0}"
  ```
  Now terminal one should print `wrist force = 12.00 N -> FAIL`.

**Done when:** numbers you publish on `/wrist_force` show up in the gate's
terminal as `PASS` when they sit inside the band and `FAIL` when they do
not. You have now built the smallest complete "sensor-driven" program — a
reading in, a decision out — which is the atom of every check the robot
makes about the real world.

## Where this fits

- This is the runnable version of the **Layer S** (sensors) exercise in
  [`../07-learning-checklist.md`](../07-learning-checklist.md).
- It is the mirror image of the broadcaster in exercise 02: that program
  **published** readings; this one **subscribes** to them. Run a mock
  station from [`02-mock-decapper.md`](02-mock-decapper.md) and a gate
  like this one together and you have the full sense-and-judge pair.
- The verdict here is the same idea as the grip check in
  [`05-grab-the-vial.md`](05-grab-the-vial.md): both turn a sensor reading
  into a `PASS`/`FAIL` (or `HELD`/`MISSED`) decision.
- The deeper write-up of how sensors ride on the robot framework is
  [`../04-mycobot-280-impl/01-only-code/02-middleware-and-control.md`](../04-mycobot-280-impl/01-only-code/02-middleware-and-control.md),
  and the full list of senses this robot has — what each one measures and
  on which channel — is in
  [`../04-mycobot-280-impl/sensor-suite.md`](../04-mycobot-280-impl/sensor-suite.md).
- The capstone, [`12-hello-cell-capstone.md`](12-hello-cell-capstone.md),
  uses gates like this one to verify each step of the full pick-drive-place
  loop.
</content>
</invoke>
