# -*- coding: utf-8 -*-
"""Device models."""
from sqlalchemy import Boolean, Column, DateTime, Float, Integer, Interval, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..database import SurrogatePK, reference_col


class GrainbinUpdate(SurrogatePK):
    """Table to hold Grainbin update data."""

    __tablename__ = "grainbin_update"

    timestamp = Column(DateTime, nullable=False, index=True)
    update_index = Column(Integer, nullable=False, index=True)

    temperature = Column(Float(), nullable=True, default=None)
    temphigh = Column(Integer(), nullable=True, default=None)  # cable number
    templow = Column(Integer(), nullable=True, default=None)  # sensor number
    sensor_name = Column(String(20), nullable=True, default=None)

    grainbin_id = reference_col("grainbin")

    def __init__(self, grainbin_id) -> None:
        """Create an instance."""

        self.grainbin_id = grainbin_id

    def __repr__(self) -> str:
        """Represent a GrainbinUpdate as a string."""

        return (
            f"GrainbinUpdate for Grainbin {self.grainbin_id} taken on {self.timestamp}"
        )


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
    total_updates = Column(Integer, nullable=False, default=0)
    average_temp = Column(String(7))
    bus_number = Column(Integer, nullable=False)
    bus_number_string = Column(String(10), nullable=False)
    user_configured = Column(Boolean, default=False)

    updates = relationship("GrainbinUpdate", backref="grainbin")
    device_id = reference_col("device", pk_name="device_id")

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
        self.bus_number_string = f"bus.{bus_number}"
        self.location = location
        self.description = description
        self.total_updates = 0

    def __repr__(self):
        """Represent the grainbin as a string."""
        return f"<Grainbin: {self.id}>"


class DeviceUpdate(SurrogatePK):
    """Table to hold Device Update data."""

    __tablename__ = "device_update"

    timestamp = Column(DateTime, nullable=False, index=True)
    update_index = Column(Integer, nullable=False, index=True)

    interior_temp = Column(Float(), nullable=True, default=None)
    exterior_temp = Column(Float(), nullable=True, default=None)
    device_temp = Column(Float(), nullable=True, default=None)
    uptime = Column(Interval, nullable=True, default=None)
    load_avg = Column(Integer(), nullable=True, default=None)
    disk_total = Column(Integer(), nullable=True, default=None)
    disk_used = Column(Integer(), nullable=True, default=None)
    disk_free = Column(Integer(), nullable=True, default=None)

    device_id = reference_col("device")

    def __init__(self, device_id) -> None:
        """Create an instance."""

        self.device_id = device_id

    def __repr__(self) -> str:
        """Represent a DeviceUpdate as a string."""

        return f"DeviceUpdate for Device {self.device_id} taken on {self.timestamp}"

    def save(self, session=None, commit=True):
        """Save the record. Check for valid interior_temp and exterior_temp."""

        if self.interior_temp is not None:
            try:
                float(self.interior_temp)
            except ValueError:
                self.interior_temp = None

        if self.exterior_temp is not None:
            try:
                float(self.exterior_temp)
            except ValueError:
                self.exterior_temp = None

        return super().save(session, commit)


class Device(SurrogatePK):
    """A device."""

    __tablename__ = "device"
    device_id = Column(String(20), unique=True)
    hardware_version = Column(String(20))
    software_version = Column(String(20))

    creation_time = Column(DateTime, default=func.now())
    last_updated = Column(DateTime, default=func.now(), onupdate=func.now())
    total_updates = Column(Integer, nullable=False, default=0)
    name = Column(String(20), nullable=False, unique=False)
    location = Column(String(20))
    description = Column(String(50))
    connected = Column(Boolean, default=False)
    user_configured = Column(Boolean, default=False)
    last_update_received = Column(DateTime, nullable=True, default=None)

    updates = relationship("DeviceUpdate", backref="device")

    # grainbin related data
    grainbin_count = Column(Integer, default=0)
    bins = relationship("Grainbin", backref="device")

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
