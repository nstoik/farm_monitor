# -*- coding: utf-8 -*-
"""Message model for farm monitor."""
import datetime as dt

from sqlalchemy import Column, DateTime, PickleType, String
from sqlalchemy.sql import func

from ..database import SurrogatePK


class Message(SurrogatePK):
    """A message sent between devices."""

    __tablename__ = "message"

    source = Column(String(20))
    destination = Column(String(20))
    classification = Column(String(20))

    created_at = Column(DateTime, default=func.now())
    valid_from = Column(DateTime)
    valid_to = Column(DateTime)

    payload = Column(PickleType, default=None)

    def __init__(self, source, destination, classification):
        """Create an instance."""
        self.source = source
        self.destination = destination
        self.classification = classification

    def set_datetime(
        self, valid_from: dt.timedelta = None, valid_to: dt.timedelta = None
    ):
        """Set the valid_from and valid_to dates. Input must be a timedelta object."""

        if valid_to is None:
            valid_to = dt.timedelta(days=1)

        if valid_from is None:
            valid_from = dt.timedelta(seconds=0)

        self.valid_from = dt.datetime.now() + valid_from
        self.valid_to = dt.datetime.now() + valid_to
