"""Application configuration."""
#  pylint: disable=too-few-public-methods
import os


class Config:
    """Base configuration."""

    SECRET_KEY = os.environ.get("FM_API_SECRET", "secret-key")
    JWT_SECRET_KEY = os.environ.get("FM_API_JWT_SECRET", "secret-key")
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

    # For Flask-Smorest
    API_TITLE = "FM API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.2"
    OPENAPI_URL_PREFIX = "/doc"
    OPENAPI_SWAGGER_UI_PATH = "/swagger"
    OPENAPI_SWAGGER_UI_URL = "https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.52.0/"
    OPENAPI_SWAGGER_URL = "/swagger"


class ProdConfig(Config):
    """Production configuration."""

    ENV = "prod"
    DEBUG = False


class DevConfig(Config):
    """Development configuration."""

    ENV = "dev"
    DEBUG = True


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    DEBUG = True


def get_config(override_default=None):
    """Return the Config option based on environment variables.

    If override_default is passed, that configuration is used instead.
    If there is no match or nothing set then the environment defaults to 'dev'.
    """

    if override_default is None:
        environment = os.environ.get("FM_API_CONFIG", default="dev")
    else:
        environment = override_default

    if environment == "dev":
        return DevConfig
    if environment == "prod":
        return ProdConfig
    if environment == "test":
        return TestConfig

    return DevConfig
