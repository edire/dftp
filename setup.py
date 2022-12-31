# setup.py placed at root directory
from setuptools import setup
setup(
    name='dftp',
    version='0.0.1',
    author='Eric Di Re',
    description='Dire Analytics Custom FTP Connections.',
    url='https://github.com/edire/dftp.git',
    python_requires='>=3.9',
    packages=['dftp'],
    install_requires=['paramiko', 'stat']
)