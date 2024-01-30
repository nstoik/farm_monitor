"""Test the setup_commands module."""

from datetime import datetime

import pytest
from click.testing import CliRunner
from fm_database.models.system import Hardware, Software, SystemSetup

from fm_server.cli.manage.setup_commands import first_setup


@pytest.mark.usefixtures("database_base_seed")
class TestSetupCommands:
    """Setup_commands module tests.

    TODO: add test for setting device name
    TODO: add test for setting interface details
    """

    @staticmethod
    def test_first_setup_execution():
        """Test that first_setup starts and executes."""

        runner = CliRunner()
        result = runner.invoke(first_setup)

        assert not result.exception
        assert "First time setup\n" in result.output

    @staticmethod
    def test_first_setup_already_completed(dbsession):
        """Test that the the cli command exits if setup already done."""

        # explicitly set first_setup_complete to True
        system = dbsession.query(SystemSetup).one()
        system.first_setup_complete = True
        system.save(dbsession)

        runner = CliRunner()
        result = runner.invoke(first_setup, input="N\n")

        assert not result.exception
        assert "Setup has already been run\n" in result.output

    @staticmethod
    def test_first_setup_no_to_all():
        """Test that first_setup works when all questions are anserwed no.

        Answer NO to changing device name, setting hardware information,
        setting software information, and setting interface details.
        """

        runner = CliRunner()
        result = runner.invoke(first_setup, input="N\nN\nN\nN")

        system = SystemSetup.query.one()

        assert not result.exception
        assert "First time setup is complete\n" in result.output
        assert bool(system.first_setup_complete)
        assert isinstance(system.first_setup_time, datetime)

    @staticmethod
    def test_first_setup_hardware_info():
        """Test setting hardware_info.

        Answer NO to changing device name, YES to setting hardware information,
        NO to setting software information, and NO to setting interface details.
        """

        runner = CliRunner()
        result = runner.invoke(first_setup, input="N\nY\n\n\nN\nN")

        hardware = Hardware.query.one()

        assert not result.exception
        assert "First time setup is complete\n" in result.output
        assert hardware.hardware_version == "pi3_0001"

    @staticmethod
    def test_first_setup_hardware_info_custom_input():
        """Test setting hardware_info with custom input.

        Answer NO to changing device name, YES to setting hardware information,
        NO to setting software information, and NO to setting interface details.
        """

        runner = CliRunner()
        result = runner.invoke(first_setup, input="N\nY\nTEST VERSION\nN\nN")

        hardware = Hardware.query.one()

        assert not result.exception
        assert "First time setup is complete\n" in result.output
        assert hardware.hardware_version == "TEST VERSION"

    @staticmethod
    def test_first_setup_software_version():
        """Test setting software_info.

        Answer NO to changing device name, NO to setting hardware information,
        YES to setting software information, and NO to setting interface details.
        """

        runner = CliRunner()
        result = runner.invoke(first_setup, input="N\nN\nY\nTEST SOFTWARE VERSION\nN")

        software = Software.query.one()

        assert not result.exception
        assert "First time setup is complete\n" in result.output
        assert software.software_version == "TEST SOFTWARE VERSION"
