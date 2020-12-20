"""Controller manager module."""
import time

import pika


def pika_test():
    """Test with Pika."""

    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="hello")
    channel.basic_publish(exchange="", routing_key="hello", body="Hello World!")

    print(" [x] Sent 'Hello World!'")
    time.sleep(15)
    connection.close()

    return
