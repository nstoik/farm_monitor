"""Tests for the info_model module."""

# ignore arg-type and list-item mypy errors in this file.
# This is test data to confirm validation works as expected.
# mypy: disable-error-code="arg-type,list-item"

import pytest

from fm_server.grainbin.info_model import GrainbinUpdate, GrainbinUpdateSensorData


class TestGrainbinUpdateSensorDataModel:
    """Test the GrainbinUpdateSensorData model."""

    def test_temp_validator_valid(self):
        """Test the temp_validator function with valid values."""

        data = GrainbinUpdateSensorData(
            sensor_name="28.1234567890",
            temperature="20.0",
            temphigh="50",
            templow="10",
        )

        assert data.temperature == 20.0

    def test_temp_validator_u_string(self):
        """Test the temp_validator function with the string 'U'."""

        data = GrainbinUpdateSensorData(
            sensor_name="28.1234567890",
            temperature="U",
            temphigh="50",
            templow="10",
        )

        assert data.temperature is None

    def test_temp_validator_invalid(self):
        """Test the temp_validator function with an invalid value."""

        with pytest.raises(ValueError):
            GrainbinUpdateSensorData(
                sensor_name="28.1234567890",
                temperature="invalid",
                temphigh="50",
                templow="10",
            )


# pylint: disable=too-few-public-methods
class TestGrainbinUpdateDataModel:
    """Test the GrainbinUpdateData model."""

    def test_device_id_validator_valid(self):
        """Test the device_id_validator function with valid values."""

        data = GrainbinUpdate(
            created_at="2021-01-01T00:00:00",
            name="my_device_id.01",
            bus_number="1",
            bus_number_string="bus.1",
            sensor_names=["28.1234567890"],
            sensor_data=[
                {
                    "sensor_name": "28.1234567890",
                    "temperature": "20.0",
                    "temphigh": "50",
                    "templow": "10",
                },
            ],
            average_temp="20.0",
        )

        assert data.device_id == "my_device_id"
