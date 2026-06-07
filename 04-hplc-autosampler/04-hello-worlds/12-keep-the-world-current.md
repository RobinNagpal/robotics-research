# 12 — Keep the world current (live obstacles & a moving tray)

> Checklist exercise: **Layer 3 extension — "keep the planning scene
> live."** See [`../09-learning-checklist.md`](../09-learning-checklist.md).

## What this program proves

In [file 03 (reach the vial)](03-reach-the-vial.md) we asked **MoveIt 2**
(the free motion-planning system for robot arms) to move the hand to a
point, and it found a path that did not hit the table. But there is a
quiet assumption hiding in that exercise: *how did MoveIt know the table
was there?*

The answer is that MoveIt plans against an **internal model of the
world** it keeps in memory, called the **planning scene** — a list of
the solid objects it must avoid (the table, the tray, a stray beaker)
and exactly where each one is. **MoveIt only avoids what is in that
list.** If the list is empty, MoveIt will cheerfully plan a path
straight through the real tray. If the list says the tray is on the left
but someone has nudged it to the right, MoveIt will plan around *empty
air on the left* and clip the tray on the right.

So in a real, moving cell something must **continuously keep that list up
to date** — watching where the tray and any obstacles actually are right
now, and telling MoveIt. That "something" is a small program that takes
the output of the perception layer ([file 04, see the
tray](04-see-the-tray.md)) and writes it into the planning scene as
**collision objects** (the planner's word for "a solid thing to avoid").

This program is that updater. It does two things:

1. **Once**, it adds the fixed **table** to the scene.
2. **Five times a second**, it refreshes the position of the **tray**,
   which we pretend is slowly sliding side to side.

The single most important idea here: **you never re-route the arm's path
yourself.** You keep the *world model* current, and MoveIt re-routes the
path for you — every time it next plans, it plans around wherever the
tray is *now*. Keep the world honest and the path takes care of itself.

> Teaching-code note: as in file 03, the exact method names in robot
> software drift between versions, and this is deliberately stripped
> down. Treat it as a clear illustration of the idea, not a guaranteed
> copy-paste for your particular install.

## What you need first

The same setup as [file 03](03-reach-the-vial.md): **the Robot Operating
System, version 2** ("ROS 2," the free toolkit that lets robot programs
talk to each other), **MoveIt 2**, and the myCobot 280's **MoveIt
configuration** running in its own terminal (it hosts the planning scene
this program writes into). We again use the small community helper
**`pymoveit2`** (a thin Python convenience layer around MoveIt 2) because
it gives the shortest clear example.

In every terminal, first load the robot framework's commands:

```bash
source /opt/ros/jazzy/setup.bash
```

## The whole program

Save this as a file named `keep_the_world_current.py`:

```python
import rclpy
from rclpy.node import Node
from pymoveit2 import MoveIt2
import math


# Each box below is described by its size (width, depth, height in
# metres) and a position (left-right, forward-back, up-down in metres
# from the base of the arm).
TABLE_SIZE = [0.60, 0.60, 0.02]        # a flat tabletop, 2 cm thick
TABLE_POSITION = [0.20, 0.00, 0.49]    # just under the vials

TRAY_SIZE = [0.10, 0.16, 0.03]         # the sample tray, a small slab

# A "level, unrotated" orientation, as four numbers (a quaternion).
LEVEL = [0.0, 0.0, 0.0, 1.0]


class LiveWorld(Node):
    def __init__(self):
        super().__init__("live_world")
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
        self.moveit2.add_collision_box(
            id="table",
            size=TABLE_SIZE,
            position=TABLE_POSITION,
            quat_xyzw=LEVEL,
        )
        self.get_logger().info("Added the fixed table to the scene.")
        self.create_timer(0.2, self.refresh_tray)

    def latest_tray_position(self):
        # Stand-in for perception (file 04): pretend the tray slides
        # slowly side to side. A real version reads the marker's pose.
        t = self.get_clock().now().nanoseconds * 1e-9
        y = 0.12 + 0.03 * math.sin(t)     # drifts ~3 cm to and fro
        return [0.15, y, 0.50]

    def refresh_tray(self):
        position = self.latest_tray_position()
        self.moveit2.add_collision_box(
            id="tray",
            size=TRAY_SIZE,
            position=position,
            quat_xyzw=LEVEL,
        )
        self.get_logger().info(
            f"Tray now at {position} — planning scene updated."
        )


def main():
    rclpy.init()
    node = LiveWorld()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
```

## Every line explained

**`import rclpy`** and **`from rclpy.node import Node`**
As in every file here: bring in the robot framework's Python library
(`rclpy`, "Robot Client Library for Python") and its `Node` tool — a
**node** being "one small program that does one job" on the robot's
network.

**`from pymoveit2 import MoveIt2`**
Brings in the `MoveIt2` helper, the single tool that talks to the MoveIt
2 planner for us. Here we use it not to *move* the arm but to *edit the
planner's world model*.

**`import math`**
Brings in Python's built-in mathematics library. We use it only to make
the tray drift back and forth in a smooth wave, to imitate a moving
obstacle.

**`TABLE_SIZE = [0.60, 0.60, 0.02]`**
The size of the tabletop as three numbers — width, depth, and thickness
in metres: a 60-centimetre square, 2 centimetres thick. A collision
object needs both a *size* and a *position*; this is the size.

**`TABLE_POSITION = [0.20, 0.00, 0.49]`**
Where the centre of that tabletop sits, in metres from the base of the
arm: 0.20 forward, centred side to side, and 0.49 up — just below the
height at which the vials stand, so the table is the surface they rest
on.

**`TRAY_SIZE = [0.10, 0.16, 0.03]`**
The size of the sample tray, the object we will keep *moving*: a small
slab 10 by 16 by 3 centimetres.

**`LEVEL = [0.0, 0.0, 0.0, 1.0]`**
An **orientation** — which way the box is turned — given as the four
numbers computers use for a rotation (a *quaternion*). This particular
set means "not rotated at all; sitting level." Both our boxes are level,
so they share it.

**`class LiveWorld(Node):`**
Defines our own node, named `LiveWorld`, built on the framework's `Node`
blueprint so it can talk on the network.

**`def __init__(self):` … `super().__init__("live_world")`**
The set-up steps that run once when the program starts. The `super()`
line runs the framework's own set-up and registers us on the network
under the readable name `live_world`.

**`self.moveit2 = MoveIt2( ... )`**
Builds our link to the MoveIt 2 planner, with exactly the same settings
as file 03 (the six joint names, the `base` it measures from, the
`link6` tip, and the `arm` group). We need this link because the
planning scene we want to edit *belongs to* MoveIt — we change the world
by talking to the planner, not by editing a file.

**`self.moveit2.add_collision_box(id="table", size=TABLE_SIZE, position=TABLE_POSITION, quat_xyzw=LEVEL)`**
This is the first real action. It adds one **collision object** — a box
— to MoveIt's planning scene. `id="table"` gives it a name; `size` and
`position` say how big it is and where it sits; `quat_xyzw` is its
orientation. From this moment, every path MoveIt plans will steer clear
of this box. We add the table just once because the table never moves.

**`self.get_logger().info("Added the fixed table to the scene.")`**
Prints a tidy, time-stamped status line confirming the table is in
place. `get_logger().info(...)` is the framework's built-in way of
printing ordinary information.

**`self.create_timer(0.2, self.refresh_tray)`**
This is the engine of the program. `create_timer` asks the framework to
call a function of ours **over and over on a fixed clock** — here, every
`0.2` seconds, which is five times a second. The function it will call
is `self.refresh_tray`. This repeating call is what makes the world
model *live* rather than a one-off snapshot.

**`def latest_tray_position(self):`**
Begins a small helper that answers the question "where is the tray
*right now*?" In this teaching program it makes up a moving answer; in
the real cell it would read the tray's measured position from the
perception layer.

**`t = self.get_clock().now().nanoseconds * 1e-9`**
Reads the current time from the robot's clock and converts it to plain
seconds (the clock counts in *nanoseconds*, billionths of a second, so
we multiply by `1e-9`, which is one-billionth, to get seconds). We use
the time only to drive the pretend motion below.

**`y = 0.12 + 0.03 * math.sin(t)`**
Makes the tray's side-to-side position swing gently. `math.sin(t)` is a
wave that rises and falls smoothly between −1 and +1 as time passes;
multiplying by `0.03` and adding `0.12` turns that into a position that
drifts about 3 centimetres either side of 0.12 metre. This is our
stand-in for "someone keeps nudging the tray."

**`return [0.15, y, 0.50]`**
Hands back the tray's current position: fixed at 0.15 forward and 0.50
up, but with the drifting side-to-side value `y` we just computed.

**`def refresh_tray(self):`**
The function the timer calls five times a second — the one that keeps the
planner's world honest.

**`position = self.latest_tray_position()`**
Asks the helper above for the tray's latest position and stores it.

**`self.moveit2.add_collision_box(id="tray", size=TRAY_SIZE, position=position, quat_xyzw=LEVEL)`**
Writes the tray into the planning scene at that fresh position. The key
detail: we reuse the **same name**, `id="tray"`, every time. Adding a
collision object whose name already exists does not pile up a second
box — it **replaces the old one**, i.e. *moves* the tray to its new
spot. So five times a second the planner's idea of where the tray is
gets corrected to match reality.

**`self.get_logger().info(f"Tray now at {position} — planning scene updated.")`**
Prints the new tray position each cycle so you can watch the world model
track the moving tray. The `f"..."` is an *f-string*, which drops the
value of `position` into the text.

**`def main():`**
Begins the program's starting routine.

**`rclpy.init()`**
Starts the connection to the robot framework; nothing can talk on the
network until this has run.

**`node = LiveWorld()`**
Builds one copy of our node, which runs the set-up: adds the table and
starts the five-times-a-second timer.

**`rclpy.spin(node)`**
This is what keeps the program **alive and looping**. `spin` hands
control to the framework and says "keep running, and every time a timer
is due, call its function." Without this line the program would set up
and immediately exit; with it, the tray keeps being refreshed until you
stop the program with Ctrl-C.

**`node.destroy_node()` and `rclpy.shutdown()`**
The tidy shutdown, reached when you stop the program: remove our node
from the network and close the connection to the framework cleanly.

**`if __name__ == "__main__":` and `main()`**
The standard Python guard — "only run `main()` if this file was launched
directly" — followed by the call that sets everything in motion.

## How to run it, and how you know it worked

Open **two** terminals; in each, first run
`source /opt/ros/jazzy/setup.bash`.

- **Terminal one** — start the myCobot 280's MoveIt configuration (the
  same launch as file 03), which hosts the planning scene and opens the
  RViz viewer:
  ```bash
  ros2 launch mycobot_280_moveit_config demo.launch.py
  ```
