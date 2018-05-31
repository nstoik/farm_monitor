""" fm_server manage module """

import click

from .commands import first_setup

@click.group()
def cli():
    """Main entry point"""

@cli.command()
def run():
    """Run the server."""
    click.echo("Starting server")
    from .main import main
    main()

cli.add_command(first_setup)
