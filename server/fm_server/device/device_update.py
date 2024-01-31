"""
Device update module.

This module processes updates that are sent to the device.
These updates are recevied from the celery task queue (tasks.py).
And results are sent back to device.

The update comes in as a dictionary (info) that looks like this:
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

from celery.utils.log import get_task_logger
from fm_database.base import get_session
from fm_database.models.device import Device, DeviceUpdate
from pydantic import ValidationError

from .info_model import DeviceUpdate as DeviceUpdateModel

LOGGER = get_task_logger("fm.device.tasks")


def process_device_update(info: dict) -> bool:
    """Process a device update."""

    session = get_session()

    try:
        update_data = DeviceUpdateModel.model_validate(info)
    except ValidationError as error:
        LOGGER.error(f"Invalid device update: {str(error)}")
        return False

    device = get_or_create_device(
        update_data.id,
        update_data.data.hardware_version,
        update_data.data.software_version,
    )

    device.hardware_version = update_data.data.hardware_version
    device.software_version = update_data.data.software_version
    device.grainbin_count = update_data.data.grainbin_count
    device.last_update_received = update_data.created_at
    device.total_updates += 1
    session.add(device)

    new_device_update = DeviceUpdate(device.id)
    new_device_update.timestamp = update_data.created_at
    new_device_update.update_index = device.total_updates
    new_device_update.interior_temp = update_data.data.interior_temp
    new_device_update.exterior_temp = update_data.data.exterior_temp

    session.add(new_device_update)
    session.commit()

    LOGGER.debug(f"New update saved for device. {new_device_update}")

    return True


def get_or_create_device(
    device_id: str, hardware_version: str, software_version: str
) -> Device:
    """Get or create a device."""

    device = Device.query.filter_by(device_id=device_id).one_or_none()

    if device is None:
        LOGGER.debug(f"Creating new device {device_id}")
        device = Device(device_id, hardware_version, software_version)
        device.save()
    else:
        LOGGER.debug(f"Found existing device {device_id}")

    return device
