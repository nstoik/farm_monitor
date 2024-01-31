"""
Grainbin update module.

This module processes the grainbin updates that are received.
These updates are recevied from the celery task queue (tasks.py).
Results are sent back to the device.

The update comes in as a dictionary (info) that looks like this:
info: {
    created_at: "2020-01-01 00:00:00",
    name: "my_device_id.01",
    bus_number: "1",
    bus_number_string: "bus.1",
    sensor_names: ["28.1234567890", "28.1234567891", "28.1234567892"],
    sensor_data: [
        {sensor_name: "28.1234567890", temperature: "20.0", temphigh: "50.0", templow: "10.0"},
        {sensor_name: "28.1234567891", temperature: "21.0", temphigh: "50.0", templow: "10.0"},
        {sensor_name: "28.1234567892", temperature: "22.0", temphigh: "50.0", templow: "10.0"},
    ],
    average_temp: "21.0",
}
"""

from celery.utils.log import get_task_logger
from fm_database.base import get_session
from fm_database.models.device import Device, Grainbin, GrainbinUpdate
from pydantic import ValidationError

from .info_model import GrainbinUpdate as GrainbinUpdateModel

LOGGER = get_task_logger("fm.grainbin.tasks")


def process_grainbin_update(info: dict) -> bool:
    """Process a grainbin update."""

    try:
        update_data = GrainbinUpdateModel.model_validate(info)
    except ValidationError as error:
        LOGGER.error(f"Invalid grainbin update: {str(error)}")
        return False

    session = get_session()

    # Confirm the device exists
    device = (
        session.query(Device).filter_by(device_id=update_data.device_id).one_or_none()
    )
    if device is None:
        LOGGER.error(f"Device '{update_data.device_id}' not found.")
        session.close()
        return False

    grainbin = get_or_create_grainbin(
        update_data.device_id, update_data.bus_number, update_data.bus_number_string
    )
    session.add(grainbin)

    grainbin.total_updates += 1
    grainbin.average_temp = update_data.average_temp

    for sensor in update_data.sensor_data:
        grainbin_update = GrainbinUpdate(grainbin.id)
        grainbin_update.timestamp = update_data.created_at
        grainbin_update.update_index = grainbin.total_updates
        grainbin_update.sensor_name = sensor.sensor_name
        grainbin_update.temperature = sensor.temperature
        grainbin_update.temphigh = sensor.temphigh
        grainbin_update.templow = sensor.templow

        LOGGER.debug(f"New grainbin update: {grainbin_update}")
        session.add(grainbin_update)

    session.commit()

    return True


def get_or_create_grainbin(
    device_id: None | str, bus_number: int, bus_number_string: str
) -> Grainbin:
    """Get or create a grainbin."""
    grainbin = Grainbin.query.filter_by(
        device_id=device_id, bus_number=bus_number
    ).one_or_none()

    if grainbin is None:
        grainbin = Grainbin(device_id, bus_number)
        grainbin.bus_number_string = bus_number_string
        LOGGER.debug(f"Creating new grainbin: {grainbin}")
        grainbin.save()
    else:
        LOGGER.debug(f"Found existing grainbin: {grainbin}")
    return grainbin
