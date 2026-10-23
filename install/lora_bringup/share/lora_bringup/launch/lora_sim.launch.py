import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    rate_arg = DeclareLaunchArgument(
        'publish_rate_hz',
        default_value='1.0',
        description='Publish frequency in Hz'
    )

    sender_id_arg = DeclareLaunchArgument(
        'sender_id',
        default_value='base_station_01',
        description='Simulated transmitter node ID'
    )

    lora_sim_node = Node(
        package='lora_bringup',
        executable='lora_sim_node',
        name='lora_sim_node',
        parameters=[{
            'publish_rate_hz': LaunchConfiguration('publish_rate_hz'),
            'sender_id': LaunchConfiguration('sender_id'),
            'base_rssi': -65.0,
            'amplitude': 25.0,
            'period_sec': 60.0
        }],
        output='screen'
    )

    return LaunchDescription([
        rate_arg,
        sender_id_arg,
        lora_sim_node
    ])
