"""Application configuration."""
# pylint: disable=too-few-public-methods

import logging
import os

from environs import Env

env = Env()
env.read_env()


class CeleryConfig:
    """Celery configuration."""

    # Broker settings.
    broker_url = "amqp://fm:farm_monitor@fm_rabbitmq/farm_monitor"

    # List of modules to import when the Celery worker starts.
    imports = ("fm_server.device.tasks", "fm_server.grainbin.tasks")

    # Using the database to store task state and results.
    result_backend = "rpc://"

    task_soft_time_limit = 60

    # retry forever
    broker_connection_max_retries = None


class Config:
    """Base configuration."""

    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

    PRESENCE_PORT = 5554

    LOG_LEVEL = env.log_level("FM_SERVER_LOG_LEVEL", default=logging.INFO)
    LOG_FILE = "/logs/farm_monitor.log"
    CELERY_LOG_FILE = "/logs/fm_celery.log"
    CELERY_MAIN_PROCESS_LOG_LEVEL = env.log_level(
        "FM_SERVER_CELERY_LOG_LEVEL", default=logging.INFO
    )

    RRDTOOL_LOCATION = "/home/pi/farm_monitor/fd/rrd/"

    UPDATER_PATH = "/home/pi/farm_monitor/farm_update/update.sh"

    RABBITMQ_HOST = "fm_rabbitmq"
    RABBITMQ_PORT = 5672
    RABBITMQ_USER = "fm"
    RABBITMQ_PASSWORD = "farm_monitor"
    RABBITMQ_VHOST = "farm_monitor"

    RABBITMQ_HEARTBEAT_EXCHANGE_NAME = "heartbeat_messages"
    RABBITMQ_HEARTBEAT_EXCHANGE_TYPE = "direct"
    RABBITMQ_HEARTBEAT_ROUTING_KEY = "heartbeat"

    RABBITMQ_MESSAGES_EXCHANGE_NAME = "device_messages"
    RABBITMQ_MESSAGES_EXCHANGE_TYPE = "topic"


class DevConfig(Config):
    """Development configuration."""

    DEBUG = True
    LOG_LEVEL = env.log_level("FM_SERVER_LOG_LEVEL", default=logging.DEBUG)


class ProdConfig(Config):
    """Production configuration."""

    DEBUG = False
    LOG_LEVEL = env.log_level("FM_SERVER_LOG_LEVEL", default=logging.WARNING)
    CELERY_MAIN_PROCESS_LOG_LEVEL = env.log_level(
        "FM_SERVER_CELERY_LOG_LEVEL", default=LOG_LEVEL
    )


class TestConfig(Config):
    """Test configuration."""

    DEBUG = True
    TESTING = True


def get_config(override_default=None):
    """Return the Config option based on environment variables.

    If override_default is passed, that configuration is used instead.
    If there is no match or nothing set then the environment defaults to 'dev'.
    """

    if override_default is None:
        environment = os.environ.get("FM_SERVER_CONFIG", default="dev")
    else:
        environment = override_default

    if environment == "dev":
        return DevConfig
    if environment == "prod":
        return ProdConfig
    if environment == "test":
        return TestConfig

    return DevConfig
