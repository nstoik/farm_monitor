"""Views for Grainbin API."""

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_smorest.pagination import PaginationParameters
from fm_database.database import get_session
from fm_database.models.device import Grainbin, GrainbinUpdate
from fm_database.paginate import Pagination
from sqlalchemy import select

from fm_api.settings import get_config

from .schemas import GrainbinSchema, GrainbinUpdateSchema

config = get_config()

blueprint = Blueprint(
    "grainbin",
    "grainbin",
    url_prefix=f"{config.API_PREFIX}/grainbin",
    description="Operations on grainbins",
)


@blueprint.route("/")
class Grainbins(MethodView):
    """MethodView for Grainbin schema."""

    @staticmethod
    @blueprint.response(200, GrainbinSchema(many=True))
    def get():
        """List all Grainbins."""
        session = get_session()
        return session.scalars(select(Grainbin)).all()

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

        session = get_session()
        select_stm = (
            select(GrainbinUpdate)
            .where(GrainbinUpdate.grainbin_id == grainbin_id)
            .order_by(GrainbinUpdate.update_index.desc())
        )
        grainbin_updates = Pagination(
            session,
            select_stm,
            page=pagination_parameters.page,
            per_page=pagination_parameters.page_size,
        )

        pagination_parameters.item_count = grainbin_updates.total
        return grainbin_updates.items


@blueprint.route("/<int:grainbin_id>/updates/latest")
class GrainbinUpdatesLatest(MethodView):
    """MethodView for GrainbinUpdate schema that require an ID."""

    @staticmethod
    @blueprint.response(200, GrainbinUpdateSchema(many=True))
    def get(grainbin_id):
        """Get the set of latest GrainbinUpdates for a given Grainbin ID.

        There is an update for each sensor reading in the Grainbin.
        """

        # get the grainbin with grainbin_id
        grainbin = Grainbin.get_by_id(grainbin_id)

        if grainbin is None:
            abort(404, message=f"Grainbin with id: {grainbin_id} not found")

        if grainbin.total_updates == 0:
            abort(404, message=f"No updates for Grainbin with id: {grainbin_id}")

        # get all updates for grainbin_id with update_index equalling the grainbin total_update count.
        # Sort by templow which is the sensor number
        session = get_session()
        grainbin_updates = session.scalars(
            select(GrainbinUpdate)
            .where(GrainbinUpdate.grainbin_id == grainbin_id)
            .where(GrainbinUpdate.update_index == grainbin.total_updates)
            .order_by(GrainbinUpdate.templow.desc())
        ).all()

        return grainbin_updates
