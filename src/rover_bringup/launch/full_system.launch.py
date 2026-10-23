import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition, UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    lidar_pkg = get_package_share_directory('lidar_bringup')
    slam_pkg = get_package_share_directory('slam_bringup')
    human_detect_pkg = get_package_share_directory('resqtether_human_detect')
    lora_pkg = get_package_share_directory('lora_bringup')

    # Launch arguments
    lidar_port_arg = DeclareLaunchArgument(
        'lidar_port',
        default_value='/dev/ttyUSB0',
        description='Serial port for hardware LiDAR (e.g. /dev/ttyUSB0)'
    )

    lidar_baud_arg = DeclareLaunchArgument(
        'lidar_baudrate',
        default_value='115200',
        description='LiDAR baudrate (115200 for A1/A2, 256000 for A3/S1/C1)'
    )

    cell_size_arg = DeclareLaunchArgument(
        'cell_size',
        default_value='0.25',
        description='Grid cell bin size in meters for RSSI map'
    )

    csv_path_arg = DeclareLaunchArgument(
        'csv_path',
        default_value='signal_map.csv',
        description='Path to output CSV file for signal observations'
    )

    use_camera_arg = DeclareLaunchArgument(
        'use_camera',
        default_value='true',
        description='Enable USB camera and human detection if true'
    )

    camera_index_arg = DeclareLaunchArgument(
        'camera_index',
        default_value='0',
        description='Camera V4L2 device index (e.g. 0 for /dev/video0)'
    )

    use_motors_arg = DeclareLaunchArgument(
        'use_motors',
        default_value='false',
        description='Enable GPIO motor driver (set true when running chassis motors)'
    )

    motor_port_arg = DeclareLaunchArgument(
        'motor_port',
        default_value='/dev/ttyUSB1',
        description='Serial port for ESP32 motor controller (e.g. /dev/ttyUSB1 or /dev/ttyACM0)'
    )

    use_lora_arg = DeclareLaunchArgument(
        'use_lora',
        default_value='false',
        description='Enable LilyGO LoRa32 hardware receiver for RSSI signal mapping (false = use native WiFi)'
    )

    use_relay_arg = DeclareLaunchArgument(
        'use_relay',
        default_value='false',
        description='Enable autonomous signal-aware wandering and victim store-and-forward relay'
    )

    lora_port_arg = DeclareLaunchArgument(
        'lora_port',
        default_value='/dev/ttyUSB0',
        description='Serial port for LilyGO LoRa32 (e.g. /dev/ttyUSB0 or /dev/ttyUSB1)'
    )

    # 1. Real Hardware LiDAR Driver
    lidar_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(lidar_pkg, 'launch', 'lidar.launch.py')
        ),
        launch_arguments={
            'serial_port': LaunchConfiguration('lidar_port'),
            'baudrate': LaunchConfiguration('lidar_baudrate'),
            'frame_id': 'laser_link'
        }.items()
    )

    # 2. SLAM Toolbox (Headless Async Scan-matching mode)
    slam_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(slam_pkg, 'launch', 'slam.launch.py')
        ),
        launch_arguments={
            'use_sim_time': 'false',
            'laser_frame': 'laser_link'
        }.items()
    )

    # 3. LoRa Receiver Node (Primary for ResQTether)
    lora_node = Node(
        package='lora_bringup',
        executable='lora_serial_node',
        name='lora_serial_node',
        parameters=[{
            'port': LaunchConfiguration('lora_port'),
            'baudrate': 115200,
            'default_sender_id': 'base_station',
            'timeout_sec': 0.5
        }],
        condition=IfCondition(LaunchConfiguration('use_lora')),
        output='screen'
    )

    # Fallback: WiFi RSSI Scanner Node (if LoRa disabled)
    wifi_rssi_node = Node(
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
        condition=UnlessCondition(LaunchConfiguration('use_lora')),
        output='screen'
    )

    # 4. SLAM Pose + Signal RSSI Fusion Node (Builds 3D Heatmap Grid)
    fuse_node = Node(
        package='signal_mapper',
        executable='fuse_node',
        name='signal_fuse_node',
        parameters=[{
            'cell_size': LaunchConfiguration('cell_size'),
            'csv_path': LaunchConfiguration('csv_path'),
            'map_frame': 'map',
            'base_frame': 'base_link',
            'publish_interval_sec': 1.0
        }],
        output='screen'
    )

    # 5. ESP32 Motor Serial Bridge Node (/cmd_vel -> ESP32)
    motor_node = Node(
        package='resqtether_bridge',
        executable='bridge_node',
        name='esp32_motor_bridge_node',
        parameters=[{
            'port': LaunchConfiguration('motor_port'),
            'baudrate': 115200,
            'rate_hz': 20.0
        }],
        condition=IfCondition(LaunchConfiguration('use_motors')),
        output='screen'
    )

    # 6. High-Performance Camera & Human Detection Node
    human_detect_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(human_detect_pkg, 'launch', 'human_detect.launch.py')
        ),
        launch_arguments={
            'camera_source': 'usb',
            'camera_index': LaunchConfiguration('camera_index'),
            'fps': '30.0',
            'confidence_threshold': '0.4'
        }.items(),
        condition=IfCondition(LaunchConfiguration('use_camera'))
    )

    # 7. Autonomous Signal-Aware Relay Decision Node
    relay_node = Node(
        package='resqtether_decision',
        executable='relay_wander_node',
        name='relay_wander_node',
        parameters=[{
            'signal_threshold_dbm': -70.0,
            'recovery_threshold_dbm': -67.0,
            'cruise_speed': 0.22,
            'turn_speed': 0.5,
            'obstacle_dist_m': 0.55
        }],
        condition=IfCondition(LaunchConfiguration('use_relay')),
        output='screen'
    )

    return LaunchDescription([
        lidar_port_arg,
        lidar_baud_arg,
        cell_size_arg,
        csv_path_arg,
        use_camera_arg,
        camera_index_arg,
        use_motors_arg,
        motor_port_arg,
        use_lora_arg,
        use_relay_arg,
        lora_port_arg,
        lidar_launch,
        slam_launch,
        lora_node,
        wifi_rssi_node,
        fuse_node,
        motor_node,
        human_detect_launch,
        relay_node
    ])
