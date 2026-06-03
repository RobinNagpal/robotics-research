# 03 — Reach the vial (Arm motion planning)

> Checklist exercise: **Layer 3 — "reach the vial."**
> See [`../07-learning-checklist.md`](../07-learning-checklist.md).

## What this program proves

The arm in this project is the **myCobot 280**: a small desktop robotic
arm with **six joints** (six places where it bends), about 280 millimetres
of reach and a payload of about 250 grams. Our goal in this exercise is to
move the arm's **hand** — the very tip, called the **end-effector** (the
business end that will eventually grip the vial) — from where it starts to
a point hovering just above the **2 millilitre glass vial**, and then to a
point above a slot in the sample tray named **A3**.

The hard part of moving a robot arm is this: you know *where in space* you
want the hand to be, but the motors only understand *joint angles* (how
far each of the six joints is bent). Turning "put the hand here" into "bend
joint one this much, joint two that much, …" is called **inverse
kinematics** (working out the joint angles needed to put the hand at a
desired point). Doing that by hand is painful and error-prone. On top of
that, the arm must not swing through the table on its way.

This program proves that we can hand both of those problems to a piece of
software called **MoveIt 2** (a free motion-planning system for robot arms;
"MoveIt" is its name, "2" is the version) and simply *state our goals*. We
say "put the hand at this point above the vial," then "now at this point
above tray slot A3," and MoveIt 2 does the arithmetic and finds a safe path.

Be honest about the division of labour: **MoveIt 2 does the genuinely hard
work.** Our script is short because it only describes *what* we want, not
*how* to achieve it. That is the whole point of using a motion planner.

> Teaching-code note: this example is deliberately stripped down, and the
> exact names in robot software drift between versions. Treat it as a clear
> illustration of the idea, not a guaranteed copy-paste for your particular
> install.

## What you need first

You need **the Robot Operating System, version 2** installed (the free
toolkit that lets robot programs talk to each other; its common short name
is "ROS 2"; we will keep calling it "the robot framework"). You also need
**MoveIt 2** installed, and the myCobot 280's **MoveIt configuration**
already running — that is the bundle of files that tells MoveIt the exact
shape and joint limits of this particular arm. That configuration ships in
the **`mycobot_ros`** package (a ready-made collection of myCobot programs
and descriptions). Start it in its own terminal before running our script;
it provides the planning service our program will call.

We use a small community helper named **`pymoveit2`** (a thin Python
wrapper — a convenience layer — around MoveIt 2). It was chosen here purely
because it produces the *shortest* clear example: a few lines instead of
dozens. The fuller, official interface is called `moveit_py`; it can do the
same thing with more ceremony.

In every terminal, first load the robot framework's commands:

```bash
source /opt/ros/jazzy/setup.bash
```

## The whole program

Save this as a file named `reach_the_vial.py`:

```python
import rclpy
from rclpy.node import Node
from pymoveit2 import MoveIt2


# A "pose" is a position in space plus an orientation.
# Each position below is three numbers: left-right, forward-back,
# up-down, measured in metres from the base of the arm.
ABOVE_VIAL = [0.20, 0.00, 0.51]      # ~5 cm above the vial on the table
ABOVE_TRAY_SLOT_A3 = [0.15, 0.12, 0.51]  # hovering over tray slot "A3"

# Orientation: point the hand straight down at the table.
# These four numbers describe a rotation; this set means "facing down."
HAND_FACING_DOWN = [1.0, 0.0, 0.0, 0.0]


class ReachTheVial(Node):
    def __init__(self):
        super().__init__("reach_the_vial")
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

    def go_to(self, position, label):
        self.get_logger().info(f"Planning a move to {label}...")
        self.moveit2.move_to_pose(
            position=position,
            quat_xyzw=HAND_FACING_DOWN,
        )
        self.moveit2.wait_until_executed()
        self.get_logger().info(f"Arrived at {label}.")


def main():
    rclpy.init()
    arm = ReachTheVial()
    arm.go_to(ABOVE_VIAL, "a point above the vial")
    arm.go_to(ABOVE_TRAY_SLOT_A3, "a point above tray slot A3")
    arm.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
```

## Every line explained

