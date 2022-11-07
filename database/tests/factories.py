"""Factories to help in tests."""
# pylint: disable=too-few-public-methods,no-self-argument,unused-argument
from factory import PostGenerationMethodCall, Sequence
from factory.alchemy import SQLAlchemyModelFactory
from factory.declarations import SelfAttribute, SubFactory

from fm_database.base import get_session
from fm_database.models.device import Device, Grainbin
from fm_database.models.user import User


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Override the _create classmethod.

        Does not actually change from the default, but
        for some reason it needs to be specified otherwise
        SubFactory elements do not get the primary key created
        correctly.
        """
        obj = model_class(*args, **kwargs)
        obj.save()
        return obj

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = get_session()


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

    device_id = Sequence(lambda n: f"Test Device {n}")
    hardware_version = "v1"
    software_version = "v1"

    class Meta:
        """Factory configuration."""

        model = Device


class GrainbinFactory(BaseFactory):
    """Grainbin factory."""

    device = SubFactory(DeviceFactory, device_id=SelfAttribute("..device_id"))
    device_id = Sequence(lambda n: f"Test Device {n}")
    bus_number = Sequence(int)

    class Meta:
        """Factory Configuration."""

        model = Grainbin
        exclude = ("device",)
