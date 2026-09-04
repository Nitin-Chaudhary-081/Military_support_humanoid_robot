from launch import LaunchDescription
from launch_ros.actions import Node
def generate_launch_description():
    return LaunchDescription([Node(package='threat_manager', executable='threat_node', parameters=['config/threat.yaml'])])
