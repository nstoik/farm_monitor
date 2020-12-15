# -*- coding: utf-8 -*-
"""Main command line interface entry point."""
import click

from .device import commands as device_commands
from .manage import commands as manage_commands
from .manage import setup_commands
from .testing import commands as testing_commands


@click.group()
def entry_point():
    """Entry point for CLI."""


entry_point.add_command(testing_commands.test)
entry_point.add_command(testing_commands.lint)

entry_point.add_command(manage_commands.run)

entry_point.add_command(setup_commands.first_setup)

entry_point.add_command(device_commands.device)
