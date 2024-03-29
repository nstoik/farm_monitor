"""Device tasks module."""

import pickle
from datetime import timedelta

from celery.utils.log import get_task_logger
from fm_database.database import get_session
from fm_database.models.message import Message

from fm_server.celery_runner import app
from fm_server.device.rabbitmq_messages import get_device_status

from .device_update import process_device_update

LOGGER = get_task_logger("fm.device.tasks")


@app.task(name="device.update")
def device_update(info):
    """Celery task for device update messages."""

    LOGGER.debug(f"Received device update from {info['id']}")

    return_code = process_device_update(info)

    if return_code is True:
        LOGGER.debug(f"Processed device update from {info['id']}")
    else:
        LOGGER.error(f"Failed to process device update from {info['id']}")

    return return_code


# TODO: Refactor this to use Celery comms model instead of the pika one.
# probably remove this completely as devices are created on first connect.
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
