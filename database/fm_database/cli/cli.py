# -*- coding: utf-8 -*-
"""Main command line interface entry point."""
import click

from .database import commands as database_commands
from .database import update_commands
from .testing import commands as testing_commands


@click.group()
def entry_point():
    """Entry point for CLI."""


entry_point.add_command(testing_commands.test)
entry_point.add_command(testing_commands.lint)

entry_point.add_command(update_commands.update)

entry_point.add_command(database_commands.create)
