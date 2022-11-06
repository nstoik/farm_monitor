"""
Pydantic models for grainbin update messages.

The update comes in as a dictionary that looks like this:
info: {
    created_at: "2020-01-01 00:00:00",
    name: "my_device_id.01",
    bus_number: "1",
    bus_number_string: "1",
    sensor_names: ["28.1234567890", "28.1234567891", "28.1234567892"],
    sensor_data: [
        {sensor_name: "28.1234567890", temperature: "20.0", temphigh: "50.0", templow: "10.0"},
        {sensor_name: "28.1234567891", temperature: "21.0", temphigh: "50.0", templow: "10.0"},
        {sensor_name: "28.1234567892", temperature: "22.0", temphigh: "50.0", templow: "10.0"},
    ],
    average_temp: "21.0",
}
"""
import logging
from datetime import datetime

from pydantic import BaseModel, NoneStr, validator

LOGGER = logging.getLogger("fm.grainbin.info_model")


class GrainbinUpdateSensorData(BaseModel):
    """Grainbin update sensor data model."""

    sensor_name: str
    temperature: float | None
    temphigh: int
    templow: int

    # pylint: disable=no-self-argument,unused-argument
    @validator("temperature", pre=True)
    def temp_validator(cls, value, field):
        """
        Validate temperature.

        If the value is "U" then set is as None.
        """
        if value == "U":
            LOGGER.warning("{field.name} value is 'U'. Setting to None.")
            return None
        return value


class GrainbinUpdate(BaseModel):
    """Grainbin update message model."""

    created_at: datetime
    name: str
    device_id: NoneStr = None
    bus_number: int
    bus_number_string: str
    sensor_names: list[str]
    sensor_data: list[GrainbinUpdateSensorData]
    average_temp: float

    # pylint: disable=no-self-argument,unused-argument
    @validator("device_id", always=True)
    def device_id_validator(cls, value, values):
        """
        Validate device_id.

        The device_id is the first part of the name.
        """

        return values["name"].split(".")[0]
