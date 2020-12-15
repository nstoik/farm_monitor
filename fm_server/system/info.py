""" system info module """

import datetime
import logging
import os
import socket
import subprocess

import netifaces
import psutil

logger = logging.getLogger('fm.system.info') # pylint: disable=invalid-name


def get_ip_of_interface(interface, broadcast=False):
    """ get the ip address of a given interface """

    if not broadcast:
        ip = netifaces.ifaddresses(interface)[2][0]['addr']

    else:
        ip = netifaces.ifaddresses(interface)[2][0]['broadcast']

    return ip


def get_uptime():
    """ get uptime of device """
    logger.debug("getting uptime")
    uptime = subprocess.check_output(["uptime", "-p"], universal_newlines=True)
    return uptime[3:]


def get_CPU_temperature():
    """ get CPU temperature """
    logger.debug("getting CPU temperature")
    filepath = "/sys/class/thermal/thermal_zone0/temp"
    res = subprocess.check_output(["cat", filepath], universal_newlines=True)
    return float(int(res) / 1000)


def get_service_status():
    """ get service status """
    logger.debug("getting service status")
    raise NotImplementedError


def get_device_name():
    """ get device name """
    logger.debug("getting device name")
    device_name = socket.gethostname()
    return device_name


def get_serial():
    """ get serial number """
    logger.debug("getting serial number")
    # Extract serial from cpuinfo file
    cpuserial = "0000000000000000"
    try:
        f = open('/proc/cpuinfo', 'r')
        for line in f:
            if line[0:6] == 'Serial':
                cpuserial = line[10:26]
        f.close()
    except:
        cpuserial = "ERROR000000000"

    return cpuserial


def get_system_data():
    """ get system data """
    logger.debug("getting system data")
    system_data = {}
    system_data['uptime'] = get_uptime()
    system_data['current_time'] = datetime.datetime.now()
    system_data['load_avg'] = os.getloadavg()
    system_data['cpu_temp'] = getCPUtemperature()

    return system_data


def get_system_memory():
    """ get system memory"""
    logger.debug("getting system memory")
    system_mem = {}

    virtual_mem = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    system_mem['ram_used'] = virtual_mem.used // 2**20  # MB
    system_mem['ram_total'] = virtual_mem.total // 2**20  # MB
    system_mem['ram_free'] = virtual_mem.free // 2**20  # MB
    system_mem['disk_used'] = round(float(disk.used) / 2**30, 3)  # GB
    system_mem['disk_total'] = round(float(disk.total) / 2**30, 3)  # GB
    system_mem['disk_free'] = round(float(disk.free) / 2**30, 3)  # GB

    return system_mem
