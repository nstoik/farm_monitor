# -*- coding: utf-8 -*-
"""Database base configuration."""
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from .settings import get_config

Base = declarative_base()

config = get_config()  # pylint: disable=invalid-name
engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
db_session = scoped_session(sessionmaker(bind=engine))


def get_session():
    """Return the sqlalchemy db_session."""

    return db_session


@contextmanager
def session_scope():
    """Provide a transactional scope for a session around a series of operations.

    Example usage:
    'with session_scope() as session:
        do session related work.
        make sure to commit the session if needed.
    """

    try:
        yield db_session
    except Exception as ex:  # noqa B902
        db_session.rollback()
        raise ex
    finally:
        db_session.close()


def get_base(with_query=False):
    """
    Return the sqlalchemy base.

    :param with_query=False. If True is passed, it adds the query property to models.
    """
    if with_query:
        # Adds Query Property to Models - enables `User.query.query_method()`
        Base.query = db_session.query_property()
    return Base


def create_all_tables():
    """Create all tables."""
    base = get_base(with_query=True)
    base.metadata.create_all(bind=engine)


def drop_all_tables():
    """Drop all tables."""
    base = get_base()
    base.metadata.drop_all(bind=engine)
