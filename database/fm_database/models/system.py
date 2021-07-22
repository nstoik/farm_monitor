# -*- coding: utf-8 -*-
"""Models for the system representations."""
from sqlalchemy import Boolean, Column, DateTime, String
from sqlalchemy.orm import relationship

from ..database import SurrogatePK, reference_col


class SystemSetup(SurrogatePK):
    """Model if the system has been setup or not."""

    __tablename__ = "system_setup"

    first_setup_complete = Column(Boolean, default=False)
    first_setup_time = Column(DateTime)
    update_in_progress = Column(Boolean, default=False)
    new_update_installed = Column(Boolean, default=False)

    def __init__(self):
        """Create an instance."""
        return


class Wifi(SurrogatePK):
    """Wifi details."""

    __tablename__ = "system_wifi"

    name = Column(String(20), default="FarmMonitor")
    password = Column(String(20), default="raspberry")
    mode = Column(String(20), default="wpa")

    interface_id = reference_col("system_interface", nullable=True)
    interface = relationship("Interface", backref="credentials")

    def __init__(self):
        """Create an instance."""
        return


class Interface(SurrogatePK):
    """Model an network interface."""

    __tablename__ = "system_interface"

    interface = Column(String(5), nullable=False)
    is_active = Column(Boolean, default=True)
    is_for_fm = Column(Boolean, default=False)
    is_external = Column(Boolean, default=False)
    state = Column(String(20))

    def __init__(self, interface, **kwargs):
        """Create an instance."""
        super().__init__(interface=interface, **kwargs)


class Hardware(SurrogatePK):
    """Model the system hardware."""

    __tablename__ = "system_hardware"

    device_name = Column(String(20))
    hardware_version = Column(String(20))
    serial_number = Column(String(20))

    def __init__(self):
        """Create an instance."""
        return


class Software(SurrogatePK):
    """The software version."""

    __tablename__ = "system_software"

    software_version = Column(String(20))
    software_version_last = Column(String(20))

    def __init__(self):
        """Create an instance."""
        return
