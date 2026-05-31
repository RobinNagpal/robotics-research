# Learn: Gazebo Harmonic — the simulator layer

> This is a hands-on tutorial for the **simulator** layer of the
> shelf-stocking robot. The simulator is the practice world the robot
> lives in before any real metal exists. Here you will learn what
> Gazebo Harmonic is, the handful of concepts you use every day, and
> then build up — from an empty world, to a world with a depth camera
> and a laser scanner, to the actual simulation setup for *this*
> project. The audience is a programmer who knows code but not
> robotics, so every robotics term is spelled out in one plain
> sentence the first time it appears.

For *why* this layer was chosen over Isaac Sim, MuJoCo, and the rest,
see the layer overview: [`../01-simulator.md`](../01-simulator.md).
For one-line definitions of any term, see the glossary:
[`../../02-glossary.md`](../../02-glossary.md).

---

## 1. Introduction and basic concepts

### What a physics simulator is

A **physics simulator** is a program that computes how virtual objects
move, fall, collide, and rub against each other, so a digital object
behaves like its real-world twin. You give it shapes, masses, and
forces; it works out — many times per second — where everything ends
up. Think of it as a tiny physics-accurate video game whose "player"
is your robot's software instead of a human.

A **simulation-first** robotics project does all of its early work
inside such a simulator before touching hardware, because it is
faster, cheaper, and safe to fail in. A real robot arm that misjudges
a grasp can break a $300 product or itself; a simulated arm just resets
and tries again. Our whole project (see
[`../../01-requirements.md`](../../01-requirements.md)) is built this
way: prove the drive-pick-place loop in simulation, then transfer the
exact same software to a physical robot.

### What Gazebo Harmonic is

**Gazebo** is a free, open-source robotics simulator. It models a
world, the robots in it, and the sensors on those robots, all under one
physics engine. **Harmonic** is the name of one specific, modern release
of Gazebo (released 2023, supported for years). You will also see the
old name **"Ignition"** in tutorials online — that was the project's
name a few years ago before it was renamed back to plain "Gazebo." The
even-older "Gazebo Classic" is a separate, now-retired codebase; ignore
it. Everything in this document is the *new* Gazebo, which you run with
the command:

```bash
gz sim
```

`gz` is the command-line program ("the Gazebo CLI"). `sim` is the
sub-command that launches the simulation. There are other sub-commands
(`gz topic`, `gz service`, `gz model`) that we will meet shortly.

### How Gazebo relates to ROS 2

**ROS 2 (Robot Operating System 2)** is the open-source framework that
lets a robot's separate software pieces — vision, navigation, arm
control — run as small programs and talk to each other over a shared
messaging system. It is the "middleware" glue for this whole project
(its own tutorial is [`02-ros2.md`](02-ros2.md) in this folder).

Gazebo is *not* part of ROS 2 — it is a separate program with its own
internal messaging. To connect the two, you run a bridge package called
**`ros_gz`** (read "ROS–Gazebo"). It has two important pieces:

- **`ros_gz_sim`** — helpers to launch Gazebo from a ROS 2 launch file
  and to spawn robots into the running world.
- **`ros_gz_bridge`** — a translator process that copies messages back
  and forth between Gazebo topics and ROS 2 topics. A camera image
  published *inside* Gazebo comes *out* on a normal ROS 2 topic your
  perception node can read, and a `/cmd_vel` drive command from ROS 2
  goes *into* Gazebo to move the wheels.

The payoff: the navigation and arm-planning code you write against the
simulator is byte-for-byte the same code that later runs on hardware.
Only the bridge is swapped for real device drivers.

### SDF worlds

Gazebo describes everything — the world, the lights, the robots — in a
text file format called **SDF (Simulation Description Format)**. It is
XML, so it looks like HTML's stricter cousin. An `.sdf` file is a
declarative scene description: "there is a ground plane here, a sun
light there, a shelf at this pose." You do not write code to build the
scene; you describe it, and Gazebo reads it. (A close relative,
**URDF**, the Unified Robot Description Format, describes just a robot's
links and joints; more on both in section 2.)

### GUI and headless modes

`gz sim` can run two ways:

