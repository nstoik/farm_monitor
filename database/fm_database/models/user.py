# -*- coding: utf-8 -*-
"""A user model."""
from datetime import datetime, timezone
from typing import List

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import SurrogatePK, str30, str80, str128
from ..extensions import pwd_context

user_roles = Table(
    "user_roles",
    SurrogatePK.metadata,
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
    Column("user_id", ForeignKey("users.id"), primary_key=True),
)


class Role(SurrogatePK):
    """A role for a user."""

    __tablename__ = "roles"
    name: Mapped[str80] = mapped_column(unique=True)
    users: Mapped[List["User"]] = relationship(
        secondary=user_roles, back_populates="roles"
    )

    def __init__(self, name, **kwargs):
        """Create instance."""
        super().__init__(name=name, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Role({self.name})>"


class User(SurrogatePK):
    """A user of the app."""

    __tablename__ = "users"
    username: Mapped[str80] = mapped_column(unique=True)
    email: Mapped[str80] = mapped_column(unique=True)
    #: The hashed password
    password: Mapped[str128 | None]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    first_name: Mapped[str30 | None]
    last_name: Mapped[str30 | None]
    active: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)

    roles: Mapped[List[Role]] = relationship(
        secondary=user_roles, back_populates="users"
    )

    def __init__(self, username, email, password=None, **kwargs):
        """Create instance."""
        super().__init__(username=username, email=email, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password) -> None:
        """Set password."""
        self.password = pwd_context.hash(password)

    def check_password(self, value) -> bool:
        """Check password."""
        return pwd_context.verify(value, self.password)

    @property
    def full_name(self) -> str:
        """Full user name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return "First and Last name not set"

    @property
    def is_active(self) -> bool:
        """Return if the user is active."""
        return self.active

    @property
    def is_authenticated(self) -> bool:
        """Return if the user is authenticated."""
        return True

    @property
    def is_anonymous(self) -> bool:
        """Return if the user is anonymous."""
        return False

    def get_id(self) -> str:
        """Return the id of the user.

        Required by Flask-Login.
        https://flask-login.readthedocs.io/en/latest/#your-user-class
        """

        return str(self.id)

    def __repr__(self) -> str:
        """Represent instance as a unique string."""
        return f"<User({self.username})>"
