"""Tests for the paginate class and method."""
import pytest

from fm_database.models.user import User
from fm_database.paginate import Pagination

from .factories import UserFactory


def test_basic_pagination():
    """Test basic pagination."""

    page = Pagination(None, 1, 20, 500, [])
    assert page.page == 1
    assert not page.has_prev
    assert page.has_next
    assert page.total == 500
    assert page.pages == 25
    assert page.next_num == 2
    assert list(page.iter_pages()) == [1, 2, 3, 4, 5, None, 24, 25]
    page.page = 10
    assert list(page.iter_pages()) == [
        1,
        2,
        None,
        8,
        9,
        10,
        11,
        12,
        13,
        14,
        None,
        24,
        25,
    ]


def test_pagination_pages_when_0_items_per_page():
    """Test pagination when there are 0 items per page."""

    page = Pagination(None, 1, 0, 500, [])
    assert page.pages == 0


def test_pagination_pages_when_total_is_none():
    """Test pagination when total is None."""
    page = Pagination(None, 1, 100, None, [])
    assert page.pages == 0


@pytest.mark.usefixtures("tables")
def test_query_paginate(dbsession):
    """Test that the query paginates correctly."""

    # Create a bunch of users
    dbsession.add_all([UserFactory() for _ in range(25)])
    dbsession.commit()

    # Paginate the users
    users = User.query.paginate()
    assert len(users.items) == 20
    assert users.total == 25


@pytest.mark.usefixtures("tables")
def test_query_paginate_specify_max_per_page(dbsession):
    """Test that the query paginates correctly when max_per_page is given."""

    # Create a bunch of users
    dbsession.add_all([UserFactory() for _ in range(25)])
    dbsession.commit()

    # Paginate the users
    users = User.query.paginate(max_per_page=10)
    assert len(users.items) == 10
    assert users.total == 25


@pytest.mark.usefixtures("tables")
def test_query_paginate_specify_page(dbsession):
    """Test that the query paginates correctly when page is given."""

    # Create a bunch of users
    dbsession.add_all([UserFactory() for _ in range(25)])
    dbsession.commit()

    # Paginate the users
    users = User.query.paginate(page=2)
    assert len(users.items) == 5
    assert users.total == 25


@pytest.mark.usefixtures("tables")
def test_query_paginate_min(dbsession):
    """Test that the query paginates correctly when min is given."""

    # Create a bunch of users
    dbsession.add_all([UserFactory() for _ in range(25)])
    dbsession.commit()

    assert User.query.paginate(page=-1).page == 1
    assert len(User.query.paginate(per_page=0).items) == 1
    assert len(User.query.paginate(per_page=-1).items) == 1


@pytest.mark.usefixtures("tables")
def test_query_paginate_without_count(dbsession):
    """Test that the query paginates correctly when count is False."""

    # Create a bunch of users
    dbsession.add_all([UserFactory() for _ in range(25)])
    dbsession.commit()

    # Paginate the users
    users = User.query.paginate(count=False)
    assert len(users.items) == 20
    assert users.total is None
