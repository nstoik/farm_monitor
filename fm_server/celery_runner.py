""" main celery module """
import logging
from logging.handlers import RotatingFileHandler
from celery import Celery, signals

from .settings import get_config


app = Celery()

app.config_from_object('fm_server.settings:CeleryConfig')

# @signals.setup_logging.connect
def setup_celery_logging(**kwargs):
    for key in kwargs:
        print("keyword arg: %s: %s" % (key, kwargs[key]))

# disabled because logging is handled by the systemd file
# @signals.after_setup_logger.connect
def after_celery_logging(logger, *args, **kwargs):
    config = get_config()

    logfile_path = config.CELERY_LOG_FILE
    log_level = logging.INFO

    logger.setLevel(log_level)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    file_handler = RotatingFileHandler(logfile_path, mode='a', maxBytes=1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)    

# disabled because logging is handled by the systemd file
# @signals.after_setup_task_logger.connect
def after_celery_task_logging(logger, *args, **kwargs):
    config = get_config()

    logfile_path = config.CELERY_LOG_FILE
    log_level = logging.INFO

    logger.setLevel(log_level)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    file_handler = RotatingFileHandler(logfile_path, mode='a', maxBytes=1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)   
