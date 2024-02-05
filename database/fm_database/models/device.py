# -*- coding: utf-8 -*-
"""Device models."""
from datetime import datetime, timedelta

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from ..database import SurrogatePK, reference_col, str7, str10, str20, str50

# https://github.com/pylint-dev/pylint/issues/8138
# can be removed once upstream issue in pylint is fixed
# pylint: disable=not-callable


class GrainbinUpdate(SurrogatePK):
    """Table to hold Grainbin update data."""

    __tablename__ = "grainbin_update"

    timestamp: Mapped[datetime] = mapped_column(index=True)
    update_index: Mapped[int] = mapped_column(index=True)

    temperature: Mapped[float | None]
    temphigh: Mapped[int | None]  # cable number
    templow: Mapped[int | None]  # sensor number
    sensor_name: Mapped[str20 | None]

    grainbin_id: Mapped[int] = reference_col("grainbin")
    grainbin: Mapped["Grainbin"] = relationship(back_populates="updates")

    def __init__(self, grainbin_id: int) -> None:
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

    creation_time: Mapped[datetime] = mapped_column(default=func.now())
    last_updated: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now()
    )
    name: Mapped[str20] = mapped_column(unique=False)
    grainbin_type: Mapped[str20 | None] = mapped_column(default="standard")
    sensor_type: Mapped[str20 | None] = mapped_column(default="temperature")
    location: Mapped[str20]
    description: Mapped[str50]
    total_updates: Mapped[int] = mapped_column(default=0)
    average_temp: Mapped[str7 | None]
    bus_number: Mapped[int]
    bus_number_string: Mapped[str10]
    user_configured: Mapped[bool] = mapped_column(default=False)

    updates: Mapped[list["GrainbinUpdate"]] = relationship(back_populates="grainbin")
    device_id_str: Mapped[str] = reference_col("device", pk_name="device_id")
    device: Mapped["Device"] = relationship(back_populates="grainbins")

    def __init__(
        self,
        device_id_str: str,
        bus_number: int,
        name: str = "New",
        location: str = "Not Set",
        description: str = "Not Set",
    ):
        """Create an instance."""
        self.name = name
        self.device_id_str = device_id_str
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

    timestamp: Mapped[datetime] = mapped_column(index=True)
    update_index: Mapped[int] = mapped_column(index=True)

    interior_temp: Mapped[float | None]
    exterior_temp: Mapped[float | None]
    device_temp: Mapped[float | None]
    uptime: Mapped[timedelta | None]
    load_avg: Mapped[int | None]
    disk_total: Mapped[int | None]
    disk_used: Mapped[int | None]
    disk_free: Mapped[int | None]

    device_id: Mapped[int] = reference_col("device")
    device: Mapped["Device"] = relationship(back_populates="updates")

    def __init__(self, device_id: int) -> None:
        """Create an instance."""

        self.device_id = device_id

    def __repr__(self) -> str:
        """Represent a DeviceUpdate as a string."""

        return f"DeviceUpdate for Device {self.device_id} taken on {self.timestamp}"

    def save(self, commit=True):
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

        return super().save(commit)


class Device(SurrogatePK):
    """A device."""

    __tablename__ = "device"
    device_id: Mapped[str20] = mapped_column(unique=True)
    hardware_version: Mapped[str20]
    software_version: Mapped[str20]

    creation_time: Mapped[datetime] = mapped_column(default=func.now())
    last_updated: Mapped[datetime] = mapped_column(
        default=func.now(), onupdate=func.now()
    )
    total_updates: Mapped[int] = mapped_column(default=0)
    name: Mapped[str20] = mapped_column(unique=False)
    location: Mapped[str20]
    description: Mapped[str50]
    connected: Mapped[bool] = mapped_column(default=False)
    user_configured: Mapped[bool] = mapped_column(default=False)
    last_update_received: Mapped[datetime | None]

    updates = relationship("DeviceUpdate", back_populates="device")

    # grainbin related data
    grainbin_count: Mapped[int] = mapped_column(default=0)
    grainbins: Mapped[list["Grainbin"]] = relationship(back_populates="device")

    def __init__(
        self,
        device_id: str,
        hardware_version: str,
        software_version: str,
        name: str = "not set",
        location: str = "not set",
        description: str = "not set",
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
