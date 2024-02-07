"""Factories to use in tests."""

# pylint: disable=too-few-public-methods
from factory import Sequence
from factory.alchemy import SQLAlchemyModelFactory
from factory.declarations import SelfAttribute, SubFactory
from fm_database.database import get_session
from fm_database.models.device import Device, Grainbin


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""

    class Meta:
        """Meta class."""

        abstract = True
        sqlalchemy_session = get_session()
        sqlalchemy_session_persistence = "flush"


class DeviceFactory(BaseFactory):
    """Device Factory."""

    device_id = Sequence(lambda n: f"Test Device {n}")
    hardware_version = "v1"
    software_version = "v1"

    class Meta:
        """Meta class."""

        model = Device


class GrainbinFactory(BaseFactory):
    """Grainbin Factory."""

    device = SubFactory(DeviceFactory, device_id=SelfAttribute("..device_id_str"))
    device_id_str = Sequence(lambda n: f"Test Device {n}")
    bus_number = Sequence(int)

    class Meta:
        """Meta class."""

        model = Grainbin
        exclude = ("device",)
