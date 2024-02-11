"""Test the API health views."""

import pytest
from flask import url_for


@pytest.mark.usefixtures("tables")
class TestAPIHealth:
    """Test the API health views."""

    @staticmethod
    def test_api_health(flaskclient):
        """Test health check."""
        url = url_for("health.Healthcheck")
        rep = flaskclient.get(url)
        reply = rep.get_data(as_text=True)

        assert rep.status_code == 200
        assert reply == "ok"

    @staticmethod
    def test_api_health_wrong_url(flaskclient):
        """Test wrong health check."""
        url = url_for("health.Healthcheck") + "wrong"
        rep = flaskclient.get(url)
        reply = rep.get_json()

        assert rep.status_code == 404
        assert reply["status"] == "Not Found"
