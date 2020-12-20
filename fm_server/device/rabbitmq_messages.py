"""Device RabbitMQ messages module."""
import json
import logging
import time

import pika

from fm_server.settings import get_config

LOGGER = logging.getLogger("fd.device.rabbitmq")


def get_connection(config=None):
    """This method connects to RabbitMQ, returning the connection handle.

    When the connection is established, the on_connection_open method
    will be invoked by pika.

    :rtype: pika.SelectConnection

    """
    LOGGER.info("Connecting to RabbitMQ")
    if not config:
        config = get_config()

    user = config.RABBITMQ_USER
    password = config.RABBITMQ_PASSWORD
    virtual_host = config.RABBITMQ_VHOST
    host = config.RABBITMQ_HOST
    port = config.RABBITMQ_PORT

    creds = pika.PlainCredentials(user, password)
    params = pika.ConnectionParameters(
        host=host, port=port, virtual_host=virtual_host, credentials=creds
    )
    return pika.BlockingConnection(parameters=params)


def send_create_message(destination="all"):
    """Send a create message to 'destination' devices."""

    config = get_config()

    connection = get_connection(config=config)
    channel = connection.channel()

    exchange_name = config.RABBITMQ_MESSAGES_EXCHANGE_NAME
    exchange_type = config.RABBITMQ_MESSAGES_EXCHANGE_TYPE

    channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)

    routing_key = destination + ".create"
    message = {"command": "create"}
    channel.basic_publish(
        exchange=exchange_name,
        routing_key=routing_key,
        body=json.dumps(message, ensure_ascii=True),
    )
    LOGGER.debug(f"Sent message with key:{routing_key} to {exchange_name} exchange")
    connection.close()


def get_device_status(device_id):
    """Get the device status from the heartbeat service for a given device_id."""

    config = get_config()

    connection = get_connection(config=config)
    channel = connection.channel()

    exchange_name = config.RABBITMQ_MESSAGES_EXCHANGE_NAME
    exchange_type = config.RABBITMQ_MESSAGES_EXCHANGE_TYPE

    channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)
    method_frame = channel.queue_declare(queue="", exclusive=True, auto_delete=True)
    reply_queue = method_frame.method.queue
    properties = pika.BasicProperties(
        content_type="application/json", reply_to=reply_queue
    )
    routing_key = "_internal"
    message = {"command": "device_status", "id": device_id}

    channel.basic_publish(
        exchange=exchange_name,
        routing_key=routing_key,
        body=json.dumps(message, ensure_ascii=True),
        properties=properties,
    )

    LOGGER.info(f"Sent request for {device_id } status to {exchange_name} exchange")

    attempts = 0
    while attempts < 5:
        # pylint: disable=unused-variable
        method_frame, header_frame, body = channel.basic_get(reply_queue)
        if method_frame:
            connection.close()
            state = str(body, "utf-8")
            LOGGER.info(f"Returned status is {state}")
            return state

        LOGGER.debug("No return message received yet")
        time.sleep(1)
        attempts += 1

    LOGGER.warning("No return message received for device status message request")
    connection.close()
    return "disconnected"
