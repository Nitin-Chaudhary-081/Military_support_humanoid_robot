"""Foxglove display — static robot without Gz, so you can see ACSR in browser immediately.
Launches: robot_state_publisher (URDF) + joint_state_publisher + foxglove_bridge (0.0.0.0:8765).
Usage: ros2 launch acsr_bringup foxglove_display.launch.py
  -> open https://app.foxglove.dev -> ws://<VPS_PUBLIC_IP>:8765 or ws://localhost:8765 via SSH tunnel
  -> add 3D panel -> Robot Model -> import layout src/acsr_bringup/config/foxglove/acsr_layout.json
"""
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.parameter_descriptions import ParameterValue
from launch.conditions import IfCondition
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkg_desc = get_package_share_directory('ares1_description')
    pkg_bringup = get_package_share_directory('acsr_bringup')
    use_sim = LaunchConfiguration('use_sim_time')
    # Foxglove 3D panel cannot resolve package:// — rewrite visual mesh URIs to CORS http://
    # Local CORS server python3 scripts/cors_http.py serves install/.../meshes at :8000 with Access-Control-Allow-Origin *
    # Use http://localhost:8000 via SSH tunnel (ssh -L 8000:localhost:8000) or http://13.207.111.213:8000 via Lightsail open port 8000
    # Fallback https://raw.githubusercontent.com/.../visual/*.stl if local http unreachable (but raw lacks CORS — prefer local)
    raw_base = 'http://localhost:8000'
    # Alternative public: http://13.207.111.213:8000  and https raw: https://raw.githubusercontent.com/Nitin-Chaudhary-081/Military_support_humanoid_robot/main/src/ares1_description
    xacro_path = os.path.join(pkg_desc, 'urdf', 'ares1.urdf.xacro')
    foxglove_urdf_cmd = [
        'bash -c "xacro ', xacro_path,
        ' | sed \'s|package://ares1_description/meshes|', raw_base, '|g\'"'
    ]
    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='false', description='Use sim time false for static display'),
        # URDF — Foxglove http-rewritten for mesh loading (package:// → https://raw.githubusercontent.com)
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{
                'robot_description': ParameterValue(Command(foxglove_urdf_cmd), value_type=str),
                'use_sim_time': use_sim,
            }],
            output='screen',
        ),
        # Publish joint states with defaults (shield stowed 0.0, hips 0 etc)
        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            parameters=[{'use_sim_time': use_sim}],
            output='screen',
        ),
        # Foxglove bridge 0.0.0.0:8765
        Node(
            package='foxglove_bridge',
            executable='foxglove_bridge',
            name='foxglove_bridge',
            parameters=[
                os.path.join(pkg_bringup, 'config', 'foxglove_bridge.yaml'),
                {'use_sim_time': use_sim},
            ],
            output='screen',
        ),
    ])
