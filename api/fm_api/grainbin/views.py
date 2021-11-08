"""Views for Grainbin API."""
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_smorest.pagination import PaginationParameters
from fm_database.models.device import Grainbin, GrainbinUpdate
from fm_database.paginate import Pagination

from .schemas import GrainbinSchema, GrainbinUpdateSchema

blueprint = Blueprint(
    "grainbin",
    "grainbin",
    url_prefix="/api/grainbin",
    description="Operations on grainbins",
)


@blueprint.route("/")
class Grainbins(MethodView):
    """MethodView for Grainbin schema."""

    @staticmethod
    @blueprint.response(200, GrainbinSchema(many=True))
    def get():
        """List all Grainbins."""
        return Grainbin.query.all()

    # TODO: Add POST method


@blueprint.route("/<int:grainbin_id>")
class GrainbinById(MethodView):
    """MethodView for Grainbin schema that require an ID."""

    @staticmethod
    @blueprint.response(200, GrainbinSchema())
    def get(grainbin_id):
        """Get Grainbin by id."""

        item = Grainbin.get_by_id(grainbin_id)
        if item is None:
            abort(404, message=f"Grainbin with id: {grainbin_id} not found.")
        return item


@blueprint.route("/<int:grainbin_id>/updates")
class GrainbinUpdates(MethodView):
    """MethodView for GrainbinUpdate schema that require an ID."""

    @staticmethod
    @blueprint.response(200, GrainbinUpdateSchema(many=True))
    @blueprint.paginate()
    def get(grainbin_id, pagination_parameters: PaginationParameters):
        """Get GrainbinUpdates for a given Grainbin ID with Pagination.

        Default pagination is set to 10 items per page.
        Ordered by most recent updates first.
        """

        grainbin_updates: Pagination = (
            GrainbinUpdate.query.filter_by(grainbin_id=grainbin_id)
            .order_by(GrainbinUpdate.update_index.desc())
            .paginate(pagination_parameters.page, pagination_parameters.page_size)
        )

        pagination_parameters.item_count = grainbin_updates.total
        return grainbin_updates.items


@blueprint.route("/<int:grainbin_id>/updates/latest")
class GrainbinUpdatesLatest(MethodView):
    """MethodView for GrainbinUpdate schema that require an ID."""

    @staticmethod
    @blueprint.response(200, GrainbinUpdateSchema())
    def get(grainbin_id):
        """Get latest GrainbinUpdate for a given Grainbin ID."""

        grainbin_update = (
            GrainbinUpdate.query.filter_by(grainbin_id=grainbin_id)
            .order_by(GrainbinUpdate.update_index.desc())
            .first()
        )

        if grainbin_update is None:
            abort(404, message=f"Grainbin with id: {grainbin_id} not found.")
        return grainbin_update
