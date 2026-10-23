import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    frame_id_arg = DeclareLaunchArgument(
        'frame_id',
        default_value='laser_link',
        description='TF frame_id for fake laser scan'
    )

    rate_arg = DeclareLaunchArgument(
        'rate_hz',
        default_value='5.0',
        description='Publish frequency in Hz'
    )

    fake_lidar_node = Node(
        package='lidar_bringup',
        executable='fake_lidar_node',
        name='fake_lidar_node',
        parameters=[{
            'frame_id': LaunchConfiguration('frame_id'),
            'rate_hz': LaunchConfiguration('rate_hz'),
            'room_width': 10.0,
            'room_height': 6.0
        }],
        output='screen'
    )

    return LaunchDescription([
        frame_id_arg,
        rate_arg,
        fake_lidar_node
    ])
