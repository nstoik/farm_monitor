"""
Pydantic models for device update messages.

The update comes in as a dictionary that looks like this:
info: {
    "id": "my_device_id",
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
"""
import logging
from datetime import datetime

from pydantic import BaseModel, validator

LOGGER = logging.getLogger("fm.device.info_model")


class DeviceUpdateData(BaseModel):
    """Device update data model."""

    hardware_version: str
    software_version: str
    grainbin_count: int = 0
    interior_temp: float | None
    exterior_temp: float | None
    last_updated: datetime

    # pylint: disable=no-self-argument,unused-argument
    @validator("interior_temp", "exterior_temp", pre=True)
    def temp_validator(cls, value, field):
        """
        Validate interior_temp or exterior_temp.

        If the value is "U" then set is as None.
        """
        if value == "U":
            LOGGER.warning("{field.name} value is 'U'. Setting to None.")
            return None
        return value


class DeviceUpdate(BaseModel):
    """Device update message model."""

    id: str
    created_at: datetime
    data: DeviceUpdateData
