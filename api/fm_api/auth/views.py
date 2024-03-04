"""Views for Auth API."""

from flask.views import MethodView
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
)
from flask_smorest import Blueprint, abort
from fm_database.database import get_session
from fm_database.models.user import User
from sqlalchemy import select

from fm_api.extensions import jwt
from fm_api.settings import get_config

from .schemas import JWTResponseSchema, LoginArgsSchema

config = get_config()

blueprint = Blueprint(
    "auth",
    "auth",
    url_prefix=f"{config.API_PREFIX}/auth",
    description="Get and refresh auth tokens",
)


@blueprint.route("/jwt/")
class JWTLogin(MethodView):
    """MethodView for JWTLogin schema."""

    @staticmethod
    @blueprint.arguments(LoginArgsSchema)
    @blueprint.response(200, JWTResponseSchema)
    def post(login_args):
        """Login and return JWT Auth."""

        username = login_args["username"]
        password = login_args["password"]

        session = get_session()
        user = session.scalars(
            select(User).where(User.username == username)
        ).one_or_none()

        if user is None or not user.check_password(password):
            abort(401, message="User not found or bad password.")

        access_token = create_access_token(identity=user, fresh=True)
        refresh_token = create_refresh_token(identity=user)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }


@blueprint.route("/jwt/refresh")
class JWTRefresh(MethodView):
    """MethodView for JWTRefresh schema."""

    decorators = [jwt_required(refresh=True)]

    @staticmethod
    @blueprint.response(200, JWTResponseSchema)
    def post():
        """Return a new access token using the refresh token."""

        current_user_id = get_jwt_identity()
        session = get_session()
        current_user = session.scalars(
            select(User).where(User.id == current_user_id)
        ).one_or_none()

        access_token = create_access_token(identity=current_user)

        return {
            "access_token": access_token,
        }


@jwt.user_lookup_loader
def user_loader_callback(_jwt_header, jwt_data) -> User | None:
    """Load the user given JWT.

    A callback function that loades a user from the database whenever
    a protected route is accessed. This returns a User or else None
    """
    identity = jwt_data["sub"]

    session = get_session()
    return session.scalars(select(User).where(User.id == identity)).one_or_none()


@jwt.user_identity_loader
def user_identity_lookup(user: User) -> int:
    """Return the user identity.

    A callback function that takes whatever object is passed in as the
    identity when creating JWTs and converts it to a JSON serializable format.
    """
    return user.id  # type: ignore[no-any-return]