- **GUI mode** — opens a 3D window where you watch the simulation,
  rotate the camera, and click things. Good for developing and
  debugging.
- **Headless mode** — runs with no window at all, just the physics. You
  use this on a server, in automated tests, or when running hundreds of
  randomized trials to measure the success rate from the requirements.
  You enable it with the `-s` ("server only") flag.

That is the whole mental model: a physics simulator, described by SDF
text files, run by the `gz sim` command, connected to your ROS 2 code
through the `ros_gz` bridge. (Later in the project we add **Isaac Sim**
for photorealistic perception work, but that is a separate, GPU-heavy
step we do not cover here.)

---

## 2. Important concepts that are used most often

These are the nouns you will see constantly. Read once, refer back.

### Worlds, models, links, joints

- **World** — the top-level container: the floor, the lighting, the
  physics settings, and everything placed in the scene. One simulation
  has one world.
- **Model** — one self-contained object in the world: a shelf, a soup
  can, or the whole robot. Models can be nested.
- **Link** — one rigid (non-bending) piece of a model, with its own
  shape, mass, and collision boundary. The robot's base is a link; each
  segment of the arm is a link.
- **Joint** — the connection between two links that defines how they
  move relative to each other. A `revolute` joint rotates (an arm
  elbow); a `prismatic` joint slides (a gripper finger); a `fixed`
  joint welds two links together; a `continuous` joint spins without
  limit (a wheel).

A model is therefore a tree of **links** held together by **joints** —
the robot's skeleton.

### SDF vs URDF

Both are XML formats that describe links and joints.

- **URDF** (Unified Robot Description Format) is the ROS-world standard
  for describing *a robot*. Arm vendors ship URDF; MoveIt 2 (the
  arm-planning layer) reads URDF.
- **SDF** is Gazebo's native format and describes a whole *world*, not
  just one robot — lights, physics, multiple models, and sensors.

Gazebo Harmonic can load URDF directly and convert it to SDF
internally, so in practice you keep your robot in URDF (shared with
MoveIt 2) and write the *world* in SDF. They overlap heavily; if you
can read one, you can read the other.

### Plugins

A **plugin** is a small piece of compiled code that you attach to part
of the SDF to give it behavior the static description cannot express.
Two kinds matter here:

- **System plugins** add behavior to the simulation or a model — for
  example, `DiffDrive` turns wheel-speed commands into base motion, and
  `JointStatePublisher` reports each joint's angle.
- **Sensor plugins** make a sensor actually produce data and publish it.
  A camera link does nothing until its sensor element is present and the
  rendering sensor system is loaded.

You enable plugins either inside the SDF (`<plugin>` tags) or as
world-level systems. Gazebo Harmonic ships most common ones built in.

### Physics engines

The **physics engine** is the math core that computes motion and
contact. Gazebo can use several; the default is **DART (Dynamic
Animation and Robotics Toolkit)**, which is a good general-purpose
choice with solid contact handling — important because our whole task
is about contact (grasping a can, setting it down gently). Alternatives
include **Bullet** and **ODE**. For this project, the DART default is
fine; you rarely change it.

### Sensors

A **sensor** is a simulated device that produces the same kind of data
its real counterpart would. The ones we use:

- **RGB-D camera** — "RGB-D" means a normal color camera ("RGB") plus a
  per-pixel **depth** channel ("D"): for every pixel it also reports how
  far away that point is. Gazebo can output the color image, the depth
  image, and a **point cloud** (a set of 3D dots reconstructing the
  scene). This is the wrist camera the robot uses to see the shelf slot.
- **2D lidar** — "lidar" is a laser range-finder; a *2D* lidar sweeps a
  single horizontal plane and reports the distance to the nearest
  obstacle at each angle, like a fan of measuring tapes. The mobile base
  uses it to map and avoid walls.
- **IMU (Inertial Measurement Unit)** — reports acceleration and
  rotation rate, used to estimate motion. Optional for us but cheap to
  add.
- **Contact sensor** — reports when one link physically touches another.
  Useful to confirm the gripper actually grabbed the can or that the can
  reached the shelf.

### The transport layer and `gz topic`

