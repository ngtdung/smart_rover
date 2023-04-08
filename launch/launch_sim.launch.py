import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import TimerAction

from launch_ros.actions import Node

from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit


def generate_launch_description():

    package_name='smart_rover'

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'true', 'use_ros2_control': 'true'}.items()
    )

    joystick = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','joystick.launch.py'
                )]), launch_arguments={'use_sim_time': 'true'}.items()
    )

    gazebo_params_file = os.path.join(get_package_share_directory(package_name), 'config', 'gazebo_params.yaml')

    # Include the Gazebo launch file, provided by the gazebo_ros package
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
                    launch_arguments={'extra_gazebo_arguments': '--ros-args --params-file ' + gazebo_params_file}.items()
             )

    # Run the spawner node from the gazebo_ros package
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'my_bot'],
                        output='screen')

    delayed_controller_manager_spawner = TimerAction(
        period=10.0,
        actions=[
            Node(
                package="controller_manager",
                executable="spawner.py",
                arguments=["diff_cont"],
            ),
            Node(
                package="controller_manager",
                executable="spawner.py",
                arguments=["joint_broad"],
            )
        ],
    )

    # Launch!
    return LaunchDescription(
        [
        rsp,
        gazebo,
        spawn_entity,
        delayed_controller_manager_spawner,
        joystick
        ]
    )