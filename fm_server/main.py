""" main starting point for fm_server """
import logging
from multiprocessing import Process

from .settings import get_config
from .presence import presence_service
from .tools.mp_logging import MultiProcessingLog, MultiProcessingLogStandardOutput
from .device.service import run_device


def configure_logging(config):
    """ configure logging for the entire app """

    logger = logging.getLogger('fm')
    logfile_path = config.LOG_FILE
    log_level = config.LOG_LEVEL
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    handler = MultiProcessingLog(logfile_path, mode='a', maxsize=1024 * 1024, rotate=10)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(log_level)
    logger.propagate = False

    if log_level == logging.DEBUG:
        debug_handler = MultiProcessingLogStandardOutput()
        debug_handler.setFormatter(formatter)
        logger.addHandler(debug_handler)

    return logger

def main():
    """ main starting point for program """

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
        logger.warning('Keyboard interrupt in main')

        presence_controller.terminate()
        device_controller.terminate()

        presence_controller.join()
        device_controller.join()
    return


if __name__ == '__main__':
    main()
