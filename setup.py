""" setup.py: see public setuptools docs for more detail """

import os
import re
import codecs
import setuptools

CURRENT_LOCATION = os.path.abspath(os.path.dirname(__file__))
VERSION_MATCH_REGEX = r"^VERSION = ['\"]([^'\"]*)['\"]"

# list of dependencies required for production use
DEPENDENCIES = [
    'click>=7',
    'pyyaml>=5',
    'click-repl>=0',
    'f5-sdk-python>=0',
    'f5-teem>=1'
]

def get_long_description():
    """ Get project description """
    with open('./README.md', 'r') as readme:
        return readme.read()

def read(*parts):
    """ Read file """
    with codecs.open(os.path.join(CURRENT_LOCATION, *parts), 'r') as _file:
        return _file.read()

def find_version(*file_paths):
    """ Parse version out of file

    Note: Assumes line "VERSION = x.x.x" exists
    """
    version_file = read(*file_paths)
    version_match = re.search(VERSION_MATCH_REGEX, version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setuptools.setup(
    name='f5-cli',
    version=find_version("f5cli", "constants.py"),
    description='F5 CLI',
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author='F5 Ecosystems Group',
    author_email='solutionsfeedback@f5.com',
    license='Apache License 2.0',
    url='',
    packages=setuptools.find_packages(
        exclude=[
            "test*",
            "test.*",
            "*.test"
        ]
    ),
    package_data={
        '': [
            '*.json',
            '*.yaml',
            '*.md',
            '*.rst'
        ]
    },
    entry_points={
        'console_scripts': [
            'f5 = f5cli.cli:cli'
        ]
    },
    install_requires=DEPENDENCIES
)
