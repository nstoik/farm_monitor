"""Views for Auth API."""
from datetime import datetime

from flask.views import MethodView
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    decode_token,
    get_jwt_identity,
    jwt_required,
)
from flask_smorest import Blueprint, abort
from fm_database.models.user import User

from fm_api.extensions import jwt

from .schemas import JWTSchema, LoginArgsSchema

blueprint = Blueprint(
    "api_auth",
    "auth",
    url_prefix="/api/auth",
    description="Get and refresh auth tokens",
)


@blueprint.route("/")
class AuthLogin(MethodView):
    """MethodView for AuthLogin schema."""

    @staticmethod
    @blueprint.arguments(LoginArgsSchema)
    @blueprint.response(200, JWTSchema)
    def post(login_args):
        """Login and return JWT Auth."""

        username = login_args["username"]
        password = login_args["password"]
        user = User.query.filter_by(username=username).first()

        if user is None or not user.check_password(password):
            abort(400, message="User not found or bad password.")

        access_token = create_access_token(identity=user, fresh=True)
        refresh_token = create_refresh_token(identity=user)

        local_timezone = datetime.utcnow().astimezone().tzinfo

        access_decoded = decode_token(access_token)
        access_expires = datetime.fromtimestamp(
            access_decoded["exp"], local_timezone
        ).isoformat()
        refresh_decoded = decode_token(refresh_token)
        refresh_expires = datetime.fromtimestamp(
            refresh_decoded["exp"], local_timezone
        ).isoformat()
        return {
            "access_token": access_token,
            "access_expires": access_expires,
            "refresh_token": refresh_token,
            "refresh_expires": refresh_expires,
        }


@blueprint.route("/refresh")
class AuthRefresh(MethodView):
    """MethodView for AuthRefresh schema."""

    decorators = [jwt_required(refresh=True)]

    @staticmethod
    @blueprint.response(200, JWTSchema)
    def post():
        """Return a new access token using the refresh token."""

        current_user_id = get_jwt_identity()
        current_user = User.query.filter_by(id=current_user_id).one_or_none()

        access_token = create_access_token(identity=current_user)

        local_timezone = datetime.utcnow().astimezone().tzinfo
        access_decoded = decode_token(access_token)
        access_expires = datetime.fromtimestamp(
            access_decoded["exp"], local_timezone
        ).isoformat()
        return {
            "access_token": access_token,
            "access_expires": access_expires,
        }


@jwt.user_lookup_loader
def user_loader_callback(_jwt_header, jwt_data):
    """Load the user given JWT.

    A callback function that loades a user from the database whenever
    a protected route is accessed. This returns a User or else None
    """
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


@jwt.user_identity_loader
def user_identity_lookup(user: User):
    """Return the user identity.

    A callback function that takes whatever object is passed in as the
    identity when creating JWTs and converts it to a JSON serializable format.
    """
    return user.id