**`import rclpy`**
The word `import` means "bring in a library of ready-made code so I can use
it." `rclpy` is the robot framework's Python library (the name is short for
"Robot Client Library for Python"). This line lets our program join the
robot's network of programs, which is how it will reach MoveIt 2.

**`from rclpy.node import Node`**
This brings in one specific tool, called `Node`. A **node** is the
framework's word for "one small program that does one job." We build our
own program on top of it.

**`from pymoveit2 import MoveIt2`**
This brings in the helper class `MoveIt2` from the `pymoveit2` library. A
**class** here is a ready-made blueprint; this one knows how to talk to the
MoveIt 2 motion planner on our behalf. It is the single tool that turns
"put the hand here" into actual joint movements.

**`ABOVE_VIAL = [0.20, 0.00, 0.51]`**
This stores our first target **position** under a clearly-named constant
(a value we set once and reuse). The three numbers are a point in space,
measured in metres from the base of the arm: 0.20 metre forward, 0.00 metre
to the side, and 0.51 metre up. That height sits about five centimetres
above the vial, which rests on the table — so this is "hovering over the
vial." The square brackets make the three numbers into a single list.

**`ABOVE_TRAY_SLOT_A3 = [0.15, 0.12, 0.51]`**
The second target position, named for **tray slot A3** (a labelled slot in
the sample tray). Same idea: a point in space, here shifted sideways to sit
over that slot, at the same hovering height.

**`HAND_FACING_DOWN = [1.0, 0.0, 0.0, 0.0]`**
A position alone is not enough; the planner also needs to know which way the
hand should *point*. That is the **orientation**. A position plus an
orientation together is called a **pose**. We give the orientation as four
numbers (a compact, standard way computers store a rotation, called a
*quaternion* — you do not need to understand the mathematics; this
particular set means "hand pointing straight down at the table," which is
what you want when reaching for something on a table).

**`class ReachTheVial(Node):`**
The word `class` starts the definition of our own node. We name our
blueprint `ReachTheVial`. The `(Node)` part means "build it on top of the
framework's `Node` blueprint," so it can talk on the network.

**`def __init__(self):`**
`def` begins a named block of instructions (a "function"). The special name
`__init__` means "the set-up steps that run once, automatically, the moment
this program is created." `self` is how the code refers to *this particular*
program while setting it up.

**`super().__init__("reach_the_vial")`**
This runs the framework's own set-up first and registers our program on the
network under the readable name `"reach_the_vial"`.

**`self.moveit2 = MoveIt2( ... )`**
This builds our connection to the motion planner from the `MoveIt2`
blueprint and stores it in `self.moveit2` so we can use it later. The
several settings inside the brackets tell MoveIt 2 exactly which arm it is
steering. Each is explained next.

**`node=self,`**
Hands the planner helper our own program, so it can send and receive
messages through us on the network.

**`joint_names=["joint1", ... "joint6"],`**
Lists the names of the arm's **six joints**, in order. MoveIt 2 needs these
names so that, once it has worked out the angles, it knows which motor each
angle belongs to. The myCobot 280 has exactly six, hence six names.

**`base_link_name="base",`**
Names the fixed part of the arm that everything else is measured from — the
**base** bolted to the table. Our target positions are measured from here.

**`end_effector_name="link6",`**
Names the **end-effector**, the moving tip of the arm (here the last
segment, `link6`). This is the part MoveIt 2 will try to place at our target
pose. ("End-effector" is the general robotics word for whatever is on the
end of the arm — a gripper, a tool, or just the tip.)

**`group_name="arm",`**
Names the **group** of joints to move together. The myCobot configuration
calls its six-joint chain `arm`. (A robot could have several groups — say an
arm and a separate gripper — so MoveIt asks which one you mean.)

**`def go_to(self, position, label):`**
This begins a small helper function of our own. We will call it twice — once
per target. It takes a `position` (where to send the hand) and a `label` (a
plain-English description, used only for the status messages).

**`self.get_logger().info(f"Planning a move to {label}...")`**
This prints a tidy, time-stamped status line. `get_logger()` is the
framework's built-in way of printing messages; `.info(...)` marks this one
as ordinary information. The `f"..."` is an *f-string*, a Python way to drop
a value (here `label`) into the middle of text.

