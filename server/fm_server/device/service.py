"""Device service package."""

import json
import logging
from typing import Dict

import pika
from fm_database.database import get_session
from fm_database.models.device import Device
from pika.adapters.utils.connection_workflow import AMQPConnectionWorkflowFailed

from fm_server.controller.receiver import Message, Receiver
from fm_server.settings import get_config

from .device_representation import DeviceRep

LOGGER = logging.getLogger("fm.device.service")

CONNECTED_DEVICES: Dict[str, DeviceRep] = {}
NEW_DEVICES: Dict[str, DeviceRep] = {}


class DeviceReceiver(Receiver):
    """Communicate with Devices via RabbitMQ."""

    def __init__(self, logger):
        """Overwrite the Receiver __init__."""
        super().__init__(logger)

        # pylint: disable=invalid-name
        self.HEARTBEAT_MESSAGES = None
        self.DEVICE_MESSAGES = None

    def on_channel_open(self, channel):
        """Overwrite the on_channel_open method.

        Run all of the normal on_channel_open commands, then
        create the HEARTBEAT_MESSAGES and DEVICE_MESSAGES objects.
        """
        super().on_channel_open(channel)

        self.HEARTBEAT_MESSAGES = HeartbeatMessage(self._connection, self._channel)
        self.DEVICE_MESSAGES = DeviceMessage(self._channel)

    def stop(self):
        """Overwrite the stop method.

        Stop the HEARTBEAT_MESSAGES and DEVICE_MESSAGES objects, then
        stop the rest of the items.
        """
        self.HEARTBEAT_MESSAGES.set_stopping(True)
        self.DEVICE_MESSAGES.set_stopping(True)
        self.HEARTBEAT_MESSAGES.stop_consuming()
        self.DEVICE_MESSAGES.stop_consuming()
        super().stop()


class HeartbeatMessage(Message):
    """Receive heartbeat messages from RabbitMQ."""

    DEVICE_CONNECTION_INTERVAL: int = 10

    def __init__(self, connection, channel):
        """Override the __init__ method from Message class.

        Create the logger instance, and set the required config info.
        Call the setup_exchange function to start the communication
        """
        super().__init__(channel)

        config = get_config()

        self.LOGGER = logging.getLogger("fm.device.service.heartbeat")

        self._session = get_session()
        self._connection = connection

        self.exchange_name = config.RABBITMQ_HEARTBEAT_EXCHANGE_NAME
        self.exchange_type = config.RABBITMQ_HEARTBEAT_EXCHANGE_TYPE
        self.routing_key = config.RABBITMQ_HEARTBEAT_ROUTING_KEY

        self.setup_exchange(self.exchange_name)

    def start_consuming(self):
        """Overwrite start_consuming method.

        Add the schedule_device_check method call.
        """
        super().start_consuming()
        self.schedule_device_check()

    def stop_consuming(self):
        """Overwrite the stop_consuming method.

        Close the database session.
        """
        self._session.close()
        super().stop_consuming()

    def schedule_device_check(self):
        """If we are not closing our connection to RabbitMQ, schedule another device check."""
        if self._stopping:
            return
        self._connection.ioloop.call_later(
            self.DEVICE_CONNECTION_INTERVAL, self.device_check
        )

    def device_check(self):
        """Check if a device is 'dead' or not."""
        for device in CONNECTED_DEVICES.copy().values():
            device.heartbeat()
            if not device.is_alive():
                self._session.query(Device).filter_by(
                    device_id=device.device_id
                ).update({Device.connected: False})
                self._session.commit()
                self.LOGGER.info(f"{device.device_id} is no longer connected")
                del CONNECTED_DEVICES[device.device_id]

        for device in NEW_DEVICES.copy().values():
            device.heartbeat()
            if not device.is_alive():
                self._session.query(Device).filter_by(
                    device_id=device.device_id
                ).update({Device.connected: False})
                self._session.commit()
                self.LOGGER.info(f"{device.device_id} is no longer connected")
                del NEW_DEVICES[device.device_id]

        self.schedule_device_check()

    def on_message(self, unused_channel, basic_deliver, properties, body):
        """Overwritten on_message method. Invoked when a message is delivered from RabbitMQ.

        Args:
            unused_channel (pika.channel.Channel): The channel object
            basic_deliver (pika.Spec.Basic.Deliver): basic_deliver method
            properties (pika.Spec.BasicProperties): properties
            body (str|unicode): The message body
        """
        # payload = json.loads(body)

        device_id = properties.app_id
        if device_id in CONNECTED_DEVICES:
            CONNECTED_DEVICES[device_id].on_message_received()
            return_message = "connected"
        else:
            return_message = self.on_new_device(device_id)

        self.acknowledge_message(basic_deliver.delivery_tag)

        reply_properties = pika.BasicProperties(
            correlation_id=properties.correlation_id
        )
        self._channel.basic_publish(
            exchange="",
            routing_key=properties.reply_to,
            properties=reply_properties,
            body=return_message,
        )

    def on_new_device(self, device_id):
        """Check if device has been configured or not when a new device connects."""

        device = self._session.query(Device).filter_by(device_id=device_id).first()

        # device has not been added to the db
        if not device:
            # device has been seen before
            if device_id in NEW_DEVICES:
                NEW_DEVICES[device_id].on_message_received()
            # device has not been seen before
            else:
                self.LOGGER.info(f"{device_id} connected. Has not been configured yet.")
                NEW_DEVICES[device_id] = DeviceRep(device_id)
            return "new"

        # device has been added to the db but was currently a NEW_DEVICE
        if device_id in NEW_DEVICES:
            self.LOGGER.info(f"{device_id} now connected and configured.")
            device_object = NEW_DEVICES.pop(device_id)
            device_object.on_message_received()
            CONNECTED_DEVICES[device_id] = device_object
        # device has been added to the db but has not been seen yet
        else:
            self.LOGGER.info(f"{device_id} connected.")
            CONNECTED_DEVICES[device_id] = DeviceRep(device_id)
        device.connected = True
        self._session.commit()
        return "connected"


