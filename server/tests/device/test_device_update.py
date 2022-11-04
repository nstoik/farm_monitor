"""Tests for the device_update file."""
import pytest
from fm_database.models.device import Device

from fm_server.device.device_update import get_or_create_device, process_device_update
from fm_server.device.info_model import DeviceUpdate


@pytest.mark.usefixtures("tables")
class TestProcessDeviceUpdate:
    """Tests for the process_device_update function."""

    info = {
        "id": "device_id",
        "created_at": "2020-01-01 00:00:00",
        "data": {
            "hardware_version": "1.0.0",
            "software_version": "1.0.0",
            "grainbin_count": "1",
            "interior_temp": "20.0",
            "exterior_temp": "20.0",
            "last_updated": "2020-01-01 00:00:00",
        },
    }

    def test_process_device_update(self):
        """Test the process_device_update function properly handles normal input."""

        return_code = process_device_update(self.info)

        assert return_code is True

    def test_process_device_update_new_device(self):
        """Test the process_device_update function correctly creates a new device."""

        process_device_update(self.info)

        update_data = DeviceUpdate.parse_obj(self.info)

        device = Device.query.filter_by(device_id=update_data.id).first()

        assert device.device_id == update_data.id
        assert device.hardware_version == update_data.data.hardware_version
        assert device.software_version == update_data.data.software_version
        assert device.grainbin_count == update_data.data.grainbin_count
        assert device.last_update_received == update_data.data.last_updated
        assert device.total_updates == 1

    def test_process_device_update_existing_device(self):
        """Test the process_device_update function correctly updates an existing device."""

        process_device_update(self.info)

        device = Device.query.filter_by(device_id="device_id").first()
        assert device.total_updates == 1

        process_device_update(self.info)

        assert device.total_updates == 2

    def test_process_device_update_invalid_temperatures(self):
        """Test the process_device_update function correctly handles invalid temperatures.

        The invalid temperature that can occur is the string 'U' which indicates
        that the temperature is unknown or unable to be read. In this case, the temperature
        should be set to None.
        """

        self.info["data"]["interior_temp"] = "U"
        self.info["data"]["exterior_temp"] = "U"

        return_code = process_device_update(self.info)

        device = Device.query.filter_by(device_id="device_id").first()

        assert return_code is True
        assert device.updates[0].interior_temp is None
        assert device.updates[0].exterior_temp is None


@pytest.mark.usefixtures("tables")
class TestGetOrCreateDevice:
    """Tests for the get_or_create_device function."""

    def test_get_or_create_device_new(self):
        """Test the get_or_create_device function properly creates a new device."""

        device_id = "device_id"
        hardware_version = "1.0.0"
        software_version = "1.0.0"

        device = get_or_create_device(device_id, hardware_version, software_version)

        assert device.device_id == device_id
        assert device.hardware_version == hardware_version
        assert device.software_version == software_version
        assert device.grainbin_count == 0
        assert device.total_updates == 0

    def test_get_or_create_device_existing(self):
        """Test the get_or_create_device function properly returns an existing device."""

        device_id = "device_id"
        hardware_version = "1.0.0"
        software_version = "1.0.0"

        new_device = Device(device_id, hardware_version, software_version)
        new_device.save()

        device = get_or_create_device(device_id, hardware_version, software_version)

        assert device.id == new_device.id
