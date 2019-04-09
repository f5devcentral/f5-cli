""" setup.py: see public setuptools docs for more detail """
from setuptools import setup, find_packages

# list of dependencies required for production use
DEPENDENCIES = [
    'click==7.0',
    'pyyaml==5.1',
    'click-repl==0.1.6',
    'f5-cloud-sdk==0.9.0'
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
    dependency_links=[
        'https://***REMOVED***/artifactory/api/pypi/f5-cloud-solutions-pypi/simple'
    ],
    install_requires=DEPENDENCIES
)
