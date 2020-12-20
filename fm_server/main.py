"""Main starting point for fm_server."""
import logging
import time
from logging.handlers import RotatingFileHandler
from multiprocessing import Process

from multiprocessing_logging import install_mp_handler

from .device.service import run_device
from .presence import presence_service
from .settings import get_config


def configure_logging(config):
    """Configure logging for the entire app."""

    logger = logging.getLogger("fm")
    logfile_path = config.LOG_FILE
    log_level = config.LOG_LEVEL

    logger.setLevel(log_level)
    logger.propagate = False

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    file_handler = RotatingFileHandler(
        logfile_path, mode="a", maxBytes=1024 * 1024, backupCount=10
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if log_level == logging.DEBUG:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    install_mp_handler(logger=logger)

    return logger


def main():
    """Main starting point for program."""

    config = get_config()
    logger = configure_logging(config)
    # pika_test()

    presence_controller = Process(target=presence_service)
    presence_controller.start()

    device_controller = Process(target=run_device)
    device_controller.start()

    try:
        presence_controller.join()
        device_controller.join()
    except KeyboardInterrupt:
        logger.warning("Keyboard interrupt in main")

        time.sleep(1)

        presence_controller.terminate()
        device_controller.terminate()

        presence_controller.join()
        device_controller.join()
    return


if __name__ == "__main__":
    main()
