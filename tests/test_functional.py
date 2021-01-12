"""Test functional aspects of the app."""

from fm_database.settings import TestConfig as DBTestConfig, get_config as db_get_config

from fm_server.settings import TestConfig, get_config


def test_main_env():
    """Test that the main environment variable is set for testing."""

    config = get_config()
    assert config == TestConfig

def test_database_env():
    """Test that the database environment is properly set using a fixture."""

    config = db_get_config()
    assert config == DBTestConfig
