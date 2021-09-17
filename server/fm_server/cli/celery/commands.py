"""Click commands for Celery."""

from subprocess import run

import click


@click.command()
def run_worker():
    """Run the Celery worker."""

    celery_worker_command = [
        "celery",
        "--app",
        "fm_server.device.tasks",
        "worker",
        "-l",
        "INFO",
    ]

    run(celery_worker_command, check=True)
