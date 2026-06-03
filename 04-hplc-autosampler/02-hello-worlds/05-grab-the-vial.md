# 05 — Grab the vial (Grasping)

> Checklist exercise: **Layer 5 — "grab the vial."**
> See [`../07-learning-checklist.md`](../07-learning-checklist.md).

## What this program proves

The arm can now reach a spot in space, but reaching is not holding. This
exercise proves the next step: turning the **known shape of the vial**
into a plan for the gripper, then closing the gripper and **checking that
it actually caught the vial** rather than closing on empty air.

The vial is a small glass cylinder, about twelve millimetres across. The
robot's hand is a **parallel-jaw gripper**: two flat fingers that slide
straight toward each other, like the jaws of a clamp. To hold a cylinder
with such a hand you press on **two opposite sides** at once — an
**antipodal pinch** ("antipodal" just means "at opposite points," like
the North and South Poles). The two squeezing forces line up through the
middle of the vial and cancel out, so the vial does not squirt sideways
out of the grip.

The program has two halves:

1. **Compute** — plain arithmetic. From the vial's centre and width we
   work out *where* the hand should be (the **grasp pose**), *which way*
   it should be turned, and *how far* the fingers should close.
2. **Command and verify** — we send the close command, then read back two
   numbers the gripper reports: the gap the fingers ended at, and how hard
   the motor is working. If the fingers stopped at about the vial's width
   **and** the motor is pushing to hold that gap, the vial is in there.
   We call this the **two-witness** check: one witness alone can lie (the
   fingers might stop short on nothing; the motor might strain against
   itself), but both together mean a real hold.

The lasting lesson is not the exact numbers — it is the **command-and-
verify** habit. A robot that closes its hand and simply *assumes* it
worked will happily carry an empty gripper across the bench. A robot that
closes and then *checks* will know it missed and can try again.

## What you need first

You need **the Robot Operating System, version 2** installed (the free
toolkit that lets the small programs on a robot talk to each other; its
common written name is "ROS 2," and we will keep calling it "the robot
framework"). Load its commands in your terminal with:

```bash
source /opt/ros/jazzy/setup.bash
```

This exercise also needs the **simulated arm and gripper** already
running — the myCobot 280 spawned into the cell from exercise 01, with
its gripper offering the standard gripper command described below.
Without that running, the arithmetic in part one will still print, but
the command in part two will wait for a gripper that is not there. So the
value of this file is twofold: the **computation** (which runs anywhere)
and the **command-and-verify pattern** (which runs against the
simulator).

> Teaching note: real grippers and real vials vary, and a production
> system would calibrate the thresholds below against the actual
> hardware. The numbers here are deliberately simple so the *shape* of
> the solution is clear.

## The whole program

Save this as a file named `grab_the_vial.py`:

```python
import numpy as np

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from control_msgs.action import GripperCommand


# --- Part one: what we know about the vial (constants) ---
VIAL_CENTRE = np.array([0.20, 0.00, 0.46])   # metres: x, y, z
VIAL_DIAMETER = 0.012                         # metres (12 mm across)
FINGER_CLEARANCE = 0.002                      # metres of squeeze (2 mm)
GRIP_FORCE = 5.0                              # newtons, gentle on glass


def plan_grasp(centre, diameter):
    grasp_position = centre.copy()
    approach_from_above = np.array([0.0, 0.0, -1.0])
    target_gap = diameter - FINGER_CLEARANCE
    return grasp_position, approach_from_above, target_gap


class VialGrabber(Node):
    def __init__(self):
        super().__init__("vial_grabber")
        self.gripper = ActionClient(
            self, GripperCommand, "gripper_action")

    def grab(self, target_gap, force):
        self.gripper.wait_for_server()
        goal = GripperCommand.Goal()
        goal.command.position = target_gap / 2.0
        goal.command.max_effort = force
        self.get_logger().info("Closing the gripper...")
        send = self.gripper.send_goal_async(goal)
        rclpy.spin_until_future_complete(self, send)
        result_future = send.result().get_result_async()
        rclpy.spin_until_future_complete(self, result_future)
        return result_future.result().result

    def verify(self, result, target_gap):
        reached_gap = result.position * 2.0
        effort = result.effort
        close_enough = abs(reached_gap - target_gap) < 0.003
        motor_working = effort > 0.5
        if close_enough and motor_working:
            self.get_logger().info("HELD")
        else:
            self.get_logger().info("MISSED")


def main():
    position, approach, target_gap = plan_grasp(
        VIAL_CENTRE, VIAL_DIAMETER)
    print("Grasp position (metres):", position)
    print("Approach direction:", approach)
    print("Target finger gap (metres):", round(target_gap, 4))

    rclpy.init()
    grabber = VialGrabber()
    result = grabber.grab(target_gap, GRIP_FORCE)
    grabber.verify(result, target_gap)
    grabber.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
```

## Every line explained

**`import numpy as np`**
Brings in **NumPy**, a free library for doing arithmetic on lists of
numbers (its name is short for "Numerical Python"). We use it to hold a
position as three numbers at once — left-right, forward-back, up-down. The
`as np` part lets us write the short label `np` instead of the full word
every time.

**`import rclpy`** … **`from rclpy.node import Node`**
These bring in the robot framework's Python library (`rclpy`, short for
"Robot Client Library for Python") and, from it, the `Node` tool. A
**node** is the framework's word for "one small program that does one
job." We build our gripper program on top of it.

