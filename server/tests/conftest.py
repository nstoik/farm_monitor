"""Define fixtures available to all tests."""

# pylint: disable=redefined-outer-name
import pytest
from fm_database.base import create_all_tables, drop_all_tables, get_session
from fm_database.models.system import SystemSetup
from fm_database.models.user import User


@pytest.fixture(scope="session")
def dbsession():
    """Returns an sqlalchemy session."""

    yield get_session()


@pytest.fixture
def tables(dbsession):
    """Create all tables for testing. Delete when done."""
    create_all_tables()
    yield
    dbsession.close()
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
