import os
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='clust_st',
    version='0.0.1',
    author='Data-Open-Algorithm',
    description='Spatio Temporal Clusters',
    url='https://github.com/Data-Open-Algorithms/clust_st',
    packages=find_packages(),
    install_requires=required
)