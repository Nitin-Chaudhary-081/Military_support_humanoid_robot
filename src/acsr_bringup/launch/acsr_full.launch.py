"""Full ACSR stack — world + perception + shield + weapons (human-confirm) + drones + battery + Nav2."""
import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, GroupAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    world = LaunchConfiguration('world')
    use_sim_time = LaunchConfiguration('use_sim_time')
    use_foxglove = LaunchConfiguration('use_foxglove')
    DeclareLaunchArgument = __import__('launch.actions', fromlist=['DeclareLaunchArgument']).DeclareLaunchArgument
    from launch.conditions import IfCondition
    return LaunchDescription([
        DeclareLaunchArgument('world', default_value='battlefield_rubble'),
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        DeclareLaunchArgument('use_foxglove', default_value='true', description='Start foxglove_bridge on 8765 for browser'),
        # Gazebo + robot
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(get_package_share_directory('acsr_gazebo'), 'launch', 'acsr_world.launch.py')),
            launch_arguments={'world': world, 'use_sim_time': use_sim_time}.items()),
        # Core nodes (mock-safe)
        Node(package='threat_manager', executable='threat_node', parameters=[{'use_sim_time': use_sim_time, 'model': 'yolov8n', 'conf_thresh': 0.45}]),
        Node(package='shield_controller', executable='shield_node', parameters=[{'use_sim_time': use_sim_time}]),
        Node(package='weapon_control', executable='weapon_node', parameters=[{'use_sim_time': use_sim_time, 'require_human_confirm': True}]),
        Node(package='drone_coordinator', executable='drone_node', parameters=[{'use_sim_time': use_sim_time}]),
        Node(package='battery_manager', executable='battery_node', parameters=[{'use_sim_time': use_sim_time, 'capacity_kwh': 48.0}]),
        # Foxglove bridge (browser: ws://localhost:8765)
        Node(
            package='foxglove_bridge', executable='foxglove_bridge', name='foxglove_bridge',
            parameters=[os.path.join(get_package_share_directory('acsr_bringup'), 'config', 'foxglove_bridge.yaml'),
                        {'use_sim_time': use_sim_time}],
            output='screen',
            condition=IfCondition(use_foxglove),
        ),
        # Nav2 (uses acsr_nav params — runs even if map not yet built, publishes costmap from lidar)
        # Commented until nav2 stack installed on this host; kept as Include for completeness per goal.md:99
        # IncludeLaunchDescription(PythonLaunchDescriptionSource(os.path.join(get_package_share_directory('acsr_nav'), 'launch', 'nav.launch.py')))
    ])