Inside Gazebo, programs talk over a **publish/subscribe** messaging
system called **Gazebo Transport**. A **topic** is a named message
channel: publishers send messages to it, subscribers receive them. It
is conceptually similar to a WebSocket event stream where many clients
listen on a named event. You inspect it from the terminal with
**`gz topic`**:

```bash
gz topic -l              # list every active topic
gz topic -i -t /clock    # info about one topic (its message type)
gz topic -e -t /clock    # echo: print messages as they arrive
```

`/clock` is the topic carrying simulation time — important because in
simulation, time can run faster or slower than the wall clock, and ROS 2
nodes must follow *sim* time.

### `gz sim` vs `gz service` / `gz topic`

Three CLI tools, three jobs:

- **`gz sim`** — start, pause, and run the simulation itself.
- **`gz topic`** — watch and publish on the streaming message channels
  (continuous data like camera frames).
- **`gz service`** — call a one-shot request/response function (like an
  HTTP request): "spawn this model," "reset the world," "delete that
  object." A service returns once; a topic streams forever.

### Spawning models

**Spawning** means inserting a model into an already-running world,
rather than baking it into the world file. You can spawn from the CLI or,
in this project, from a ROS 2 launch file using `ros_gz_sim`'s `create`
helper. This is how the robot and individual soup cans get dropped into
the aisle at run time.

### The `ros_gz_bridge`

As introduced above, the **`ros_gz_bridge`** is the translator that maps
Gazebo topics to ROS 2 topics and back. You give it a list of
mappings — each says "this Gazebo topic, with this Gazebo message type,
corresponds to this ROS 2 topic, with this ROS 2 message type, flowing
in this direction." We will write a real one in sections 4 and 5.

---

## 3. Hello world example with code

### Launch an empty world

The simplest possible run. Gazebo ships a stock world called `empty`
(ground plane + sun + nothing else):

```bash
# Launch the built-in empty world with the GUI window.
# -r means "run immediately" (don't start paused).
gz sim -r empty.sdf
```

You get a window with a grey floor and a light. Press the play/pause
controls at the bottom to step physics. Close the window to quit.

### A tiny SDF world with a ground plus one shape

Now write your own world: the ground, a sun, and a single box that
falls under gravity. Save this as `hello.sdf`:

```xml
<?xml version="1.0" ?>
<!-- SDF version 1.10 ships with Gazebo Harmonic. -->
<sdf version="1.10">
  <world name="hello_world">

    <!-- The physics system: how often to step, which engine.
         max_step_size is the simulated seconds per physics tick. -->
    <physics name="default" type="dart">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
    </physics>

    <!-- Core simulation systems. Without Physics, nothing moves;
         without SceneBroadcaster/UserCommands the GUI can't show or
         edit the scene. These are the standard four. -->
    <plugin filename="gz-sim-physics-system"
            name="gz::sim::systems::Physics"/>
    <plugin filename="gz-sim-user-commands-system"
            name="gz::sim::systems::UserCommands"/>
    <plugin filename="gz-sim-scene-broadcaster-system"
            name="gz::sim::systems::SceneBroadcaster"/>

    <!-- A directional light, i.e. the sun. -->
    <light type="directional" name="sun">
      <direction>-0.5 0.1 -0.9</direction>
      <diffuse>1 1 1 1</diffuse>
      <cast_shadows>true</cast_shadows>
    </light>

    <!-- The ground: a flat, infinite, immovable plane.
         'static' means physics never moves it. -->
    <model name="ground_plane">
      <static>true</static>
      <link name="link">
        <!-- collision = the shape physics uses for contact -->
        <collision name="collision">
          <geometry><plane><normal>0 0 1</normal></plane></geometry>
        </collision>
        <!-- visual = the shape you see (can differ from collision) -->
        <visual name="visual">
          <geometry><plane>
            <normal>0 0 1</normal><size>20 20</size>
          </plane></geometry>
        </visual>
      </link>
    </model>

    <!-- One box, 0.2 m on a side, dropped 1 m above the floor so you
         can watch it fall and land. -->
    <model name="falling_box">
      <pose>0 0 1.0 0 0 0</pose>   <!-- x y z roll pitch yaw -->
      <link name="link">
        <inertial><mass>1.0</mass></inertial>
        <collision name="collision">
          <geometry><box><size>0.2 0.2 0.2</size></box></geometry>
        </collision>
        <visual name="visual">
          <geometry><box><size>0.2 0.2 0.2</size></box></geometry>
        </visual>
      </link>
    </model>

  </world>
</sdf>
```

