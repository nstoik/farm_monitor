"""Test the presence service."""
import time
from multiprocessing import Process

import pytest

from fm_server.presence import presence_service


@pytest.mark.usefixtures("database_base_seed")
def test_presence_start():
    """Test that the presence service starts."""

    presence_controller = Process(target=presence_service)
    presence_controller.start()

    time.sleep(1)

    presence_controller.terminate()
    presence_controller.join()

    # exitcode is the negative of the signal used to terminate
    # the process. 15 is SIGTERM
    assert presence_controller.exitcode == -15
