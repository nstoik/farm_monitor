"""Grainbin tasks module."""
from celery.utils.log import get_task_logger
from fm_database.base import get_session
from fm_database.models.device import Grainbin, GrainbinUpdate

from fm_server.celery_runner import app

LOGGER = get_task_logger("fm.grainbin.tasks")


@app.task(name="grainbin.update")
def grainbin_update(info):
    """Celery task for grainbin update messages."""
    session = get_session()

    # the device_id is found from the name which is in the form of DEVICE_ID.BIN_NUMBER
    # get all the characters up until the first '.'
    grainbin_name: str = info["name"]
    device_id = grainbin_name.split(".")[0]
    bus_number = info["bus_number"]
    LOGGER.debug(f"Received grainbin update from {grainbin_name}")

    grainbin = (
        session.query(Grainbin)
        .filter_by(device_id=device_id, bus_number=bus_number)
        .one_or_none()
    )

    if grainbin is None:
        LOGGER.info(f"Adding new grainbin to the databse. {grainbin_name}")
        grainbin = Grainbin(device_id=device_id, bus_number=bus_number)
        grainbin.bus_number_string = info["bus_number_string"]
        grainbin.save(session=session)

    grainbin.total_updates += 1
    grainbin.average_temp = info["average_temp"]

    sensor_data: list = info["sensor_data"]
    for sensor in sensor_data:
        new_grainbin_update = GrainbinUpdate(grainbin.id)
        new_grainbin_update.timestamp = info["created_at"]
        new_grainbin_update.update_index = grainbin.total_updates
        new_grainbin_update.sensor_name = sensor["sensor_name"]
        new_grainbin_update.temperature = sensor["temperature"]
        new_grainbin_update.temphigh = sensor["temphigh"]
        new_grainbin_update.templow = sensor["templow"]

        LOGGER.debug(f"New update saved for device. {new_grainbin_update}")
        session.add(new_grainbin_update)

    session.commit()

    return True
