# Simulation plan — Gazebo Harmonic build

> A full, phased plan for standing up the shelf-stocking robot in
> **Gazebo Harmonic** and proving the pick-drive-place loop end to end
> in simulation. This is the **first build stage** from the recommended
> path in `../03-high-level-tech.md` §7: get the *mechanics* working in
> the open, ROS-native, CPU-friendly simulator before moving the
> *perception* half to Isaac Sim later.
>
> New to a term? See `../02-glossary.md`. The technology choices here
> are justified in `../03-stack/` (one file per layer).

---

## Why Gazebo Harmonic for stage 1

Gazebo Harmonic (the `gz-sim` line, LTS, pairs with ROS 2 Jazzy on
Ubuntu 24.04) is the cheapest, most ROS-native way to prove the loop:

- **Open and free**, runs on a plain CPU laptop — no RTX GPU needed
  (see `../03-stack/01-simulator.md`).
- **First-class ROS 2 bridge** (`ros_gz`) so every node we write here is
  the *same* node that later runs on hardware and in Isaac Sim — the
  transfer is a driver swap, not a rewrite (`../03-stack/02-middleware.md`).
- **Native Nav2 + MoveIt 2 integration**, which are the two layers the
  robot cannot do without (`../03-stack/03-mobile-base-navigation.md`,
  `../03-stack/04-arm-motion-planning.md`).

What Gazebo is *weak* at — photorealistic rendering and domain
randomization — is exactly the part we **defer to Isaac Sim**. In stage 1
perception is geometric / known-pose (the v1 framing in
`../01-requirements.md`), so Gazebo's moderate rendering is fine.

## What we are building

The smallest scene that exercises the whole loop from
`../01-requirements.md`:

- a **single aisle** with one shelving unit (standard grocery
  dimensions), flat floor, uniform lighting;
- one **rigid SKU** (e.g. a 400 g can) as a physics body, presented in a
  **known tray layout** on the robot;
- a **mobile manipulator** — differential-drive base + 5–6 DoF arm +
  simple gripper — with a 2D lidar, wheel odometry, and a wrist RGB-D
  camera;
- the full **drive → pick → locate slot → place → verify → repeat** loop,
  driven by a Behavior Tree, with a per-unit success/failure log.

## Target software versions

Approximate and worth re-checking before you start (versions drift):

| Component | Pin | Notes |
|-----------|-----|-------|
| OS | Ubuntu 24.04 LTS | Jazzy's tier-1 platform |
| ROS 2 | **Jazzy Jalisco** | or Humble 22.04 + Gazebo Harmonic via the non-default pairing |
| Simulator | **Gazebo Harmonic** (`gz-sim` 8) | `gz sim` CLI, SDF worlds |
| Bridge | `ros_gz` (Harmonic branch) | `ros_gz_bridge`, `ros_gz_image`, `ros_gz_sim` |
| Control | `gz_ros2_control` + `ros2_control` | base + arm controllers |
| Navigation | Nav2 + `slam_toolbox` (AMCL for runs) | |
| Arm motion | MoveIt 2 | config via Setup Assistant |
| Orchestration | BehaviorTree.CPP (+ Groot2) | `../03-stack/07-orchestration.md` |

## Phase roadmap

Each phase is a milestone with a concrete deliverable and a checkpoint
you can demo before moving on. Read them in order.

| # | File | Milestone | Checkpoint (done when…) |
|---|------|-----------|--------------------------|
| 0 | `01-setup-and-workspace.md` | Toolchain + ROS 2 workspace + package skeleton | `gz sim` launches an empty world from a ROS 2 launch file |
| 1 | `02-world-and-assets.md` | The store world + shelf / SKU / tray models | Aisle, shelf, and a can load and sit stably under gravity |
| 2 | `03-robot-model-and-sensors.md` | Mobile-manipulator model + sensors + `ros2_control` | Robot spawns; you can teleop the base and see lidar + RGB-D + odom in rviz2 |
| 3 | `04-navigation.md` | SLAM map + Nav2 driving to the picking pose | Robot autonomously drives to a stable pose in front of the shelf |
| 4 | `05-manipulation.md` | MoveIt 2 pick from the known tray pose + grasp in sim + geometric place | Arm picks a can and sets it on the shelf, collision-free |
| 5 | `06-integration-and-metrics.md` | Behavior-Tree loop + perception inputs + logging + randomization | Full autonomous run stocks the row; per-unit success log produced |

## Definition of done (this stage)

Mirrors `../01-requirements.md` §9, scoped to Gazebo:

- Load the robot with a tray of one SKU and issue a one-slot job.
- The robot autonomously drives to the shelf and places **every** unit
  into the correct slot, upright, without collisions.
- A log shows per-unit success rate over repeated runs with **randomized
  start poses and small tray-position perturbations** (Gazebo-level
  randomization; full visual DR waits for Isaac Sim).
- Every node talks ROS 2 over the same interfaces hardware will use.

When that runs reliably, stage 2 (Isaac Sim, photoreal + learned
perception) becomes a swap of the simulator under the same nodes.

## Key risks & gotchas (read before you start)

- **Grasping in Gazebo is the hard part.** Rigid-body friction grasping
  is unreliable; the pragmatic fix is a **`DetachableJoint`** attached on
  a gripper contact event and detached on release. Covered in
  `05-manipulation.md`. Don't burn days fighting contact friction.
- **`ros_gz` topic typing.** The bridge needs explicit type mappings;
  mismatched QoS or types are the most common "nothing is publishing"
  bug. Keep a single bridge config (`02-` / `03-` phases).
- **Sim time everywhere.** Run every node with `use_sim_time:=true` or
  tf and Nav2 will fight the clock.
- **Coordinate frames.** Get `base_link`, `odom`, `map`, and the camera
  frame right in tf2 early (`03-` phase) — most downstream bugs are
  frame bugs.
- **Keep it v1-simple.** Known tray poses, one SKU, static aisle,
  safe-stop (not re-plan). Resist adding scope (`../01-requirements.md`
  §8).