A few things to read off the file: `<pose>` is six numbers —
position `x y z` in metres, then orientation `roll pitch yaw` in
radians. `<collision>` is the shape the physics engine uses for
contact; `<visual>` is the shape you see. They are separate so you can
draw a detailed mesh but collide against a cheap box. `<static>true`
pins the ground in place.

Run it:

```bash
gz sim -r hello.sdf
```

The box falls and lands on the ground. That is a complete simulation.

### Echo a topic with `gz topic`

While the simulation runs, open a second terminal and inspect its
message channels:

```bash
gz topic -l                       # list topics; you'll see /clock, /stats
gz topic -e -t /clock             # stream the simulation clock
```

You will watch the simulated time tick upward — proof that the world is
live and publishing.

---

## 4. A bit advanced example with code

Now we add **sensors** and connect them to ROS 2. The goal: an SDF
model carrying an **RGB-D camera** and a **2D lidar**, with a
`ros_gz_bridge` so the data appears on normal ROS 2 topics that Nav2 and
the perception layer can read.

### A sensor post model

Save this as `sensor_post.sdf`. It is a small static tower holding both
sensors, dropped into a world. (In the next section the same sensors
live on the real robot; here we isolate them to learn the pattern.)

```xml
<?xml version="1.0" ?>
<sdf version="1.10">
  <model name="sensor_post">
    <static>true</static>

    <link name="post_link">
      <pose>0 0 0.5 0 0 0</pose>
      <visual name="visual">
        <geometry><box><size>0.1 0.1 1.0</size></box></geometry>
      </visual>
      <collision name="collision">
        <geometry><box><size>0.1 0.1 1.0</size></box></geometry>
      </collision>

      <!-- ===== RGB-D (depth) camera sensor ===== -->
      <!-- type 'rgbd_camera' gives color image + depth + point cloud -->
      <sensor name="wrist_camera" type="rgbd_camera">
        <pose>0.05 0 0.45 0 0 0</pose>  <!-- pointing +x -->
        <update_rate>15</update_rate>    <!-- frames per second -->
        <topic>wrist_camera</topic>      <!-- base Gazebo topic name -->
        <camera>
          <horizontal_fov>1.05</horizontal_fov>  <!-- ~60 degrees -->
          <image><width>640</width><height>480</height></image>
          <clip><near>0.1</near><far>10.0</far></clip>  <!-- depth range -->
        </camera>
      </sensor>

      <!-- ===== 2D lidar (laser scanner) sensor ===== -->
      <sensor name="base_lidar" type="gpu_lidar">
        <pose>0 0 0.2 0 0 0</pose>
        <update_rate>10</update_rate>
        <topic>scan</topic>
        <lidar>
          <scan>
            <horizontal>
              <samples>360</samples>        <!-- one reading per degree -->
              <resolution>1</resolution>
              <min_angle>-3.14159</min_angle>
              <max_angle>3.14159</max_angle> <!-- full 360-degree sweep -->
            </horizontal>
          </scan>
          <range>
            <min>0.12</min><max>12.0</max>   <!-- metres -->
          </range>
        </lidar>
      </sensor>
    </link>
  </model>
</sdf>
```

For these sensors to actually render and publish, the *world* must load
the sensor systems. Add these world-level plugins (alongside the four
from section 3):

```xml
<!-- Makes camera/lidar sensors produce data. -->
<plugin filename="gz-sim-sensors-system"
        name="gz::sim::systems::Sensors">
  <render_engine>ogre2</render_engine>
</plugin>
```

Spawn the post into a running empty world from the CLI:

```bash
# Start an empty world with the sensors system loaded, then spawn:
gz sim -r empty.sdf &
gz service -s /world/empty/create \
  --reqtype gz.msgs.EntityFactory \
  --reptype gz.msgs.Boolean --timeout 2000 \
  --req 'sdf_filename: "sensor_post.sdf", name: "sensor_post"'
```

