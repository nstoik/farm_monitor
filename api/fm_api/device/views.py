"""Views for Device API."""

from flask import current_app
from flask.views import MethodView

# from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort
from flask_smorest.pagination import PaginationParameters
from fm_database.database import get_session
from fm_database.models.device import Device, DeviceUpdate
from fm_database.paginate import Pagination
from sqlalchemy import select

from fm_api.settings import get_config

from .schemas import DeviceSchema, DeviceUpdateSchema

config = get_config()

blueprint = Blueprint(
    "device",
    "device",
    url_prefix=f"{config.API_PREFIX}/device",
    description="Operations on devices",
)


@blueprint.route("/")
class Devices(MethodView):
    """MethodView for Device Schema."""

    # decorators = [jwt_required()]

    @staticmethod
    @blueprint.response(200, DeviceSchema(many=True))
    def get():
        """List all Devices."""
        session = get_session()
        return session.scalars(select(Device)).all()

    @staticmethod
    @blueprint.arguments(DeviceSchema)
    @blueprint.response(201, DeviceSchema)
    def post(new_device):
        """Add a Device."""

        new_device.save()
        current_app.logger.info(f"API device POST returns {new_device}")
        return new_device


@blueprint.route("/<int:device_id>")
class DevicesById(MethodView):
    """MethodView for Device schema that require an ID."""

    # decorators = [jwt_required()]

    @staticmethod
    @blueprint.response(200, DeviceSchema)
    def get(device_id):
        """Get Device by ID."""

        item = Device.get_by_id(device_id)
        if item is None:
            abort(404, message=f"Device with device id: {device_id} not found.")
        return item


@blueprint.route("/<int:device_id>/updates")
class DeviceUpdates(MethodView):
    """MethodView for DeviceUpdate schema that require an ID."""

    # decorators = [jwt_required()]

    @staticmethod
    @blueprint.response(200, DeviceUpdateSchema(many=True))
    @blueprint.paginate()
    def get(device_id: int, pagination_parameters: PaginationParameters):
        """Get DeviceUpdates for a given Device ID with Pagination.

        Default pagination parameters are 10 per page starting at page 1.
        Ordered by most recent updates first.
        """
        session = get_session()
        select_stm = (
            select(DeviceUpdate)
            .where(DeviceUpdate.device_id == device_id)
            .order_by(DeviceUpdate.update_index.desc())
        )
        device_updates = Pagination(
            session,
            select_stm,
            page=pagination_parameters.page,
            per_page=pagination_parameters.page_size,
        )

        pagination_parameters.item_count = device_updates.total
        return device_updates.items


@blueprint.route("/<int:device_id>/updates/latest")
class DeviceUpdatesLatest(MethodView):
    """MethodView for DeviceUpdate schema that require an ID."""

    # decorators = [jwt_required()]

    @staticmethod
    @blueprint.response(200, DeviceUpdateSchema)
    def get(device_id):
        """Get the latest DeviceUpdate for a given Device ID."""

        session = get_session()
        device_update = session.scalars(
            select(DeviceUpdate)
            .where(DeviceUpdate.device_id == device_id)
            .order_by(DeviceUpdate.update_index.desc())
            .limit(1)
        ).one_or_none()

        if device_update is None:
            abort(404, message=f"Device with device id: {device_id} not found.")
        return device_update
