"""Views for Health API."""

from flask.views import MethodView
from flask_smorest import Blueprint

from ..settings import get_config

config = get_config()

blueprint = Blueprint(
    name="health",
    import_name="health",
    url_prefix=f"{config.API_PREFIX}/health",
    description="Health endpoint",
)


@blueprint.route("/")
class Healthcheck(MethodView):
    """Healthcheck endpoint."""

    @staticmethod
    def get():
        """Healthcheck endpoint."""
        return "ok"
