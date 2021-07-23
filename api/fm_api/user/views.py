"""Views for User and Role API."""
from flask import current_app
from flask.views import MethodView
from flask_jwt_extended import jwt_required
from flask_smorest import Blueprint, abort
from fm_database.base import get_session
from fm_database.models.user import User

from .schemas import UserSchema, UserSchemaDict

blueprint = Blueprint(
    "api_user",
    "user",
    url_prefix="/api/users",
    description="Operations on users and roles",
)


@blueprint.route("/")
class Users(MethodView):
    """MethodView for Users Schema."""

    decorators = [jwt_required()]

    @staticmethod
    @blueprint.response(200, UserSchema(many=True))
    def get():
        """List all Users."""
        return User.query.all()

    @staticmethod
    @blueprint.arguments(UserSchema)
    @blueprint.response(201, UserSchema)
    def post(new_user):
        """Add a User."""

        dbsession = get_session()
        new_user.save(dbsession)
        current_app.logger.info(f"API user POST returns {new_user}")
        return new_user


@blueprint.route("/<user_id>")
class UsersById(MethodView):
    """MethodView for Users schema that require an ID."""

    decorators = [jwt_required()]

    @staticmethod
    @blueprint.response(200, UserSchema)
    def get(user_id):
        """Get User by ID."""

        item = User.get_by_id(user_id)
        if item is None:
            abort(404, message="User not found.")
        return item

    @staticmethod
    @blueprint.arguments(UserSchemaDict)
    @blueprint.response(200, UserSchema)
    def put(update_data, user_id):
        """Update existing User."""

        dbsession = get_session()
        item = User.get_by_id(user_id, session=dbsession)
        if item is None:
            abort(404, message="User not found.")
        # pass in update_data dict as named variables
        item.update(dbsession, **update_data)
        current_app.logger.info(f"API user PUT returns {item}")
        return item

    @staticmethod
    @blueprint.response(204)
    def delete(user_id):
        """Delete a User by ID."""
        dbsession = get_session()
        item = User.get_by_id(user_id, session=dbsession)
        if item is None:
            abort(404, message="User not found.")
        item.delete(session=dbsession)
