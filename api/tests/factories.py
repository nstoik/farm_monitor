# -*- coding: utf-8 -*-
"""Factories to help in tests."""
# pylint: disable=too-few-public-methods
from factory import PostGenerationMethodCall, Sequence
from factory.alchemy import SQLAlchemyModelFactory
from factory.declarations import SelfAttribute, SubFactory
from fm_database.database import get_session
from fm_database.models.device import Device, Grainbin
from fm_database.models.user import User


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = get_session()
        sqlalchemy_session_persistence = "flush"


class UserFactory(BaseFactory):
    """User factory."""

    username = Sequence(lambda n: f"user{n}")
    email = Sequence(lambda n: f"user{n}@example.com")
    password = PostGenerationMethodCall("set_password", "example")
    active = True

    class Meta:
        """Factory configuration."""

        model = User


class DeviceFactory(BaseFactory):
    """Device factory."""

    device_id = Sequence(lambda n: f"Test Device{n}")
    hardware_version = "v1"
    software_version = "v1"

    class Meta:
        """Factory configuration."""

        model = Device


class GrainbinFactory(BaseFactory):
    """Grainbin factory."""

    device = SubFactory(DeviceFactory)
    device_id_str = SelfAttribute("device.device_id")
    bus_number = Sequence(int)

    class Meta:
        """Factory configuration."""

        model = Grainbin
        exclude = ("device",)
