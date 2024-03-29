"""Test user models."""

import datetime as dt

import pytest

from fm_database.models.user import Role, User

from ..factories import UserFactory


@pytest.mark.usefixtures("tables")
class TestUser:
    """User tests."""

    @staticmethod
    def test_get_by_id():
        """Get user by ID."""
        user = User("foo", "foo@bar.com")
        user.save()

        retrieved = User.get_by_id(user.id)
        assert isinstance(retrieved, User)
        assert retrieved.id == user.id

    @staticmethod
    def test_created_at_defaults_to_datetime():
        """Test creation date."""
        user = User(username="foo", email="foo@bar.com")
        user.save()
        assert bool(user.created_at)
        assert isinstance(user.created_at, dt.datetime)

    @staticmethod
    def test_password_is_nullable():
        """Test null password."""
        user = User(username="foo", email="foo@bar.com")
        user.save()
        assert user.password is None

    @staticmethod
    def test_factory():
        """Test user factory."""
        user = UserFactory(password="myprecious")
        user.save()
        assert bool(user.username)
        assert bool(user.email)
        assert bool(user.created_at)
        assert user.is_admin is False
        assert user.active is True
        assert user.check_password("myprecious")

    @staticmethod
    def test_check_password():
        """Check password."""
        user = User.create(username="foo", email="foo@bar.com", password="foobarbaz123")
        assert user.check_password("foobarbaz123") is True
        assert user.check_password("barfoobaz") is False

    @staticmethod
    def test_full_name():
        """User full name."""
        user = UserFactory(first_name="Foo", last_name="Bar")
        assert user.full_name == "Foo Bar"

    @staticmethod
    def test_roles():
        """Add a role to a user."""
        role = Role(name="admin")
        role.save()
        user = UserFactory()
        user.roles.append(role)
        user.save()
        assert role in user.roles

    @staticmethod
    def test_multiple_roles():
        """Add multiple roles and users."""
        role1 = Role(name="admin")
        role1.save()
        role2 = Role(name="test")
        role2.save()
        user1 = UserFactory()
        user1.roles.append(role1)
        user1.roles.append(role2)
        user1.save()
        user2 = UserFactory()
        user2.roles.append(role1)
        user2.save()
        assert role1 in user1.roles
        assert role2 in user1.roles
        assert role1 in user2.roles
        assert user1 in role1.users
        assert user2 in role1.users
