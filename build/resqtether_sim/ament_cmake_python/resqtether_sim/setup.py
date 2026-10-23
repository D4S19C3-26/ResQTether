from setuptools import find_packages
from setuptools import setup

setup(
    name='resqtether_sim',
    version='0.0.0',
    packages=find_packages(
        include=('resqtether_sim', 'resqtether_sim.*')),
)
