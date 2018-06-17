""" system control module """

import subprocess
import logging
from sqlalchemy.orm.exc import NoResultFound

from fm_database.base import get_session
from fm_database.models.system import Hardware, Software
from .info import get_device_name, get_serial


def set_device_name(name):
    """ set device name """
    name = "hostname -b "+ name
    subprocess.call(name)
    return


def shutdown():
    """ shutdown device """
    command = ['sudo', 'shutdown', 'now']
    subprocess.check_call(command)

    return

def restart():
    """ restart device """
    command = ['sudo', 'reboot']
    subprocess.check_call(command)

    return


def set_service_state(control):
    """ set the state of the service """
    logger = logging.getLogger('fm.system.control')
    logger.info("Setting service state: %s", control)
    command = ["sudo", "systemctl", control, "farm-monitor.service"]
    subprocess.check_output(command, universal_newlines=True)

    return


def set_hardware_info(hardware_version):
    """ set hardware info """
    logger = logging.getLogger('fm.system.control')
    logger.debug("Setting hardware: %s", hardware_version)
    session = get_session()

    device_name = get_device_name()
    serial_number = get_serial()

    try:
        hd = session.query(Hardware).one()
        hd.hardware_version = hardware_version
        hd.device_name = device_name
        hd.serial_number = serial_number

    except NoResultFound:
        hd = Hardware()
        hd.hardware_version = hardware_version
        hd.device_name = device_name
        hd.serial_number = serial_number
        session.add(hd)

    session.commit()
    session.close()

    return


def set_software_info(software_version, device_service=None, grainbin_service=None):
    """ set software info """
    logger = logging.getLogger('fm.system.control')
    logger.debug("Setting software: %s, device: %s, grainbin: %s", software_version,\
                                                                   device_service,\
                                                                   grainbin_service)
    session = get_session()

    try:
        sd = session.query(Software).one()
        sd.software_version = software_version
        if device_service is not None:
            sd.device_service = device_service
        if grainbin_service is not None:
            sd.grainbin_service = grainbin_service

    except NoResultFound:
        sd = Software()
        sd.software_version = software_version
        if device_service is not None:
            sd.device_service = device_service
        if grainbin_service is not None:
            sd.grainbin_service = grainbin_service
        session.add(sd)

    session.commit()
    session.close()

    return
