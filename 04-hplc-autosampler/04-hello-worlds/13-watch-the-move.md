# 13 — Watch the move (closing the loop on motion)

> Checklist exercise: **Layer 3 extension — "close the loop on motion."**
> See [`../09-learning-checklist.md`](../09-learning-checklist.md).

## What this program proves

[File 03 (reach the vial)](03-reach-the-vial.md) ends with the arm
arriving at a pose and a cheerful `Arrived.` printed to the screen. But
pause on that word: *how do we actually know it arrived?* The program
printed `Arrived` simply because the command returned — not because
anything checked the hand's real position. In a glass-and-liquids lab
that is not good enough. We need to **measure** where the hand ended up
and **prove** it matches where we sent it.

This program answers two questions that file 03 left open.

**First: who keeps the arm moving?** It is easy to assume MoveIt "runs
the arm." It does not. **MoveIt is a service you call**: you hand it one
goal pose and it works out and executes one path to it, then stops and
waits. It never decides *where* to go, and it does not fire off new goals
on its own. The job of *deciding the goal* — "the vial is here now, send
the hand there" — and of *calling MoveIt over and over* belongs to a
separate program we will call the **executive** (also called the control
loop or task controller). In the finished cell that executive is the
behaviour tree of [file 09 (the per-vial loop)](09-per-vial-loop.md);
here we build the smallest possible version so you can see its shape.

**Second: how do we check the move was correct?** We use **two
independent layers of feedback**:

1. **The controller's own report.** When MoveIt executes a path it sends
   it to a *joint-trajectory controller* (the low-level program that
   actually turns the motors) and gets back a **result**: did the move
   finish, or was it aborted partway? That is the planner's own word on
   whether it succeeded.
2. **An independent geometric cross-check.** We do not just take the
   controller's word for it. We look up the hand's **measured** position
   from the robot's live tree of coordinate frames — the **TF tree**
   (short for *transforms*; the constantly-updated record of where every
   part of the robot is, computed from the joint sensors) — and compare
   it to the position we commanded. If the gap between *commanded* and
   *measured* is within a small **tolerance**, the move passes; if not,
   it failed and a real run would re-plan or retry.

The whole program is therefore a loop: **read the target → call MoveIt →
measure where the hand really went → pass or fail.** That loop, repeated,
*is* closed-loop arm control.

> Teaching-code note: as in file 03, exact method names drift between
> versions and this is deliberately stripped down. The shape of the loop
> is the lesson, not a guaranteed copy-paste.

## What you need first

The same setup as [file 03](03-reach-the-vial.md): **ROS 2** (the robot
framework), **MoveIt 2**, and the myCobot 280's **MoveIt configuration**
running in its own terminal, plus the **`pymoveit2`** helper for the
shortest example. We also use **`tf2_ros`**, the framework's standard
library for reading the TF tree of coordinate frames; it ships with ROS
2, so there is nothing extra to install.

In every terminal, first load the robot framework's commands:

```bash
source /opt/ros/jazzy/setup.bash
```

## The whole program

Save this as a file named `watch_the_move.py`:

