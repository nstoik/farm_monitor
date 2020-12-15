""" device tasks module """
import logging
import pickle
from datetime import timedelta

from celery.utils.log import get_task_logger
from fm_database.base import get_session
from fm_database.models.message import Message

from fm_server.celery_runner import app
from fm_server.device.rabbitmq_messages import get_device_status

LOGGER = logging.getLogger('fm.device.tasks')
# LOGGER = get_task_logger('fm.device.tasks')

print(__name__)


@app.task(name='device.create')
def device_create(info):
    """ celery task for device create messages
    info is all required device information """

    device_id = info['id']
    device_status = get_device_status(device_id)

    if device_status == 'new':
        LOGGER.info(f'Device create message received from {device_id}')
        session = get_session()
        # check if a message has been recieved already
        saved_message = session.query(Message)\
                               .filter((Message.source == device_id) &
                                       (Message.classification == 'create'))\
                               .first()
        # if not, create a new message
        if not saved_message:
            saved_message = Message(device_id, 'server', 'create')
            session.add(saved_message)
        saved_message.payload = pickle.dumps(info)
        saved_message.set_datetime(valid_to=timedelta(minutes=30))
        session.commit()
        session.close()
    else:
        LOGGER.error(f"create message received from device {device_id} which is not connected")

    return
