""" setup.py: see public setuptools docs for more detail """
from setuptools import setup, find_packages

# This should be a list of dependencies required for production use only
DEPENDENCIES = [
    'click==7.0'
]

setup(
    name='f5-cloud-cli',
    version='0.9.0',
    description='F5 Cloud CLI',
    url='http://github.com/F5Networks/f5-cloud-cli',
    author='F5 Ecosystems Group',
    author_email='solutionsfeedback@f5.com',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': [
            'f5 = f5cloudcli.cli:cli'
        ]
    },
    install_requires=DEPENDENCIES
)
