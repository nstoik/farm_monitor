"""Test device models."""
import datetime as dt

import pytest

from fm_database.models.device import Device, DeviceUpdate, Grainbin, GrainbinUpdate

from ..factories import DeviceFactory, GrainbinFactory


@pytest.mark.usefixtures("tables")
class TestGrainbinUpdate:
    """GrainbinUpdate model tests."""

    @staticmethod
    def test_create_grainbin_update():
        """Create a GrainbinUpdate instance."""

        grainbin = GrainbinFactory()
        grainbin.save()

        grainbin_update = GrainbinUpdate(grainbin_id=grainbin.id)
        grainbin_update.timestamp = dt.datetime.now()
        grainbin_update.update_index = 0
        grainbin_update.save()

        assert grainbin_update.temperature is None
        assert grainbin_update.temphigh is None
        assert grainbin_update.templow is None
        assert grainbin_update.sensor_name is None

    @staticmethod
    def test_grainbin_update_properties():
        """Add all the properties to a GrainbinUpdate instance."""

        payload = {
            "created_at": dt.datetime.now(),
            "name": "10000000255c26b4.01",
            "bus_number": 1,
            "bus_number_string": "bus.1",
            "sensor_names": ["28.CC9A290D0000", "28.BC9A290D0000", "28.BBE5290D0000"],
            "sensor_data": [
                {
                    "temperature": 23.5,
                    "temphigh": 75,
                    "templow": 70,
                    "sensor_name": "28.CC9A290D0000",
                },
                {
                    "temperature": 23.5,
                    "temphigh": 75,
                    "templow": 70,
                    "sensor_name": "28.BC9A290D0000",
                },
                {
                    "temperature": 23.5,
                    "temphigh": 75,
                    "templow": 70,
                    "sensor_name": "28.BBE5290D0000",
                },
            ],
            "average_temp": 23.5,
        }

        grainbin = GrainbinFactory()
        grainbin.save()

        grainbin_update = GrainbinUpdate(grainbin_id=grainbin.id)
        grainbin_update.timestamp = payload["created_at"]
        grainbin_update.update_index = 0
        grainbin_update.temperature = payload["sensor_data"][0]["temperature"]
        grainbin_update.temphigh = payload["sensor_data"][0]["temphigh"]
        grainbin_update.templow = payload["sensor_data"][0]["templow"]
        grainbin_update.sensor_name = payload["sensor_data"][0]["sensor_name"]
        grainbin_update.save()

        retrieved: GrainbinUpdate = GrainbinUpdate.get_by_id(grainbin_update.id)

        assert retrieved.temperature == payload["sensor_data"][0]["temperature"]
        assert retrieved.temphigh == payload["sensor_data"][0]["temphigh"]
        assert retrieved.templow == payload["sensor_data"][0]["templow"]
        assert retrieved.sensor_name == payload["sensor_data"][0]["sensor_name"]
        assert retrieved.timestamp == payload["created_at"]


@pytest.mark.usefixtures("tables")
class TestGrainbin:
    """Grainbin model tests."""

    @staticmethod
    def test_create_grainbin():
        """Create a grainbin instance."""
        device = DeviceFactory()
        device.save()
        grainbin = Grainbin(device_id=device.device_id, bus_number=1)
        grainbin.save()

        assert grainbin.device_id == device.device_id
        assert grainbin.bus_number == 1
        assert grainbin.bus_number_string == "bus.1"

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
        device = Device.get_by_id(grainbin.device.id)

        assert grainbin.id == retrieved.id
        assert isinstance(grainbin.device_id, str)
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
        assert grainbin.total_updates == 0
        assert grainbin.average_temp is None
        assert isinstance(grainbin.bus_number, int)
        assert not grainbin.user_configured


@pytest.mark.usefixtures("tables")
class TestDeviceUpdate:
    """DeviceUpdate model tests."""

    @staticmethod
    def test_create_device_update():
        """Create a DeviceUpdate instance."""

        device = DeviceFactory()
        device.save()

        device_update = DeviceUpdate(device_id=device.id)
        device_update.timestamp = dt.datetime.now()
        device_update.update_index = 0
        device_update.save()

        retrieved = DeviceUpdate.get_by_id(device_update.id)

        assert retrieved.interior_temp is None
        assert retrieved.exterior_temp is None
        assert retrieved.device_temp is None
        assert retrieved.uptime is None
        assert retrieved.load_avg is None
        assert retrieved.disk_total is None
        assert retrieved.disk_used is None
        assert retrieved.disk_free is None

    @staticmethod
    def test_device_update_properties():
        """Add all the properties to a DeviceUpdate instance."""

        payload = {
            "created_at": dt.datetime.now(),
            "id": "10000000255c26b4",
            "data": {
                "device_id": "10000000255c26b4",
                "hardware_version": "pi3_0001",
                "software_version": "0.1",
                "interior_temp": 21.06,
                "exterior_temp": 20.85,
                "grainbin_count": 2,
                "last_updated": "2021-10-21T00:16:00.104077",
            },
        }

        device = DeviceFactory()
        device.save()

        device_update = DeviceUpdate(device_id=device.id)
        device_update.timestamp = payload["created_at"]
        device_update.update_index = 0
        device_update.interior_temp = payload["data"]["interior_temp"]
        device_update.exterior_temp = payload["data"]["exterior_temp"]
        device_update.save()

        retrieved = DeviceUpdate.get_by_id(device_update.id)

        assert retrieved.interior_temp == payload["data"]["interior_temp"]
        assert retrieved.exterior_temp == payload["data"]["exterior_temp"]
        assert retrieved.timestamp == payload["created_at"]


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
        assert device.total_updates == 0
