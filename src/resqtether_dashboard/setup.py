from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'resqtether_dashboard'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'www'), glob('resqtether_dashboard/www/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='dsc',
    maintainer_email='chaathura.155@gmail.com',
    description='Unified Central Mission Command Web Dashboard for ResQTether',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'dashboard_node = resqtether_dashboard.dashboard_node:main',
        ],
    },
)
