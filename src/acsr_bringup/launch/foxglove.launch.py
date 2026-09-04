"""Foxglove bridge — ws://localhost:8765 for browser Foxglove Studio.
Verified: foxglove_bridge 3.4.1 listens on 0.0.0.0:8765 and advertises /rosout.
Usage:
  ros2 launch acsr_bringup foxglove.launch.py
  # then open https://app.foxglove.dev -> Open connection -> ws://localhost:8765
  # or studio.foxglove.dev with same URL
"""
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg = get_package_share_directory('acsr_bringup')
    use_sim = LaunchConfiguration('use_sim_time')
    port = LaunchConfiguration('port')
    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        DeclareLaunchArgument('port', default_value='8765'),
        Node(
            package='foxglove_bridge',
            executable='foxglove_bridge',
            name='foxglove_bridge',
            parameters=[
                os.path.join(pkg, 'config', 'foxglove_bridge.yaml'),
                {'port': port, 'use_sim_time': use_sim},
            ],
            output='screen',
        ),
    ])