class DeviceMessage(Message):
    """Receive and respond to internal message requests."""

    def __init__(self, channel):
        """Override the __init__ method from Message class.

        Create the logger instance, and set the required config info.
        Call the setup_exchange function to start the communication
        """
        super().__init__(channel)

        config = get_config()

        self.LOGGER = logging.getLogger("fm.device.service.messages")

        self.exchange_name = config.RABBITMQ_MESSAGES_EXCHANGE_NAME
        self.exchange_type = config.RABBITMQ_MESSAGES_EXCHANGE_TYPE
        self.routing_key = "_internal"

        self.setup_exchange(self.exchange_name)

    def on_message(self, unused_channel, basic_deliver, properties, body):
        """Invoked by pika when a message is delivered from RabbitMQ.

        The channel is passed for your convenience. The basic_deliver object that
        is passed in carries the exchange, routing key, delivery tag and
        a redelivered flag for the message. The properties passed in is an
        instance of BasicProperties with the message properties and the body
        is the message that was sent.

        :param pika.channel.Channel unused_channel: The channel object
        :param pika.Spec.Basic.Deliver: basic_deliver method
        :param pika.Spec.BasicProperties: properties
        :param str|unicode body: The message body

        """

        payload = json.loads(body)
        command = payload["command"]
        device_id = payload["id"]
        return_message = "done"

        LOGGER.debug(f"Received request {command} for {device_id}")

        if command == "device_status":
            if device_id in NEW_DEVICES:
                return_message = "new"
            elif device_id in CONNECTED_DEVICES:
                return_message = "connected"
            else:
                return_message = "disconnected"
        else:
            return_message = "unknown command"

        self.acknowledge_message(basic_deliver.delivery_tag)

        reply_properties = pika.BasicProperties()
        self._channel.basic_publish(
            exchange="",
            routing_key=properties.reply_to,
            properties=reply_properties,
            body=return_message,
        )


def run_device():
    """Run the device receiver."""
    device_receiver = DeviceReceiver(logger=LOGGER)

    try:
        device_receiver.run()
    except AMQPConnectionWorkflowFailed:
        LOGGER.error(
            "AMQPConnectionError. Device Service did not start. Is RabbitMQ server running?"
        )
    except KeyboardInterrupt:
        LOGGER.info("Stopping device receiver")
        device_receiver.stop()
