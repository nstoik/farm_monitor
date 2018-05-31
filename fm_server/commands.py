""" fm_server commands module """

from datetime import datetime

import click
from sqlalchemy.orm.exc import NoResultFound

from fm_database.base import get_session
from fm_database.models.system import SystemSetup
from fm_server.system.control import set_hardware_info, set_software_info, set_device_name
from fm_server.network.ethernet import get_interfaces
from fm_server.network.wifi import set_interfaces

@click.command()
def first_setup():
    """first time setup.
    load required data
    """
    click.echo("first time setup")
    session = get_session()

    try:
        system = session.query(SystemSetup).one()
    except NoResultFound:
        system = SystemSetup()
        session.add(system)

    if system.first_setup:
        click.echo("Setup has already been run")
        if not click.confirm('Do you want to run first time setup again?'):
            session.close()
            return

    system.first_setup = True
    system.first_setup_time = datetime.now()

    session.commit()
    session.close()

    if click.confirm("Do you want to change the device name?"):
        name = click.prompt("Please enter a new device name")
        set_device_name(name)

    if click.confirm("Do you want to set hardware informations?"):
        hardware_version = click.prompt("Enter the hardware version", default="pi3_0001")
        set_hardware_info(hardware_version)

    if click.confirm("Do you want to set the software information?"):
        software_version = click.prompt("Enter the software version")
        set_software_info(software_version)

    if click.confirm("Do you want to set details for the interfaces?"):
        interfaces = get_interfaces()
        x = 1
        interface_details = []
        for interface in interfaces:
            click.echo("{0}. {1}".format(x, interface))
            x = x + 1
            interface_details.append(get_interface_details(interface))
        set_interfaces(interface_details)


def get_interface_details(interface):
    """
    Collect all required details for an interface from user
    interface: a string that is the name of the interface

    Returns: a dictionary with required info. Keys are 'is_for_fm',
    'state', and 'ssid' and 'password' if applicable
    """
    info = {}
    info['name'] = interface
    for_fm = click.confirm("Is this interface for Farm Monitor(y) or for external access(n)",
                           default=False)
    info['is_for_fm'] = for_fm
    info['state'] = click.prompt("Should this interface be configured as an 'ap' or 'dhcp'",
                                 default='dhcp')
    if info['state'] == 'ap':
        creds = {}
        creds['ssid'] = click.prompt("Enter the access point SSID", default='FarmMonitor')
        creds['password'] = click.prompt("Enter the access point password", default="raspberry")
        info['creds'] = creds
    elif info['state'] == 'dhcp':
        if click.confirm("Do you want to preopulate wifi credentials", default=True):
            creds = {}
            creds['ssid'] = click.prompt("Enter the wifi SSID", default='FarmMonitor')
            creds['password'] = click.prompt("Enter the wifi password", default="raspberry")
            info['creds'] = creds

    return info
