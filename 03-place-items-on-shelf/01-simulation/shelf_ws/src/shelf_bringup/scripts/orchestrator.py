#!/usr/bin/env python3
"""Autonomous shelf-stocking mission (v1, known-pose).

Runs the full loop from ../../01-requirements.md §6:
  drive to the shelf -> spawn the tray of cans -> for each can:
  pick (IK + grasp) -> place into the slot -> verify -> log -> repeat.

Kept deliberately simple for a reliable Gazebo demo: the base drives by
odometry, the 5-DoF arm is solved with ikpy, and the grasp is a friction
grasp (the known-hard part — tune gripper.grip / can friction if a can
slips; see ../../05-manipulation.md for the DetachableJoint alternative).
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
from rclpy.node import Node
from rclpy.action import ActionClient

from ament_index_python.packages import get_package_share_directory
from geometry_msgs.msg import TwistStamped
from nav_msgs.msg import Odometry
from control_msgs.action import FollowJointTrajectory
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration

from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink

ARM_JOINTS = ['joint_pan', 'joint_lift', 'joint_elbow',
              'joint_wrist_pitch', 'joint_wrist_roll']
FINGER_JOINTS = ['left_finger_joint', 'right_finger_joint']
WORLD = 'store_aisle'


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


class Orchestrator(Node):
    def __init__(self):
        super().__init__('orchestrator')
        pkg = get_package_share_directory('shelf_bringup')
        with open(os.path.join(pkg, 'config', 'planogram.yaml')) as f:
            self.plan = yaml.safe_load(f)
        self.can_sdf = os.path.join(pkg, 'models', 'can_sku', 'model.sdf')

        self.chain = build_chain()
        self.full_angles = [0.0] * 7
        # Arm base in world when parked: base offset (-0.05,0,0.325) + spawn z 0.175.
        p = self.plan['picking_pose']
        self.arm_base = np.array([p['x'] - 0.05, p['y'], 0.5])

        self.odom_x = None
        self.create_subscription(Odometry, '/odom', self._odom, 10)
        self.cmd_pub = self.create_publisher(TwistStamped, '/diff_drive_controller/cmd_vel', 10)
        self.arm_ac = ActionClient(self, FollowJointTrajectory,
                                   '/arm_controller/follow_joint_trajectory')
        self.grip_ac = ActionClient(self, FollowJointTrajectory,
                                    '/gripper_controller/follow_joint_trajectory')

        os.makedirs('/ws/logs', exist_ok=True)
        stamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.log_path = f'/ws/logs/run_{stamp}.csv'
        self.results = []

    # ---------- helpers ----------
    def _odom(self, msg):
        self.odom_x = msg.pose.pose.position.x

    def _spin(self, secs):
        end = time.time() + secs
        while time.time() < end:
            rclpy.spin_once(self, timeout_sec=0.05)

    def wait_ready(self):
        self.get_logger().info('Waiting for controllers and odometry...')
        self.arm_ac.wait_for_server(timeout_sec=60.0)
        self.grip_ac.wait_for_server(timeout_sec=60.0)
        t0 = time.time()
        while self.odom_x is None and time.time() - t0 < 30.0:
            rclpy.spin_once(self, timeout_sec=0.1)

    def drive_to(self, target_x):
        self.get_logger().info(f'Driving to picking pose x={target_x:.2f}...')
        while rclpy.ok():
            rclpy.spin_once(self, timeout_sec=0.05)
            if self.odom_x is None:
                continue
            err = target_x - self.odom_x
            if err < 0.02:
                break
            cmd = TwistStamped()
            cmd.header.stamp = self.get_clock().now().to_msg()
            cmd.header.frame_id = 'base_link'
            cmd.twist.linear.x = float(max(0.05, min(0.4, 0.6 * err)))
            self.cmd_pub.publish(cmd)
        # stop
        for _ in range(5):
            cmd = TwistStamped()
            cmd.header.stamp = self.get_clock().now().to_msg()
            self.cmd_pub.publish(cmd)
            self._spin(0.05)
        self.get_logger().info('Parked at the shelf.')

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
        self._spin(2.0)  # let cans settle
        self.get_logger().info(f"Spawned {self.plan['num_units']} cans in the tray.")

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
            self.get_logger().warn(f'IK residual {best_err*100:.1f} cm at {world_xyz}')
        return [best[i] for i in range(1, 6)]

    def move_arm(self, world_xyz, secs=3.0):
        angles = self.ik(world_xyz)
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
        rclpy.spin_until_future_complete(self, gh_future, timeout_sec=10.0)
        gh = gh_future.result()
        if gh is None or not gh.accepted:
            return False
        res_future = gh.get_result_async()
        rclpy.spin_until_future_complete(self, res_future, timeout_sec=secs + 8.0)
        self._spin(0.3)
        return res_future.result() is not None

    def model_pose(self, name):
        """Return (x,y,z) of a model via the gz CLI, or None if unavailable."""
        try:
            out = subprocess.run(['gz', 'model', '-m', name, '-p'],
                                 capture_output=True, text=True, timeout=8.0).stdout
            nums = re.findall(r'-?\d+\.\d+', out)
            if len(nums) >= 3:
                return tuple(float(n) for n in nums[:3])
        except Exception:
            pass
        return None

    # ---------- the loop ----------
    def run(self):
        self.wait_ready()
        self.drive_to(self.plan['picking_pose']['x'])
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
                # pick
                self.move_arm([tray['x'], cy, tray['z'] + h])     # pre-pick
                self.move_gripper(self.plan['gripper']['open'])
                self.move_arm([tray['x'], cy, tray['z']])          # descend
                self.move_gripper(self.plan['gripper']['grip'])    # grasp
                self.move_arm([tray['x'], cy, tray['z'] + h])      # lift
                # place
                self.move_arm([sx, sy, sz + h])                    # pre-place
                self.move_arm([sx, sy, sz])                        # set down
                self.move_gripper(self.plan['gripper']['open'])    # release
                self.move_arm([sx, sy, sz + h])                    # retreat
                # verify
                pose = self.model_pose(f'can_{i}')
                if pose is not None:
                    on_shelf = pose[2] > 0.80 and abs(pose[0] - sx) < 0.15
                    if not on_shelf:
                        outcome, reason = 'missed_slot', f'can at {pose}'
                else:
                    reason = 'unverified (gz pose unavailable)'
            except Exception as e:  # noqa: BLE001
                outcome, reason = 'error', str(e)
            dt = time.time() - t0
            self.results.append((i, outcome, round(dt, 1), reason))
            self.get_logger().info(f'Unit {i}: {outcome} ({dt:.1f}s) {reason}')

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
        self.get_logger().info('=' * 56)
        self.get_logger().info(f'JOB COMPLETE: {placed}/{n} placed ({rate:.0f}%).')
        self.get_logger().info(f'Per-unit log: {self.log_path}')
        self.get_logger().info('=' * 56)


def main():
    rclpy.init()
    node = Orchestrator()
    try:
        node.run()
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
