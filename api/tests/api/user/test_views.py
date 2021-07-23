"""Test the API User Views."""

import pytest
from flask import url_for
from fm_database.models.user import User

from ...factories import UserFactory


@pytest.mark.usefixtures("tables")
class TestAPIUser:
    """Test the API user views."""

    @staticmethod
    def test_api_users_list_users_authorize(flaskclient):
        """Test that authorization is required to return data."""

        url = url_for("api_user.Users")
        rep = flaskclient.get(url)
        assert rep.status_code == 401

    @staticmethod
    def test_api_users_list_users(flaskclient, auth_headers):
        """Test that auth headers work."""

        url = url_for("api_user.Users")
        rep = flaskclient.get(url, headers=auth_headers)
        assert rep.status_code == 200

    @staticmethod
    def test_api_users_list_all_users(flaskclient, auth_headers):
        """Test that multiple users are returned."""

        for _ in range(10):
            user = UserFactory()
            user.save()

        url = url_for("api_user.Users")
        rep = flaskclient.get(url, headers=auth_headers)
        fetched_users = rep.get_json()

        assert rep.status_code == 200
        assert len(fetched_users) == 11

    @staticmethod
    def test_api_users_create(flaskclient, auth_headers):
        """Test that a new user can be created with required fields."""

        json = {
            "email": "test@notanemail.com",
            "username": "new_user",
        }

        url = url_for("api_user.Users")
        rep = flaskclient.post(url, json=json, headers=auth_headers)

        returned_user = rep.get_json()
        assert returned_user["username"] == "new_user"
        assert rep.status_code == 201

    @staticmethod
    def test_api_users_create_extra_fields(flaskclient, auth_headers):
        """Test that a new user is created with additional fields."""

        json = {
            "email": "test@notanemail.com",
            "username": "new_user",
            "first_name": "Bob",
        }

        url = url_for("api_user.Users")
        rep = flaskclient.post(url, json=json, headers=auth_headers)

        returned_user = rep.get_json()
        assert returned_user["username"] == "new_user"
        assert returned_user["first_name"] == "Bob"
        assert rep.status_code == 201


@pytest.mark.usefixtures("tables")
class TestAPIUserById:
    """Test the API user by ID views."""

    @staticmethod
    def test_api_users_get_by_id_list(flaskclient, auth_headers, user):
        """Test that a user can be returned by ID."""

        url = url_for("api_user.UsersById", user_id=user.id)
        rep = flaskclient.get(url, headers=auth_headers)

        returned_user = rep.get_json()
        assert returned_user["username"] == user.username
        assert returned_user["email"] == user.email
        assert rep.status_code == 200

    @staticmethod
    def test_api_users_get_by_id_not_exist(flaskclient, auth_headers):
        """Test that a non-existent user returns 404."""

        url = url_for("api_user.UsersById", user_id="5")
        rep = flaskclient.get(url, headers=auth_headers)

        returned_message = rep.get_json()
        assert rep.status_code == 404
        assert returned_message["message"] == "User not found."

    @staticmethod
    def test_api_users_put_by_id(flaskclient, auth_headers, user):
        """Test that a user can be updated and returned by ID."""

        json = {
            "username": "Updated Username",
            "email": user.email,
            "first_name": "Bob",
        }

        url = url_for("api_user.UsersById", user_id=user.id)
        rep = flaskclient.put(url, json=json, headers=auth_headers)

        returned_user = rep.get_json()
        assert rep.status_code == 200
        assert returned_user["username"] == "Updated Username"
        assert returned_user["first_name"] == "Bob"
        assert returned_user["email"] == user.email
        assert returned_user["active"] == user.active

    @staticmethod
    def test_api_users_put_not_found(flaskclient, auth_headers, user):
        """Test that a non existent user returns a 404."""

        json = {
            "username": user.username,
            "email": user.email,
        }

        url = url_for("api_user.UsersById", user_id=9999)
        rep = flaskclient.put(url, json=json, headers=auth_headers)

        returned_message = rep.get_json()
        assert rep.status_code == 404
        assert returned_message["message"] == "User not found."

    @staticmethod
    def test_api_users_put_no_changes(flaskclient, auth_headers, user):
        """Test that input with no changes returns the same values."""

        json = {
            "username": user.username,
            "email": user.email,
        }

        url = url_for("api_user.UsersById", user_id=user.id)
        rep = flaskclient.put(url, json=json, headers=auth_headers)

        returned_user = rep.get_json()
        assert rep.status_code == 200
        assert returned_user["username"] == user.username
        assert returned_user["first_name"] == user.first_name
        assert returned_user["email"] == user.email
        assert returned_user["active"] == user.active

    @staticmethod
    def test_api_users_delete(flaskclient, auth_headers, user):
        """Test deleting a user by ID."""

        url = url_for("api_user.UsersById", user_id=user.id)
        rep = flaskclient.delete(url, headers=auth_headers)

        deleted_user = User.query.filter_by(id=user.id).first()

        assert rep.status_code == 204
        assert deleted_user is None

    @staticmethod
    def test_api_users_delete_not_found(flaskclient, auth_headers):
        """Test deleting a user by ID that does not exist."""

        url = url_for("api_user.UsersById", user_id=9999)
        rep = flaskclient.delete(url, headers=auth_headers)

        returned_message = rep.get_json()
        assert rep.status_code == 404
        assert returned_message["message"] == "User not found."
