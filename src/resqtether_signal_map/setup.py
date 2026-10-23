from setuptools import find_packages, setup

package_name = 'resqtether_signal_map'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='dsc',
    maintainer_email='chaathura.155@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'real_rssi_node = resqtether_signal_map.real_rssi_node:main',
            'signal_map_node = resqtether_signal_map.signal_map_node:main',
            'plot_rssi = resqtether_signal_map.plot_rssi:main',
        ],
    },
)
