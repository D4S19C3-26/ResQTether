import os
from glob import glob
from setuptools import setup

package_name = 'resqtether_human_detect'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'data'), glob('data/*.xml')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='user',
    maintainer_email='user@todo.todo',
    description='Human detection node using YOLOv8 and Multi-Scale Haar/HOG',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'human_detect_node = resqtether_human_detect.human_detect_node:main',
            'victim_locator_node = resqtether_human_detect.victim_locator_node:main'
        ],
    },
)
