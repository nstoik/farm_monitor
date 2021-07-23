# -*- coding: utf-8 -*-
"""Click commands for the database management."""
import click
from alembic import command as al_command
from alembic.config import Config as AlConfig

from fm_database.base import create_all_tables, drop_all_tables, get_base, get_session

# import all models so they are available to the SqlAlchemy base
# pylint: disable=unused-import
from fm_database.models.device import Device  # noqa: F401
from fm_database.models.message import Message  # noqa: F401
from fm_database.models.system import SystemSetup  # noqa: F401
from fm_database.models.user import User  # noqa: F401
from fm_database.settings import get_config


@click.group()
def create():
    """Command group for database create commands."""


@create.command()
@click.option(
    "--confirm",
    default=False,
    is_flag=True,
    help="Confirm this action. This will delete all previous database data.",
)
def delete_all_data(confirm):
    """Delete all data from the database."""

    if not confirm:
        click.echo(
            "Action was not confirmed (command option '--confirm'). No change made."
        )
    else:
        click.echo("deleting all data from the database.")

        base = get_base()
        session = get_session()
        for table in reversed(base.metadata.sorted_tables):
            session.execute(table.delete())
        session.commit()

        click.echo("done")


@create.command()
@click.pass_context
def recreate_database(ctx):
    """Drop and recreate database tables."""

    click.echo("dropping all tables")
    drop_all_tables()
    ctx.forward(create_tables)


@create.command()
def create_tables():
    """Create database tables."""

    click.echo("creating all tables")
    create_all_tables()

    config = get_config()
    alembic_cnf = AlConfig(config.PROJECT_ROOT + "/migrations/alembic.ini")
    alembic_cnf.set_main_option("script_location", config.PROJECT_ROOT + "/migrations")
    click.echo("stamping alembic head")
    al_command.stamp(alembic_cnf, "head")
    click.echo("done")


@click.option(
    "--username",
    default="admin",
    help="The username to use for the default user.",
)
@click.option(
    "--email",
    default="admin@farm_monitor.ca",
    help="The email to use for the default user.",
)
@click.option(
    "--password",
    default="farm_monitor",
    help="The password to use for the default user.",
)
@create.command()
def create_default_user(username, email, password):
    """Create a default admin user."""

    user = User("admin", "admin@farm_monitor.ca", "farm_monitor")
    user = User(username=username, email=email, password=password)
    user.is_admin = True
    user.save()
    click.echo(f"Default user '{username}' created.")