**`from rclpy.action import ActionClient`**
Brings in the tool for talking to an **action**. An **action** is a
third way for robot programs to talk, alongside two you have already met:
a *broadcast* (a steady stream of readings) and a *request-and-reply* (a
single quick question and answer). An action is for jobs that **take
time** and that you want progress on — "close the gripper" is exactly
such a job: it is not instant, and you care about the result. An
`ActionClient` is the side that *sends* the job and waits for the
outcome.

**`from control_msgs.action import GripperCommand`**
Brings in the ready-made **message shape** for commanding a gripper,
called `GripperCommand`. The robot framework requires an agreed shape for
every action. This one carries, on the way out, a target finger position
and a maximum force; and on the way back, the position the fingers
actually reached and the effort the motor is using. `control_msgs` is a
standard collection of shapes used for controlling motors.

**`VIAL_CENTRE = np.array([0.20, 0.00, 0.46])`**
Stores where the middle of the vial is, as three numbers in metres:
0.20 to one side, 0.00 forward, 0.46 up — the same resting spot the vial
was given when we built the world in exercise 01. `np.array([...])`
bundles the three numbers into one tidy package NumPy can do maths on.
Writing the name in capital letters is a common signal that this is a
**constant** — a fixed value we set once and never change while running.

**`VIAL_DIAMETER = 0.012`**
The width of the vial across the middle: 0.012 metre, which is twelve
millimetres. This is the single most important number for grasping,
because the fingers must close to a little less than this.

**`FINGER_CLEARANCE = 0.002`**
How much *narrower* than the vial we tell the fingers to close — two
millimetres. Aiming a hair *inside* the glass means the fingers press
firmly rather than just kissing the surface. Without this squeeze the
vial would slip.

**`GRIP_FORCE = 5.0`**
The most force the gripper motor is allowed to use, measured in
**newtons** (the standard unit of push or pull; one newton is roughly the
weight of a small apple). Five newtons is gentle — enough to hold a light
glass vial, not enough to crack it.

**`def plan_grasp(centre, diameter):`**
Begins a small function (a named block of steps) that does the **compute**
half of the job. You hand it the vial's centre and width; it hands back a
plan. Keeping this separate means the arithmetic can be read and trusted
on its own, with no robot attached.

**`grasp_position = centre.copy()`**
The point the hand should aim for is the centre of the vial. We take a
**copy** of the centre (rather than the original) so that if later code
nudges the grasp position, it does not accidentally move our record of
where the vial actually is.

**`approach_from_above = np.array([0.0, 0.0, -1.0])`**
Which direction the hand travels as it comes in to grip. The three
numbers point straight **down** (the `-1.0` is the down-ward part), so
the hand descends onto the vial from above — the natural way to pick a
small bottle off a table. This direction, together with the position,
is what makes up the full **grasp pose** ("pose" = a position *and* an
orientation).

