import os
import logging

class Config(object):
    """Base configuration."""

    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

    PRESENCE_PORT = 5554
    LOG_LEVEL = logging.INFO
    LOG_FILE = "/home/pi/farm_monitor/fl/farm_monitor.log"

    RRDTOOL_LOCATION = "/home/pi/farm_monitor/fd/rrd/"

    UPDATER_PATH = "/home/pi/farm_monitor/farm_update/update.sh"

    RABBITMQ_HOST = 'localhost'
    RABBITMQ_PORT = 5672
    RABBITMQ_USER = 'fm'
    RABBITMQ_PASSWORD = 'farm_monitor'
    RABBITMQ_VHOST = 'farm_monitor'

    RABBITMQ_HEARTBEAT_EXCHANGE_NAME = 'heartbeat_events'
    RABBITMQ_HEARTBEAT_EXCHANGE_TYPE = 'direct'
    RABBITMQ_HEARTBEAT_ROUTING_KEY = 'heartbeat'

    RABBITMQ_MESSAGES_EXCHANGE_NAME = 'device_messages'
    RABBITMQ_MESSAGES_EXCHANGE_TYPE = 'topic'

class DevConfig(Config):
    """Development configuration."""

    DEBUG = True
    LOG_LEVEL = logging.DEBUG


class ProdConfig(Config):
    """Production configuration."""

    DEBUG = False
    LOG_LEVEL = logging.ERROR


class TestConfig(Config):
    """Test configuration."""

    DEBUG = True
    TESTING = True


def get_config():

    environment = os.environ.get("FM_SERVER_CONFIG", default='dev')

    if environment == 'dev':
        return DevConfig
    elif environment == 'prod':
        return ProdConfig
    elif environment == 'test':
        return TestConfig
    else:
        return DevConfig
