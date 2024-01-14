from setuptools import setup, find_packages

setup(
    name='clust_st',
    version='0.0.1',
    author='Data-Open-Algorithm',
    description='Spatio Temporal Clusters',
    url='https://github.com/Data-Open-Algorithms/clust_st',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.24.3',
        'pandas>=2.0.1'
    ]
)