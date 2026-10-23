from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    auto_walk_arg = DeclareLaunchArgument(
        'auto_walk',
        default_value='false',
        description='If true, auto-walk in expanding spiral. If false, stay at position until clicked in RViz or moved by SLAM.'
    )

    # 1. WiFi RSSI Measurement Node (Reads live dBm from wlan0)
    rssi_node = Node(
        package='resqtether_signal_map',
        executable='real_rssi_node',
        name='wifi_rssi_node',
        parameters=[{
            'interface': 'wlan0',
            'rate_hz': 1.0,
            'topic_float': '/signal/rssi_measured',
            'topic_status': '/lora/rssi',
            'base_station_id': 'laptop_base'
        }],
        output='screen'
    )

    # 2. Walk Controller (Publishes map -> base_link transform)
    walk_node = Node(
        package='signal_mapper',
        executable='walk_controller',
        name='walk_controller',
        parameters=[{
            'auto_walk': LaunchConfiguration('auto_walk'),
            'speed_mps': 0.3,
            'radius_m': 3.0
        }],
        output='screen'
    )

    # 3. Signal Map Fusion Node (Fuses position + RSSI into spatial grid cubes)
    fuse_node = Node(
        package='signal_mapper',
        executable='fuse_node',
        name='signal_fuse_node',
        parameters=[{
            'cell_size': 0.25,
            'csv_path': 'signal_map.csv',
            'map_frame': 'map',
            'base_frame': 'base_link',
            'publish_interval_sec': 1.0
        }],
        output='screen'
    )

    return LaunchDescription([
        auto_walk_arg,
        rssi_node,
        walk_node,
        fuse_node
    ])
