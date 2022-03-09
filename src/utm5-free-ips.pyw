#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from __future__ import annotations
from mysql.connector import MySQLConnection
from configparser import ConfigParser
from PyQt5.QtWidgets import QApplication
from Gui import Window
from typing import List, Dict, Tuple
from argparse import ArgumentParser
import logging
import os
from ipaddress import ip_network
import sys


# Used in logging module
APP_NAME: str = os.path.splitext(os.path.basename(sys.argv[0]))[0]
# Used in arguments parsing module
DESCRIPTION: str = """The script searches for free
ip addresses in NetUp UTM5 billing system."""
# Application can work either in gui or console mode
MODES: Tuple[str] = ("gui", "con")
# Query for getting ip addresses that are not marked for deletion
SQL_QUERY: str = "SELECT INET_NTOA(ip) FROM ip_groups WHERE is_deleted=0"
# IP addresses are stored in the database in decimal format
# Some addresses have negative values
# To make them positive it is necessary to add them to the value below
COEFFICIENT: int = 4294967296
# Used in printing results in console mode
TEMPLATE: str = "{}\n------------------\n{}\n"
# Logging configuration section
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(threadName)s] [%(levelname)s] - %(message)s",
    handlers=[
        logging.FileHandler("{0}/{1}.log".format(os.getcwd(), APP_NAME)),
        logging.StreamHandler(sys.stdout)
    ]
)
# Arguments parsing configuration section
parser = ArgumentParser(description=DESCRIPTION)
parser.add_argument("-m",
                    dest="mode",
                    choices=["gui", "con"],
                    default="gui",
                    help="choose application mode")
parser.add_argument("-a",
                    dest="all",
                    action="store_true",
                    default=False,
                    help="list all available ip addresses")
args = parser.parse_args()


def get_config(filename: str = "config.ini") -> Dict:
    """
    Function returns database connection settings

    :param filename: Config filename
    :type filename: str

    :returns: Dictionary with connection settings
    :rtype: Dict[str, {Dict[str], List[str]}]
    """

    config = {
        "database": {
            "host": "",
            "database": "",
            "user": "",
            "password": ""
        },
        "subnets": [],
        "exceptions": []
    }
    parser = ConfigParser()
    if sys.platform.startswith("win32"):
        full_name: str = sys.path[0] + "\\" + filename
    else:
        full_name: str = sys.path[0] + "/" + filename
    try:
        parser.read(full_name)
        items: List[Tuple[str]] = parser.items("database")
        for item in items:
            config["database"][item[0]] = item[1]
        for section in ("subnets", "exceptions"):
            items: List[Tuple[str]] = parser.items(section)
            for item in items:
                config[section].append({item[0]: item[1]})
        return config
    except Exception as err:
        logging.error("Error in config file or file does not exist.")
        logging.error(err)
    quit()


def connect_to_db() -> MySQLConnection:
    """
    Function connects to a database using parameters
    from config file and returns a connection

    :returns: Reference to an object representing a database connection
    :rtype: MySQLConnection
    """

    db_config = get_config()["database"]
    if db_config:
        try:
            conn = MySQLConnection(**db_config)
            if conn.is_connected():
                return conn
            else:
                logging.error("Could not connect to the database.")
        except Exception as err:
            logging.error("Unable to raise database connection.")
            logging.error(err)
    else:
        logging.error("Could not get database configuration.")
    quit()


def get_ips_from_db() -> List:
    """
    Function returns list of ip addresses from a database

    :returns: Array of ip addresses
    :rtype: List[str]
    """

    ips_from_db: List[str] = []
    conn = connect_to_db()
    try:
        cursor = conn.cursor()
        cursor.execute(SQL_QUERY)
        db_data = cursor.fetchall()
    except Exception as err:
        logging.error("Unable to fetch addresses from database.")
        logging.error(err)
    if len(db_data) > 0:
        if args.all:
            for ip in db_data:
                ips_from_db.append(ip[0])
            conn.close()
        else:
            ips_from_db.append(db_data[0][0])
        return ips_from_db
    else:
        logging.error("Could not find any address in the database.")
    quit()


def get_free_ips() -> Dict:
    """
    Function returns dictionary with free ip addresses

    :returns: Dictionary with ip addresses
    :rtype: Dict[str, List[str]]
    """

    ips_from_db = get_ips_from_db()
    # Key of the dictionary is a subnet address
    # Value is a list of free ip addresses
    # available in the given subnet
    ip_addresses: Dict[str, List[str]] = {}
    exceptions: List[str] = []
    config: Dict = get_config()
    subnets: List[str] = config["subnets"]
    for item in config["exceptions"]:
        for key, value in item.items():
            exceptions.append(value)
    if subnets:
        for subnet in subnets:
            items = subnet.items()
            for key, value in items:
                value = ip_network(value)
                ip_addresses[key] = []
                hosts = value.hosts()
                for ip in hosts:
                    ip = str(ip)
                    if ip not in ips_from_db and ip not in exceptions:
                        ip_addresses[key].append(ip)
                        # If -a parameter is not passed, only one free
                        # ip address for each subnet must be added to the list
                        if not args.all:
                            break
        return ip_addresses
    else:
        logging.error("No subnet defined in config file.")
    quit()


def main():
    """ Application entry point """

    ip_addresses: List[str] = get_free_ips()
    if args.mode == "con":
        for key, value in ip_addresses.items():
            print(TEMPLATE.format(key, "\n".join(value)))
    else:
        app = QApplication(sys.argv)
        frm_main = Window()
        for key, value in ip_addresses.items():
            frm_main.add_subnet(key, value)
        frm_main.show()
        frm_main.fix_size()
        sys.exit(app.exec_())


if __name__ == "__main__":
    main()
