# Glossary — terms used in the tech doc

> Read this first. `03-high-level-tech.md` and the `03-stack/` deep-dives
> use a lot of robotics and computer-vision shorthand. Every term is
> explained here in 1-2 plain sentences, grouped in the same order the
> tech doc introduces them. You don't need to memorize these — skim once,
> then refer back.

---

## Project-wide ideas

- **ROS 2 (Robot Operating System 2).** Despite the name it is not an
  operating system; it is the open-source framework that lets a robot's
  separate software pieces (vision, navigation, arm control) run as
  small programs and talk to each other over a shared messaging system.
- **ROS-native.** Describes a tool that was built to work inside the ROS
  ecosystem out of the box, so it plugs in without custom glue code.
- **Middleware.** The connective software layer that every other part
  plugs into so they can communicate — here, that is ROS 2.
- **Simulation-first.** A build approach where all the early work is done
  in a virtual copy of the world before touching real hardware, because
  it is faster, cheaper, and safe to fail in.
- **Mobile manipulator.** A robot that combines a driving base (wheels)
  with a robotic arm, so it can both move around and pick things up —
  exactly what a shelf-stocking robot is.
- **SKU (Stock Keeping Unit).** Retail term for one specific product
  type/variant (one brand and size of soup can); "one SKU per run" means
  the robot handles a single product type at a time.

---

## Simulation

- **Physics engine.** The part of a simulator that computes how things
  move, fall, collide, and rub together, so virtual objects behave like
  real ones.
- **Rigid body.** An object that does not bend or squish (a can, a box) —
  the easiest kind of object for a physics engine to model, unlike a bag
  or cloth.
- **Mass and friction.** An object's weight and how much its surfaces
  resist sliding; both must be realistic or grasping and placing will
  behave wrongly.
- **Contact physics.** The simulation of what happens when surfaces touch
  — friction, grip, pushing — which decides whether a virtual grasp or
  set-down matches reality.
- **Photorealism / photorealistic.** How closely the simulator's rendered
  images look like real camera photos; it matters because the vision
  model learns from those images.
- **Assets.** The ready-made 3D models (shelves, products, robot parts)
  you drop into a simulated scene.
- **NVIDIA Isaac Sim.** A high-end, photorealistic robot simulator from
  NVIDIA; strong for vision and mobile-manipulation work but needs a
  powerful NVIDIA graphics card.
- **Isaac Lab.** An add-on to Isaac Sim focused on training robot skills
  with machine learning (reinforcement learning).
- **Gazebo (Harmonic).** A free, open-source simulator that integrates
  tightly with ROS; lighter and cheaper than Isaac Sim but less
  photorealistic. "Harmonic" is a recent version name.
- **MuJoCo.** A free simulator famous for fast, accurate contact physics;
  great for tuning grasp/place motions in isolation, less suited to a
  whole navigable store.
- **Genesis.** A newer (2024) fast, GPU-based simulator; promising but
  with a young, still-maturing ecosystem.
- **USD (Universal Scene Description).** A 3D scene file format (created
  by Pixar, used heavily by NVIDIA) for describing and assembling virtual
  worlds; "USD-based scene composition" means you build the simulated
  store by snapping together USD pieces.
- **SimReady assets.** 3D models prepared with realistic physics and
  materials so they can be dropped straight into a simulation.
- **CAD (Computer-Aided Design) model.** A precise 3D engineering model
  of an object; used both to build simulated products and to tell the
  robot a product's exact shape.
- **Replicator.** Isaac Sim's tool for domain randomization: it
  automatically generates many varied versions of a scene to train robust
  vision.
- **Domain randomization.** Deliberately varying a simulation's look and
  conditions (lighting, colors, object positions) so a vision model
  learns the general task instead of memorizing one perfect scene.
- **Overfit.** When a model learns its training examples too literally and
  then fails on anything slightly different; randomization is the cure.
- **Sim-to-real gap.** The mismatch between simulation and the real world
  that can make a sim-trained robot fail on real hardware; realistic
  physics and randomization exist to shrink it.
- **Reinforcement learning (RL) / learned policy.** A machine-learning
  approach where the robot learns a skill by trial and error in
  simulation; the result is a "policy," a learned controller. Optional
  for this project.
