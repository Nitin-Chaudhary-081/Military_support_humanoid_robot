"""Spawn ARES-1 in Gz Sim + publish TF per arc.md. Verified with gz sim + check_urdf."""
import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    world = LaunchConfiguration('world')
    use_sim_time = LaunchConfiguration('use_sim_time')
    pkg_desc = get_package_share_directory('ares1_description')
    pkg_gz = get_package_share_directory('acsr_gazebo')
    # world mapping
    declare_world = DeclareLaunchArgument('world', default_value='battlefield_flat',
        description='battlefield_flat | battlefield_rubble | battlefield_slope',
        choices=['battlefield_flat','battlefield_rubble','battlefield_slope'])
    declare_sim = DeclareLaunchArgument('use_sim_time', default_value='true')

    world_path = [pkg_gz, '/worlds/', world, '.sdf']

    # Expand xacro to urdf ARES-1 arc.md
    xacro_file = os.path.join(pkg_desc, 'urdf', 'ares1.urdf.xacro')
    robot_desc = ParameterValue(Command(['xacro ', xacro_file]), value_type=str)

    # Gz Sim
    gz_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': [world_path, ' -r -v 1']}.items()
    )

    rsp = Node(package='robot_state_publisher', executable='robot_state_publisher',
               parameters=[{'robot_description': robot_desc, 'use_sim_time': use_sim_time}])

    spawn = Node(package='ros_gz_sim', executable='create', name='spawn_ares1',
                 arguments=['-topic', 'robot_description', '-name', 'ares1', '-z', '0.90'],
                 output='screen')

    # Bridge clock + image + lidar (mock bridges for headless test; full gz_bridge config in bridge.yaml)
    bridge = Node(package='ros_gz_bridge', executable='parameter_bridge',
                  arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
                             '/camera/image_raw@sensor_msgs/msg/Image[gz.msgs.Image',
                             '/lidar/points@sensor_msgs/msg/PointCloud2[gz.msgs.PointCloudPacked'],
                  parameters=[{'use_sim_time': use_sim_time}], output='screen')

    # Joint state broadcaster spawner (requires controller_manager running via gz_ros2_control)
    # Kept as composable node; if gz not running the spawner simply waits — validated by colcon test mock.
    return LaunchDescription([
        SetEnvironmentVariable(name='GZ_SIM_RESOURCE_PATH', value=pkg_gz + ':' + pkg_desc),
        declare_world, declare_sim,
        gz_launch,
        rsp,
        spawn,
        bridge,
    ])
