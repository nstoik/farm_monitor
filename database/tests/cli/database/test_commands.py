"""Test the commands module."""
import pytest
from click.testing import CliRunner

from fm_database.cli.database.commands import create_default_user
from fm_database.models.user import User


@pytest.mark.usefixtures("tables")
class TestSetupCommands:
    """Commands module tests."""

    @staticmethod
    def test_create_default_user():
        """Test that a default user can be created with no options."""

        runner = CliRunner()
        result = runner.invoke(create_default_user)

        user = User.query.one()
        success_string = "Default user 'admin' created."

        assert not result.exception
        assert success_string in result.output
        assert isinstance(user, User)
        assert user.username == "admin"
        assert bool(user.check_password("farm_monitor"))
        assert bool(user.is_admin)

    @staticmethod
    def test_create_default_user_options():
        """Test that override options work to create a user."""

        runner = CliRunner()
        result = runner.invoke(
            create_default_user, ["--username", "Bob", "--password", "myprecious"]
        )

        user = User.query.one()
        success_string = "Default user 'Bob' created."

        assert not result.exception
        assert success_string in result.output
        assert isinstance(user, User)
        assert user.username == "Bob"
        assert bool(user.check_password("myprecious"))
        assert bool(user.is_admin)