Confirm the Gazebo-side topics exist:

```bash
gz topic -l | grep -E "wrist_camera|scan"
# expect: /wrist_camera/image, /wrist_camera/depth_image,
#         /wrist_camera/points, /scan
```

### Bridge the sensors to ROS 2

The data is now flowing inside Gazebo, but ROS 2 cannot see it yet. The
**`ros_gz_bridge`** translates it. The cleanest way is a YAML config
listing each mapping. Save as `bridge.yaml`:

```yaml
# Each entry maps one Gazebo topic to one ROS 2 topic.
# direction GZ_TO_ROS = sensor data flowing out of the simulator.

- ros_topic_name: "/wrist_camera/color/image_raw"
  gz_topic_name: "/wrist_camera/image"
  ros_type_name: "sensor_msgs/msg/Image"
  gz_type_name: "gz.msgs.Image"
  direction: GZ_TO_ROS

- ros_topic_name: "/wrist_camera/depth/points"   # the point cloud
  gz_topic_name: "/wrist_camera/points"
  ros_type_name: "sensor_msgs/msg/PointCloud2"
  gz_type_name: "gz.msgs.PointCloudPacked"
  direction: GZ_TO_ROS

- ros_topic_name: "/scan"                          # the 2D lidar
  gz_topic_name: "/scan"
  ros_type_name: "sensor_msgs/msg/LaserScan"
  gz_type_name: "gz.msgs.LaserScan"
  direction: GZ_TO_ROS

- ros_topic_name: "/clock"                         # sim time into ROS 2
  gz_topic_name: "/clock"
  ros_type_name: "rosgraph_msgs/msg/Clock"
  gz_type_name: "gz.msgs.Clock"
  direction: GZ_TO_ROS
```

Run the bridge:

```bash
ros2 run ros_gz_bridge parameter_bridge \
  --ros-args -p config_file:=bridge.yaml
```

### Verify from the ROS 2 side

In another terminal, the sensor data is now ordinary ROS 2:

```bash
ros2 topic list                       # see /scan, /wrist_camera/..., /clock
ros2 topic echo /scan --once          # one LaserScan message
ros2 topic hz /wrist_camera/depth/points   # publishing rate of the cloud
```

If `ros2 topic echo /scan` prints an array of `ranges`, the loop is
closed: a simulated laser → Gazebo Transport → the bridge → a ROS 2
topic your navigation code subscribes to. That is the entire trick of
simulation-first development.

---

## 5. Explanation of the place-on-shelf code

Now we assemble the real setup for this project: a world holding the
aisle, the shelf, and the loading tray; the **mobile manipulator** (a
wheeled base plus a 6-jointed arm with a parallel-jaw gripper) loaded
from URDF; the wrist RGB-D camera and base 2D lidar; and the bridge that
wires the sensors *and* the drive command to ROS 2 so Nav2 (navigation)
and MoveIt 2 (arm planning) can drive it. A "parallel-jaw gripper" is a
two-fingered hand that pinches an object between flat jaws.

### The world: aisle, shelf, tray

Save as `grocery_aisle.sdf`. Each block is annotated.

