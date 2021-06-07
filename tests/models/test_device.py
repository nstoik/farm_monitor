"""Test device models."""
import datetime as dt

import pytest

from fm_database.models.device import (
    Device,
    Grainbin,
    TemperatureCable,
    TemperatureSensor,
)

from ..factories import (
    DeviceFactory,
    GrainbinFactory,
    TemperatureCableFactory,
    TemperatureSensorFactory,
)


@pytest.mark.usefixtures("tables")
class TestTemperatureSensor:
    """Temperature Sensor model tests."""

    @staticmethod
    def test_create_temperature_sensor():
        """Create a temperature sensor instance."""
        temperature_cable = TemperatureCableFactory()
        temperature_cable.save()

        temperature_sensor = TemperatureSensor(temperature_cable.id)
        temperature_sensor.save()

        assert temperature_sensor.cable_id == temperature_cable.id
        assert temperature_sensor.last_value == "unknown"

    @staticmethod
    def test_get_temperature_sensor_by_id():
        """Test retrieving a temperature sensor by its id."""
        temperature_cable = TemperatureCableFactory()
        temperature_cable.save()

        temperature_sensor = TemperatureSensor(temperature_cable.id)
        temperature_sensor.save()

        retrieved = TemperatureSensor.get_by_id(temperature_sensor.id)
        assert retrieved.id == temperature_sensor.id

    @staticmethod
    def test_temperature_sensor_factory():
        """Test the TemperatureSensor factory."""
        temperature_sensor = TemperatureSensorFactory()
        temperature_sensor.save()

        retrieved = TemperatureSensor.get_by_id(temperature_sensor.id)
        assert retrieved.id == temperature_sensor.id

    @staticmethod
    def test_temperature_sensor_properties():
        """Test TemperatureSensor properties."""
        temperature_sensor = TemperatureSensorFactory()
        temperature_sensor.save()

        assert temperature_sensor.templow is None
        assert temperature_sensor.temphigh is None
        assert temperature_sensor.last_value == "unknown"
        assert isinstance(temperature_sensor.cable_id, int)

    @staticmethod
    def test_multiple_temperature_sensors_per_cable():
        """Test adding multiple temperature sensors to the same cable."""
        temperature_cable = TemperatureCableFactory()
        temperature_cable.save()

        for _ in range(5):
            sensor = TemperatureSensor(temperature_cable.id)
            sensor.save()

        assert isinstance(temperature_cable.sensors, list)
        assert len(temperature_cable.sensors) == 5


@pytest.mark.usefixtures("tables")
class TestTemperatureCable:
    """Temperature Cable model tests."""

    @staticmethod
    def test_create_temperature_cable():
        """Create a temperature cable instance."""
        grainbin = GrainbinFactory()
        grainbin.save()

        temperature_cable = TemperatureCable(grainbin.id)
        temperature_cable.save()

        assert temperature_cable.grainbin_id == grainbin.id

    @staticmethod
    def test_get_temperature_cable_by_id():
        """Test retrieving a temperature cable by its id."""
        grainbin = GrainbinFactory()
        grainbin.save()

        temperature_cable = TemperatureCable(grainbin.id)
        temperature_cable.save()

        retrieved = TemperatureCable.get_by_id(temperature_cable.id)
        assert retrieved.id == temperature_cable.id

    @staticmethod
    def test_temperature_cable_factory():
        """Test the TemperatureCable factory."""
        temperature_cable = TemperatureCableFactory()
        temperature_cable.save()

        retrieved = TemperatureCable.get_by_id(temperature_cable.id)
        assert retrieved.id == temperature_cable.id

    @staticmethod
    def test_temperature_cable_properties():
        """Test TemperatureCable properties."""
        temperature_cable = TemperatureCableFactory()
        temperature_cable.save()

        assert temperature_cable.sensor_count == 0
        assert temperature_cable.cable_type == "temperature"
        assert temperature_cable.bin_cable_number == 0
        assert isinstance(temperature_cable.grainbin_id, int)

    @staticmethod
    def test_multiple_temperature_cables_per_bin():
        """Test adding multiple temperature cables to the same grainbin."""
        grainbin = GrainbinFactory()
        grainbin.save()

        for _ in range(5):
            cable = TemperatureCable(grainbin.id)
            cable.save()

        assert isinstance(grainbin.cables, list)
        assert len(grainbin.cables) == 5


