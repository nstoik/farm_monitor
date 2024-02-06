"""Test the API Device views."""

import datetime as dt
import json

import pytest
from flask import url_for
from fm_database.models.device import DeviceUpdate

from ..factories import DeviceFactory


@pytest.mark.usefixtures("tables")
class TestAPIDevices:
    """Test the API Devices views."""

    @staticmethod
    def test_api_device_list_all_authorize(flaskclient, auth_headers):
        """Test that all devices are returned."""

        for _ in range(5):
            device = DeviceFactory()
            device.save()

        url = url_for("device.Devices")
        rep = flaskclient.get(url, headers=auth_headers)
        fetched_devices = rep.get_json()

        assert rep.status_code == 200
        assert len(fetched_devices) == 5

    @staticmethod
    def test_api_device_create(flaskclient, auth_headers):
        """Test that a new device can be created with required fields."""

        custom_json = {
            "device_id": "my-device-id",
            "name": "my-device-name",
            "hardware_version": "v0.1",
            "software_version": "v0.2",
            "description": "my-device-description",
            "location": "my-device-location",
        }
        url = url_for("device.Devices")
        rep = flaskclient.post(url, json=custom_json, headers=auth_headers)

        returned_device = rep.get_json()
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

        url = url_for("device.DevicesById", device_id=device.id)
        rep = flaskclient.get(url, headers=auth_headers)
        fetched_device = rep.get_json()

        assert rep.status_code == 200
        assert fetched_device["device_id"] == device.device_id

    @staticmethod
    def test_api_devices_by_id_url(flaskclient, auth_headers):
        """Test that the URL is returned and is correct."""

        device = DeviceFactory()
        device.save()

        url = url_for("device.DevicesById", device_id=device.id)
        rep = flaskclient.get(url, headers=auth_headers)
        fetched_device = rep.get_json()

        assert rep.status_code == 200
        assert fetched_device["url"] == url

    @staticmethod
    def test_api_devices_by_id_get_404(flaskclient, auth_headers):
        """Test that a 404 message is returned for non-existent device."""

        url = url_for("device.DevicesById", device_id=5)
        rep = flaskclient.get(url, headers=auth_headers)
        message = rep.get_json()

        assert rep.status_code == 404
        assert message["message"] == "Device with device id: 5 not found."


@pytest.mark.usefixtures("tables")
class TestAPIDeviceUpdates:
    """Test the API DeviceUpdates views."""

    @staticmethod
    def test_api_device_updates_get(flaskclient, auth_headers, dbsession):
        """Test that a device update is returned by ID."""

        device = DeviceFactory()
        device.save()

        # create a bunch of DeviceUpdates
        for x in range(25):
            device_update = DeviceUpdate(device.id)
            device_update.timestamp = dt.datetime.now()
            device_update.update_index = x
            dbsession.add(device_update)

        dbsession.commit()

        url = url_for("device.DeviceUpdates", device_id=device.id)
        rep = flaskclient.get(url, headers=auth_headers)
        fetched_device_update = rep.get_json()

        assert rep.status_code == 200
        assert len(fetched_device_update) == 10

    @staticmethod
    def test_api_device_updates_get_multiple_devices(
        flaskclient, auth_headers, dbsession
    ):
        """Test that a device update is returned by ID. when there are multiple devices."""

        device_1 = DeviceFactory()
        device_1.save()
        device_2 = DeviceFactory()
        device_2.save()

        # create a bunch of DeviceUpdates
        for x in range(25):
            device_update_1 = DeviceUpdate(device_1.id)
            device_update_1.timestamp = dt.datetime.now()
            device_update_1.update_index = x
            device_update_2 = DeviceUpdate(device_2.id)
            device_update_2.timestamp = dt.datetime.now()
            device_update_2.update_index = x
            dbsession.add(device_update_1, device_update_2)

        dbsession.commit()

        url = url_for("device.DeviceUpdates", device_id=device_1.id)
        rep = flaskclient.get(url, headers=auth_headers)
        fetched_device_update = rep.get_json()

        returned_header = json.loads(rep.headers.get("X-Pagination"))

        assert rep.status_code == 200
        assert len(fetched_device_update) == 10
        assert fetched_device_update[0]["device"] == device_1.id
        assert returned_header["total"] == 25

    @staticmethod
    def test_api_device_updates_empty_for_no_device(flaskclient, auth_headers):
        """Test that a no DeviceUpdates is returned for non-existent device."""

        url = url_for("device.DeviceUpdates", device_id=5)
        rep = flaskclient.get(url, headers=auth_headers)
        message = rep.get_json()

        assert rep.status_code == 200
        assert len(message) == 0

    @staticmethod
    def test_api_device_updates_pagination_header(flaskclient, auth_headers, dbsession):
        """Test that the pagination header is present and accurate."""

        device = DeviceFactory()
        device.save()

        # create a bunch of DeviceUpdates
        for x in range(25):
            device_update = DeviceUpdate(device.id)
            device_update.timestamp = dt.datetime.now()
            device_update.update_index = x
            dbsession.add(device_update)

        dbsession.commit()

        url = url_for("device.DeviceUpdates", device_id=device.id)
        rep = flaskclient.get(url, headers=auth_headers)
        returned_header = json.loads(rep.headers.get("X-Pagination"))
        fetched_device_update = rep.get_json()

        assert rep.status_code == 200
        assert len(fetched_device_update) == 10
        assert returned_header["total"] == 25
        assert returned_header["total_pages"] == 3


@pytest.mark.usefixtures("tables")
class TestAPIDeviceUpdatesLatest:
    """Test the API DeviceUpdatesLatest MethodView."""

    @staticmethod
    def test_api_device_updates_latest_get(flaskclient, auth_headers, dbsession):
        """Test that the latest update is returned for a device."""

        device = DeviceFactory()
        device.save()

        # create a bunch of DeviceUpdates
        for x in range(25):
            device_update = DeviceUpdate(device.id)
            device_update.timestamp = dt.datetime.now()
            device_update.update_index = x
            dbsession.add(device_update)

        dbsession.commit()

        url = url_for("device.DeviceUpdatesLatest", device_id=device.id)
        rep = flaskclient.get(url, headers=auth_headers)
        fetched_device_update = rep.get_json()

        assert rep.status_code == 200
        assert fetched_device_update["update_index"] == 24

    @staticmethod
    def test_api_device_updates_latest_get_no_device(flaskclient, auth_headers):
        """Test that a 404 message is returned for non-existent device."""

        url = url_for("device.DeviceUpdatesLatest", device_id=5)
        rep = flaskclient.get(url, headers=auth_headers)
        message = rep.get_json()

        assert rep.status_code == 404
        assert message["message"] == "Device with device id: 5 not found."
