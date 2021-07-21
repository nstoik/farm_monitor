"""Test functional aspects of the app."""

from fm_database.models.system import SystemSetup
from fm_database.models.user import User
from fm_database.settings import TestConfig as DBTestConfig
from fm_database.settings import get_config as db_get_config

from fm_server.settings import TestConfig, get_config


def test_main_env():
    """Test that the main environment variable is set for testing."""

    config = get_config()
    assert config == TestConfig


def test_database_env():
    """Test that the database environment is properly set using a fixture."""

    config = db_get_config()
    assert config == DBTestConfig


# pylint: disable=unused-argument
def test_database_setup_for_testing(database_base_seed, dbsession):
    """Test that the database base seed is correctly added to the database."""

    system_setup = SystemSetup.query.first()

    assert not bool(system_setup.first_setup_complete)
    assert not bool(system_setup.update_in_progress)
    assert not bool(system_setup.new_update_installed)
    assert system_setup.first_setup_time is None

    user = User.query.filter_by(username="admin").first()

    assert user.username == "admin"
    assert user.email == "admin@mail.com"
    assert user.check_password("admin")
    assert bool(user.active)
    assert bool(user.is_admin)