```python
import rclpy
from rclpy.node import Node
from pymoveit2 import MoveIt2
from tf2_ros import Buffer, TransformListener
import math


# Point the hand straight down, as in file 03.
HAND_FACING_DOWN = [1.0, 0.0, 0.0, 0.0]

# How close to the target counts as "arrived": 5 millimetres.
TOLERANCE_M = 0.005


class WatchTheMove(Node):
    def __init__(self):
        super().__init__("watch_the_move")
        self.moveit2 = MoveIt2(
            node=self,
            joint_names=[
                "joint1", "joint2", "joint3",
                "joint4", "joint5", "joint6",
            ],
            base_link_name="base",
            end_effector_name="link6",
            group_name="arm",
        )
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

    def latest_target(self):
        # Stand-in for perception (file 04): pretend the vial wobbles a
        # little. A real version reads the vial's measured pose.
        t = self.get_clock().now().nanoseconds * 1e-9
        x = 0.20 + 0.01 * math.sin(t)     # drifts ~1 cm
        return [x, 0.00, 0.51]

    def measured_hand_position(self):
        frame = self.tf_buffer.lookup_transform(
            "base", "link6", rclpy.time.Time()
        )
        spot = frame.transform.translation
        return [spot.x, spot.y, spot.z]

    def gap(self, a, b):
        return math.sqrt(sum((p - q) ** 2 for p, q in zip(a, b)))

    def command_and_verify(self, target):
        self.get_logger().info(f"Commanding the hand to {target} ...")
        self.moveit2.move_to_pose(
            position=target, quat_xyzw=HAND_FACING_DOWN
        )
        finished = self.moveit2.wait_until_executed()
        if not finished:
            self.get_logger().warn("Controller reported the move ABORTED.")
            return False
        measured = self.measured_hand_position()
        error = self.gap(target, measured)
        self.get_logger().info(
            f"commanded={target} measured={measured} "
            f"error={error * 1000:.1f} mm"
        )
        if error <= TOLERANCE_M:
            self.get_logger().info("PASS: hand is on target.")
            return True
        self.get_logger().warn("FAIL: off target — a real run would retry.")
        return False


def main():
    rclpy.init()
    node = WatchTheMove()
    for cycle in range(1, 4):
        node.get_logger().info(f"--- control cycle {cycle} ---")
        rclpy.spin_once(node, timeout_sec=1.0)
        target = node.latest_target()
        node.command_and_verify(target)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
```

## Every line explained

**`import rclpy` / `from rclpy.node import Node`**
Bring in the robot framework's Python library and its `Node` tool, as in
every file here.

**`from pymoveit2 import MoveIt2`**
Brings in the `MoveIt2` helper — the tool that *commands* the move. It is
the thing our executive *calls*; it is not the executive.

**`from tf2_ros import Buffer, TransformListener`**
Brings in two tools for reading the **TF tree** — the live record of
where every part of the robot is. A `TransformListener` quietly collects
those positions as they are broadcast, and a `Buffer` stores the recent
ones so we can ask "where is the hand?" at any moment. This is how we
*measure* the result, independently of MoveIt.

**`import math`**
Python's mathematics library. We use it for the square root in the
distance calculation, and to make the target wobble slightly.

**`HAND_FACING_DOWN = [1.0, 0.0, 0.0, 0.0]`**
The same "hand pointing straight down" orientation as file 03, given as
the four numbers computers use for a rotation.

**`TOLERANCE_M = 0.005`**
The pass/fail threshold: **5 millimetres** (0.005 metre). If the
measured hand position is within this distance of the target, we call the
move correct. Choosing this number is a real engineering decision —
loose enough to allow for normal play in the joints, tight enough that a
genuinely wrong move is caught.

**`class WatchTheMove(Node):` … `super().__init__("watch_the_move")`**
Defines our executive node and registers it on the network under the name
`watch_the_move`.

**`self.moveit2 = MoveIt2( ... )`**
Builds the link to the MoveIt 2 planner, with the same arm settings as
file 03. This is the service our loop will call each cycle.

**`self.tf_buffer = Buffer()`**
Creates the store that will hold recent frame positions from the TF tree.

**`self.tf_listener = TransformListener(self.tf_buffer, self)`**
Starts listening to the TF tree and feeding what it hears into that
store. From now on, the buffer always holds an up-to-date picture of
where the arm's parts are — including the hand.

**`def latest_target(self):`**
Begins the helper that answers "where do we want the hand *right now*?"
In this teaching program it makes up a slightly wobbling target; in the
real cell it would read the vial's measured pose from the perception
layer. This helper is the "**calculates where the arm needs to go**"
part — and notice it lives in *our* executive, not in MoveIt.

**`t = self.get_clock().now().nanoseconds * 1e-9`**
Reads the clock and converts to seconds (it counts in nanoseconds,
billionths of a second), used only to drive the wobble.

**`x = 0.20 + 0.01 * math.sin(t)`**
Makes the target drift about 1 centimetre back and forth, imitating a
vial whose measured position keeps being refreshed.

