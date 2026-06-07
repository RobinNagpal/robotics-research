# 01 — Spawn the cell (Simulator & digital twin)

> Checklist exercise: **Layer 1 — "spawn the cell."**
> See [`../09-learning-checklist.md`](../09-learning-checklist.md).

## What this program proves

Before touching a real robot, we build a **digital twin**: a copy of the
work area that lives inside a physics simulator — a video-game-like world
that has gravity, solid objects, and collisions. This first exercise
creates the smallest possible version of that world: a flat floor, a
**table**, and a single **2 millilitre glass vial** (the small sample
bottle the robot will eventually pick up) sitting on the table. You then
open it on screen and see it.

If you can make a table and a vial appear and rest on each other under
gravity, you have proven the most basic thing of all: the simulator runs,
and you can place objects in it. Everything else in this project is built
inside this world.

The simulator we use is called **Gazebo**. The worlds it loads are
written in a plain-text format called the **Simulation Description
Format** (a set of labelled tags, very similar in look to the code behind
a web page). The second file is a **launch file**: a short Python program
whose only job is to start other programs for you with the right
settings.

## What you need first

Install the **Gazebo** simulator (the release named **Harmonic**) and
**the Robot Operating System, version 2** (the free toolkit that lets
robot programs talk to each other; its common short name is "ROS 2"). In
each terminal window you will first load the robot framework's commands:

```bash
source /opt/ros/jazzy/setup.bash
```

## The whole program — part one: the world

Save this as `cell.sdf`. (The ending `.sdf` marks it as a Simulation
Description Format file.)

```xml
<?xml version="1.0" ?>
<sdf version="1.10">
  <world name="hplc_cell">

    <plugin filename="gz-sim-physics-system"
            name="gz::sim::systems::Physics"/>
    <plugin filename="gz-sim-user-commands-system"
            name="gz::sim::systems::UserCommands"/>
    <plugin filename="gz-sim-scene-broadcaster-system"
            name="gz::sim::systems::SceneBroadcaster"/>

    <light type="directional" name="sun">
      <pose>0 0 10 0 0 0</pose>
      <diffuse>1 1 1 1</diffuse>
      <direction>-0.5 0.1 -0.9</direction>
    </light>

    <model name="ground">
      <static>true</static>
      <link name="surface">
        <collision name="collision">
          <geometry><plane><normal>0 0 1</normal></plane></geometry>
        </collision>
        <visual name="visual">
          <geometry><plane><normal>0 0 1</normal><size>5 5</size></plane></geometry>
        </visual>
      </link>
    </model>

    <model name="table">
      <static>true</static>
      <pose>0 0 0.4 0 0 0</pose>
      <link name="top">
        <collision name="collision">
          <geometry><box><size>1.0 0.6 0.05</size></box></geometry>
        </collision>
        <visual name="visual">
          <geometry><box><size>1.0 0.6 0.05</size></box></geometry>
        </visual>
      </link>
    </model>

    <model name="vial">
      <pose>0.2 0.0 0.46 0 0 0</pose>
      <link name="body">
        <collision name="collision">
          <geometry><cylinder><radius>0.006</radius><length>0.032</length></cylinder></geometry>
        </collision>
        <visual name="visual">
          <geometry><cylinder><radius>0.006</radius><length>0.032</length></cylinder></geometry>
        </visual>
      </link>
    </model>

  </world>
</sdf>
```

## Every line explained — the world

**`<?xml version="1.0" ?>`**
A required first line that simply announces "this is a structured tag
file." Every file of this kind begins with it; you never change it.

**`<sdf version="1.10">`**
Opens the whole description and states which version of the Simulation
Description Format the simulator should expect. The matching
`</sdf>` at the very bottom closes it. Everything lives in between.

