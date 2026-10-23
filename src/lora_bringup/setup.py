from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'lora_bringup'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='dsc',
    maintainer_email='chaathura.155@gmail.com',
    description='LoRa serial telemetry and simulation for ROS 2',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'lora_sim_node = lora_bringup.lora_sim_node:main',
            'lora_serial_node = lora_bringup.lora_serial_node:main',
        ],
    },
)
