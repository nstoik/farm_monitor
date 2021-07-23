"""Add Flask commands to CLI."""

import click
from flask.cli import FlaskGroup

from fm_api.app import create_app


@click.group(cls=FlaskGroup, create_app=create_app)
def flask_cli():
    """Add Flask to CLI."""
