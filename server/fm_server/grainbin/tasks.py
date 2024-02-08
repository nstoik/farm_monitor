"""Grainbin tasks module."""

from celery.utils.log import get_task_logger

from fm_server.celery_runner import app

from .grainbin_update import process_grainbin_update

LOGGER = get_task_logger("fm.grainbin.tasks")


@app.task(name="grainbin.update")
def grainbin_update(info):
    """Celery task for grainbin update messages."""

    LOGGER.debug(f"Received grainbin update from {info['name']}")

    return_code = process_grainbin_update(info)

    if return_code is True:
        LOGGER.debug(f"Processed grainbin update from {info['name']}")
    else:
        LOGGER.error(f"Failed to process grainbin update from {info['name']}")

    return return_code
