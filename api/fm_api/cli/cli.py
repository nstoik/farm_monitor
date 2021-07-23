"""Main command line interface entry point."""
import click

from .manage import commands as manage_commands
from .manage import flask_commands
from .testing import commands as testing_commands


@click.group()
def entry_point():
    """Entry point for the CLI."""


entry_point.add_command(manage_commands.clean)
entry_point.add_command(manage_commands.urls)

entry_point.add_command(flask_commands.flask_cli)

entry_point.add_command(testing_commands.test)
entry_point.add_command(testing_commands.lint)
