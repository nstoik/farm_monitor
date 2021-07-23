"""Views for Device API."""
from flask import current_app
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort
from fm_database.models.device import Device

from .schemas import DeviceSchema

blueprint = Blueprint(
    "api_device",
    "device",
    url_prefix="/api/devices",
    description="Operations on devices",
)


@blueprint.route("/")
class Devices(MethodView):
    """MethodView for Device Schema."""

    decorators = [jwt_required()]

    @staticmethod
    @blueprint.response(200, DeviceSchema(many=True))
    def get():
        """List all Devices."""
        return Device.query.all()

    @staticmethod
    @blueprint.arguments(DeviceSchema)
    @blueprint.response(201, DeviceSchema)
    def post(new_device):
        """Add a Device."""

        new_device.save()
        current_app.logger.info(f"API device POST returns {new_device}")
        return new_device


@blueprint.route("/<device_id>")
class DevicesById(MethodView):
    """MethodView for Device schema that require an ID."""

    decorators = [jwt_required()]

    @staticmethod
    @blueprint.response(200, DeviceSchema)
    def get(device_id):
        """Get Device by ID."""

        item = Device.get_by_id(device_id)
        if item is None:
            abort(404, message=f"Device with device id: {device_id} not found.")
        return item