**`target_gap = diameter - FINGER_CLEARANCE`**
The finger gap we will aim for: the vial's width minus our two-millimetre
squeeze. Twelve millimetres minus two gives ten millimetres. This is the
opening the fingers should settle at when they have the glass between
them.

**`return grasp_position, approach_from_above, target_gap`**
Hands the three results back to whoever called the function: where to be,
which way to come in, and how far to close.

**`class VialGrabber(Node):`**
Starts the blueprint for our node, named `VialGrabber`, built on top of
the framework's `Node` so it can talk on the network. The **command-and-
verify** half of the job lives inside it.

**`def __init__(self):`** and **`super().__init__("vial_grabber")`**
`__init__` holds the set-up steps that run once when the node is created.
`super().__init__("vial_grabber")` runs the framework's own set-up and
registers our node on the network under the readable name
`"vial_grabber"`.

**`self.gripper = ActionClient(self, GripperCommand, "gripper_action")`**
Creates the client that will send gripper jobs. We tell it three things:
`self` (our node, which carries the network connection), the message
shape it will use (`GripperCommand`), and the public name of the action
to send to (`"gripper_action"`). We store it in `self.gripper` for later.

**`def grab(self, target_gap, force):`**
Begins the function that actually sends the close command. It takes the
target gap and the force we worked out earlier.

**`self.gripper.wait_for_server()`**
Pauses here until the gripper on the other end is actually listening. If
the simulated arm is not running, this is where the program waits. It
prevents us from firing a command into the void.

**`goal = GripperCommand.Goal()`**
Makes one empty **goal** — the outgoing part of the action message, ready
to fill in. The empty brackets mean "make a fresh one."

**`goal.command.position = target_gap / 2.0`**
Sets the target finger position. The gripper measures each finger from
the centre line, so a *gap* of ten millimetres means each finger sits
*five* millimetres out — half the gap. Dividing by two converts our gap
into the per-finger number the gripper expects.

**`goal.command.max_effort = force`**
Sets the most force the motor may use — our gentle five newtons from
above. The gripper will close until it either reaches the target gap or
hits this force, whichever comes first.

**`self.get_logger().info("Closing the gripper...")`**
Prints a tidy status line so you can see, in the terminal, the moment the
command goes out. `get_logger().info(...)` is the framework's built-in way
of printing time-stamped messages.

**`send = self.gripper.send_goal_async(goal)`**
Sends the goal to the gripper. The `_async` ending means "send it and let
me carry on" rather than freezing until it is done; what comes back
(`send`) is a kind of claim ticket we can later check for an answer.

**`rclpy.spin_until_future_complete(self, send)`**
Waits, in a way that keeps the node responsive, until the gripper has
*accepted* the job. A **future** is the framework's word for "an answer
that will arrive later"; this line simply blocks until that answer is in.

**`result_future = send.result().get_result_async()`**
Now that the job is accepted, this asks for the **final outcome** — the
report the gripper sends once it has finished closing. Again this comes
back as a future (an answer-to-arrive-later), stored in `result_future`.

**`rclpy.spin_until_future_complete(self, result_future)`**
Waits until that final report has actually arrived.

**`return result_future.result().result`**
Digs the finished report out of the future and hands it back. (The chain
of `.result` calls is just the framework's wrapping: the outer ones
unwrap the future; the innermost `.result` is the gripper's own report,
holding the reached position and effort.)

**`def verify(self, result, target_gap):`**
Begins the **check** — the heart of this exercise. It takes the gripper's
report and the gap we were aiming for.

**`reached_gap = result.position * 2.0`**
The report gives the per-finger position; multiplying by two turns it
back into a full gap, so we can compare it with what we aimed for. This
is the **first witness**: where the fingers actually stopped.

**`effort = result.effort`**
Reads how hard the motor is working to hold that position, in newtons.
This is the **second witness**. A motor straining to keep the fingers
apart means something solid is between them. (On a real motor this is
read from the electric **current** it draws — more current means more
push — which is why "effort" and "current" are often used to mean the
same thing here.)

