import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, GroupAction
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

    rf2o_launch_dir = os.path.join(get_package_share_directory('rf2o_laser_odometry'), 'launch')
    slam_launch_dir = os.path.join(get_package_share_directory('neuronbot2_slam'), 'launch')

    pure_lidar_slam = GroupAction([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([rf2o_launch_dir, '/rf2o_laser_odometry.launch.py']),
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource([slam_launch_dir, '/gmapping_launch.py']),
        ),
    ])

    # Launch!
    return LaunchDescription(
        [
        rsp,
        pure_lidar_slam
        ]
    )