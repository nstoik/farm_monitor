"""
Pydantic models for grainbin update messages.

The update comes in as a dictionary that looks like this:
info: {
    "created_at": "2020-01-01 00:00:00",
    "name": "my_device_id.01",
    "bus_number": "1",
    "bus_number_string": "bus.1",
    "sensor_names": ["28.1234567890", "28.1234567891", "28.1234567892"],
    "sensor_data": [
        {"sensor_name": "28.1234567890", "temperature": "20.0", "temphigh": "50", "templow": "10"},
        {"sensor_name": "28.1234567891", "temperature": "21.0", "temphigh": "50", "templow": "10"},
        {"sensor_name": "28.1234567892", "temperature": "22.0", "temphigh": "50", "templow": "10"},
    ],
    average_temp: "21.0",
}
"""

import logging
from datetime import datetime

from pydantic import BaseModel, ValidationInfo, computed_field, field_validator

LOGGER = logging.getLogger("fm.grainbin.info_model")


class GrainbinUpdateSensorData(BaseModel):
    """Grainbin update sensor data model."""

    sensor_name: str
    temperature: float | None
    temphigh: int
    templow: int

    # pylint: disable=unused-argument
    @field_validator("temperature", mode="before")
    @classmethod
    def temp_validator(cls, value: str, info: ValidationInfo) -> str | None:
        """
        Validate temperature.

        If the value is "U" then set is as None.
        Because the mode is "before" the value is a string (it hasn't been converted to a float yet)
        """
        if value == "U":
            LOGGER.warning("{info.field_name} value is 'U'. Setting to None.")
            return None
        return value


class GrainbinUpdate(BaseModel):
    """Grainbin update message model."""

    created_at: datetime
    name: str
    bus_number: int
    bus_number_string: str
    sensor_names: list[str]
    sensor_data: list[GrainbinUpdateSensorData]
    average_temp: str

    @computed_field  # type: ignore[misc]
    @property
    def device_id(self) -> str:
        """Return the device_id."""
        return self.name.split(".")[0]
