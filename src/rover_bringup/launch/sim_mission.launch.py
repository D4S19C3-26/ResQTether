#!/usr/bin/env python3
"""
sim_mission.launch.py
---------------------
Full End-to-End Mission Launcher (Hardware-Free & Real-Time):
Launches:
1. Mock Mission Simulator (Robot Kinematics, 360 LiDAR Scan, LoRa RSSI propagation)
2. Signal Mapper Fuse Node (Generates 3D Heatmap cubes + 2D Occupancy Overlay)
3. Signal-Aware Relay Decision Node (Wanders, detects victims, retreats in dead zones)
4. Real-time Live RSSI vs Time Graph Monitor (Matplotlib GUI)
5. RViz2 (LiDAR, Heatmap Overlays, Robot TF)
"""

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    rover_bringup_pkg = get_package_share_directory('rover_bringup')
    rviz_config = os.path.join(rover_bringup_pkg, 'rviz', 'full_system.rviz')

    # Arguments
    launch_rviz_arg = DeclareLaunchArgument('rviz', default_value='true', description='Open RViz2 if true')
    launch_plot_arg = DeclareLaunchArgument('plot', default_value='true', description='Open live RSSI plot GUI')

    # 1. Mock Mission Simulator (Kinematics, Scan, LoRa RSSI with dead zones)
    sim_node = Node(
        package='resqtether_sim',
        executable='mock_mission_node.py',
        name='mock_mission_simulator',
        output='screen'
    )

    # 2. Signal Mapper Fuse Node (3D Markers + 2D Overlay on LiDAR map)
    fuse_node = Node(
        package='signal_mapper',
        executable='fuse_node',
        name='signal_fuse_node',
        parameters=[{
            'cell_size': 0.25,
            'csv_path': 'signal_map.csv',
            'map_frame': 'map',
            'base_frame': 'base_link',
            'publish_interval_sec': 0.5
        }],
        output='screen'
    )

    # 3. Autonomous Signal-Aware Relay Decision Node
    relay_node = Node(
        package='resqtether_decision',
        executable='relay_wander_node',
        name='relay_wander_node',
        parameters=[{
            'signal_threshold_dbm': -70.0,
            'recovery_threshold_dbm': -67.0,
            'cruise_speed': 0.25,
            'turn_speed': 0.6,
            'obstacle_dist_m': 0.60
        }],
        output='screen'
    )

    # 4. Live RSSI Graph Plotter Window
    plot_node = Node(
        package='resqtether_signal_map',
        executable='plot_rssi',
        name='rssi_plotter_node',
        output='screen'
    )

    # 5. RViz2
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config],
        output='screen'
    )

    return LaunchDescription([
        launch_rviz_arg,
        launch_plot_arg,
        sim_node,
        fuse_node,
        relay_node,
        plot_node,
        rviz_node
    ])