- **Terminal two** — run this updater:
  ```bash
  python3 keep_the_world_current.py
  ```

You should see `Added the fixed table to the scene.` once, then a steady
stream of `Tray now at [0.15, …, 0.50] — planning scene updated.` lines,
with the middle number drifting up and down. **In the RViz viewer you
will see a tray-sized box slide gently back and forth** while the table
stays put.

Now prove that the path follows the world. Leave this updater running and,
in a third terminal, run the reach program from
[file 03](03-reach-the-vial.md) a few times. Each time MoveIt plans, it
routes the arm around *wherever the tray is at that instant* — pause the
updater with the tray on the left and the arm curves right; let it slide
and plan again and the avoidance moves with it. You never edited the
path; you only kept the world current.

**Done when:** the tray box visibly moves in RViz as the program runs,
and a fresh reach plan steers around the tray's *current* position — not
a stale one — without you computing a single waypoint yourself.

## Where this fits

- This extends the **Layer 3** motion exercise,
  [file 03 (reach the vial)](03-reach-the-vial.md), with the missing
  half: keeping MoveIt's world model honest so its collision-checking
  means something.
- Its input — where the tray and obstacles actually are — is the job of
  the perception layer, [file 04 (see the tray)](04-see-the-tray.md).
- The companion exercise, [file 13 (watch the
  move)](13-watch-the-move.md), closes the *other* loop: after a move, it
  checks the hand actually arrived where it was sent.
- The deeper write-up of motion planning and the planning scene is
  [`../06-mycobot-280-impl/01-only-code/03-arm-motion-planning.md`](../06-mycobot-280-impl/01-only-code/03-arm-motion-planning.md).
- The capstone,
  [`14-hello-cell-capstone.md`](14-hello-cell-capstone.md), assumes a
  current world model underneath its motion steps.
