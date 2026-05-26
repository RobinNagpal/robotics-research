"""Top-level simulation launch.

CP1: start Gazebo Harmonic (headless or GUI) and the ros_gz clock bridge.
Later checkpoints add the robot, controllers, sensors, and the autonomous
mission to this same file so `./run.sh` stays a single command.
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def launch_setup(context, *args, **kwargs):
    pkg = get_package_share_directory('shelf_bringup')

    headless = LaunchConfiguration('headless').perform(context)
    world = LaunchConfiguration('world').perform(context)

    # Resolve the world: a file in our worlds/ dir, an absolute path, or a
    # Gazebo built-in name (e.g. empty.sdf) as a fallback.
    candidate = os.path.join(pkg, 'worlds', world)
    world_path = candidate if os.path.exists(candidate) else world

    gz_args = ['-r', '-v', '3', world_path]
    if headless == 'true':
        gz_args = ['-s'] + gz_args

    gz = ExecuteProcess(
        cmd=['gz', 'sim'] + gz_args,
        output='screen',
    )

    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        name='ros_gz_bridge',
        parameters=[{
            'config_file': os.path.join(pkg, 'config', 'bridge.yaml'),
            'use_sim_time': True,
        }],
        output='screen',
    )

    return [gz, bridge]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            'headless', default_value='true',
            description='Run Gazebo without the GUI (server only).'),
        DeclareLaunchArgument(
            'world', default_value='empty.sdf',
            description='World file in shelf_bringup/worlds, an absolute path, '
                        'or a Gazebo built-in name.'),
        OpaqueFunction(function=launch_setup),
    ])