@pytest.mark.usefixtures("tables")
class TestGrainbin:
    """Grainbin model tests."""

    @staticmethod
    def test_create_grainbin():
        """Create a grainbin instance."""
        device = DeviceFactory()
        device.save()
        grainbin = Grainbin(device_id=device.id, bus_number=1)
        grainbin.save()

        assert grainbin.device_id == device.id
        assert grainbin.bus_number == 1

    @staticmethod
    def test_get_grainbin_by_id():
        """Test retrieving a grainbin by its ID."""
        device = DeviceFactory()
        device.save()
        grainbin = Grainbin(device_id=device.id, bus_number=1)
        grainbin.save()

        retrieved = Grainbin.get_by_id(grainbin.id)

        assert grainbin.id == retrieved.id

    @staticmethod
    def test_grainbin_factory():
        """Test GrainbinFactory."""

        grainbin = GrainbinFactory()
        grainbin.save()

        retrieved = Grainbin.get_by_id(grainbin.id)
        device = Device.get_by_id(grainbin.device_id)

        assert grainbin.id == retrieved.id
        assert isinstance(grainbin.device_id, int)
        assert isinstance(device, Device)

    @staticmethod
    def test_grainbin_properties():
        """Test all Grainbin properties."""
        grainbin = GrainbinFactory()
        grainbin.save()

        assert isinstance(grainbin.creation_time, dt.datetime)
        assert isinstance(grainbin.last_updated, dt.datetime)
        assert grainbin.name == "New"
        assert grainbin.grainbin_type == "standard"
        assert grainbin.sensor_type == "temperature"
        assert grainbin.location == "Not Set"
        assert grainbin.description == "Not Set"
        assert isinstance(grainbin.total_updates, int)
        assert grainbin.average_temp is None
        assert isinstance(grainbin.bus_number, int)
        assert not grainbin.user_configured


@pytest.mark.usefixtures("tables")
class TestDevice:
    """Device model tests."""

    @staticmethod
    def test_create_device():
        """Create a device instance."""

        device = Device(
            device_id="Test Device", hardware_version="1", software_version="1"
        )
        device.save()

        assert device.device_id == "Test Device"
        assert device.hardware_version == "1"
        assert device.software_version == "1"

    @staticmethod
    def test_get_device_by_id():
        """Test retrieving a device by its ID."""

        device = Device(
            device_id="Test Device", hardware_version="1", software_version="1"
        )
        device.save()

        retrieved = Device.get_by_id(device.id)

        assert device.id == retrieved.id

    @staticmethod
    def test_device_factory():
        """Test DeviceFactory."""

        device = DeviceFactory()
        device.save()

        retrieved = Device.get_by_id(device.id)

        assert device.id == retrieved.id

    @staticmethod
    def test_device_properties():
        """Test all Device properties."""

        device = DeviceFactory()
        device.save()

        assert isinstance(device.creation_time, dt.datetime)
        assert isinstance(device.last_updated, dt.datetime)
        assert device.name == "not set"
        assert device.location == "not set"
        assert device.description == "not set"
        assert not bool(device.connected)
        assert not bool(device.user_configured)
        assert device.last_update_received is None
        assert device.interior_temp is None
        assert device.exterior_temp is None
        assert device.device_temp is None
        assert device.uptime is None
        assert device.current_time is None
        assert device.load_avg is None
        assert device.disk_total is None
        assert device.disk_used is None
        assert device.disk_free is None
