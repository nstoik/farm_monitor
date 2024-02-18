"""Schema for Auth."""

from marshmallow.fields import Str
from marshmallow.validate import Length

from ..base import BaseSchema


class LoginArgsSchema(BaseSchema):  # pylint: disable=too-few-public-methods
    """Marshmallow schema for login."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta configuration for LoginQueryArgsSchema."""

        ordered = True

    username = Str(required=True, validate=Length(min=2, max=80))
    password = Str(required=True, validate=Length(min=2, max=128))


class JWTResponseSchema(BaseSchema):
    """Marshmallow schema for JWT token response."""

    access_token = Str(required=True)
    refresh_token = Str()
