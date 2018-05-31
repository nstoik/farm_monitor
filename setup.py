from setuptools import setup, find_packages

__version__ = '0.1'


setup(
    name='fm_server',
    version=__version__,
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'click',
        'pika',
    ],
    entry_points={
        'console_scripts': [
            'fm_server = fm_server.manage:cli'
        ]
    }
)
