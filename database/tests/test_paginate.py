"""Tests for the paginate class and method."""

import pytest
from sqlalchemy import select

from fm_database.database import create_all_tables, drop_all_tables
from fm_database.models.user import User
from fm_database.paginate import paginate

from .factories import UserFactory


# fixture to tables and 25 users for the paginate tests
@pytest.fixture(scope="module")
def setup_users(dbsession):
    """Create a bunch of users."""

    create_all_tables()
    dbsession.add_all([UserFactory() for _ in range(25)])
    dbsession.commit()
    yield
    dbsession.close()
    drop_all_tables()


@pytest.mark.usefixtures("setup_users")
def test_paginate_no_items(dbsession):
    """Test that the query paginates correctly when there are no items."""

    # Paginate the users
    select_stmt = select(User).where(User.id >= 1000).order_by(User.id)
    users = paginate(dbsession, select_stmt)
    assert len(users.items) == 0
    assert users.total == 0


@pytest.mark.usefixtures("setup_users")
def test_paginate(dbsession):
    """Test that the query paginates correctly."""

    # Paginate the users
    select_stmt = select(User).order_by(User.id)
    users = paginate(dbsession, select_stmt)
    assert len(users.items) == 20
    assert users.total == 25


@pytest.mark.usefixtures("setup_users")
def test_paginate_specify_page(dbsession):
    """Test that the query paginates correctly when page is given."""

    # Paginate the users
    select_stmt = select(User).order_by(User.id)
    users = paginate(dbsession, select_stmt, page=2)
    assert len(users.items) == 5
    assert users.total == 25


@pytest.mark.usefixtures("setup_users")
def test_paginate_specify_per_page(dbsession):
    """Test that the query paginates correctly when per_page is given."""

    # Paginate the users
    select_stmt = select(User).order_by(User.id)
    users = paginate(dbsession, select_stmt, per_page=10)
    assert len(users.items) == 10


@pytest.mark.usefixtures("setup_users")
def test_paginate_specify_max_per_page(dbsession):
    """Test that the query paginates correctly when max_per_page is given."""

    # Paginate the users
    select_stmt = select(User).order_by(User.id)
    users = paginate(dbsession, select_stmt, max_per_page=10)
    assert len(users.items) == 10
    assert users.total == 25


@pytest.mark.usefixtures("setup_users")
def test_paginate_invalid_page(dbsession):
    """Test that the query paginates correctly with an invalid page."""

    # Paginate the users
    select_stmt = select(User).order_by(User.id)
    assert paginate(dbsession, select_stmt, page=-1).page == 1
    assert len(paginate(dbsession, select_stmt, per_page=0).items) == 20
    assert len(paginate(dbsession, select_stmt, per_page=-1).items) == 20


@pytest.mark.usefixtures("setup_users")
def test_paginate_without_count(dbsession):
    """Test that the query paginates correctly when count is False."""

    # Paginate the users
    select_stmt = select(User).order_by(User.id)
    users = paginate(dbsession, select_stmt, count=False)
    assert len(users.items) == 20
    assert users.total is None


@pytest.mark.usefixtures("setup_users")
def test_paginate_property_first(dbsession):
    """Test the first property of the paginate class."""

    # Paginate the users
    select_stmt = select(User).order_by(User.id)
    users = paginate(dbsession, select_stmt, page=2)
    assert users.first == 21


@pytest.mark.usefixtures("setup_users")
def test_paginate_property_last(dbsession):
    """Test the last property of the paginate class."""

    # Paginate the users
    select_stmt = select(User).order_by(User.id)
    users = paginate(dbsession, select_stmt, page=2)
    assert users.last == 25


@pytest.mark.usefixtures("setup_users")
def test_paginate_property_pages(dbsession):
    """Test the pages property of the paginate class."""

    # Paginate the users
    select_stmt = select(User).order_by(User.id)
    users = paginate(dbsession, select_stmt, per_page=10)
    assert users.pages == 3


@pytest.mark.usefixtures("setup_users")
def test_paginate_property_has_prev(dbsession):
    """Test the has_prev property of the paginate class."""

    # Paginate the users
    select_stmt = select(User).order_by(User.id)
    users = paginate(dbsession, select_stmt, page=2)
    assert users.has_prev


@pytest.mark.usefixtures("setup_users")
def test_paginate_property_prev_num(dbsession):
    """Test the prev_num property of the paginate class."""

    # Paginate the users
    select_stmt = select(User).order_by(User.id)
    users = paginate(dbsession, select_stmt, page=2)
    assert users.prev_num == 1


@pytest.mark.usefixtures("setup_users")
def test_paginate_property_prev(dbsession):
    """Test the prev method of the paginate class."""

    # Paginate the users
    select_stmt = select(User).order_by(User.id)
    users = paginate(dbsession, select_stmt, page=2)
    prev_users = users.prev()
    assert prev_users.page == 1


@pytest.mark.usefixtures("setup_users")
def test_paginate_property_has_next(dbsession):
    """Test the has_next property of the paginate class."""

    # Paginate the users
    select_stmt = select(User).order_by(User.id)
    users = paginate(dbsession, select_stmt)
    assert users.has_next


@pytest.mark.usefixtures("setup_users")
def test_paginate_property_next_num(dbsession):
    """Test the next_num property of the paginate class."""

    # Paginate the users
    select_stmt = select(User).order_by(User.id)
    users = paginate(dbsession, select_stmt)
    assert users.next_num == 2


@pytest.mark.usefixtures("setup_users")
def test_paginate_property_next(dbsession):
    """Test the next method of the paginate class."""

    # Paginate the users
    select_stmt = select(User).order_by(User.id)
    users = paginate(dbsession, select_stmt)
    next_users = users.next()
    assert next_users.page == 2


@pytest.mark.usefixtures("setup_users")
def test_paginate_property_iter_pages(dbsession):
    """Test the iter_pages method of the paginate class."""

    # Paginate the users
    select_stmt = select(User).order_by(User.id)
    users = paginate(dbsession, select_stmt, per_page=1)
    print(list(users.iter_pages()))
    assert list(users.iter_pages()) == [1, 2, 3, 4, 5, None, 24, 25]


@pytest.mark.usefixtures("setup_users")
def test_paginate_iterate(dbsession):
    """Test that the paginate class can be iterated over."""

    # Paginate the users
    select_stmt = select(User).order_by(User.id)
    users = paginate(dbsession, select_stmt, per_page=1)
    for user in users:
        assert user.id == users.page
