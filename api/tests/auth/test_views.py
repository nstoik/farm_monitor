"""Test the API Auth views."""

import pytest
from flask import url_for


@pytest.mark.usefixtures("tables")
class TestAPIJWTLogin:
    """Test the API JWT login views."""

    @staticmethod
    def test_api_jwt_login(admin_user, flaskclient):
        """Test successful login."""

        data = {"username": admin_user.username, "password": "admin"}
        url = url_for("auth.JWTLogin")
        rep = flaskclient.post(url, json=data)
        tokens = rep.get_json()

        assert rep.status_code == 200
        assert "access_token" in tokens
        assert "refresh_token" in tokens

    @staticmethod
    def test_api_jwt_wrong_password(admin_user, flaskclient):
        """Test bad login with wrong password."""

        data = {"username": admin_user.username, "password": "wrong"}
        url = url_for("auth.JWTLogin")
        rep = flaskclient.post(url, json=data)
        reply = rep.get_json()

        assert rep.status_code == 401
        assert reply["message"] == "User not found or bad password."

    @staticmethod
    def test_api_jwt_wrong_user(flaskclient):
        """Test bad login with wrong user."""

        data = {"username": "wrong", "password": "admin"}
        url = url_for("auth.JWTLogin")
        rep = flaskclient.post(url, json=data)
        reply = rep.get_json()

        assert rep.status_code == 401
        assert reply["message"] == "User not found or bad password."

    @staticmethod
    def test_api_jwt_no_input(flaskclient):
        """Test bad login with no input."""

        url = url_for("auth.JWTLogin")
        rep = flaskclient.post(url)
        reply = rep.get_json()

        assert rep.status_code == 422
        assert reply["status"] == "Unprocessable Entity"

    @staticmethod
    def test_api_jwt_get(flaskclient):
        """Test bad login with get."""

        url = url_for("auth.JWTLogin")
        rep = flaskclient.get(url)
        reply = rep.get_json()

        print(reply)

        assert rep.status_code == 405
        assert reply["status"] == "Method Not Allowed"


@pytest.mark.usefixtures("tables", "admin_user")
class TestAPIJWTRefresh:
    """Test the API JWT refresh views."""

    @staticmethod
    def get_tokens(flaskclient):
        """Helper function to get tokens from API."""

        data = {"username": "admin", "password": "admin"}
        url_login = url_for("auth.JWTLogin")
        rep = flaskclient.post(url_login, json=data)
        return rep.get_json()

    @staticmethod
    def test_api_jwt_refresh(flaskclient):
        """Test refresh token is provided."""

        tokens = TestAPIJWTRefresh.get_tokens(flaskclient)

        auth_headers = {
            "content-type": "application/json",
            "authorization": f"Bearer {tokens['refresh_token']}",
        }
        url_refresh = url_for("auth.JWTRefresh")
        rep = flaskclient.post(url_refresh, headers=auth_headers)
        tokens = rep.get_json()

        assert rep.status_code == 200
        assert "access_token" in tokens

    @staticmethod
    def test_api_jwt_refresh_wrong_type(flaskclient):
        """Test that a refresh token has to be sent."""

        tokens = TestAPIJWTRefresh.get_tokens(flaskclient)

        auth_headers = {
            "content-type": "application/json",
            "authorization": f"Bearer {tokens['access_token']}",
        }
        url_refresh = url_for("auth.JWTRefresh")
        rep = flaskclient.post(url_refresh, headers=auth_headers)
        message = rep.get_json()

        assert rep.status_code == 422
        assert message["msg"] == "Only refresh tokens are allowed"
