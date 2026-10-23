import os
import shutil
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    serial_port_arg = DeclareLaunchArgument(
        'serial_port',
        default_value='/dev/ttyUSB0',
        description='USB serial port device path (e.g. /dev/ttyUSB0)'
    )

    baudrate_arg = DeclareLaunchArgument(
        'baudrate',
        default_value='115200',
        description='Serial baudrate (115200 for A1/A2, 256000 for A3/S1/C1)'
    )

    frame_id_arg = DeclareLaunchArgument(
        'frame_id',
        default_value='laser_link',
        description='TF frame_id header for /scan messages'
    )

    inverted_arg = DeclareLaunchArgument(
        'inverted',
        default_value='false',
        description='Whether LiDAR is mounted inverted'
    )

    angle_compensate_arg = DeclareLaunchArgument(
        'angle_compensate',
        default_value='true',
        description='Enable hardware angle compensation'
    )

    # In ROS 2 Jazzy rplidar_ros binary is rplidar_composition
    # In older ROS 2 distros it was rplidar_node
    executable_name = 'rplidar_composition'
    if not os.path.exists('/opt/ros/jazzy/lib/rplidar_ros/rplidar_composition'):
        if os.path.exists('/opt/ros/jazzy/lib/rplidar_ros/rplidar_node'):
            executable_name = 'rplidar_node'

    lidar_driver_node = Node(
        package='rplidar_ros',
        executable=executable_name,
        name='rplidar_node',
        output='screen',
        parameters=[{
            'serial_port': LaunchConfiguration('serial_port'),
            'serial_baudrate': LaunchConfiguration('baudrate'),
            'frame_id': LaunchConfiguration('frame_id'),
            'inverted': LaunchConfiguration('inverted'),
            'angle_compensate': LaunchConfiguration('angle_compensate'),
            'scan_mode': 'Standard'
        }],
        remappings=[
            ('scan', '/scan')
        ]
    )

    return LaunchDescription([
        serial_port_arg,
        baudrate_arg,
        frame_id_arg,
        inverted_arg,
        angle_compensate_arg,
        lidar_driver_node
    ])