```xml
<?xml version="1.0" ?>
<sdf version="1.10">
  <world name="grocery_aisle">

    <!-- DART physics; standard sim systems plus the Sensors system so
         the robot's camera and lidar render. -->
    <physics name="default" type="dart">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
    </physics>
    <plugin filename="gz-sim-physics-system"
            name="gz::sim::systems::Physics"/>
    <plugin filename="gz-sim-user-commands-system"
            name="gz::sim::systems::UserCommands"/>
    <plugin filename="gz-sim-scene-broadcaster-system"
            name="gz::sim::systems::SceneBroadcaster"/>
    <plugin filename="gz-sim-sensors-system"
            name="gz::sim::systems::Sensors">
      <render_engine>ogre2</render_engine>
    </plugin>

    <light type="directional" name="sun">
      <direction>-0.3 0.2 -0.9</direction>
      <diffuse>1 1 1 1</diffuse>
      <cast_shadows>true</cast_shadows>
    </light>

    <!-- The floor of the aisle: flat and immovable. -->
    <model name="ground_plane">
      <static>true</static>
      <link name="link">
        <collision name="c">
          <geometry><plane><normal>0 0 1</normal></plane></geometry>
        </collision>
        <visual name="v">
          <geometry><plane>
            <normal>0 0 1</normal><size>30 30</size>
          </plane></geometry>
        </visual>
      </link>
    </model>

    <!-- The shelving unit, modelled as a static block with one open
         shelf surface at ~0.9 m. Real grocery shelving is taller and
         multi-tier; v1 needs one reachable slot row. Pose places it
         2 m down the aisle in front of where the robot starts. -->
    <model name="shelf_unit">
      <static>true</static>
      <pose>2.0 0 0 0 0 0</pose>
      <link name="shelf_link">
        <!-- the shelf back panel -->
        <collision name="back">
          <pose>0.2 0 0.9 0 0 0</pose>
          <geometry><box><size>0.05 1.2 1.8</size></box></geometry>
        </collision>
        <visual name="back_v">
          <pose>0.2 0 0.9 0 0 0</pose>
          <geometry><box><size>0.05 1.2 1.8</size></box></geometry>
        </visual>
        <!-- the open shelf surface the cans are placed on -->
        <collision name="surface">
          <pose>0 0 0.9 0 0 0</pose>
          <geometry><box><size>0.4 1.2 0.03</size></box></geometry>
        </collision>
        <visual name="surface_v">
          <pose>0 0 0.9 0 0 0</pose>
          <geometry><box><size>0.4 1.2 0.03</size></box></geometry>
        </visual>
      </link>
    </model>

    <!-- The loading tray: a low rim that holds soup cans in a known
         layout, sitting where a human would have placed it. In v1 the
         can positions are fixed and known, so the first pick needs no
         vision. -->
    <model name="loading_tray">
      <static>true</static>
      <pose>0.4 0 0.4 0 0 0</pose>
      <link name="tray_link">
        <collision name="c">
          <geometry><box><size>0.4 0.6 0.02</size></box></geometry>
        </collision>
        <visual name="v">
          <geometry><box><size>0.4 0.6 0.02</size></box></geometry>
        </visual>
      </link>
    </model>

    <!-- One soup can: the SKU 'soup_can_400g'. A rigid cylinder, 0.4 kg,
         ~6.5 cm wide, ~11 cm tall. Sits on the tray. NOT static, so the
         arm can pick it up. Friction lets the gripper hold it. -->
    <model name="soup_can_400g">
      <pose>0.4 0 0.46 0 0 0</pose>
      <link name="link">
        <inertial><mass>0.4</mass></inertial>
        <collision name="c">
          <geometry><cylinder>
            <radius>0.033</radius><length>0.11</length>
          </cylinder></geometry>
          <surface><friction><ode>
            <mu>1.0</mu><mu2>1.0</mu2>   <!-- grip friction -->
          </ode></friction></surface>
        </collision>
        <visual name="v">
          <geometry><cylinder>
            <radius>0.033</radius><length>0.11</length>
          </cylinder></geometry>
        </visual>
      </link>
    </model>

  </world>
</sdf>
```

Reading it top to bottom: the **physics + four systems** make the world
live and able to render sensors; the **sun** lights it; the
**ground_plane** is the floor; the **shelf_unit** is a static block with
a back panel and one open surface at 0.9 m (the height the arm must
reach); the **loading_tray** holds product where a human set it down;
and **soup_can_400g** is the actual SKU — a non-static rigid cylinder
with mass and friction so the gripper can grasp it and so it sits still
once placed. The can's pose comes from the **planogram**, a small static
file mapping each shelf slot to an SKU, the slot's origin pose, how many
"facings" (side-by-side copies) fit, and their spacing. The world does
not contain the planogram; the orchestration layer reads it to decide
*where* each can goes and spawns or moves cans accordingly.

### The robot and its sensors

The robot itself lives in a **URDF** file (shared with MoveIt 2). It is
the kinematic tree referenced throughout the project:

```
map → odom → base_link → arm_base_link → ... → wrist_camera_link
                                          └→ tool0  (gripper tip)
```

