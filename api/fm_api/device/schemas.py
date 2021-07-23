"""Schema for Device."""
from flask import url_for
from fm_database.models.device import Device
from marshmallow.fields import Method

from ..base import BaseSchema


class DeviceSchema(BaseSchema):
    """Marshmallow DeviceSchema that loads the instance."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta configuration for DeviceSchema."""

        exclude = ("id",)

        model = Device
        include_relationships = True
        load_instance = True

    url = Method("get_url")

    def get_url(self, obj):  # pylint: disable=no-self-use
        """For marshmallow Method field to get a url for the resource."""

        return url_for("api_device.DevicesById", device_id=obj.id)
