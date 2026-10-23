import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    port_arg = DeclareLaunchArgument(
        'port',
        default_value='/dev/ttyUSB0',
        description='LoRa serial port device path (e.g. /dev/ttyUSB0, /dev/ttyUSB1)'
    )

    baudrate_arg = DeclareLaunchArgument(
        'baudrate',
        default_value='115200',
        description='LoRa serial baudrate (typically 115200)'
    )

    default_sender_id_arg = DeclareLaunchArgument(
        'default_sender_id',
        default_value='base_station',
        description='Default sender ID if packet lacks one'
    )

    lora_serial_node = Node(
        package='lora_bringup',
        executable='lora_serial_node',
        name='lora_serial_node',
        parameters=[{
            'port': LaunchConfiguration('port'),
            'baudrate': LaunchConfiguration('baudrate'),
            'default_sender_id': LaunchConfiguration('default_sender_id'),
            'timeout_sec': 0.5
        }],
        output='screen'
    )

    return LaunchDescription([
        port_arg,
        baudrate_arg,
        default_sender_id_arg,
        lora_serial_node
    ])