Read this as a chain of coordinate frames. A **frame** is a labelled set
of axes attached to one part of the robot; **tf2** is the ROS 2 system
that tracks how each frame relates to its parent over time. `map` is the
fixed world; `odom` drifts with wheel odometry; `base_link` is the body;
`arm_base_link` is where the arm bolts on; `wrist_camera_link` is the
camera's viewpoint; and `tool0` is the gripper tip that must reach the
slot. We do not reprint the full URDF here — it is a standard mobile-base
+ 6-DoF-arm description — but it carries three Gazebo additions:

```xml
<!-- Inside the robot's URDF, as <gazebo> extensions -->

<!-- Differential drive: turns ROS 2 /cmd_vel into wheel motion and
     publishes /odom and the odom->base_link transform. -->
<gazebo>
  <plugin filename="gz-sim-diff-drive-system"
          name="gz::sim::systems::DiffDrive">
    <left_joint>left_wheel_joint</left_joint>
    <right_joint>right_wheel_joint</right_joint>
    <wheel_separation>0.4</wheel_separation>
    <wheel_radius>0.1</wheel_radius>
    <topic>cmd_vel</topic>            <!-- listens here -->
    <odom_topic>odom</odom_topic>     <!-- publishes here -->
    <tf_topic>tf</tf_topic>
  </plugin>
</gazebo>

<!-- Publishes every joint angle so MoveIt 2 knows the arm's pose. -->
<gazebo>
  <plugin filename="gz-sim-joint-state-publisher-system"
          name="gz::sim::systems::JointStatePublisher"/>
</gazebo>

<!-- The wrist RGB-D camera, attached to the wrist_camera_link. -->
<gazebo reference="wrist_camera_link">
  <sensor name="wrist_camera" type="rgbd_camera">
    <update_rate>15</update_rate>
    <topic>wrist_camera</topic>
    <camera>
      <horizontal_fov>1.05</horizontal_fov>
      <image><width>640</width><height>480</height></image>
      <clip><near>0.1</near><far>5.0</far></clip>
    </camera>
  </sensor>
</gazebo>

<!-- The 2D lidar on the base, attached to a base_scan link. -->
<gazebo reference="base_scan_link">
  <sensor name="base_lidar" type="gpu_lidar">
    <update_rate>10</update_rate>
    <topic>scan</topic>
    <lidar>
      <scan><horizontal>
        <samples>360</samples><resolution>1</resolution>
        <min_angle>-3.14159</min_angle><max_angle>3.14159</max_angle>
      </horizontal></scan>
      <range><min>0.12</min><max>12.0</max></range>
    </lidar>
  </sensor>
</gazebo>
```

The **DiffDrive** plugin is the steering wheel: it subscribes to a
velocity command and reports back where the base has moved. The
**JointStatePublisher** tells the arm planner the current angle of every
joint. The two **sensor** blocks are the same camera and lidar from
section 4, now bolted to the robot's own frames.

### The bridge that wires sim to ROS 2

This is the contract between the simulator and the rest of the stack.
Save as `shelf_bridge.yaml`:

```yaml
# --- Sensor data: simulator -> ROS 2 (perception + navigation read it) ---

- ros_topic_name: "/wrist_camera/color/image_raw"
  gz_topic_name: "/wrist_camera/image"
  ros_type_name: "sensor_msgs/msg/Image"
  gz_type_name: "gz.msgs.Image"
  direction: GZ_TO_ROS

- ros_topic_name: "/wrist_camera/depth/points"
  gz_topic_name: "/wrist_camera/points"
  ros_type_name: "sensor_msgs/msg/PointCloud2"
  gz_type_name: "gz.msgs.PointCloudPacked"
  direction: GZ_TO_ROS

- ros_topic_name: "/scan"
  gz_topic_name: "/scan"
  ros_type_name: "sensor_msgs/msg/LaserScan"
  gz_type_name: "gz.msgs.LaserScan"
  direction: GZ_TO_ROS

- ros_topic_name: "/odom"
  gz_topic_name: "/odom"
  ros_type_name: "nav_msgs/msg/Odometry"
  gz_type_name: "gz.msgs.Odometry"
  direction: GZ_TO_ROS

- ros_topic_name: "/joint_states"
  gz_topic_name: "/joint_states"
  ros_type_name: "sensor_msgs/msg/JointState"
  gz_type_name: "gz.msgs.Model"
  direction: GZ_TO_ROS

- ros_topic_name: "/clock"
  gz_topic_name: "/clock"
  ros_type_name: "rosgraph_msgs/msg/Clock"
  gz_type_name: "gz.msgs.Clock"
  direction: GZ_TO_ROS

# --- Commands: ROS 2 -> simulator (Nav2 drives the base) ---

- ros_topic_name: "/cmd_vel"
  gz_topic_name: "/cmd_vel"
  ros_type_name: "geometry_msgs/msg/Twist"
  gz_type_name: "gz.msgs.Twist"
  direction: ROS_TO_GZ
```

