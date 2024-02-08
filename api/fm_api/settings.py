"""Application configuration."""

#  pylint: disable=too-few-public-methods
import os


class Config:
    """Base configuration."""

    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    TEST_PATH = os.path.join(PROJECT_ROOT, "tests")

    SECRET_KEY = os.environ.get("FM_API_SECRET", "secret-key")
    JWT_SECRET_KEY = os.environ.get("FM_API_JWT_SECRET", "secret-key")

    CORS_EXPOSE_HEADERS = ["X-Pagination"]

    # API prefix
    API_PREFIX = os.environ.get("FM_API_PREFIX", "/api")

    # For Flask-Smorest
    API_TITLE = "FM API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.2"
    OPENAPI_URL_PREFIX = os.environ.get("FM_API_OPENAPI_URL_PREFIX", "/api")
    OPENAPI_SWAGGER_UI_PATH = "/swagger"
    OPENAPI_SWAGGER_UI_URL = "https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/3.52.0/"


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
