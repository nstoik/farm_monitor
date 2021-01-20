"""Test the setup_commands module."""
import pytest
from click.testing import CliRunner
from fm_database.models.system import SystemSetup

from fm_server.cli.manage.setup_commands import first_setup


@pytest.mark.usefixtures("database_base_seed")
class TestSetupCommands:
    """Setup_commands module tests."""

    @staticmethod
    # pylint: disable=unused-argument
    def test_first_setup(dbsession):
        """First setup command test."""

        runner = CliRunner()
        result = runner.invoke(first_setup)

        assert not result.exception
        assert "first time setup\n" in result.output

    @staticmethod
    def test_first_setup_already_completed(dbsession):
        """Test the the cli command exits if setup already done."""

        # explicitly set first_setup_complete to True
        system = dbsession.query(SystemSetup).one()
        system.first_setup_complete = True
        system.save(dbsession)

        runner = CliRunner()
        result = runner.invoke(first_setup, input="N\n")

        assert not result.exception
        assert "Setup has already been run\n" in result.output
