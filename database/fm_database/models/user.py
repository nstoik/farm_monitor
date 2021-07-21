# -*- coding: utf-8 -*-
"""A user model."""
import datetime as dt

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from ..database import SurrogatePK
from ..extensions import pwd_context

user_roles = Table(
    "user_roles",
    SurrogatePK.metadata,
    Column("role_id", Integer, ForeignKey("roles.id")),
    Column("user_id", Integer, ForeignKey("users.id")),
)


class Role(SurrogatePK):
    """A role for a user."""

    __tablename__ = "roles"
    name = Column(String(80), unique=True, nullable=False)
    users = relationship("User", secondary=user_roles, backref="roles")

    def __init__(self, name, **kwargs):
        """Create instance."""
        super().__init__(name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return "<Role({name})>".format(name=self.name)


class User(SurrogatePK):
    """A user of the app."""

    __tablename__ = "users"
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(String(128), nullable=True)
    created_at = Column(DateTime, nullable=False, default=dt.datetime.utcnow)
    first_name = Column(String(30), nullable=True)
    last_name = Column(String(30), nullable=True)
    active = Column(Boolean(), nullable=False, default=True)
    is_admin = Column(Boolean(), nullable=False, default=False)

    def __init__(self, username, email, password=None, **kwargs):
        """Create instance."""
        super().__init__(username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        """Set password."""
        self.password = pwd_context.hash(password)

    def check_password(self, value):
        """Check password."""
        return pwd_context.verify(value, self.password)

    @property
    def full_name(self):
        """Full user name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return "First and Last name not set"

    @property
    def is_active(self):
        """Return if the user is active."""
        return self.active

    @property
    def is_authenticated(self):
        """Return if the user is authenticated."""
        return True

    @property
    def is_anonymous(self):
        """Return if the user is anonymous."""
        return False

    def get_id(self):
        """Return the id of the user.

        Required by Flask-Login.
        https://flask-login.readthedocs.io/en/latest/#your-user-class
        """

        return str(self.id)

    def __repr__(self):
        """Represent instance as a unique string."""
        return "<User({username!r})>".format(username=self.username)
