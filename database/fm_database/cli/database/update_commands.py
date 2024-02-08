"""Click commands for the database update commands."""

import click
from alembic import command as al_command
from alembic.config import Config as AlConfig

from fm_database.settings import get_config


@click.group()
def update():
    """Command group for database update commands."""


@update.command()
@click.option(
    "--message",
    prompt="Provide a message for the revision",
    help="Message for revision",
)
def create_revision(message):
    """Create a database migration using alembic."""

    config = get_config()
    alembic_cnf = AlConfig(config.PROJECT_ROOT + "/migrations/alembic.ini")
    alembic_cnf.set_main_option("script_location", config.PROJECT_ROOT + "/migrations")

    al_command.revision(alembic_cnf, message=message, autogenerate=True)


@update.command()
@click.option(
    "--revision",
    default="head",
    prompt="What revision to upgrade to?",
    help="What revision to upgrade to",
)
def database_upgrade(revision):
    """Upgrade database to given revision."""

    config = get_config()
    alembic_cnf = AlConfig(config.PROJECT_ROOT + "/migrations/alembic.ini")
    alembic_cnf.set_main_option("script_location", config.PROJECT_ROOT + "/migrations")

    al_command.upgrade(alembic_cnf, revision)
