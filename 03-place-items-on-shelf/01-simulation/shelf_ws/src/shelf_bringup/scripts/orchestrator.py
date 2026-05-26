#!/usr/bin/env python3
"""Autonomous shelf-stocking mission (v1).

Runs the full loop from ../../01-requirements.md §6:
  drive to the shelf -> spawn the tray of cans -> for each can:
  pick (IK + grasp) -> place into the slot -> verify -> log -> repeat.

Arm motion has two backends (env SHELF_ARM_BACKEND, set by the launch):
  * 'moveit'  - MoveIt 2 plans a collision-free path (shelf + already-placed
                cans as collision objects) to a joint goal seeded by ikpy.
  * 'direct'  - send the ikpy joint goal straight to the trajectory
                controller (no planning). Also the automatic fallback if
                MoveItPy fails to initialise.

The base drives by odometry and the grasp is a friction grasp (the known-hard
part — tune planogram gripper.grip / can friction; see ../../05-manipulation.md).
"""
import os
import re
import csv
import math
import time
import subprocess
from datetime import datetime

import numpy as np
import yaml

import rclpy
from rclpy.action import ActionClient
from rclpy.parameter import Parameter

from ament_index_python.packages import get_package_share_directory
from geometry_msgs.msg import TwistStamped, PoseStamped
from nav_msgs.msg import Odometry
from nav2_msgs.action import NavigateToPose
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration

from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink

try:
    from moveit.planning import MoveItPy
    from moveit.core.robot_state import RobotState
    from moveit_msgs.msg import CollisionObject
    from shape_msgs.msg import SolidPrimitive
    from geometry_msgs.msg import Pose
    _MOVEIT_OK = True
except Exception:  # noqa: BLE001
    _MOVEIT_OK = False

ARM_JOINTS = ['joint_pan', 'joint_lift', 'joint_elbow',
              'joint_wrist_pitch', 'joint_wrist_roll']
FINGER_JOINTS = ['left_finger_joint', 'right_finger_joint']
WORLD = 'store_aisle'
SPAWN_Z = 0.175  # base_link height when spawned


def build_chain():
    """ikpy chain matching shelf_description arm geometry (arm_base frame)."""
    return Chain(name='arm', links=[
        OriginLink(),
        URDFLink('pan', [0, 0, 0.06], [0, 0, 0], rotation=[0, 0, 1], bounds=(-3.14, 3.14)),
        URDFLink('lift', [0, 0, 0.04], [0, 0, 0], rotation=[0, 1, 0], bounds=(-3.14, 3.14)),
        URDFLink('elbow', [0, 0, 0.40], [0, 0, 0], rotation=[0, 1, 0], bounds=(-3.14, 3.14)),
        URDFLink('wrist_pitch', [0, 0, 0.35], [0, 0, 0], rotation=[0, 1, 0], bounds=(-3.14, 3.14)),
        URDFLink('wrist_roll', [0, 0, 0.10], [0, 0, 0], rotation=[0, 0, 1], bounds=(-3.14, 3.14)),
        URDFLink('tool', [0, 0, 0.11], [0, 0, 0], rotation=[0, 0, 1]),
    ], active_links_mask=[False, True, True, True, True, True, False])


