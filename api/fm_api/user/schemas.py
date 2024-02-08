"""Schema for User and Roles."""

from fm_database.models.user import Role, User

from ..base import BaseSchema


class UserSchema(BaseSchema):  # pylint: disable=too-few-public-methods
    """Marshmallow UserSchema that loads the instance."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta configuration for UserSchema."""

        exclude = ("password",)

        model = User
        include_relationships = True
        load_instance = True


class UserDictSchema(BaseSchema):  # pylint: disable=too-few-public-methods
    """Marshmallow UserSchema that produces a dict of changed values."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta configuration for UserSchema."""

        exclude = ("password",)

        model = User
        include_relationships = True


class RoleSchema(BaseSchema):  # pylint: disable=too-few-public-methods
    """Marshmallow RoleSchema."""

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta configuration for RoleSchema."""

        model = Role
        include_relationships = True
        load_instance = True