- **ROS 2 bridge.** A connector that lets a simulator exchange messages
  with ROS 2, so the same robot software can drive the simulated robot.

---

## The robot model

- **URDF (Unified Robot Description Format).** A standard file describing
  a robot's physical structure — its links, joints, sizes, and limits —
  used by Gazebo and MoveIt to understand how the robot is built.
- **Kinematic tree.** The description of how a robot's parts connect
  joint-by-joint, from the base out to the gripper, so software can
  compute where each part is in space.
- **Whole-body reach.** Considering the moving base and the arm together
  when deciding whether the gripper can reach a spot, rather than planning
  them separately.
- **2D lidar.** A spinning laser sensor that measures distances in a flat
  plane around the robot, used to map a room and detect obstacles.
- **Wheel odometry.** Estimating how far and which way the robot has moved
  by counting wheel rotations; a rough position estimate that navigation
  refines using other sensors.
- **RGB-D camera.** A camera that captures a normal color image (RGB)
  plus a depth value for every pixel (D = distance), so the robot sees
  both what an object looks like and how far away it is.
- **RealSense.** Intel's popular line of RGB-D depth cameras — the typical
  sensor assumed here.
- **Joint limits / link masses.** The allowed range of each joint's
  motion and the weight of each arm segment; realistic values make
  planning and physics match the real robot.
- **Gripper.** The "hand" at the end of the arm that grabs products —
  here either a parallel-jaw (two fingers) or a suction type.

---

## Navigation (the mobile base)

- **Nav2 (Navigation 2).** The standard ROS 2 system for mobile-robot
  navigation: it maps, locates the robot, plans a route, and drives the
  base to a goal.
- **SLAM (Simultaneous Localization and Mapping).** Building a map of an
  unknown space while at the same time tracking where the robot is within
  it.
- **Pre-built map.** A map made ahead of time (e.g. once during setup)
  that the robot then reuses each run, instead of mapping live every time.
- **Localization.** Working out where the robot currently is on the map.
- **AMCL (Adaptive Monte Carlo Localization).** A specific, widely used
  localization method that matches live lidar scans against a known map to
  pin down the robot's position.
- **Global + local planning.** Global planning picks the overall route to
  the goal; local planning makes the moment-to-moment steering
  adjustments to follow it while dodging obstacles.
- **Recovery behaviors.** Pre-set actions (back up, rotate, retry) the
  robot takes when it gets stuck or confused, to get navigation unstuck.
- **Costmap.** A grid the navigation system keeps, marking which cells are
  free, occupied, or risky; used to plan safe paths and to notice
  obstacles like a shopper.
- **Picking pose / placing pose.** The exact position and orientation the
  base should stop at in front of the shelf so the arm can comfortably
  reach.
- **Vision-based alignment.** Using the camera to fine-tune the robot's
  position relative to the shelf after navigation gets it roughly in
  place.
- **Safe-stop.** Halting all motion when something unexpected (a person)
  appears, instead of trying to plan around it — the v1 safety rule.

---

## Arm motion (manipulation)

- **MoveIt 2.** The standard ROS 2 system for planning and executing arm
  movements without collisions.
- **Nav2 + MoveIt 2 integration.** Nav2 (driving) and MoveIt 2 (arm
  motion) are the two standard ROS tools this robot leans on; "integration"
  means a simulator works smoothly with both out of the box, which saves a
  large amount of setup effort — a key reason to pick one simulator over
  another.
- **Motion planning.** Computing a path for the arm's joints that moves
  the gripper from one pose to another without hitting anything.
- **Collision-free trajectory.** A planned arm movement that has been
  checked to avoid hitting the shelf, the products, or the robot itself.
- **Collision world / collision objects.** The software's model of the
  obstacles around the arm (shelf, neighboring products) that planning
  must avoid.
- **cuMotion.** NVIDIA's GPU-accelerated motion planner; a faster drop-in
  option for when planning speed becomes a bottleneck.
- **Pinocchio.** A fast software library for the math of arm kinematics
  and dynamics, usable as a building block for a custom motion planner.
- **Planning latency.** How long the software takes to compute a move; if
  it grows large it slows the whole task down.
