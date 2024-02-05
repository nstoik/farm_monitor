# -*- coding: utf-8 -*-
"""Database module, including the SQLAlchemy database object and DB-related utilities."""
from typing import Any, Self

from sqlalchemy import ForeignKey, String, create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    scoped_session,
    sessionmaker,
)
from typing_extensions import Annotated

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


# special types for SQLAlchemy
str128 = Annotated[str, 128]  # pylint: disable=invalid-name
str80 = Annotated[str, 80]  # pylint: disable=invalid-name
str50 = Annotated[str, 50]  # pylint: disable=invalid-name
str30 = Annotated[str, 30]  # pylint: disable=invalid-name
str20 = Annotated[str, 20]  # pylint: disable=invalid-name
str10 = Annotated[str, 10]  # pylint: disable=invalid-name
str7 = Annotated[str, 7]  # pylint: disable=invalid-name
str5 = Annotated[str, 5]  # pylint: disable=invalid-name


class Base(DeclarativeBase):  # pylint: disable=too-few-public-methods
    """Base class for all SQLAlchemy models."""

    type_annotation_map = {
        str128: String(128),
        str80: String(80),
        str50: String(50),
        str30: String(30),
        str20: String(20),
        str10: String(10),
        str7: String(7),
        str5: String(5),
    }


class CRUDMixin:
    """Mixin that adds convenience methods for CRUD (create, read, update, delete) operations."""

    @classmethod
    def create(cls, **kwargs) -> Self:
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs) -> Self:
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return self.save() if commit else self

    def save(self, commit=True) -> Self:
        """Save the record."""
        db_session.add(self)
        if commit:
            db_session.commit()
        return self

    def delete(self, commit=True) -> None:
        """Remove the record from the database."""
        db_session.delete(self)
        if commit:
            db_session.commit()


class Model(CRUDMixin, Base):
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
    def get_by_id(cls, record_id: str | bytes | int | float) -> Self | None:
        """Get record by ID."""
        if any(
            (
                isinstance(record_id, (str, bytes)) and record_id.isdigit(),
                isinstance(record_id, (int, float)),
            ),
        ):
            return db_session.get(cls, int(record_id))
        return None


def reference_col(tablename, nullable=False, pk_name="id", **kwargs) -> Mapped[Any]:
    """Column that adds primary key foreign key reference.

    The returned column type will be either `int` or `str`

    Usage: ::

    For a bi-directional one to many relationship

    Parent:
        children: Mapped[List["Child"]] = relationship(back_populates="parent")

    Child:
        parent_id: Mapped[int] = reference_col('parent')
        parent: Mapped["Parent"] = relationship(back_populates='children')


    For a bi-directional many to one relationship

    Parent:
        child_id: Mapped[int] = reference_col('child')
        child: Mapped["Child"] = relationship(back_populates='parents')

    Child:
        parents: Mapped[List["Parent"]] = relationship(back_populates='child')

    For a many to many relationship see:
    https://docs.sqlalchemy.org/en/20/orm/basic_relationships.html#many-to-many
    """
    return mapped_column(
        ForeignKey(f"{tablename}.{pk_name}"), nullable=nullable, **kwargs
    )
