"""Module to add pagination to the database.

Taken from https://github.com/pallets/flask-sqlalchemy/blob/main/src/flask_sqlalchemy/__init__.py#L342
"""
from math import ceil

from sqlalchemy.orm import Query


class Pagination:
    """Internal helper class returned by :meth:`BaseQuery.paginate`.

    You can also construct it from any other SQLAlchemy query object if you are
    working with other libraries.  Additionally it is possible to pass `None`
    as query object in which case the :meth:`prev` and :meth:`next` will
    no longer work.
    """

    def __init__(self, query, page, per_page, total, items):
        """Initiate the class."""
        #: the unlimited query object that was used to create this
        #: pagination object.
        self.query = query
        #: the current page number (1 indexed)
        self.page = page
        #: the number of items to be displayed on a page.
        self.per_page = per_page
        #: the total number of items matching the query
        self.total = total
        #: the items for the current page
        self.items = items

    @property
    def pages(self):
        """The total number of pages."""
        if self.per_page == 0 or self.total is None:
            pages = 0
        else:
            pages = int(ceil(self.total / float(self.per_page)))
        return pages

    def prev(self, error_out=False):
        """Returns a :class:`Pagination` object for the previous page."""
        assert (
            self.query is not None
        ), "a query object is required for this method to work"
        return self.query.paginate(self.page - 1, self.per_page, error_out)

    @property
    def prev_num(self):
        """Number of the previous page."""
        if not self.has_prev:
            return None
        return self.page - 1

    @property
    def has_prev(self):
        """True if a previous page exists."""
        return self.page > 1

    def next(self, error_out=False):
        """Returns a :class:`Pagination` object for the next page."""
        assert (
            self.query is not None
        ), "a query object is required for this method to work"
        return self.query.paginate(self.page + 1, self.per_page, error_out)

    @property
    def has_next(self):
        """True if a next page exists."""
        return self.page < self.pages

    @property
    def next_num(self):
        """Number of the next page."""
        if not self.has_next:
            return None
        return self.page + 1

    def iter_pages(self, left_edge=2, left_current=2, right_current=5, right_edge=2):
        """Iterates over the page numbers in the pagination.

        The four parameters control the thresholds how many numbers should be produced
        from the sides.  Skipped page numbers are represented as `None`.
        This is how you could render such a pagination in the templates:
        .. sourcecode:: html+jinja
            {% macro render_pagination(pagination, endpoint) %}
              <div class=pagination>
              {%- for page in pagination.iter_pages() %}
                {% if page %}
                  {% if page != pagination.page %}
                    <a href="{{ url_for(endpoint, page=page) }}">{{ page }}</a>
                  {% else %}
                    <strong>{{ page }}</strong>
                  {% endif %}
                {% else %}
                  <span class=ellipsis>???</span>
                {% endif %}
              {%- endfor %}
              </div>
            {% endmacro %}
        """
        last = 0
        for num in range(1, self.pages + 1):
            if (
                num <= left_edge
                or (
                    num  # pylint: disable=chained-comparison
                    > self.page - left_current - 1
                    and num < self.page + right_current
                )
                or num > self.pages - right_edge
            ):
                if last + 1 != num:
                    yield None
                yield num
                last = num


class PaginateQuery(Query):  # pylint: disable=too-many-ancestors
    """Custom Query class to add paginate method."""

    def paginate(
        self, page=None, per_page=None, error_out=True, max_per_page=None, count=True
    ):  # pylint: disable=unused-argument
        """Paginate method  returns ``per_page`` items from page ``page``.

        If ``page`` and ``per_page`` are ``None``, they default to 1 and 20 respectively.
        If ``max_per_page`` is specified, ``per_page`` will be limited to that value.
        If ``count`` is ``False``, no query to help determine total page count will be run.

        ``error_out`` is included in the method signature to be compatibale with the
        Flask-Sqlalchemy extenssion where this idea is from.

        Returns a :class:`Pagination` object.
        """

        if page is None:
            page = 1

        page = max(1, page)

        if per_page is None:
            per_page = 20

        per_page = max(1, per_page)

        if max_per_page is not None:
            per_page = min(per_page, max_per_page)

        items = self.limit(per_page).offset((page - 1) * per_page).all()

        if not count:
            total = None
        else:
            total = self.order_by(None).count()

        return Pagination(self, page, per_page, total, items)
