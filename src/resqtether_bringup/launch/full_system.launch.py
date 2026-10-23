from rover_bringup.launch.full_system_launch import generate_launch_description as _gen

# Re-export from rover_bringup
from launch import LaunchDescription
import os
from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    pkg = get_package_share_directory('rover_bringup')
    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg, 'launch', 'full_system.launch.py')
            )
        )
    ])
