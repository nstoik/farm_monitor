# -*- coding: utf-8 -*-
"""Application configuration."""
import os


class Config:  # pylint: disable=too-few-public-methods
    """Base configuration."""

    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_DATABASE_URI = "postgresql://fm:farm_monitor@database/farm_monitor.db"


class ProdConfig(Config):  # pylint: disable=too-few-public-methods
    """Production configuration."""

    ENV = "prod"
    DEBUG = False


class DevConfig(Config):  # pylint: disable=too-few-public-methods
    """Development configuration."""

    ENV = "dev"
    DEBUG = True


class TestConfig(Config):  # pylint: disable=too-few-public-methods
    """Test configuration."""

    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/fm_monitor_test_db.sqlite"


def get_config(override_default=None):
    """Return the Config option based on environment variables.

    If override_default is passed, that configuration is used instead.
    If there is no match or nothing set then the environment defaults to 'dev'.
    """

    if override_default is None:
        environment = os.environ.get("FM_DATABASE_CONFIG", default="dev")
    else:
        environment = override_default

    if environment == "dev":
        return DevConfig
    if environment == "prod":
        return ProdConfig
    if environment == "test":
        return TestConfig
    return DevConfig