**`return [x, 0.00, 0.51]`**
Hands back the current target position — the drifting forward value,
centred sideways, at hovering height.

**`def measured_hand_position(self):`**
Begins the helper that answers "where did the hand *actually* end up?" —
the heart of the cross-check.

**`frame = self.tf_buffer.lookup_transform("base", "link6", rclpy.time.Time())`**
Asks the TF buffer: where is `link6` (the hand) relative to `base` (the
fixed foot of the arm), right now? `rclpy.time.Time()` means "the latest
available." The answer, `frame`, describes exactly where the hand is —
computed from the joint sensors, *not* from anything MoveIt told us. That
independence is the whole point: it is a second opinion. (In real code
you would wrap this in a short wait/retry, because the very first lookup
can arrive before the listener has heard anything.)

**`spot = frame.transform.translation`**
Pulls the *position* part out of that answer (a transform also carries an
orientation, which we ignore here).

**`return [spot.x, spot.y, spot.z]`**
Returns the measured hand position as the same three-number
left-right / forward-back / up-down list we use for targets, so the two
can be compared directly.

**`def gap(self, a, b):`**
Begins a tiny helper that measures the straight-line distance between two
points `a` and `b`.

**`return math.sqrt(sum((p - q) ** 2 for p, q in zip(a, b)))`**
This is the standard distance formula. `zip(a, b)` pairs up the two
points coordinate by coordinate; for each pair it takes the difference
`p - q` and squares it (`** 2`); `sum(...)` adds those up; and
`math.sqrt(...)` takes the square root. The result is a single number:
how far apart the commanded and measured points are, in metres.

**`def command_and_verify(self, target):`**
Begins the routine that runs **one full closed-loop step**: command the
move, then verify it. This is the body that the loop in `main` repeats.

**`self.get_logger().info(f"Commanding the hand to {target} ...")`**
Prints which target we are about to send, so the run is easy to follow.

**`self.moveit2.move_to_pose(position=target, quat_xyzw=HAND_FACING_DOWN)`**
Calls MoveIt — exactly the line from file 03 — to plan and execute a path
to the target. Behind this one call MoveIt does the inverse kinematics,
the path planning, and the collision-checking (against the planning scene
that [file 12](12-keep-the-world-current.md) keeps current). Our executive
just *asks*; MoveIt does the hard work.

**`finished = self.moveit2.wait_until_executed()`**
Waits for the move to actually run on the motors, and captures the
**controller's report** — our first layer of feedback. We store whether
the move *finished* (rather than being aborted partway, for example
because an obstacle appeared mid-path). (Exactly what this call returns
varies by `pymoveit2` version; treat the value as "did the controller
say it completed?")

**`if not finished:` … `return False`**
If the controller says the move did **not** complete, we report it and
stop here — there is no point checking the position of a move that was
abandoned. We hand back `False` to mean "this step failed."

**`measured = self.measured_hand_position()`**
The move says it finished — now we **check for ourselves**. We read the
hand's actual position from the TF tree. This is the second, independent
layer of feedback.

**`error = self.gap(target, measured)`**
Computes how far the measured hand position is from where we sent it.
This single number is the verdict's evidence.

**`self.get_logger().info(f"commanded={target} measured={measured} error={error * 1000:.1f} mm")`**
Prints all three things side by side — where we aimed, where the hand
really is, and the gap in millimetres (`* 1000` converts metres to
millimetres; `:.1f` shows one decimal place). This line is what makes the
cross-check *visible*.

**`if error <= TOLERANCE_M:` … `return True`**
The verdict. If the gap is within the 5-millimetre tolerance, the move is
correct: we print `PASS` and hand back `True`.

**`self.get_logger().warn("FAIL: off target — a real run would retry.")` … `return False`**
Otherwise the hand is not where we asked. We warn and hand back `False`.
In the full cell this `False` is what the behaviour tree of
[file 09](09-per-vial-loop.md) would catch, to re-plan, retry, or
quarantine — rather than charging ahead as if the move had worked.

**`def main():` … `rclpy.init()`**
The starting routine; `rclpy.init()` opens the connection to the
framework.

**`node = WatchTheMove()`**
Builds our executive node, which starts the TF listener.

**`for cycle in range(1, 4):`**
This loop **is the executive**: it repeats the command-and-verify step
three times (`range(1, 4)` gives 1, 2, 3). A real cell would loop
continuously, once per target; we do a few cycles so the output is easy
to read. *This loop is the answer to "who calls MoveIt continuously."*

**`node.get_logger().info(f"--- control cycle {cycle} ---")`**
Prints a banner for each cycle.

**`rclpy.spin_once(node, timeout_sec=1.0)`**
Lets the framework do a little work — in particular, lets the TF listener
receive the latest frame positions and the clock advance — before we read
the target and measure the result. Without an occasional `spin`, those
background updates never arrive.

**`target = node.latest_target()`**
Reads the (slightly wobbling) target for this cycle. Because we re-read it
every cycle, the executive naturally tracks a moving goal.

**`node.command_and_verify(target)`**
Runs the full step for this cycle: command the move, then verify it
landed.

**`node.destroy_node()` and `rclpy.shutdown()`**
Tidy shutdown after the loop: remove the node and close the framework
connection.

**`if __name__ == "__main__":` and `main()`**
The standard "only run if launched directly" guard, then the call that
starts everything.

## How to run it, and how you know it worked

Open **two** terminals; in each, first run
`source /opt/ros/jazzy/setup.bash`.

- **Terminal one** — start the myCobot 280's MoveIt configuration (as in
  file 03), which also publishes the TF tree this program reads:
  ```bash
  ros2 launch mycobot_280_moveit_config demo.launch.py
  ```
