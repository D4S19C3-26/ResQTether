from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'rover_bringup'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'rviz'), glob('rviz/*.rviz')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='dsc',
    maintainer_email='chaathura.155@gmail.com',
    description='Master full integration launch for rover system',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'motor_driver_node = rover_bringup.motor_driver_node:main',
            'keyboard_teleop = rover_bringup.keyboard_teleop:main',
        ],
    },
)
