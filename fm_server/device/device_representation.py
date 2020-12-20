"""Represent a device to a worker."""


class DeviceRep:
    """Helper class to represent a device to a worker."""

    HEARTBEAT_LIVES = 3

    def __init__(self, device_id):
        """Create a DeviceRep object."""
        self.device_id = device_id
        self.lives = self.HEARTBEAT_LIVES

    def heartbeat(self):
        """Decrease live count by ."""
        if self.lives > 0:
            self.lives -= 1

    def on_message_received(self):
        """Set live count to max when message received."""
        self.lives = self.HEARTBEAT_LIVES

    def is_alive(self):
        """Determine if the device is still alive."""
        return self.lives > 0
