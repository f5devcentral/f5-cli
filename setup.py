from setuptools import setup

setup(name='f5-cloud-cli',
      version='0.9.0',
      description='F5 Cloud CLI',
      url='http://github.com/F5Networks/f5-cloud-cli',
      author='F5 Ecosystems Group',
      author_email='solutionsfeedback@f5.com',
      license='MIT',
      packages=['f5cloudcli', 'f5cloudcli.commands', 'f5cloudcli.shared'],
      entry_points={
          'console_scripts': [
              'f5 = f5cloudcli.cli:cli'
          ]
      },
      zip_safe=False)
