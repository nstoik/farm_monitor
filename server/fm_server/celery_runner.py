"""Main celery module."""
# pylint: disable=unused-argument
import logging
from logging.handlers import RotatingFileHandler

from celery import Celery, signals

from .settings import get_config

app = Celery()

app.config_from_object("fm_server.settings:CeleryConfig")

# disabled for now
# @signals.setup_logging.connect
def setup_celery_logging(**kwargs):
    """Setup the logging for celery."""
    for key in kwargs.items():
        print(f"keyword arg: {key}: {kwargs[key]}")


@signals.after_setup_logger.connect
def after_celery_logging(logger, *args, **kwargs):
    """Sent after the setup of every global logger (not task loggers).

    Used to augment logging configuration.
    """
    config = get_config()
    celery_logger = logger

    logfile_path = config.CELERY_LOG_FILE
    log_level = config.CELERY_MAIN_PROCESS_LOG_LEVEL

    celery_logger.setLevel(log_level)

    celery_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    file_handler = RotatingFileHandler(
        logfile_path, mode="a", maxBytes=1024 * 1024, backupCount=10
    )
    file_handler.setFormatter(celery_formatter)
    celery_logger.addHandler(file_handler)


@signals.after_setup_task_logger.connect
def after_celery_task_logging(logger, *args, **kwargs):
    """Sent after the setup of every single task logger.

    Used to augment logging configuration.
    """
    config = get_config()

    logfile_path = config.CELERY_LOG_FILE
    log_level = config.LOG_LEVEL

    logger.setLevel(log_level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    file_handler = RotatingFileHandler(
        logfile_path, mode="a", maxBytes=1024 * 1024, backupCount=10
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # if log_level == logging.DEBUG:
    #     console_handler = logging.StreamHandler()
    #     console_handler.setFormatter(formatter)
    #     logger.addHandler(console_handler)
