"""Tests for the grainbin_update module."""

import pytest
from fm_database.models.device import Device, Grainbin
from sqlalchemy import select

from fm_server.grainbin.grainbin_update import (
    get_or_create_grainbin,
    process_grainbin_update,
)
from fm_server.grainbin.info_model import GrainbinUpdate

from ..factories import DeviceFactory, GrainbinFactory


@pytest.mark.usefixtures("tables")
class TestProcessGrainbinUpdate:
    """Tests for the proccess_grainbin_update function."""

    info = {
        "created_at": "2020-01-01 00:00:00",
        "name": "my_device_id.01",
        "bus_number": "1",
        "bus_number_string": "bus.1",
        "sensor_names": ["28.1234567890", "28.1234567891", "28.1234567892"],
        "sensor_data": [
            {
                "sensor_name": "28.1234567890",
                "temperature": "20.0",
                "temphigh": "50",
                "templow": "10",
            },
            {
                "sensor_name": "28.1234567891",
                "temperature": "21.0",
                "temphigh": "50",
                "templow": "10",
            },
            {
                "sensor_name": "28.1234567892",
                "temperature": "22.0",
                "temphigh": "50",
                "templow": "10",
            },
        ],
        "average_temp": "21.0",
    }

    def test_process_grainbin_update(self):
        """Test the process_grainbin_update function properly handles normal input."""

        DeviceFactory(device_id="my_device_id")

        return_value = process_grainbin_update(self.info)

        assert return_value is True

    def test_process_grainbin_update_new_grainbin(self, dbsession):
        """Test the process_grainbin_update function correctly creates a new grainbin."""

        DeviceFactory(device_id="my_device_id")

        process_grainbin_update(self.info)

        update_data = GrainbinUpdate.model_validate(self.info)

        grainbin = dbsession.scalars(
            select(Grainbin).where(Grainbin.device_id_str == "my_device_id")
        ).one_or_none()

        assert isinstance(grainbin, Grainbin)
        assert grainbin.device_id_str == update_data.device_id
        assert grainbin.bus_number == update_data.bus_number
        assert grainbin.bus_number_string == update_data.bus_number_string
        assert grainbin.average_temp == update_data.average_temp
        assert grainbin.total_updates == 1

    def test_process_grainbin_update_existing_grainbin(self, dbsession):
        """Test the process_grainbin_update function correctly updates an existing grainbin."""

        DeviceFactory(device_id="my_device_id")

        process_grainbin_update(self.info)

        grainbin = dbsession.scalars(
            select(Grainbin).where(Grainbin.device_id_str == "my_device_id")
        ).one_or_none()
        assert isinstance(grainbin, Grainbin)
        assert grainbin.total_updates == 1

        process_grainbin_update(self.info)

        assert grainbin.total_updates == 2

    def test_process_grainbin_update_no_device(self, caplog):
        """Test the process_grainbin_update function correctly handles a grainbin with no device."""

        return_value = process_grainbin_update(self.info)

        assert return_value is False
        assert "Device 'my_device_id' not found" in caplog.text

    def test_process_grainbin_update_invalid_temperature(self, dbsession):
        """Test the process_grainbin_update function correctly handles invalid temperature data."""

        self.info["sensor_data"][0]["temperature"] = "U"  # type: ignore[index]

        DeviceFactory(device_id="my_device_id")

        return_value = process_grainbin_update(self.info)

        grainbin = dbsession.scalars(
            select(Grainbin).where(Grainbin.device_id_str == "my_device_id")
        ).one_or_none()

        assert return_value is True
        assert isinstance(grainbin, Grainbin)
        assert grainbin.updates[0].temperature is None
        assert grainbin.updates[1].temperature == 21.0
        assert grainbin.updates[2].temperature == 22.0


@pytest.mark.usefixtures("tables")
class TestGetOrCreateGrainbin:
    """Tests for the get_or_create_grainbin function."""

    def test_get_or_create_grainbin_new(self):
        """Test the get_or_create_grainbin function properly creates a new grainbin."""

        device = DeviceFactory(device_id="my_device_id")

        grainbin = get_or_create_grainbin(device.device_id, 1, "bus.1")

        assert grainbin.device_id_str == device.device_id
        assert grainbin.bus_number == 1
        assert len(device.grainbins) == 1

    def test_get_or_create_grainbin_existing(self):
        """Test the get_or_create_grainbin function properly returns an existing grainbin."""

        grainbin = GrainbinFactory()
        device = Device.get_by_id(grainbin.device.id)

        retrieved = get_or_create_grainbin(
            device.device_id, grainbin.bus_number, grainbin.bus_number_string
        )

        assert device.device_id == grainbin.device_id_str
        assert retrieved.id == grainbin.id
