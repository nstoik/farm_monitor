"""Test system models."""
import pytest

from fm_database.models.system import Hardware, Interface, Software, SystemSetup, Wifi


@pytest.mark.usefixtures("tables")
class TestSystemSetup:
    """SystemSetup model tests."""

    @staticmethod
    def test_create_systemsetup(dbsession):
        """Create a SystemSetup instance."""
        system_setup = SystemSetup()
        system_setup.save(dbsession)

        assert not bool(system_setup.first_setup_complete)
        assert not bool(system_setup.update_in_progress)
        assert not bool(system_setup.new_update_installed)
        assert system_setup.first_setup_time is None

    @staticmethod
    def test_systemsetup_get_by_id(dbsession):
        """Retrieve a SystemSetup by ID."""
        system_setup = SystemSetup()
        system_setup.save(dbsession)

        retrieved = SystemSetup.get_by_id(system_setup.id)
        assert retrieved == system_setup


@pytest.mark.usefixtures("tables")
class TestInterface:
    """Interface model tests."""

    @staticmethod
    def test_create_interface(dbsession):
        """Create a Interface instance."""
        interface = Interface("eth0")
        interface.save(dbsession)

        assert interface.interface == "eth0"
        assert bool(interface.is_active)
        assert not bool(interface.is_for_fm)
        assert not bool(interface.is_external)
        assert interface.state is None
        assert interface.credentials == []

    @staticmethod
    def test_interface_get_by_id(dbsession):
        """Retrieve an interface by the id."""
        interface = Interface("eth0")
        interface.save(dbsession)

        retrieved = Interface.get_by_id(interface.id)
        assert retrieved == interface


@pytest.mark.usefixtures("tables")
class TestWifi:
    """WiFi model tests."""

    @staticmethod
    def test_create_wifi(dbsession):
        """Create a WiFi instance."""
        wifi = Wifi()
        wifi.save(dbsession)

        assert wifi.name == "FarmMonitor"
        assert wifi.password == "raspberry"
        assert wifi.mode == "wpa"
        assert wifi.interface_id is None
        assert wifi.interface is None

    @staticmethod
    def test_create_wifi_with_interface(dbsession):
        """Create a WiFi instance with an interface."""
        interface = Interface("eth0")
        interface.save(dbsession)

        wifi = Wifi()
        wifi.interface = interface
        wifi.save(dbsession)

        assert wifi.interface == interface
        assert wifi.interface_id == interface.id

    @staticmethod
    def test_wifi_get_by_id(dbsession):
        """Test retrieving a WiFi instance by id."""
        wifi = Wifi()
        wifi.save(dbsession)

        retrieved = Wifi.get_by_id(wifi.id)

        assert retrieved == wifi


@pytest.mark.usefixtures("tables")
class TestHardware:
    """Hardware model tests."""

    @staticmethod
    def test_create_hardware(dbsession):
        """Create a Hardware instance."""
        hardware = Hardware()
        hardware.save(dbsession)

        assert hardware.device_name is None
        assert hardware.hardware_version is None
        assert hardware.serial_number is None

    @staticmethod
    def test_hardware_get_by_id(dbsession):
        """Retrieve a Hardware instance by the id."""
        hardware = Hardware()
        hardware.save(dbsession)

        retrieved = Hardware.get_by_id(hardware.id)
        assert retrieved == hardware


@pytest.mark.usefixtures("tables")
class TestSoftware:
    """Software model tests."""

    @staticmethod
    def test_create_software(dbsession):
        """Create a Software instance."""
        software = Software()
        software.save(dbsession)

        assert software.software_version is None
        assert software.software_version_last is None

    @staticmethod
    def test_software_get_by_id(dbsession):
        """Retrieve a Software instance by the id."""
        software = Software()
        software.save(dbsession)

        retrieved = Software.get_by_id(software.id)
        assert retrieved == software
