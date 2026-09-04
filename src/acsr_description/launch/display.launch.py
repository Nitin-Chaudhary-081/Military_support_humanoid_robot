from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os, xacro

def generate_launch_description():
    pkg = get_package_share_directory('acsr_description')
    xacro_file = os.path.join(pkg, 'urdf', 'acsr.urdf.xacro')
    robot_desc = xacro.process_file(xacro_file).toxml()
    return LaunchDescription([
        Node(package='robot_state_publisher', executable='robot_state_publisher',
             parameters=[{'robot_description': robot_desc, 'use_sim_time': False}]),
        Node(package='joint_state_publisher_gui', executable='joint_state_publisher_gui'),
        Node(package='rviz2', executable='rviz2', arguments=['-d', os.path.join(pkg, 'config', 'acsr.rviz')],
             condition=None),
    ])
