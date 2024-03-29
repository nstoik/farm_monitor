"""Test message models."""

import datetime as dt

import pytest

from fm_database.models.message import Message


@pytest.mark.usefixtures("tables")
class TestMessage:
    """Message model tests."""

    @staticmethod
    def test_create_message():
        """Create a Message instance."""
        message = Message(
            source="Source", destination="Destination", classification="Test"
        )
        message.save()

        assert message.source == "Source"
        assert message.destination == "Destination"
        assert message.classification == "Test"
        assert isinstance(message.created_at, dt.datetime)

    @staticmethod
    def test_message_get_by_id():
        """Retrieve a Message by ID."""
        message = Message(
            source="Source", destination="Destination", classification="Test"
        )
        message.save()

        retrieved = Message.get_by_id(message.id)
        assert isinstance(retrieved, Message)
        assert retrieved.id == message.id

    @staticmethod
    def test_message_set_datetime_default():
        """Test the default validity time of a message."""
        message = Message(
            source="Source", destination="Destination", classification="Test"
        )
        message.set_datetime()
        message.save()

        assert isinstance(message.valid_from, dt.datetime)
        assert isinstance(message.valid_to, dt.datetime)

    @staticmethod
    def test_message_set_datetime():
        """Test setting the validity time of a message."""
        message = Message(
            source="Source", destination="Destination", classification="Test"
        )
        message.set_datetime(
            valid_from=dt.timedelta(days=1), valid_to=dt.timedelta(days=3)
        )
        message.save()

        assert isinstance(message.valid_from, dt.datetime)
        assert isinstance(message.valid_to, dt.datetime)
        assert (
            message.valid_from.hour == (dt.datetime.now() + dt.timedelta(days=1)).hour
        )
        assert message.valid_to.hour == (dt.datetime.now() + dt.timedelta(days=3)).hour

    @staticmethod
    def test_message_pickle():
        """Test pickling a message."""
        message = Message(
            source="Source", destination="Destination", classification="Test"
        )
        message.payload = {"test": "test"}
        message.save()

        retrieved = Message.get_by_id(message.id)

        assert isinstance(retrieved, Message)
        assert retrieved.id == message.id
        assert retrieved.payload == {"test": "test"}
