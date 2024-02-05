"""Base Schema setup for api."""
from fm_database.base import get_session

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemyAutoSchemaOpts

session = get_session()


# pylint: disable=too-few-public-methods
class BaseOpts(SQLAlchemyAutoSchemaOpts):
    """Define a BaseOpts with a common Session object.

    https://marshmallow-sqlalchemy.readthedocs.io/en/latest/recipes.html#base-schema-ii
    """

    def __init__(self, meta, ordered=False):
        """Add a sqla_session if it doesn't already exist."""
        if not hasattr(meta, "sqla_session"):
            meta.sqla_session = session()
        super().__init__(meta, ordered=ordered)


class BaseSchema(SQLAlchemyAutoSchema):
    """Define a BaseSchema with a common Session object.

    https://marshmallow-sqlalchemy.readthedocs.io/en/latest/recipes.html#base-schema-ii
    """

    OPTIONS_CLASS = BaseOpts
