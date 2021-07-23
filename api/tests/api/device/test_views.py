"""Test the API Device views."""
import pytest
from flask import url_for

from ...factories import DeviceFactory


@pytest.mark.usefixtures("tables")
class TestAPIDevices:
    """Test the API Devices views."""

    @staticmethod
    def test_api_device_list_all_authorize(flaskclient, auth_headers):
        """Test that all devices are returned."""

        for _ in range(5):
            device = DeviceFactory()
            device.save()

        url = url_for("api_device.Devices")
        rep = flaskclient.get(url, headers=auth_headers)
        fetched_devices = rep.get_json()

        assert rep.status_code == 200
        assert len(fetched_devices) == 5

    @staticmethod
    def test_api_device_create(flaskclient, auth_headers):
        """Test that a new device can be created with required fields."""

        json = {
            "device_id": "my-device-id",
            "name": "my-device-name",
            "hardware_version": "v0.1",
            "software_version": "v0.2",
        }
        url = url_for("api_device.Devices")
        rep = flaskclient.post(url, json=json, headers=auth_headers)

        returned_device = rep.get_json()
        print(returned_device)
        assert returned_device["device_id"] == "my-device-id"
        assert rep.status_code == 201


@pytest.mark.usefixtures("tables")
class TestAPIDevicesById:
    """Test the API DevicesById views."""

    @staticmethod
    def test_api_devices_by_id_get(flaskclient, auth_headers):
        """Test that a device is returned by ID."""

        device = DeviceFactory()
        device.save()

        url = url_for("api_device.DevicesById", device_id=device.id)
        rep = flaskclient.get(url, headers=auth_headers)
        fetched_device = rep.get_json()

        assert rep.status_code == 200
        assert fetched_device["device_id"] == device.device_id

    @staticmethod
    def test_api_devices_by_id_url(flaskclient, auth_headers):
        """Test that the URL is returned and is correct."""

        device = DeviceFactory()
        device.save()

        url = url_for("api_device.DevicesById", device_id=device.id)
        rep = flaskclient.get(url, headers=auth_headers)
        fetched_device = rep.get_json()

        assert rep.status_code == 200
        assert fetched_device["url"] == url

    @staticmethod
    def test_api_devices_by_id_get_404(flaskclient, auth_headers):
        """Test that a 404 message is returned for non-existent device."""

        url = url_for("api_device.DevicesById", device_id=5)
        rep = flaskclient.get(url, headers=auth_headers)
        message = rep.get_json()

        assert rep.status_code == 404
        assert message["message"] == "Device with device id: 5 not found."
