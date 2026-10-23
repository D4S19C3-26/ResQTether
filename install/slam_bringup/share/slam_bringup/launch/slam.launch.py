import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    pkg_share = get_package_share_directory('slam_bringup')
    default_params_file = os.path.join(pkg_share, 'config', 'slam_params.yaml')

    # Launch arguments
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation (Gazebo) clock if true'
    )

    params_file_arg = DeclareLaunchArgument(
        'params_file',
        default_value=default_params_file,
        description='Full path to the ROS2 parameters file to use for the slam_toolbox node'
    )

    laser_frame_arg = DeclareLaunchArgument(
        'laser_frame',
        default_value='laser_link',
        description='Frame ID of the laser sensor (e.g. laser_link or laser)'
    )

    # 1. Static transform: odom -> base_link (required when no wheel encoders exist)
    odom_to_base_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='odom_to_base_tf',
        arguments=['0', '0', '0', '0', '0', '0', 'odom', 'base_link'],
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}],
        output='screen'
    )

    # 2. Static transform: base_link -> laser_link
    base_to_laser_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='base_to_laser_tf',
        arguments=['0', '0', '0', '0', '0', '0', 'base_link', 'laser_link'],
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}],
        output='screen'
    )

    # Alias TF in case frame is named 'laser' instead of 'laser_link'
    laser_alias_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='laser_alias_tf',
        arguments=['0', '0', '0', '0', '0', '0', 'base_link', 'laser'],
        parameters=[{'use_sim_time': LaunchConfiguration('use_sim_time')}],
        output='screen'
    )

    # 3. Async SLAM Toolbox node
    slam_toolbox_node = Node(
        package='slam_toolbox',
        executable='async_slam_toolbox_node',
        name='slam_toolbox',
        parameters=[
            LaunchConfiguration('params_file'),
            {'use_sim_time': LaunchConfiguration('use_sim_time')}
        ],
        output='screen'
    )

    # 4. Lifecycle manager to automatically configure and activate slam_toolbox
    lifecycle_manager_node = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_slam',
        output='screen',
        parameters=[{
            'use_sim_time': LaunchConfiguration('use_sim_time'),
            'autostart': True,
            'node_names': ['slam_toolbox'],
            'bond_timeout': 0.0
        }]
    )

    return LaunchDescription([
        use_sim_time_arg,
        params_file_arg,
        laser_frame_arg,
        odom_to_base_tf,
        base_to_laser_tf,
        laser_alias_tf,
        slam_toolbox_node,
        lifecycle_manager_node
    ])
