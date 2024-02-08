# -*- coding: utf-8 -*-
"""Message model for farm monitor."""
from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import PickleType
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from ..database import SurrogatePK, str20

# https://github.com/pylint-dev/pylint/issues/8138
# can be removed once upstream issue in pylint is fixed
# pylint: disable=not-callable


class Message(SurrogatePK):
    """A message sent between devices."""

    __tablename__ = "message"

    source: Mapped[str20]
    destination: Mapped[str20]
    classification: Mapped[str20]

    created_at: Mapped[datetime] = mapped_column(default=func.now())
    valid_from: Mapped[datetime | None]
    valid_to: Mapped[datetime | None]

    payload: Mapped[Any | None] = mapped_column(PickleType)

    def __init__(self, source: str, destination: str, classification: str):
        """Create an instance."""
        self.source = source
        self.destination = destination
        self.classification = classification

    def set_datetime(
        self, valid_from: timedelta | None = None, valid_to: timedelta | None = None
    ):
        """Set the valid_from and valid_to dates. Input must be a timedelta object."""

        if valid_to is None:
            valid_to = timedelta(days=1)

        if valid_from is None:
            valid_from = timedelta(seconds=0)

        self.valid_from = datetime.now() + valid_from
        self.valid_to = datetime.now() + valid_to
