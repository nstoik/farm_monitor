# -*- coding: utf-8 -*-
"""Models for the system representations."""
from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..database import SurrogatePK, reference_col, str5, str20


class SystemSetup(SurrogatePK):
    """Model if the system has been setup or not."""

    __tablename__ = "system_setup"

    first_setup_complete: Mapped[bool] = mapped_column(default=False)
    first_setup_time: Mapped[datetime | None]
    update_in_progress: Mapped[bool] = mapped_column(default=False)
    new_update_installed: Mapped[bool] = mapped_column(default=False)

    def __init__(self):
        """Create an instance."""
        return


class Wifi(SurrogatePK):
    """Wifi details."""

    __tablename__ = "system_wifi"

    name: Mapped[str20] = mapped_column(default="FarmMonitor")
    password: Mapped[str20] = mapped_column(default="raspberry")
    mode: Mapped[str20] = mapped_column(default="wpa")

    interface_id: Mapped[int] = reference_col("system_interface", nullable=True)
    interface_details: Mapped["Interface"] = relationship(back_populates="credentials")

    def __init__(self):
        """Create an instance."""
        return


class Interface(SurrogatePK):
    """Model an network interface."""

    __tablename__ = "system_interface"

    interface: Mapped[str5]
    is_active: Mapped[bool] = mapped_column(default=True)
    is_for_fm: Mapped[bool] = mapped_column(default=False)
    is_external: Mapped[bool] = mapped_column(default=False)
    state: Mapped[str20 | None]

    credentials: Mapped[list["Wifi"]] = relationship(back_populates="interface_details")

    def __init__(self, interface, **kwargs):
        """Create an instance."""
        super().__init__(interface=interface, **kwargs)


class Hardware(SurrogatePK):
    """Model the system hardware."""

    __tablename__ = "system_hardware"

    device_name: Mapped[str20 | None]
    hardware_version: Mapped[str20 | None]
    serial_number: Mapped[str20 | None]

    def __init__(self):
        """Create an instance."""
        return


class Software(SurrogatePK):
    """The software version."""

    __tablename__ = "system_software"

    software_version: Mapped[str20 | None]
    software_version_last: Mapped[str20 | None]

    def __init__(self):
        """Create an instance."""
        return
