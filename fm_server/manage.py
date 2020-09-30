""" fm_server manage module """

import click

from fm_server.device.commands import send_create
from .commands import first_setup
from .main import main

@click.group()
def cli():
    """Main entry point"""

@cli.command()
def run():
    """Run the server."""
    click.echo("Starting server")
    main()

cli.add_command(first_setup)

cli.add_command(send_create)