Notice the **directions**. Everything a real robot's sensors would
*produce* — camera, point cloud, laser, odometry, joint angles, clock —
flows `GZ_TO_ROS`, *out* of the simulator into ROS 2. The one command,
`/cmd_vel` (a `Twist`, meaning a linear + angular velocity for the
base), flows `ROS_TO_GZ`, from Nav2 *into* the simulator to move the
wheels. MoveIt 2's arm commands reach the simulated joints through a
controller interface set up separately; the lines above are the sensor
and base-drive backbone.

### Bringing it up with a launch file

A ROS 2 launch file starts the world, spawns the robot, and runs the
bridge together. Save as `shelf_sim.launch.py`:

```python
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    pkg_ros_gz = get_package_share_directory("ros_gz_sim")

    # 1. Start Gazebo Harmonic with our aisle world (-r = run now).
    gz = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz, "launch", "gz_sim.launch.py")),
        launch_arguments={"gz_args": "-r grocery_aisle.sdf"}.items(),
    )

    # 2. Spawn the mobile manipulator from its URDF into the world,
    #    one metre back from the shelf, facing it.
    spawn_robot = Node(
        package="ros_gz_sim", executable="create",
        arguments=[
            "-name", "stock_bot",
            "-file", "stock_bot.urdf",
            "-x", "0.0", "-y", "0.0", "-z", "0.05", "-Y", "0.0",
        ],
        output="screen",
    )

    # 3. Start the bridge so sim sensors and /cmd_vel reach ROS 2.
    bridge = Node(
        package="ros_gz_bridge", executable="parameter_bridge",
        arguments=["--ros-args", "-p",
                   "config_file:=shelf_bridge.yaml"],
        output="screen",
    )

    return LaunchDescription([gz, spawn_robot, bridge])
```

Launch and verify:

```bash
ros2 launch shelf_sim.launch.py

# In another terminal, confirm the full interface is live:
ros2 topic list
# /wrist_camera/color/image_raw   /wrist_camera/depth/points
# /scan   /odom   /joint_states   /cmd_vel   /clock

ros2 topic echo /scan --once          # the base sees the shelf/walls
ros2 topic echo /odom --once          # the base reports its pose

# Nudge the base forward to prove /cmd_vel reaches the wheels:
ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.1}, angular: {z: 0.0}}"
```

If the robot rolls forward in the GUI and `/scan` shows the shelf
getting closer, the simulation layer is complete: a virtual grocery
aisle, a robot with the project's exact sensors, and a ROS 2 interface
identical to the one the real hardware will expose. From here, Nav2
subscribes to `/scan` and `/odom` and publishes `/cmd_vel` to drive to
the shelf; MoveIt 2 reads `/joint_states` and the camera's
`/wrist_camera/depth/points` to plan the pick and place. None of that
code knows or cares that the world behind the topics is simulated.

---

## Where this fits / next

The simulator is the bottom of the stack — the practice world every
other layer acts on. With Gazebo Harmonic standing up the aisle, the
robot, and the sensors, the next thing to learn is the **middleware**
that ties all the software together and carries every topic you saw
above: **ROS 2**. Continue with [`02-ros2.md`](02-ros2.md) in this same
folder. Later in the project, once the mechanics work here, the
perception half moves to the photorealistic **Isaac Sim** — but that is
a separate, GPU-heavy step, and everything in *this* document runs on a
plain laptop.
