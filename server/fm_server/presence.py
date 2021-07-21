"""Run a service that responds to pings with the address of the rabbitmq broker."""
import logging
import socket
import time

from fm_database.base import get_session
from fm_database.models.system import Interface

from fm_server.settings import get_config
from fm_server.system.info import get_ip_of_interface


def presence_service():
    """Presence service that responds to pings."""

    logger = logging.getLogger("fm.presence")

    session = get_session()
    interface = session.query(Interface.interface).filter_by(is_for_fm=True).scalar()
    session.close()
    config = get_config()
    presence_port = config.PRESENCE_PORT

    if interface is None:
        logger.warning(
            "Interface from database is None. Has initial configuration been run? Setting interface to 'eth0'"
        )
        interface = "eth0"

    logger.debug("Interface and port are: %s %s", interface, presence_port)
    broadcast_address = get_ip_of_interface(interface, broadcast=True)
    logger.debug("Presence broadcast address is: %s", broadcast_address)

    # Create UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # Ask operating system to let us do broadcasts from socket
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    # Bind UDP socket to local port so we can receive pings
    sock.bind((broadcast_address, int(presence_port)))

    logger.info("Presence service is active")
    try:
        # send ping every 5 seconds for first 1 day
        for _ in range(int(86400 / 60)):
            # logger.debug("Sending ping via: %s:%s", broadcast_address, presence_port)
            sock.sendto(b"!", 0, (broadcast_address, int(presence_port)))
            time.sleep(5)

        # then send once every minute until stopped
        while True:
            # Broadcast our beacon
            # logger.debug("Sending ping via: %s:%s", broadcast_address, presence_port)
            sock.sendto(b"!", 0, (broadcast_address, int(presence_port)))
            time.sleep(60)
    except KeyboardInterrupt:
        logger.info("Stopping presence service")
        sock.close()


if __name__ == "__main__":
    presence_service()
