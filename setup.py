from setuptools import setup

setup(name='f5cloudcli',
      version='0.9.0',
      description='F5 CLoud CLI',
      url='http://github.com/F5Networks/f5-cloud-cli',
      author='F5 Ecosystems Group',
      author_email='solutionsfeedback@f5.com',
      license='MIT',
      packages=['f5cloudcli', 'f5cloudcli.commands', 'f5cloudcli.shared'],
      zip_safe=False)