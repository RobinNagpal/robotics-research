# Phase 2 — Robot model, sensors & control

> **Goal:** describe the mobile manipulator as one kinematic tree, spawn
> it into the store world, expose its sensors over ROS 2, and drive its
> joints through `ros2_control`. This is the URDF/USD "mobile
> manipulator" the requirements call for (`../01-requirements.md` §4,
> `../03-high-level-tech.md` §2).
>
> **Checkpoint:** robot spawns; you can teleop the base, command the arm,
> and see lidar scan + RGB-D cloud + wheel odometry + correct tf in
> rviz2.

---

## 2.1 One kinematic tree (base + arm + gripper + camera)

`shelf_description/urdf/robot.urdf.xacro` — a single Xacro-built URDF so
base and arm are reasoned about together (the whole-body reach problem):

- **Mobile base:** differential-drive, two drive wheels + casters, a
  payload deck for the tray. Frame `base_link`, with `odom`→`base_link`
  produced by the controller.
- **Arm:** a 5–6 DoF manipulator mounted on the deck. Use a real model
  (e.g. a low-cost collaborative arm class) with **realistic joint
  limits, link masses, and inertias** — these drive both planning and
  the sim-to-real gap, so don't fake them.
- **Gripper:** a simple parallel-jaw (or a suction tool) sized to the
  SKU.
- **Wrist camera frame:** an RGB-D camera link rigidly attached near the
  gripper (eye-in-hand), with its optical frame correctly oriented.
- **Tray mount:** attach the tray model from Phase 1 at a known fixed
  pose on the deck.

Split the Xacro into `base.xacro`, `arm.xacro`, `gripper.xacro`,
`sensors.xacro` for sanity.

## 2.2 Gazebo + ros2_control wiring

Two plugin layers live in the URDF:

- **`gz_ros2_control`** system plugin (the `<gazebo>` + `<ros2_control>`
  blocks) so ROS 2 controllers drive the simulated joints. Point it at a
  controllers YAML in `shelf_bringup/config/controllers.yaml`.
- **Controllers** to spawn:
  - `diff_drive_controller` for the base (subscribes `/cmd_vel`,
    publishes `/odom` + tf).
  - `joint_trajectory_controller` for the arm (this is what MoveIt 2
    commands in Phase 4).
  - a gripper controller (`position` or
    `parallel_gripper`/`gripper_action`).
  - `joint_state_broadcaster` (publishes `/joint_states` for tf).

> Use `gz_ros2_control` rather than Gazebo's standalone DiffDrive plugin
> — it gives the same `ros2_control` interface MoveIt and hardware use,
> keeping sim↔real parity.

## 2.3 Sensors

Modeled in `sensors.xacro` as `gz-sim` sensors, then **bridged**:

| Sensor | gz sensor | ROS 2 topic | Bridge |
|--------|-----------|-------------|--------|
| 2D lidar | `gpu_lidar` | `/scan` (`LaserScan`) | `ros_gz_bridge` |
| Wheel odometry | from `diff_drive_controller` | `/odom` (`Odometry`) | native (controller) |
| Wrist RGB-D | `rgbd_camera` | `/wrist_camera/image`, `/depth`, `/points` | `ros_gz_image` + bridge |
| IMU (optional) | `imu` | `/imu` | `ros_gz_bridge` |

Add each new topic to the single `bridge.yaml` from Phase 0. Verify the
**camera optical frame** and **lidar frame** are correct in tf2 — a
flipped optical frame is the #1 cause of "the point cloud is sideways."

## 2.4 Spawn & teleop

- Extend the launch file: load the URDF to `robot_state_publisher`, spawn
  the robot into `store_aisle.sdf` via `ros_gz_sim create`, start the
  controllers.
- Drive the base with `teleop_twist_keyboard` on `/cmd_vel`.
- Nudge the arm with a test trajectory or `rqt_joint_trajectory_controller`.

## 2.5 Verify in rviz2

Load a config showing: `RobotModel`, `TF`, `LaserScan` (`/scan`),
`PointCloud2` (`/points`), `Image` (`/wrist_camera/image`), `Odometry`
(`/odom`). Everything should be consistent and move with the robot.

## Deliverables

- `robot.urdf.xacro` mobile manipulator with realistic limits/masses.
- `controllers.yaml` + spawned diff-drive, arm, gripper, joint-state
  controllers.
- All sensors bridged and visible in rviz2 with correct tf.

## Checkpoint

Teleop drives the base around the aisle; the arm moves on command; lidar,
depth cloud, camera, and odom all render correctly in rviz2. The robot is
real (in sim) — move to Phase 3 (navigation).
