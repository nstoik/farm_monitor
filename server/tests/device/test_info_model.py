"""Tests for the info_model module."""

import pytest

from fm_server.device.info_model import DeviceUpdateData


class TestDeviceUpdateDataModel:
    """Test the DeviceUpdateData model."""

    def test_temp_validator_valid(self):
        """Test the temp_validator function with valid values."""

        data = DeviceUpdateData(
            hardware_version="1.0.0",
            software_version="1.0.0",
            grainbin_count="0",
            interior_temp="20.0",
            exterior_temp="20.0",
            last_updated="2021-01-01T00:00:00",
        )

        assert data.interior_temp == 20.0
        assert data.exterior_temp == 20.0

    def test_temp_validator_u_string(self):
        """Test the temp_validator function with the string 'U'."""

        data = DeviceUpdateData(
            hardware_version="1.0.0",
            software_version="1.0.0",
            grainbin_count="0",
            interior_temp="U",
            exterior_temp="U",
            last_updated="2021-01-01T00:00:00",
        )

        assert data.interior_temp is None
        assert data.exterior_temp is None

    def test_temp_validator_invalid(self):
        """Test the temp_validator function with an invalid value."""

        with pytest.raises(ValueError):
            DeviceUpdateData(
                hardware_version="1.0.0",
                software_version="1.0.0",
                grainbin_count="0",
                interior_temp="invalid",
                exterior_temp="invalid",
                last_updated="2021-01-01T00:00:00",
            )
