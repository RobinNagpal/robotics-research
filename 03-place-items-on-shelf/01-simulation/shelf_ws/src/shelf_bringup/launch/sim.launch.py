"""Top-level simulation launch.

Starts Gazebo Harmonic, the ros_gz bridge, robot_state_publisher, spawns the
mobile manipulator, and brings up the ros2_control controllers. CP4 adds the
autonomous mission on top of this, so `./run.sh` stays a single command.
"""
import os

import xacro
from moveit_configs_utils import MoveItConfigsBuilder
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (DeclareLaunchArgument, EmitEvent, ExecuteProcess,
                            OpaqueFunction, RegisterEventHandler)
from launch.event_handlers import OnProcessExit
from launch.events import Shutdown
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def launch_setup(context, *args, **kwargs):
    bringup = get_package_share_directory('shelf_bringup')
    description = get_package_share_directory('shelf_description')

    headless = LaunchConfiguration('headless').perform(context)
    world = LaunchConfiguration('world').perform(context)
    run_mission = LaunchConfiguration('mission').perform(context)
    arm_backend = LaunchConfiguration('arm_backend').perform(context)

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

    # Start the autonomous mission once the controllers are up, and shut the
    # whole launch down cleanly when the mission node exits.
    if run_mission == 'true':
        # MoveIt 2 config (planning pipeline + SRDF + controllers) passed to
        # the mission node so MoveItPy can plan collision-free arm motions.
        moveit_params = []
        if arm_backend == 'moveit':
            description = get_package_share_directory('shelf_description')
            moveit_config = (
                MoveItConfigsBuilder('shelf_bot', package_name='shelf_moveit_config')
                .robot_description(
                    file_path=os.path.join(description, 'urdf', 'robot.urdf.xacro'))
                .robot_description_semantic(file_path='config/shelf_bot.srdf')
                .robot_description_kinematics(file_path='config/kinematics.yaml')
                .joint_limits(file_path='config/joint_limits.yaml')
                .trajectory_execution(file_path='config/moveit_controllers.yaml')
                .planning_pipelines(pipelines=['ompl'], default_planning_pipeline='ompl')
                .to_moveit_configs()
            )
            moveit_params = [moveit_config.to_dict()]

        # Node is named 'moveit_py' so the MoveIt params scope to the node
        # MoveItPy creates; the backend choice is passed via env.
        orchestrator = Node(
            package='shelf_bringup', executable='orchestrator.py', name='moveit_py',
            output='screen',
            parameters=moveit_params + [{'use_sim_time': True}],
            additional_env={'SHELF_ARM_BACKEND': arm_backend})
        after_controllers = RegisterEventHandler(
            OnProcessExit(target_action=grip, on_exit=[orchestrator]))
        on_mission_done = RegisterEventHandler(
            OnProcessExit(target_action=orchestrator,
                          on_exit=[EmitEvent(event=Shutdown())]))
        actions += [after_controllers, on_mission_done]

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
        DeclareLaunchArgument('arm_backend', default_value='moveit',
            description="Arm motion: 'moveit' (collision-aware planning) or "
                        "'direct' (ikpy joint-trajectory, no planning)."),
        OpaqueFunction(function=launch_setup),
    ])
