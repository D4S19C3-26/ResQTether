from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    port_arg = DeclareLaunchArgument(
        'port',
        default_value='8090',
        description='Port for HTTP dashboard web server'
    )

    return LaunchDescription([
        port_arg,
        Node(
            package='resqtether_dashboard',
            executable='dashboard_node',
            name='central_dashboard_node',
            output='screen',
            parameters=[{'port': LaunchConfiguration('port')}]
        )
    ])