**`<world name="hplc_cell">`**
Opens the **world** — the container for the floor, lights, and objects.
We name it `hplc_cell` (for "high-performance-liquid-chromatography
cell," the laboratory work area this project automates). The matching
`</world>` near the bottom closes it.

**The three `<plugin .../>` lines**
A **plugin** is an extra piece of behaviour you switch on. These three
turn on the essentials: the **Physics** plugin gives the world gravity
and collisions; the **UserCommands** plugin lets you add or move things
while it runs; the **SceneBroadcaster** plugin sends the picture of the
world out so a viewer window can show it. Each is self-closing (it ends
with `/>`), meaning it has no contents — it is just switched on.

**`<light type="directional" name="sun">`**
Opens a **light** so the scene is not pitch black. `type="directional"`
means the light behaves like the sun: parallel rays coming from one
direction. The matching `</light>` closes it.

**`<pose>0 0 10 0 0 0</pose>`**
A **pose** is a position and an angle. The six numbers are, in order, the
left-right, forward-back, and up-down position (in metres), then three
rotation angles. Here the light sits 10 metres up. (Distances in this
format are always in metres; 10 means ten metres.)

**`<diffuse>1 1 1 1</diffuse>`**
The colour of the light, given as four numbers for red, green, blue, and
opacity, each from 0 to 1. `1 1 1 1` is full white.

**`<direction>-0.5 0.1 -0.9</direction>`**
Which way the sun's rays point. The mostly-negative third number means
they point downward, so the light comes from above at a slant.

**`<model name="ground">`**
Opens the first **model**. A model is one object in the world. This one
is the floor; we name it `ground`. Its `</model>` closes it.

**`<static>true</static>`**
Marks the object as **static**, meaning fixed in place — gravity does not
move it and nothing can push it. A floor must never fall or slide, so it
is static. (The vial later will *not* be static, so it can be picked up.)

**`<link name="surface">`**
Opens a **link**. A link is one solid piece of a model. Simple objects
like the floor have just one link. Its `</link>` closes it.

**`<collision name="collision">`**
Opens the **collision shape** — the invisible solid form the physics
engine uses to decide when this object touches another. We give it the
name `collision`.

**`<geometry><plane><normal>0 0 1</normal></plane></geometry>`**
Describes that shape. `geometry` means "here is the form," `plane` means
"a flat infinite sheet," and `normal 0 0 1` means the sheet faces
straight up (it is the ground). The closing tags on the same line end
each of those in turn.

**`<visual name="visual">` … `</visual>`**
The **visual shape** — what you actually *see*. It is given separately
from the collision shape (a real robot part might look detailed but
collide as a simple block, which is faster). Here the visual is the same
flat sheet, sized `5 5` (a five-by-five-metre patch so it is not endless
on screen).

**`<model name="table">`**
Opens the second object, the table, and closes with its `</model>`.

**`<static>true</static>`**
The table is also fixed in place.

**`<pose>0 0 0.4 0 0 0</pose>`**
Places the centre of the table 0.4 metres (forty centimetres) above the
floor — roughly bench height — with no rotation.

**`<link name="top">` … `<box><size>1.0 0.6 0.05</size></box>`**
The table is one link named `top`, shaped as a **box** (a rectangular
block). Its size is 1.0 metre long, 0.6 metre deep, and 0.05 metre (five
centimetres) thick. The collision and visual both use this same box.

**`<model name="vial">`**
Opens the third object, the glass sample bottle. Notice there is **no**
`<static>` line this time — so the vial is *not* fixed; gravity acts on
it and it can be picked up. This is the only movable object.

**`<pose>0.2 0.0 0.46 0 0 0</pose>`**
Places the vial 0.2 metre to one side and 0.46 metre up — that is, resting
on the table top (the table surface is at about 0.425 metre, and the
vial's centre sits a little above it).

**`<cylinder><radius>0.006</radius><length>0.032</length></cylinder>`**
The vial's form is a **cylinder** (a round tube). Its radius is 0.006
metre (six millimetres, so twelve millimetres across — the real width of
a 2-millilitre vial) and its length is 0.032 metre (about three
centimetres tall). Again the collision and visual use the same shape.

**`</world>` and `</sdf>`**
These close the world and the whole description, in reverse order of how
they were opened. Every opened tag must be closed.

## The whole program — part two: the launcher

Save this as `spawn_the_cell.launch.py` in the same folder as `cell.sdf`:

```python
from launch import LaunchDescription
from launch.actions import ExecuteProcess
import os


def generate_launch_description():
    here = os.path.dirname(__file__)
    world_file = os.path.join(here, "cell.sdf")

    start_simulator = ExecuteProcess(
        cmd=["gz", "sim", world_file],
        output="screen")

    start_viewer = ExecuteProcess(
        cmd=["rviz2"],
        output="screen")

    return LaunchDescription([start_simulator, start_viewer])
```

## Every line explained — the launcher

**`from launch import LaunchDescription`**
Brings in a tool called `LaunchDescription` from the robot framework's
"launch" library. A launch description is simply a **list of programs to
start**. We will fill it with two entries.

**`from launch.actions import ExecuteProcess`**
Brings in `ExecuteProcess`, a tool that means "run this command as if I
typed it into a terminal." We will use it twice.

**`import os`**
Brings in Python's built-in `os` library, which has helpers for working
with file paths (the addresses of files on your computer).

**`def generate_launch_description():`**
Begins the one function the framework looks for by name. Whatever list of
programs this function hands back is what gets started.

**`here = os.path.dirname(__file__)`**
`__file__` is the address of this launch file itself. `os.path.dirname`
strips off the filename to leave just the folder it lives in. We store
that folder in `here`, so we can find `cell.sdf` sitting next to it.

**`world_file = os.path.join(here, "cell.sdf")`**
Glues the folder and the filename `cell.sdf` together into one complete
address, and stores it in `world_file`. Building the path this way means
the launcher works no matter which folder you run it from.

**`start_simulator = ExecuteProcess(cmd=["gz", "sim", world_file], output="screen")`**
Describes the first program to run. `cmd` is the command, given as a list
of words: `gz sim <world_file>` is the instruction that starts Gazebo on
our world. `output="screen"` means "show its printed messages in this
terminal." We save this description in `start_simulator`.

**`start_viewer = ExecuteProcess(cmd=["rviz2"], output="screen")`**
Describes the second program: `rviz2`, the robot framework's
three-dimensional viewer window, where the robot and its sensor data are
drawn. It is started the same way.

**`return LaunchDescription([start_simulator, start_viewer])`**
Hands back the list of the two programs to start. The square brackets
make a list; the framework reads it and launches both.

## How to run it, and how you know it worked

In a terminal (after `source /opt/ros/jazzy/setup.bash`), from the folder
containing both files:

```bash
ros2 launch spawn_the_cell.launch.py
```

`ros2 launch` reads the launch file and starts everything in it. A Gazebo
window opens showing a floor, a table, and a small vial resting on the
table; a viewer window also opens.

**Done when:** the table and the vial appear in the simulator and the
vial sits on the table without falling through it.

**Going further (optional):** to add the actual arm, install the
`mycobot_ros` package (which ships a ready-made description of the
myCobot 280) and spawn it into this same world with the framework's
`create` tool, for example:

```bash
ros2 run ros_gz_sim create -name mycobot -topic robot_description
```

This places the six-joint arm beside the table, completing the picture
the checklist describes — the arm, a table, and a vial, all in one world.

## Where this fits

- This is the runnable version of the **Layer 1** exercise in
  [`../09-learning-checklist.md`](../09-learning-checklist.md).
- The deeper write-up of simulators (and why we choose Gazebo) is
  [`../06-mycobot-280-impl/01-only-code/01-simulation-and-digital-twin.md`](../06-mycobot-280-impl/01-only-code/01-simulation-and-digital-twin.md).
- Every later exercise assumes this world exists; the capstone
  [`14-hello-cell-capstone.md`](14-hello-cell-capstone.md) runs the whole
  loop inside it.
