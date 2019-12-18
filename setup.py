""" setup.py: see public setuptools docs for more detail """
from setuptools import setup, find_packages

# list of dependencies required for production use
DEPENDENCIES = [
    'click==7.0',
    'pyyaml==3.13',
    'click-repl==0.1.6',
    'f5-sdk-python==0.9.0'
]

setup(
    name='f5-cli',
    version='0.9.0',
    description='F5 CLI',
    url='http://github.com/F5Networks/f5-cli',
    author='F5 Ecosystems Group',
    author_email='solutionsfeedback@f5.com',
    license='MIT',
    packages=find_packages(exclude=['tests']),
    package_data={'': ['*.json', '*.yaml', '*.md', '*.rst']},
    entry_points={
        'console_scripts': [
            'f5 = f5cli.cli:cli'
        ]
    },
    dependency_links=[
        'https://***REMOVED***/artifactory/api/pypi/f5-cloud-solutions-pypi/simple'
    ],
    install_requires=DEPENDENCIES
)
