"""Define fixtures available to all tests."""
# pylint: disable=redefined-outer-name
import pytest
from _pytest.monkeypatch import MonkeyPatch
from fm_database.base import create_all_tables, drop_all_tables, get_session
from fm_database.models.system import SystemSetup
from fm_database.models.user import User


@pytest.fixture(scope="session")
# pylint: disable=unused-argument
def monkeysession(request):
    """Create a MonkeyPatch object that can be scoped to a session.

    https://github.com/pytest-dev/pytest/issues/363#issuecomment-289830794
    """
    mpatch = MonkeyPatch()
    yield mpatch
    mpatch.undo()


@pytest.fixture(scope="session", autouse=True)
# pylint: disable=unused-argument
def set_testing_env(monkeysession, database_env):
    """Set the environment variable for testing.

    This executes once for the entire session of testing.
    The environment variables are set back to the default after.
    Makes sure that the database env is also called and set.
    """
    monkeysession.setenv("FM_SERVER_CONFIG", "test")
    yield
    monkeysession.setenv("FM_SERVER_CONFIG", "dev")


@pytest.fixture(scope="session")
def database_env(monkeysession):
    """Set the fm_database env variable for testing and set back when done.."""
    monkeysession.setenv("FM_DATABASE_CONFIG", "test")
    yield
    monkeysession.setenv("FM_DATABASE_CONFIG", "dev")


@pytest.fixture(scope="session")
def dbsession():
    """Returns an sqlalchemy session."""

    yield get_session()


@pytest.fixture
def tables():
    """Create all tables for testing. Delete when done."""
    create_all_tables()
    yield
    drop_all_tables()


@pytest.fixture
# pylint: disable=unused-argument
def database_base_seed(dbsession, tables):
    """Enter the base configuration data into the database."""

    system = SystemSetup()
    dbsession.add(system)

    user = User(
        username="admin",
        email="admin@mail.com",
        password="admin",
        active=True,
        is_admin=True,
    )
    dbsession.add(user)

    dbsession.commit()
