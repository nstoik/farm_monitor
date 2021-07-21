# -*- coding: utf-8 -*-
"""Device models."""
from sqlalchemy import Boolean, Column, DateTime, Integer, Interval, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import SurrogatePK, reference_col


class TemperatureSensor(SurrogatePK):
    """Model a temperature sensor."""

    __tablename__ = "temperature_sensor"

    templow = Column(String(4))
    temphigh = Column(String(4))
    last_value = Column(String(7))
    cable_id = reference_col("temperature_cable")

    def __init__(self, cable_id):
        """Create the instance."""
        self.cable_id = cable_id
        self.last_value = "unknown"

    def __repr__(self):
        """Represent the instance as a string."""
        return f"<TemperatureSensor: {self.id}>"


class TemperatureCable(SurrogatePK):
    """Model a temperature cable."""

    __tablename__ = "temperature_cable"

    sensor_count = Column(Integer, default=0)
    cable_type = Column(String(20), default="temperature")
    bin_cable_number = Column(Integer, default=0)

    sensors = relationship("TemperatureSensor")
    grainbin_id = reference_col("grainbin")

    def __init__(self, grainbin_id):
        """Create the instance."""
        self.grainbin_id = grainbin_id

    def __repr__(self):
        """Represent the instance as a string."""
        return f"<TemperatureCable: {self.id}>"


class Grainbin(SurrogatePK):
    """A grainbin."""

    __tablename__ = "grainbin"

    creation_time = Column(DateTime, default=func.now())
    last_updated = Column(DateTime, default=func.now(), onupdate=func.now())
    name = Column(String(20), nullable=False, unique=False)
    grainbin_type = Column(String(20), nullable=True, default="standard")
    sensor_type = Column(String(20), nullable=True, default="temperature")
    location = Column(String(20))
    description = Column(String(50))
    total_updates = Column(Integer)
    average_temp = Column(String(7))
    bus_number = Column(Integer, nullable=False)
    user_configured = Column(Boolean, default=False)

    cables = relationship("TemperatureCable")
    device_id = reference_col("device")

    def __init__(
        self,
        device_id,
        bus_number,
        name="New",
        location="Not Set",
        description="Not Set",
    ):
        """Create an instance."""
        self.name = name
        self.device_id = device_id
        self.bus_number = bus_number
        self.location = location
        self.description = description
        self.total_updates = 0

    def __repr__(self):
        """Represent the grainbin as a string."""
        return f"<Grainbin: {self.id}>"


class Device(SurrogatePK):
    """A device."""

    __tablename__ = "device"
    device_id = Column(String(20), unique=True)
    hardware_version = Column(String(20))
    software_version = Column(String(20))

    creation_time = Column(DateTime, default=func.now())
    last_updated = Column(DateTime, default=func.now(), onupdate=func.now())
    name = Column(String(20), nullable=False, unique=False)
    location = Column(String(20))
    description = Column(String(50))
    connected = Column(Boolean, default=False)
    user_configured = Column(Boolean, default=False)

    last_update_received = Column(DateTime, nullable=True, default=None)
    interior_temp = Column(String(7), nullable=True, default=None)
    exterior_temp = Column(String(7), nullable=True, default=None)
    device_temp = Column(String(7), nullable=True, default=None)
    uptime = Column(Interval, nullable=True, default=None)
    current_time = Column(DateTime, nullable=True, default=None)
    load_avg = Column(String(20), nullable=True, default=None)
    disk_total = Column(String(20), nullable=True, default=None)
    disk_used = Column(String(20), nullable=True, default=None)
    disk_free = Column(String(20), nullable=True, default=None)

    # grainbin related data
    grainbin_count = Column(Integer, default=0)
    bins = relationship("Grainbin")

    def __init__(
        self,
        device_id,
        hardware_version,
        software_version,
        name="not set",
        location="not set",
        description="not set",
    ):
        """Create the instance."""
        self.device_id = device_id
        self.name = name
        self.hardware_version = hardware_version
        self.software_version = software_version
        self.location = location
        self.description = description

    def __repr__(self):
        """Represent the device as a string."""
        return f"<Device: {self.name}>"
