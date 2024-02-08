"""Test the API Grainbin views."""

import datetime as dt
import json

import pytest
from flask import url_for
from fm_database.models.device import GrainbinUpdate

from ..factories import GrainbinFactory


@pytest.mark.usefixtures("tables")
class TestAPIGrainbins:
    """Test the API Grainbin MethodView."""

    @staticmethod
    def test_grainbins_get_all(flaskclient, auth_headers):
        """Test all grainbins are returned."""

        for _ in range(5):
            grainbin = GrainbinFactory()
            grainbin.save()

        url = url_for("grainbin.Grainbins")
        rep = flaskclient.get(url, headers=auth_headers)
        fetched_grainbins = rep.get_json()

        assert rep.status_code == 200
        assert len(fetched_grainbins) == 5

    @staticmethod
    def test_grainbin_get_by_id(flaskclient, auth_headers):
        """Test an individuual grainbin is returned by ID."""
        grainbin = GrainbinFactory().save()

        url = url_for("grainbin.GrainbinById", grainbin_id=grainbin.id)
        response = flaskclient.get(url, headers=auth_headers)
        fetched_grainbin = response.get_json()

        print(fetched_grainbin)

        assert response.status_code == 200
        assert fetched_grainbin["device"] == grainbin.device.id

    @staticmethod
    def test_grainbin_get_by_id_not_found(flaskclient, auth_headers):
        """Test the route returns 404 for an incorrect ID."""

        grainbin = GrainbinFactory().save()

        url = url_for("grainbin.GrainbinById", grainbin_id=grainbin.id + 1)
        response = flaskclient.get(url, headers=auth_headers)

        assert response.status_code == 404


@pytest.mark.usefixtures("tables")
class TestAPIGrainbinUpdates:
    """Test the API GrainbinUpdates MethodViews."""

    @staticmethod
    def test_grainbin_updates_get(flaskclient, auth_headers, dbsession):
        """Test that all updates are returned for a grainbin."""

        grainbin = GrainbinFactory().save()

        # create some GrainbinUpdates
        for x in range(25):
            grainbin_update = GrainbinUpdate(grainbin.id)
            grainbin_update.timestamp = dt.datetime.now()
            grainbin_update.update_index = x
            dbsession.add(grainbin_update)

        dbsession.commit()

        url = url_for("grainbin.GrainbinUpdates", grainbin_id=grainbin.id)
        rep = flaskclient.get(url, headers=auth_headers)
        fetched_updates = rep.get_json()

        assert rep.status_code == 200
        assert len(fetched_updates) == 10

    @staticmethod
    def test_grainbin_updates_get_no_grainbin(flaskclient, auth_headers):
        """Test that the route returns 0 updates for an incorrect grainbin ID."""

        url = url_for("grainbin.GrainbinUpdates", grainbin_id=1)
        rep = flaskclient.get(url, headers=auth_headers)
        fetched_updates = rep.get_json()

        assert rep.status_code == 200
        assert len(fetched_updates) == 0

    @staticmethod
    def test_grainbin_updates_pagination_header(flaskclient, auth_headers, dbsession):
        """Test that the pagination header is present and acurate."""

        grainbin = GrainbinFactory().save()

        # create some GrainbinUpdates
        for x in range(25):
            grainbin_update = GrainbinUpdate(grainbin.id)
            grainbin_update.timestamp = dt.datetime.now()
            grainbin_update.update_index = x
            dbsession.add(grainbin_update)

        url = url_for("grainbin.GrainbinUpdates", grainbin_id=grainbin.id)
        rep = flaskclient.get(url, headers=auth_headers)
        returned_header = json.loads(rep.headers["X-Pagination"])
        fetched_updates = rep.get_json()

        assert rep.status_code == 200
        assert len(fetched_updates) == 10
        assert returned_header["total"] == 25
        assert returned_header["total_pages"] == 3


@pytest.mark.usefixtures("tables")
class TestAPIGrainbinUpdatesLatest:
    """Test the API GrainbinUpdatesLatest MethodView."""

    @staticmethod
    def test_grainbin_updates_latest_get(flaskclient, auth_headers, dbsession):
        """Test that the latest update is returned for a grainbin."""

        grainbin = GrainbinFactory().save()

        # create some GrainbinUpdates
        for x in range(25):
            grainbin_update = GrainbinUpdate(grainbin.id)
            grainbin_update.timestamp = dt.datetime.now()
            grainbin_update.update_index = x
            grainbin.total_updates = x
            dbsession.add(grainbin_update)

        dbsession.commit()

        url = url_for("grainbin.GrainbinUpdatesLatest", grainbin_id=grainbin.id)
        rep = flaskclient.get(url, headers=auth_headers)
        fetched_update = rep.get_json()

        assert rep.status_code == 200
        assert fetched_update[0]["update_index"] == 24

    @staticmethod
    def test_grainbin_updates_latest_get_multiple(flaskclient, auth_headers, dbsession):
        """Test that all the latest updates are returned for a grainbin."""

        grainbin = GrainbinFactory().save()

        # create two GrainbinUpdates for each iteration
        for x in range(5):
            grainbin_update = GrainbinUpdate(grainbin.id)
            grainbin_update.timestamp = dt.datetime.now()
            grainbin_update.update_index = x
            grainbin_update_2 = GrainbinUpdate(grainbin.id)
            grainbin_update_2.timestamp = dt.datetime.now()
            grainbin_update_2.update_index = x
            grainbin.total_updates = x
            dbsession.add(grainbin_update)
            dbsession.add(grainbin_update_2)

        dbsession.commit()

        url = url_for("grainbin.GrainbinUpdatesLatest", grainbin_id=grainbin.id)
        rep = flaskclient.get(url, headers=auth_headers)
        fetched_update = rep.get_json()

        assert rep.status_code == 200
        assert len(fetched_update) == 2
        assert fetched_update[0]["update_index"] == 4

    @staticmethod
    def test_grainbin_updates_latest_get_no_grainbin(flaskclient, auth_headers):
        """Test that the route returns 404 for an incorrect grainbin ID."""

        url = url_for("grainbin.GrainbinUpdatesLatest", grainbin_id=1)
        rep = flaskclient.get(url, headers=auth_headers)
        rep_json = rep.get_json()

        assert rep.status_code == 404
        assert rep_json["message"] == "Grainbin with id: 1 not found"

    @staticmethod
    def test_grainbin_updates_latest_get_no_updates(flaskclient, auth_headers):
        """Test that the route returns 404 for a bin that has no updates."""

        grainbin = GrainbinFactory().save()

        url = url_for("grainbin.GrainbinUpdatesLatest", grainbin_id=grainbin.id)
        rep = flaskclient.get(url, headers=auth_headers)
        rep_json = rep.get_json()

        assert rep.status_code == 404
        assert rep_json["message"] == f"No updates for Grainbin with id: {grainbin.id}"