- **Terminal two** — run the closed-loop program:
  ```bash
  python3 watch_the_move.py
  ```

For each of the three cycles you should see the command line, then a line
reporting `commanded=…`, `measured=…`, and an `error=… mm`, then a
`PASS:` line — for example:

```
--- control cycle 1 ---
Commanding the hand to [0.20…, 0.0, 0.51] ...
commanded=[0.20…, 0.0, 0.51] measured=[0.20…, 0.0, 0.50…] error=1.8 mm
PASS: hand is on target.
```

To watch the **failure** path fire, make the check stricter than the arm
can manage — set `TOLERANCE_M = 0.0001` (a tenth of a millimetre) and run
again. Now the normal small gap between commanded and measured exceeds
the tolerance, and every cycle prints `FAIL: off target — a real run
would retry.` You have just watched the cross-check catch a move it
judges wrong — which is exactly the signal the per-vial behaviour tree
needs.

**Done when:** the program commands a move, then reports the measured
position and a pass/fail verdict computed from the TF tree — *not* from
MoveIt's own say-so — and you can flip it between PASS and FAIL by
changing the tolerance.

## Where this fits

- This extends the **Layer 3** motion exercise,
  [file 03 (reach the vial)](03-reach-the-vial.md), with the feedback it
  was missing: proof that the hand reached the goal.
- Its target comes from perception,
  [file 04 (see the tray)](04-see-the-tray.md); its world model is kept
  current by [file 12 (keep the world current)](12-keep-the-world-current.md).
- The `True`/`False` verdict it produces is exactly what the orchestration
  layer consumes:
  [file 09 (the per-vial loop)](09-per-vial-loop.md) turns a `False` into
  a retry or a quarantine instead of charging ahead.
- It is the *motion* counterpart of the *grip* check in
  [file 11 (subscribe to a sense)](11-subscribe-to-a-sense.md): both turn
  a raw measurement into a pass/fail gate.
- The deeper write-up of motion planning and control is
  [`../06-mycobot-280-impl/01-only-code/03-arm-motion-planning.md`](../06-mycobot-280-impl/01-only-code/03-arm-motion-planning.md);
  of orchestration,
  [`../06-mycobot-280-impl/01-only-code/07-orchestration-and-task-logic.md`](../06-mycobot-280-impl/01-only-code/07-orchestration-and-task-logic.md).
- The capstone,
  [`14-hello-cell-capstone.md`](14-hello-cell-capstone.md), gates every
  step on a verification just like this one.
