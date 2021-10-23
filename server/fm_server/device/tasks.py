"""Device tasks module."""
import pickle
from datetime import timedelta

from celery.utils.log import get_task_logger
from fm_database.base import get_session
from fm_database.models.device import Device, DeviceUpdate
from fm_database.models.message import Message

from fm_server.celery_runner import app
from fm_server.device.rabbitmq_messages import get_device_status

LOGGER = get_task_logger("fm.device.tasks")


@app.task(name="device.update")
def device_update(info):
    """Celery task for device update messages."""
    session = get_session()

    device_id = info["id"]
    hardware_version = info["data"]["hardware_version"]
    software_version = info["data"]["software_version"]
    LOGGER.debug(f"Received device update from {device_id}")
    device = session.query(Device).filter_by(device_id=device_id).one_or_none()

    # check if the device is already in the database. Create it if it is not.
    if device is None:
        LOGGER.info(f"Adding new device to the database. {device_id}")
        device = Device(device_id, hardware_version, software_version)
        device.save(session=session)
    else:
        device.hardware_version = hardware_version
        device.software_version = software_version
    device.grainbin_count = info["data"]["grainbin_count"]
    device.last_update_received = info["data"]["last_updated"]

    new_device_update = DeviceUpdate(device.id)
    new_device_update.timestamp = info["data"]["last_updated"]
    new_device_update.interior_temp = info["data"]["interior_temp"]
    new_device_update.exterior_temp = info["data"]["exterior_temp"]

    session.add(new_device_update)
    session.commit()

    LOGGER.debug(f"New update saved for device. {new_device_update}")

    return True


@app.task(name="device.create")
def device_create(info):
    """Celery task for device create messages.

    info is all required device information
    """

    device_id = info["id"]
    device_status = get_device_status(device_id)

    if device_status == "new":
        LOGGER.info(f"Device create message received from {device_id}")
        session = get_session()
        # check if a message has been recieved already
        saved_message = (
            session.query(Message)
            .filter(
                (Message.source == device_id) & (Message.classification == "create")
            )
            .first()
        )
        # if not, create a new message
        if not saved_message:
            saved_message = Message(device_id, "server", "create")
            session.add(saved_message)
        saved_message.payload = pickle.dumps(info)
        saved_message.set_datetime(valid_to=timedelta(minutes=30))
        session.commit()
        session.close()
    else:
        LOGGER.error(
            f"create message received from device {device_id} which is not connected"
        )
