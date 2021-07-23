# -*- coding: utf-8 -*-
"""fm_database setup module."""
from setuptools import find_packages, setup  # type: ignore [import]

__version__ = "0.1"


setup(
    name="fm_database",
    version=__version__,
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "click>=7",
        "sqlalchemy>=1.4",
        "passlib",
        "psycopg2",
        "alembic>=1.6",
    ],
    entry_points={"console_scripts": ["fm_database = fm_database.cli.cli:entry_point"]},
)
