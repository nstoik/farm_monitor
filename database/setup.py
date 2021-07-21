# -*- coding: utf-8 -*-
"""fm_database setup module."""
from setuptools import find_packages, setup  # type: ignore [import]

__version__ = "0.1"


setup(
    name="fm_database",
    version=__version__,
    packages=find_packages(exclude=["tests"]),
    install_requires=["click", "sqlalchemy", "passlib", "psycopg2"],
    entry_points={"console_scripts": ["fm_database = fm_database.cli.cli:entry_point"]},
)
