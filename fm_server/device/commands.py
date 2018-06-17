""" device commands module """

import click

from .rabbitmq_messages import send_create_message


@click.command()
def send_create():
    """
    send a 'create' message via RabbitMQ to all connected
    devices
    """

    click.echo("sending create message to all devices")
    send_create_message()
