# -*- coding: utf-8 -*-
"""Database module, including the SQLAlchemy database object and DB-related utilities."""
from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    scoped_session,
    sessionmaker,
)

from .settings import get_config

config = get_config()  # pylint: disable=invalid-name
engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
db_session = scoped_session(sessionmaker(bind=engine))


def get_session():
    """Return the sqlalchemy db_session."""

    return db_session


def create_all_tables():
    """Create all tables."""
    Base.metadata.create_all(bind=engine)


def drop_all_tables():
    """Drop all tables."""
    Base.metadata.drop_all(bind=engine)


class Base(DeclarativeBase):  # pylint: disable=too-few-public-methods
    """Base class for all SQLAlchemy models."""

    type_annotation_map = {}


class CRUDMixin:
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return self.save() if commit else self

    def save(self, commit=True):
        """Save the record."""
        db_session.add(self)
        if commit:
            db_session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db_session.delete(self)
        return commit and db_session.commit()


class Model(CRUDMixin, Base):  # type: ignore[valid-type, misc]
    """Base model class that includes CRUD convenience methods."""

    __abstract__ = True


# From Mike Bayer's "Building the app" talk
# https://speakerdeck.com/zzzeek/building-the-app
class SurrogatePK(Model):  # pylint: disable=too-few-public-methods
    """A mixin that adds a surrogate integer 'primary key' column named ``id`` to any declarative-mapped class."""

    __table_args__ = {"extend_existing": True}
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)

    @classmethod
    def get_by_id(cls, record_id):
        """Get record by ID."""
        if any(
            (
                isinstance(record_id, (str, bytes)) and record_id.isdigit(),
                isinstance(record_id, (int, float)),
            ),
        ):
            return db_session.get(cls, int(record_id))
        return None


def reference_col(tablename, nullable=False, pk_name="id", **kwargs) -> Mapped[int]:
    """Column that adds primary key foreign key reference.

    Usage: ::

        category_id: Mapped[ForeignKey] = reference_col('category')
        categorys: Mapped[List["Category"]] = relationship(backref='categories')
    """
    return mapped_column(
        ForeignKey(f"{tablename}.{pk_name}"), nullable=nullable, **kwargs
    )
