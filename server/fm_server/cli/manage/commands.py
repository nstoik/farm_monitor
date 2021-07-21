"""Click commands for managing the app."""

import click

from fm_server.main import main


@click.command()
def run():
    """Run the server."""
    click.echo("Starting server")
    main()
