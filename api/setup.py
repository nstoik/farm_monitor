"""Setup the application."""

from setuptools import find_packages, setup

__version__ = "0.1"


setup(
    name="fm_api",
    version=__version__,
    packages=find_packages(exclude=["tests"]),
    install_requires=[],
    entry_points={"console_scripts": ["fm_api = fm_api.cli.cli:entry_point"]},
)