class Mission:
    def __init__(self):
        # Mission node (separate from MoveItPy's 'moveit_py' node).
        self.node = rclpy.create_node(
            'shelf_mission',
            parameter_overrides=[Parameter('use_sim_time', Parameter.Type.BOOL, True)])
        self.log = self.node.get_logger()

        pkg = get_package_share_directory('shelf_bringup')
        with open(os.path.join(pkg, 'config', 'planogram.yaml')) as f:
            self.plan = yaml.safe_load(f)
        self.can_sdf = os.path.join(pkg, 'models', 'can_sku', 'model.sdf')

        self.chain = build_chain()
        self.full_angles = [0.0] * 7
        p = self.plan['picking_pose']
        self.base_x = p['x']                       # base_link world x when parked
        self.arm_base = np.array([p['x'] - 0.05, p['y'], 0.5])

        # diff_drive_controller publishes odometry under its own name.
        self.odom_x = None
        self.odom_y = 0.0
        self.odom_yaw = 0.0
        self.node.create_subscription(
            Odometry, '/diff_drive_controller/odom', self._odom, 10)
        self.cmd_pub = self.node.create_publisher(
            TwistStamped, '/diff_drive_controller/cmd_vel', 10)
        self.arm_ac = ActionClient(self.node, FollowJointTrajectory,
                                   '/arm_controller/follow_joint_trajectory')
        self.grip_ac = ActionClient(self.node, FollowJointTrajectory,
                                    '/gripper_controller/follow_joint_trajectory')
        self.nav_ac = ActionClient(self.node, NavigateToPose, '/navigate_to_pose')
        self.drive_backend = os.environ.get('SHELF_DRIVE_BACKEND', 'nav2')

        self.backend = os.environ.get('SHELF_ARM_BACKEND', 'moveit')
        self.moveit = None
        if self.backend == 'moveit':
            self._init_moveit()

        os.makedirs('/ws/logs', exist_ok=True)
        stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.log_path = f'/ws/logs/run_{stamp}.csv'
        self.results = []

    # ---------- MoveIt ----------
    def _init_moveit(self):
        if not _MOVEIT_OK:
            self.log.warn('moveit_py unavailable; using direct arm backend.')
            self.backend = 'direct'
            return
        try:
            self.moveit = MoveItPy(node_name='moveit_py')
            self.arm_group = self.moveit.get_planning_component('arm')
            self.robot_model = self.moveit.get_robot_model()
            self._collision_box('shelf_board', [0.50, 0.95, 0.04], [1.70, 0.0, 0.80])
            self._collision_box('shelf_back', [0.05, 0.95, 1.60], [1.925, 0.0, 0.80])
            self._collision_box('shelf_left', [0.50, 0.02, 1.60], [1.70, 0.475, 0.80])
            self._collision_box('shelf_right', [0.50, 0.02, 1.60], [1.70, -0.475, 0.80])
            self.log.info('MoveIt 2 arm backend ready (collision-aware planning).')
        except Exception as e:  # noqa: BLE001
            self.log.warn(f'MoveIt init failed ({e}); using direct arm backend.')
            self.backend = 'direct'
            self.moveit = None

    def _apply_co(self, co):
        psm = self.moveit.get_planning_scene_monitor()
        with psm.read_write() as scene:
            scene.apply_collision_object(co)
            scene.current_state.update()

    def _world_to_base(self, world_xyz):
        return [world_xyz[0] - self.base_x, world_xyz[1], world_xyz[2] - SPAWN_Z]

    def _collision_box(self, oid, size, world_pos):
        co = CollisionObject()
        co.id = oid
        co.header.frame_id = 'base_link'
        prim = SolidPrimitive()
        prim.type = SolidPrimitive.BOX
        prim.dimensions = [float(s) for s in size]
        pose = Pose()
        x, y, z = self._world_to_base(world_pos)
        pose.position.x, pose.position.y, pose.position.z = x, y, z
        pose.orientation.w = 1.0
        co.primitives = [prim]
        co.primitive_poses = [pose]
        co.operation = CollisionObject.ADD
        self._apply_co(co)

    def _add_placed_can(self, idx, world_pos):
        if self.backend != 'moveit' or self.moveit is None:
            return
        co = CollisionObject()
        co.id = f'placed_{idx}'
        co.header.frame_id = 'base_link'
        prim = SolidPrimitive()
        prim.type = SolidPrimitive.CYLINDER
        prim.dimensions = [0.12, 0.033]  # height, radius
        pose = Pose()
        x, y, z = self._world_to_base(world_pos)
        pose.position.x, pose.position.y, pose.position.z = x, y, z
        pose.orientation.w = 1.0
        co.primitives = [prim]
        co.primitive_poses = [pose]
        co.operation = CollisionObject.ADD
        self._apply_co(co)

    def _plan_execute(self, angles):
        try:
            rs = RobotState(self.robot_model)
            rs.set_joint_group_positions('arm', np.array(angles, dtype=float))
            rs.update()
            self.arm_group.set_start_state_to_current_state()
            self.arm_group.set_goal_state(robot_state=rs)
            result = self.arm_group.plan()
            traj = getattr(result, 'trajectory', None) if result else None
            if traj is not None:
                self.moveit.execute(traj, controllers=[])
                self._spin(0.3)
                return True
            self.log.warn('MoveIt found no plan; direct fallback for this move.')
        except Exception as e:  # noqa: BLE001
            self.log.warn(f'MoveIt plan/exec error ({e}); direct fallback.')
        return False

    # ---------- low-level helpers ----------
    def _odom(self, msg):
        p = msg.pose.pose.position
        q = msg.pose.pose.orientation
        self.odom_x = p.x
        self.odom_y = p.y
        self.odom_yaw = math.atan2(2.0 * (q.w * q.z + q.x * q.y),
                                   1.0 - 2.0 * (q.y * q.y + q.z * q.z))

    def _spin(self, secs):
        end = time.time() + secs
        while time.time() < end:
            rclpy.spin_once(self.node, timeout_sec=0.05)

    def wait_ready(self):
        self.log.info('Waiting for controllers and odometry...')
        self.arm_ac.wait_for_server(timeout_sec=60.0)
        self.grip_ac.wait_for_server(timeout_sec=60.0)
        t0 = time.time()
        while self.odom_x is None and time.time() - t0 < 30.0:
            rclpy.spin_once(self.node, timeout_sec=0.1)

    def drive(self):
        p = self.plan['picking_pose']
        if self.drive_backend == 'nav2' and self._nav2_drive(p['x'], p['y'], p['yaw']):
            pass  # Nav2 got us close; fine-align below for manipulation precision.
        elif self.drive_backend == 'nav2':
            self.log.warn('Nav2 drive failed; falling back to odometry drive.')
        # Precise final pose (both backends) so the fixed arm/collision geometry
        # holds: rotate to the target heading, then drive to the target x.
        self.align_to(p['x'], p['yaw'])

    def _nav2_drive(self, x, y, yaw):
        if not self.nav_ac.wait_for_server(timeout_sec=30.0):
            self.log.warn('Nav2 action server not available.')
            return False
        self.log.info(f'Navigating to picking pose ({x:.2f}, {y:.2f}) via Nav2...')
        goal = NavigateToPose.Goal()
        ps = PoseStamped()
        ps.header.frame_id = 'map'
        ps.header.stamp = self.node.get_clock().now().to_msg()
        ps.pose.position.x = float(x)
        ps.pose.position.y = float(y)
        ps.pose.orientation.z = math.sin(yaw / 2.0)
        ps.pose.orientation.w = math.cos(yaw / 2.0)
        goal.pose = ps
        gh_future = self.nav_ac.send_goal_async(goal)
        rclpy.spin_until_future_complete(self.node, gh_future, timeout_sec=15.0)
        gh = gh_future.result()
        if gh is None or not gh.accepted:
            return False
        res_future = gh.get_result_async()
        rclpy.spin_until_future_complete(self.node, res_future, timeout_sec=90.0)
        if res_future.result() is None:
            return False
        self.log.info('Nav2 reached the picking pose.')
        return True

    def _publish_twist(self, vx=0.0, wz=0.0):
        cmd = TwistStamped()
        cmd.header.stamp = self.node.get_clock().now().to_msg()
        cmd.header.frame_id = 'base_link'
        cmd.twist.linear.x = float(vx)
        cmd.twist.angular.z = float(wz)
        self.cmd_pub.publish(cmd)

    def align_to(self, target_x, target_yaw=0.0, timeout=40.0):
        self.log.info(f'Aligning to picking pose x={target_x:.2f}, yaw={target_yaw:.2f}...')
        # Phase 1: rotate to the target heading.
        t0 = time.time()
        while rclpy.ok() and time.time() - t0 < timeout:
            rclpy.spin_once(self.node, timeout_sec=0.05)
            if self.odom_x is None:
                continue
            yaw_err = math.atan2(math.sin(target_yaw - self.odom_yaw),
                                 math.cos(target_yaw - self.odom_yaw))
            if abs(yaw_err) < 0.02:
                break
            self._publish_twist(wz=max(-0.8, min(0.8, 1.5 * yaw_err)))
        # Phase 2: drive forward/back to the target x (bidirectional).
        t0 = time.time()
        while rclpy.ok() and time.time() - t0 < timeout:
            rclpy.spin_once(self.node, timeout_sec=0.05)
            err = target_x - self.odom_x
            if abs(err) < 0.02:
                break
            v = 0.6 * err
            v = max(0.05, min(0.4, v)) if v > 0 else max(-0.4, min(-0.05, v))
            self._publish_twist(vx=v)
        for _ in range(5):
            self._publish_twist()
            self._spin(0.05)
        self.log.info('Parked at the shelf.')

    def spawn_cans(self):
        t = self.plan['tray']
        for i, y in enumerate(t['ys'][:self.plan['num_units']]):
            jitter = np.random.uniform(-0.01, 0.01)
            cmd = ['ros2', 'run', 'ros_gz_sim', 'create',
                   '-world', WORLD, '-file', self.can_sdf, '-name', f'can_{i}',
                   '-x', str(t['x']), '-y', str(y + jitter), '-z', str(t['z'])]
            subprocess.run(cmd, check=False,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self._spin(1.0)
        self._spin(2.0)
        self.log.info(f"Spawned {self.plan['num_units']} cans in the tray.")

    def ik(self, world_xyz):
        rel = np.array(world_xyz) - self.arm_base
        best, best_err = None, 1e9
        for mode, ori in (('Z', [0, 0, -1]), (None, None)):
            sol = self.chain.inverse_kinematics(
                rel, target_orientation=ori, orientation_mode=mode,
                initial_position=self.full_angles)
            pos = self.chain.forward_kinematics(sol)[:3, 3]
            err = float(np.linalg.norm(pos - rel))
            if err < best_err:
                best, best_err = sol, err
            if err < 0.03:
                break
        self.full_angles = list(best)
        if best_err > 0.05:
            self.log.warn(f'IK residual {best_err*100:.1f} cm at {world_xyz}')
        return [best[i] for i in range(1, 6)]

    def move_arm(self, world_xyz, secs=3.0):
        angles = self.ik(world_xyz)
        if self.backend == 'moveit' and self._plan_execute(angles):
            return True
        return self._send(self.arm_ac, ARM_JOINTS, angles, secs)

    def move_gripper(self, opening, secs=1.5):
        return self._send(self.grip_ac, FINGER_JOINTS, [opening, opening], secs)

    def _send(self, client, names, positions, secs):
        goal = FollowJointTrajectory.Goal()
        goal.trajectory = JointTrajectory()
        goal.trajectory.joint_names = names
        pt = JointTrajectoryPoint()
        pt.positions = [float(p) for p in positions]
        pt.time_from_start = Duration(sec=int(secs), nanosec=int((secs % 1) * 1e9))
        goal.trajectory.points = [pt]
        gh_future = client.send_goal_async(goal)
        rclpy.spin_until_future_complete(self.node, gh_future, timeout_sec=10.0)
        gh = gh_future.result()
        if gh is None or not gh.accepted:
            return False
        res_future = gh.get_result_async()
        rclpy.spin_until_future_complete(self.node, res_future, timeout_sec=secs + 8.0)
        self._spin(0.3)
        return res_future.result() is not None

    def model_pose(self, name):
        try:
            out = subprocess.run(['gz', 'model', '-m', name, '-p'],
                                 capture_output=True, text=True, timeout=8.0).stdout
            nums = re.findall(r'-?\d+\.\d+', out)
            if len(nums) >= 3:
                return tuple(float(n) for n in nums[:3])
        except Exception:  # noqa: BLE001
            pass
        return None

    # ---------- the loop ----------
    def run(self):
        self.wait_ready()
        self.drive()
        self.move_gripper(self.plan['gripper']['open'])
        self.spawn_cans()

        tray, slot = self.plan['tray'], self.plan['slot']
        h = self.plan['approach_height']
        for i in range(self.plan['num_units']):
            t0 = time.time()
            outcome, reason = 'placed', ''
            try:
                cy = tray['ys'][i]
                sx, sy, sz = slot['x'], slot['ys'][i], slot['z']
                self.move_arm([tray['x'], cy, tray['z'] + h])    # pre-pick
                self.move_gripper(self.plan['gripper']['open'])
                self.move_arm([tray['x'], cy, tray['z']])         # descend
                self.move_gripper(self.plan['gripper']['grip'])   # grasp
                self.move_arm([tray['x'], cy, tray['z'] + h])     # lift
                self.move_arm([sx, sy, sz + h])                   # pre-place
                self.move_arm([sx, sy, sz])                       # set down
                self.move_gripper(self.plan['gripper']['open'])   # release
                self.move_arm([sx, sy, sz + h])                   # retreat
                self._add_placed_can(i, [sx, sy, sz])             # avoid neighbor
                pose = self.model_pose(f'can_{i}')
                if pose is not None:
                    if not (pose[2] > 0.80 and abs(pose[0] - sx) < 0.15):
                        outcome, reason = 'missed_slot', f'can at {pose}'
                else:
                    reason = 'unverified (gz pose unavailable)'
            except Exception as e:  # noqa: BLE001
                outcome, reason = 'error', str(e)
            dt = time.time() - t0
            self.results.append((i, outcome, round(dt, 1), reason))
            self.log.info(f'Unit {i}: {outcome} ({dt:.1f}s) {reason}')

        self.move_arm([self.plan['tray']['x'], 0.0, 0.7])  # home-ish
        self.write_log()

    def write_log(self):
        with open(self.log_path, 'w', newline='') as f:
            w = csv.writer(f)
            w.writerow(['unit', 'outcome', 'cycle_time_s', 'reason'])
            w.writerows(self.results)
        placed = sum(1 for r in self.results if r[1] == 'placed')
        n = len(self.results)
        rate = 100.0 * placed / n if n else 0.0
        self.log.info('=' * 56)
        self.log.info(f'JOB COMPLETE: {placed}/{n} placed ({rate:.0f}%) '
                      f'[drive: {self.drive_backend}, arm: {self.backend}].')
        self.log.info(f'Per-unit log: {self.log_path}')
        self.log.info('=' * 56)


def main():
    rclpy.init()
    mission = Mission()
    try:
        mission.run()
    finally:
        mission.node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
