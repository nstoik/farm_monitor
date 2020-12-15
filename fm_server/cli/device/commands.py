"""Click commands for device interaction."""

import click

from fm_server.device.rabbitmq_messages import send_create_message


@click.group()
def device():
    """Command group for device commands."""

@device.command()
def send_create():
    """send a 'create' message via RabbitMQ to all connected devices."""

    click.echo("sending create message to all devices")
    send_create_message()