**`self.moveit2.move_to_pose(position=position, quat_xyzw=HAND_FACING_DOWN)`**
This is the heart of the program. It asks MoveIt 2 to move the hand to the
given pose: the `position` we passed in, with the orientation
`HAND_FACING_DOWN`. (`quat_xyzw` is just the setting's name for "the
orientation as those four numbers.") Behind this single line, MoveIt 2 does
all of the following on its own:

- **Inverse kinematics** — working out the joint angles needed to put the
  hand at that point.
- **Planning** — choosing a smooth sequence of in-between positions that
  carries the hand from where it is now to the goal.
- **Collision-checking** — verifying that nothing along that path bumps into
  the table or the arm into itself, and rejecting paths that would.

We write one line; MoveIt does the hard work.

**`self.moveit2.wait_until_executed()`**
The move takes real time as the motors turn. This line **pauses our program
until the arm has actually finished arriving**, so we do not fire off the
next goal while the arm is still mid-swing.

**`self.get_logger().info(f"Arrived at {label}.")`**
A status line confirming the hand reached this target before we move on.

**`def main():`**
This begins the program's main starting routine — the steps that run when
you launch the file.

**`rclpy.init()`**
Starts up the connection to the robot framework. Nothing can talk on the
network until this has run, so it always comes first.

**`arm = ReachTheVial()`**
Builds one copy of our program from the blueprint, which automatically runs
the `__init__` set-up and so creates the link to MoveIt 2.

**`arm.go_to(ABOVE_VIAL, "a point above the vial")`**
The first real instruction: send the hand to the point above the vial. This
call does not return until the arm has arrived (because of the wait line
inside).

**`arm.go_to(ABOVE_TRAY_SLOT_A3, "a point above tray slot A3")`**
The second instruction: now send the hand to the point above tray slot A3.
Together these two calls are the whole "reach" demonstration: home → above
vial → above the tray slot, with MoveIt planning each leg safely.

**`arm.destroy_node()`**
Politely removes our program from the network, freeing its name and
resources.

**`rclpy.shutdown()`**
Closes the connection to the robot framework cleanly — the mirror image of
`rclpy.init()`.

**`if __name__ == "__main__":`**
A standard Python guard meaning "only run the next line if this file was
launched directly (rather than imported by another file)."

**`main()`**
Finally calls the starting routine, setting everything above in motion.

## How to run it, and how you know it worked

Open **two** terminal windows. In each, first load the robot framework's
commands with `source /opt/ros/jazzy/setup.bash`.

- **Terminal one** — start the myCobot 280's MoveIt configuration (the part
  that provides the planning service). With the `mycobot_ros` package
  installed, this is typically a single launch command, for example:
  ```bash
  ros2 launch mycobot_280_moveit_config demo.launch.py
  ```
  A viewer window opens showing the arm. Wait until it reports that it is
  ready to plan. (The exact launch-file name varies by package version;
  check the `mycobot_ros` documentation.)

- **Terminal two** — run our script:
  ```bash
  python3 reach_the_vial.py
  ```
  You should see `Planning a move to a point above the vial...` and then
  `Arrived at a point above the vial.`, followed by the same pair of lines
  for tray slot A3. In the viewer, the arm visibly swings to a spot above
  the vial, then over to the tray slot — without ever passing through the
  table.

**Done when:** the arm moves to both target poses in turn, you did **not**
compute a single joint angle yourself, and the path never collides with the
table. You have now used a motion planner to turn "put the hand here" into
real, safe movement.

## Where this fits

- This is the runnable version of the **Layer 3** exercise in
  [`../07-learning-checklist.md`](../07-learning-checklist.md).
- The deeper write-up of arm motion planning (and why we choose MoveIt 2)
  is
  [`../04-mycobot-280-impl/01-only-code/03-arm-motion-planning.md`](../04-mycobot-280-impl/01-only-code/03-arm-motion-planning.md).
- The capstone, [`12-hello-cell-capstone.md`](12-hello-cell-capstone.md),
  uses these same "move above the vial" and "move above the tray slot" steps
  as part of the full pick-and-place loop.