- **Cycle time.** How long one complete pick-and-place takes, end to end.
- **Place motion.** The specific arm movement that sets a product down on
  the shelf; "tuning the place motion" means adjusting its parameters so
  the set-down is gentle and reliable.
- **Guarded / compliant set-down.** Placing the product by gently
  approaching until light contact with the shelf, then releasing —
  "compliant" means the arm yields softly on contact instead of pushing
  rigidly.
- **Free-space drop.** Releasing the object in mid-air above the target;
  avoided here because it is unreliable and can topple neighbors.

---

## Perception (vision)

- **Perception.** The robot's vision software that interprets camera data
  to find the product to pick and the shelf slot to fill.
- **6-DoF pose.** An object's full placement in space — its location
  (x, y, z) plus its orientation (roll, pitch, yaw), six "degrees of
  freedom" — everything the arm needs to grab it correctly.
- **FoundationPose.** A modern model that estimates a known object's
  6-DoF pose from an RGB-D image plus the object's 3D model, without
  needing per-object training.
- **Mesh.** A 3D model of an object's surface built from triangles; used
  as the reference shape for pose estimation.
- **Point cloud.** The set of 3D points a depth camera captures,
  representing the surfaces it sees.
- **Planar fit of the shelf face.** Mathematically fitting a flat plane to
  the shelf's front surface in the point cloud, to locate the shelf and
  decide where to place items.
- **Planogram.** A retailer's plan of which product goes where on a shelf
  and how many fit; the robot reads it to know the target slot.
- **Facing.** One front-row position for a product on a shelf; "the next
  facing" is the next slot to fill in the row.
- **Segment / segmentation.** Identifying exactly which pixels in an image
  belong to a particular object or region (e.g. the empty shelf space).
- **SAM 2 (Segment Anything Model 2).** A general-purpose model from Meta
  that can segment (cut out) almost any object in an image or video when
  given a prompt.
- **Open-vocabulary detection.** Object detection that can find things
  described by free text ("the soup cans") instead of only a fixed,
  pre-trained list of categories.
- **YOLO-World.** A fast object detector that supports open-vocabulary
  (text-prompted) detection in real time.
- **Grounding DINO.** A model that locates objects in an image from a text
  description; strong at open-vocabulary detection, often paired with
  SAM 2 to get precise masks.

---

## Grasping

- **Grasp synthesis.** Computing how to grab an object — the gripper's
  position, orientation, and (for a parallel gripper) how wide to open.
- **Analytical / antipodal grasp.** A grasp worked out by simple geometry
  rather than learning; "antipodal" means gripping an object from two
  opposite sides, like pinching a can.
- **Suction grasp.** Grabbing with a suction cup on a flat surface (good
  for box tops) instead of pinching.
- **AnyGrasp.** A learned model that proposes reliable grasps for a wide
  range of objects from an RGB-D view.
- **Contact-GraspNet.** Another widely used learned model that proposes
  6-DoF grasps from a depth point cloud, even in clutter.

---

## Orchestration (sequencing the task)

- **Orchestration.** The top-level logic that sequences the whole task and
  decides what to do at each step, and what to do on failure.
- **Behavior Tree (BT).** A popular way to organize a robot's
  decision-making as a tree of tasks checked repeatedly; it makes complex
  "do this, then that, and on failure do this" logic clear and reusable.
- **BehaviorTree.CPP.** A widely used C++ library for building Behavior
  Trees — the same engine Nav2 uses internally.
- **Nav2 BT.** The Behavior Tree engine that already runs inside Nav2,
  which you can reuse to drive the whole task.
- **Leaf / ROS 2 action.** A leaf is a single executable step at the
  bottom of a Behavior Tree; here each one is a "ROS 2 action," a request
  to another part of the system to do a job and report back (e.g.
  `PickProduct`).
- **State machine (SMACH / YASMIN).** An alternative way to sequence a
  task as a set of named states with transitions between them; SMACH (ROS
  1) and YASMIN (ROS 2) are two implementations. Simpler, but less
  reactive than a Behavior Tree.

---

## Delivery

- **Hardware pilot.** A first real-world trial on actual robot hardware,
  done only after the simulation version works reliably.
- **Drivers.** The small software pieces that connect generic robot
  software to specific physical devices (this motor, that camera);
  switching from simulation to real hardware is mostly a change of
  drivers, not a rewrite.
