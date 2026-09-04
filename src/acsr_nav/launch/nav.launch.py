from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    nav2 = get_package_share_directory('nav2_bringup')
    acsr_nav = get_package_share_directory('acsr_nav')
    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(nav2, 'launch', 'navigation_launch.py')),
            launch_arguments={'params_file': os.path.join(acsr_nav, 'config', 'nav2_params.yaml'), 'use_sim_time': 'true'}.items()
        )
    ])
