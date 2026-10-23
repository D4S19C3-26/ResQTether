import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    camera_source_arg = DeclareLaunchArgument(
        'camera_source',
        default_value='usb',
        description='Camera source type (usb, csi, ip)'
    )
    
    camera_index_arg = DeclareLaunchArgument(
        'camera_index',
        default_value='0',
        description='USB Camera index if source is usb'
    )
    
    sensor_id_arg = DeclareLaunchArgument(
        'sensor_id',
        default_value='0',
        description='CSI Camera sensor ID if source is csi'
    )

    width_arg = DeclareLaunchArgument(
        'width',
        default_value='640',
        description='Image frame width'
    )

    height_arg = DeclareLaunchArgument(
        'height',
        default_value='480',
        description='Image frame height'
    )

    fps_arg = DeclareLaunchArgument(
        'fps',
        default_value='30.0',
        description='Streaming frame rate in FPS'
    )
    
    conf_thresh_arg = DeclareLaunchArgument(
        'confidence_threshold',
        default_value='0.4',
        description='Detection confidence threshold'
    )

    human_detect_node = Node(
        package='resqtether_human_detect',
        executable='human_detect_node',
        name='human_detect_node',
        output='screen',
        parameters=[{
            'camera_source': LaunchConfiguration('camera_source'),
            'camera_index': LaunchConfiguration('camera_index'),
            'sensor_id': LaunchConfiguration('sensor_id'),
            'width': LaunchConfiguration('width'),
            'height': LaunchConfiguration('height'),
            'fps': LaunchConfiguration('fps'),
            'confidence_threshold': LaunchConfiguration('confidence_threshold'),
        }]
    )

    return LaunchDescription([
        camera_source_arg,
        camera_index_arg,
        sensor_id_arg,
        width_arg,
        height_arg,
        fps_arg,
        conf_thresh_arg,
        human_detect_node
    ])
