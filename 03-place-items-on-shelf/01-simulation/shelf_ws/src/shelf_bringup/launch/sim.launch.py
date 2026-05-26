"""Top-level simulation launch.

Starts Gazebo Harmonic, the ros_gz bridge, robot_state_publisher, spawns the
mobile manipulator, and brings up the ros2_control controllers. CP4 adds the
autonomous mission on top of this, so `./run.sh` stays a single command.
"""
import os

import xacro
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (DeclareLaunchArgument, ExecuteProcess,
                            OpaqueFunction, RegisterEventHandler)
from launch.event_handlers import OnProcessExit
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def launch_setup(context, *args, **kwargs):
    bringup = get_package_share_directory('shelf_bringup')
    description = get_package_share_directory('shelf_description')

    headless = LaunchConfiguration('headless').perform(context)
    world = LaunchConfiguration('world').perform(context)
    run_mission = LaunchConfiguration('mission').perform(context)

    candidate = os.path.join(bringup, 'worlds', world)
    world_path = candidate if os.path.exists(candidate) else world

    gz_args = ['-r', '-v', '3', world_path]
    if headless == 'true':
        gz_args = ['-s'] + gz_args
    gz = ExecuteProcess(cmd=['gz', 'sim'] + gz_args, output='screen')

    # Process the robot Xacro, injecting the controllers config path.
    controllers_yaml = os.path.join(bringup, 'config', 'controllers.yaml')
    xacro_file = os.path.join(description, 'urdf', 'robot.urdf.xacro')
    robot_description = xacro.process_file(
        xacro_file, mappings={'controllers_yaml': controllers_yaml}).toxml()

    rsp = Node(
        package='robot_state_publisher', executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description,
                     'use_sim_time': True}],
    )

    bridge = Node(
        package='ros_gz_bridge', executable='parameter_bridge', name='ros_gz_bridge',
        parameters=[{'config_file': os.path.join(bringup, 'config', 'bridge.yaml'),
                     'use_sim_time': True}],
        output='screen',
    )

    spawn = Node(
        package='ros_gz_sim', executable='create', output='screen',
        arguments=['-topic', 'robot_description', '-name', 'shelf_bot',
                   '-x', '0.0', '-y', '0.0', '-z', '0.175', '-Y', '0.0'],
    )

    def spawner(name):
        return Node(package='controller_manager', executable='spawner',
                    arguments=[name, '--controller-manager', '/controller_manager'],
                    output='screen')

    jsb = spawner('joint_state_broadcaster')
    diff = spawner('diff_drive_controller')
    arm = spawner('arm_controller')
    grip = spawner('gripper_controller')

    # Order: spawn model -> joint_state_broadcaster -> the rest.
    after_spawn = RegisterEventHandler(
        OnProcessExit(target_action=spawn, on_exit=[jsb]))
    after_jsb = RegisterEventHandler(
        OnProcessExit(target_action=jsb, on_exit=[diff, arm, grip]))

    actions = [gz, bridge, rsp, spawn, after_spawn, after_jsb]

    # CP4: optionally start the autonomous mission once controllers are up.
    if run_mission == 'true':
        orchestrator = Node(
            package='shelf_bringup', executable='orchestrator.py',
            output='screen', parameters=[{'use_sim_time': True}])
        perception = Node(
            package='shelf_bringup', executable='perception_node.py',
            output='screen', parameters=[{'use_sim_time': True}])
        after_controllers = RegisterEventHandler(
            OnProcessExit(target_action=grip, on_exit=[perception, orchestrator]))
        actions.append(after_controllers)

    return actions


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('headless', default_value='true',
            description='Run Gazebo without the GUI (server only).'),
        DeclareLaunchArgument('world', default_value='store_aisle.sdf',
            description='World in shelf_bringup/worlds, an absolute path, or a '
                        'Gazebo built-in name.'),
        DeclareLaunchArgument('mission', default_value='true',
            description='Start the autonomous stocking mission automatically.'),
        OpaqueFunction(function=launch_setup),
    ])