**`close_enough = abs(reached_gap - target_gap) < 0.003`**
The first witness's verdict. `abs(...)` takes the size of the difference
ignoring its sign, so we are asking "did the fingers stop within three
millimetres of the vial's width?" If they slammed shut to near zero, they
caught nothing and this is **false**. The result (`true` or `false`) is
stored in `close_enough`.

**`motor_working = effort > 0.5`**
The second witness's verdict: is the motor pushing with more than half a
newton? If the fingers closed on empty air there is nothing to push
against, the effort stays near zero, and this is **false**.

**`if close_enough and motor_working:`**
Combines the two witnesses. Only if **both** are true — the fingers
stopped at the vial's width *and* the motor is straining to hold it — do
we believe the vial is held. The word `and` requires both.

**`self.get_logger().info("HELD")`** / **`self.get_logger().info("MISSED")`**
Prints the verdict. `HELD` when both witnesses agree; otherwise `MISSED`.
This single printed word is the whole point of the exercise: the robot now
*knows* whether it succeeded.

**`def main():`**
Begins the starting routine that runs when you launch the file.

**`position, approach, target_gap = plan_grasp(VIAL_CENTRE, VIAL_DIAMETER)`**
Runs the **compute** half first, before any robot is involved, and unpacks
its three answers into three named values.

**The three `print(...)` lines**
Print the plan in plain numbers so you can read it with your own eyes: the
grasp position, the approach direction, and the target finger gap.
`round(target_gap, 4)` trims the gap to four decimal places so it is easy
to read.

**`rclpy.init()`**
Starts the connection to the robot framework. Nothing can talk on the
network until this has run.

**`grabber = VialGrabber()`**
Builds one copy of our node from the blueprint, which runs its set-up
steps and brings the gripper client to life.

**`result = grabber.grab(target_gap, GRIP_FORCE)`**
Sends the close command and waits for the gripper's final report, storing
it in `result`.

**`grabber.verify(result, target_gap)`**
Runs the two-witness check on that report and prints `HELD` or `MISSED`.

**`grabber.destroy_node()`** and **`rclpy.shutdown()`**
Politely remove the node from the network and close the connection to the
framework cleanly — the mirror image of the start-up.

**`if __name__ == "__main__":`** and **`main()`**
A standard Python guard meaning "only run if this file was launched
directly," followed by the call that sets everything above in motion.

## How to run it, and how you know it worked

First, with the **simulated arm and gripper running** (the myCobot 280
spawned into the cell as in exercise 01), open a terminal and load the
framework with `source /opt/ros/jazzy/setup.bash`. Then, from the folder
containing the file:

```bash
python3 grab_the_vial.py
```

You should first see the **plan** printed — the grasp position, the
approach direction, and a target finger gap of `0.01` metre (ten
millimetres). Then you should see `Closing the gripper...`, and finally
either:

- `HELD` — the fingers stopped at about the vial's width **and** the
  motor is straining to hold it, or
- `MISSED` — one or both witnesses failed (the fingers slammed shut on
  nothing, or the motor is not pushing).

**Done when:** the program prints the computed plan, sends the close
command, and prints a `HELD`/`MISSED` verdict based on the gripper's own
reported gap and effort. You have now built the **compute-then-command-
then-verify** pattern that every pick in this project relies on.

If you want to run just the **compute** half (no simulator needed),
temporarily comment out everything from `rclpy.init()` onward in `main`;
the three `print` lines will still show the plan.

## Where this fits

- This is the runnable version of the **Layer 5** exercise in
  [`../07-learning-checklist.md`](../07-learning-checklist.md).
- The deeper write-up of grasping (antipodal grips, analytical grasp
  planning, and when learned methods like AnyGrasp are worth it) is
  [`../04-mycobot-280-impl/01-only-code/05-grasping-and-manipulation.md`](../04-mycobot-280-impl/01-only-code/05-grasping-and-manipulation.md).
- The verify step here is a close cousin of the sensor gate in
  [`11-subscribe-to-a-sense.md`](11-subscribe-to-a-sense.md): both turn a
  reading into a pass/fail decision. The capstone,
  [`12-hello-cell-capstone.md`](12-hello-cell-capstone.md), runs this grab
  as one step of the full pick-drive-place loop.
