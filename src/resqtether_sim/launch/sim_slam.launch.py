import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_share = get_package_share_directory('resqtether_sim')
    
    # 1. Include the simulation launch file (Gazebo + Robot Spawn + Bridge)
    sim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_share, 'launch', 'sim.launch.py')
        )
    )
    
    # 2. SLAM Toolbox node (Online Async)
    # Get the path to the default slam_toolbox config file
    slam_toolbox_share = get_package_share_directory('slam_toolbox')
    default_mapper_params = os.path.join(slam_toolbox_share, 'config', 'mapper_params_online_async.yaml')
    
    slam_toolbox_node = Node(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        output='screen',
        parameters=[
            default_mapper_params,
            {
                'use_sim_time': True,
                'odom_frame': 'odom',
                'base_frame': 'base_footprint',
                'scan_topic': '/scan'
            }
        ]
    )

    # 3. Signal Map Node
    signal_map_node = Node(
        package='resqtether_sim',
        executable='signal_map_node',
        name='signal_map_node',
        output='screen',
        parameters=[{'use_sim_time': True}]
    )

    # 4. RViz2 node with pre-configured map display
    rviz_config_file = os.path.join(pkg_share, 'rviz', 'slam.rviz')
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_file],
        parameters=[{'use_sim_time': True}],
        output='screen'
    )

    return LaunchDescription([
        sim_launch,
        slam_toolbox_node,
        signal_map_node,
        rviz_node
    ])
