#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from __future__ import annotations
from mysql.connector import MySQLConnection
from configparser import ConfigParser
from PyQt5.QtWidgets import QApplication
# from Gui import Gui
from typing import List, Dict, Tuple
import argparse
import logging
import os
import ipaddress
import sys


APP_NAME: str = os.path.splitext(os.path.basename(sys.argv[0]))[0]
DESCRIPTION: str = """The script searches for free
ip addresses in NetUp UTM5 billing system."""
MODES: Tuple[str] = ("gui", "con")
SQL_QUERY: str = "SELECT ip FROM ip_groups WHERE is_deleted=0"
# IP addresses are stored in the database in decimal format
# Some addresses have negative values
# To make them positive it is necessary to add the value above to them
COEFFICIENT: int = 4294967296
TEMPLATE: str = """
Subnet: {}
----------------------------
{}
"""

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(threadName)s] [%(levelname)s] - %(message)s",
    handlers=[
        logging.FileHandler("{0}/{1}.log".format(os.getcwd(), APP_NAME)),
        logging.StreamHandler(sys.stdout)
    ]
)

parser = argparse.ArgumentParser(description=DESCRIPTION)
parser.add_argument('subnet',
                    nargs="+",
                    help="ipv4 subnet (192.168.0.0/24)")
parser.add_argument("-m",
                    dest="mode",
                    choices=["gui", "con"],
                    required=True,
                    help="choose application mode")
parser.add_argument("-a",
                    dest="all",
                    action="store_true",
                    default=False,
                    help="list all available ip addresses")
args = parser.parse_args()


def read_db_config(filename: str = "config.ini",
                   section: str = "mysql") -> Dict:
    """
    Function returns database connection settings

    :param filename: Config filename
    :type filename: str

    :param section: Config section
    :type section: str

    :returns: Dictionary with connection settings
    :rtype: Dict[str, str]
    """

    parser = ConfigParser()
    if sys.platform.startswith("win32"):
        full_name: str = sys.path[0] + "\\" + filename
    else:
        full_name: str = sys.path[0] + "/" + filename
    parser.read(full_name)
    db: Dict[str, str] = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db[item[0]] = item[1]
    else:
        logging.error("File {} has no section {}.".format(filename, section))
    return db


def connect_to_db() -> MySQLConnection:
    """
    Function connects to a database using parameters
    from config file and returns a connection

    :returns: Reference to an object representing a database connection
    :rtype: MySQLConnection
    """

    conn = None
    db_config = read_db_config()
    if db_config:
        try:
            conn = MySQLConnection(**db_config)
            if conn.is_connected():
                return conn
        except Exception as err:
            logging.error("Unable to raise database connection.")
            logging.error(err)
    else:
        logging.error("Could not get database configuration.")
    return conn


def get_ips_from_db() -> List:
    """
    Function returns list of ip addresses from a database

    :returns: Array of ip addresses
    :rtype: List[str]
    """

    ips_from_db: List[str] = []
    real_ip: str = ""
    conn: MySQLConnection = connect_to_db()
    cursor = conn.cursor()
    cursor.execute(SQL_QUERY)
    db_data = cursor.fetchall()
    if len(db_data) > 0:
        for ip in db_data:
            # Ip address is in the first place of returned tulip
            # Need a separate variable cause tulips are immutable
            real_ip = ip[0]
            if real_ip < 0:
                real_ip += COEFFICIENT
            ips_from_db.append(ipaddress.ip_address(real_ip))
        conn.close()
    else:
        logging.error("Unable to fetch addresses from database.")
    return ips_from_db


def get_free_ips() -> Dict:
    """
    Function returns dictionary with free ip addresses

    :returns: Dictionary with ip addresses
    :rtype: Dict[str, List[str]]
    """

    # Key of the dictionary is a subnet address
    # Value is a list of free ip addresses
    # available in the given subnet
    ip_addresses: Dict[str, List[str]] = {}
    subnets: List[str] = []
    for subnet in args.subnet:
        subnets.append(ipaddress.ip_network(subnet))
    ips_from_db = get_ips_from_db()
    if len(ips_from_db) > 0:
        if args.all:
            for subnet in subnets:
                ip_addresses[str(subnet)] = []
                for ip in subnet.hosts():
                    if ip not in ips_from_db:
                        ip_addresses[str(subnet)].append(str(ip))
        else:
            for subnet in subnets:
                ip_addresses[str(subnet)] = []
                for ip in subnet.hosts():
                    if ip not in ips_from_db:
                        ip_addresses[str(subnet)].append(str(ip))
                        break
    return ip_addresses


def main():
    """ Application entry point """

    if args.mode == "con":
        ip_addresses = get_free_ips()
        if ip_addresses:
            for key, value in ip_addresses.items():
                print(TEMPLATE.format(key, "\n".join(value)))
    else:
        app = QApplication(sys.argv)
        sys.exit(app.exec_())


if __name__ == "__main__":
    main()
