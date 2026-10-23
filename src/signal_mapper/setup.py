from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'signal_mapper'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['tests', 'test']),
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
    description='Signal Strength Mapping and SLAM-LoRa Fusion',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'fuse_node = signal_mapper.fuse_node:main',
            'plot_heatmap = signal_mapper.plot_heatmap:main',
            'walk_controller = signal_mapper.walk_controller:main',
        ],
    },
)
