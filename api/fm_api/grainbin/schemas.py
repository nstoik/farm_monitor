"""Schema for Grainbin."""
from flask import url_for
from fm_database.models.device import Grainbin, GrainbinUpdate
from marshmallow.fields import Method

from ..base import BaseSchema


class GrainbinSchema(BaseSchema):
    """Marshmallow Grainbin Schema that loads the instance."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta class for GrainbinSchema."""

        exclude = ("creation_time", "updates")

        model = Grainbin
        include_relationships = True
        load_instance = True

    url = Method("get_url")

    def get_url(self, obj):  # pylint: disable=no-self-use
        """Return url for Grainbin."""

        return url_for("grainbin.GrainbinById", grainbin_id=obj.id)


class GrainbinUpdateSchema(BaseSchema):
    """Marshmallow GrainbinUpdate Schema that loads the instance."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta class for GrainbinUpdateSchema."""

        # exclude = ("id",)

        model = GrainbinUpdate
        include_relationships = True
        load_instance = True
