import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.substitutions import Command
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessStart

from launch_ros.actions import Node



def generate_launch_description():

    package_name='smart_rover'

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'false', 'use_ros2_control': 'true'}.items()
    )

    robot_description = Command(['ros2 param get --hide-type /robot_state_publisher robot_description'])

    controller_params_file = os.path.join(get_package_share_directory(package_name), 'config', 'controller_configuration.yaml')

    joystick = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','joystick.launch.py'
                )]), launch_arguments={'use_sim_time': 'false'}.items()
    )

    delayed_controller_manager = TimerAction(
        period=3.0,
        actions=[
            Node(
                package="controller_manager",
                executable="ros2_control_node",
                parameters=[{'robot_description': robot_description}, 
                            controller_params_file], 
            )])       
    diff_drive_spawner=Node(
                package="controller_manager",
                executable="spawner.py",
                arguments=["diff_cont"],
            )
    delayed_diff_drive_spawner = RegisterEventHandler(
          event_handler=OnProcessStart(
          target_action=delayed_controller_manager,
          on_start=[diff_drive_spawner],
        )
        )       
    joint_broad_spawner= Node(
                package="controller_manager",
                executable="spawner.py",
                arguments=["joint_broad"],
            )
    delayed_joint_broad_spawner = RegisterEventHandler(
          event_handler=OnProcessStart(
          target_action=delayed_controller_manager,
          on_start=[joint_broad_spawner],
        )
        )     
    # Launch!
    return LaunchDescription(
        [
        rsp,
        joystick,
        delayed_controller_manager,
        delayed_diff_drive_spawner,
        delayed_joint_broad_spawner
        ]
    )