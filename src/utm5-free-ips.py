#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from __future__ import annotations
from mysql.connector import MySQLConnection, Error
from configparser import ConfigParser
from PyQt5.QtWidgets import QApplication
from Gui import Gui
import argparse
import logging
import os
import ipaddress
import sys


APP_NAME: str = os.path.splitext(os.path.basename(sys.argv[0]))[0]
DESCRIPTION: str = "The script searches for free ip addresses in NetUp UTM5 billing system."
SUBNET: str = "192.168.0.0/24"
SQL_QUERY: str = "SELECT ip FROM ip_groups WHERE is_deleted=0"

logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s [%(threadName)s] [%(levelname)s] - %(message)s",
    handlers = [
        logging.FileHandler("{0}/{1}.log".format(os.getcwd(), APP_NAME)),
        logging.StreamHandler(sys.stdout)
    ]
)


def get_args() -> List:
    """
    Function returns arguments passed to the application

    :returns: Array of arguments
    :rtype: List[str]
    """

    # parser: Object = argparse.ArgumentParser(description = DESCRIPTION)
    # parser.add_argument('subnet', 
    #                     metavar = "SUBNET", 
    #                     type = str, 
    #                     nargs = "?", 
    #                     default = "192.168.0.0/24", 
    #                     help = "Subnet of IP address ({})".format(SUBNET))
    # parser.add_argument('mode', 
    #                     metavar = "MODE", 
    #                     type = str, 
    #                     nargs = "?", 
    #                     default = "gui", 
    #                     help = "Application mode (gui, con).")
    # parser.add_argument('-a', 
    #                     help = "List all available ip addresses.")
    # return parser.parse_args()


def read_db_config(filename: str = "config.ini", section: str = "mysql") -> Dict:
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
    try:
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            return conn
    except Exception as err:
        logging.error("Unable to raise database connection.")
        logging.error(err)
    return conn


def get_ips_from_db() -> List:
    """
    Function returns list of ip addresses from a database

    :returns: Array of ip addresses
    :rtype: List[str]
    """

    ips_from_db: List[str] = []
    conn: MySQLConnection = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(SQL_QUERY)
        db_data = cursor.fetchall()
        if len(db_data) > 0:
            for ip in db_data:
                ips_from_db.append(ipaddress.ip_address(ip[0]))
            conn.close()
        return ips_from_db

def main():
    """ Application entry point """

    args: List[str] = get_args()
    app = QApplication(sys.argv)
    subnet = ipaddress.ip_network(args.subnet)
    ips_from_db = get_ips_from_db()
    if len(ips_from_db) > 0:
        for ip in subnet.hosts():
            if ip not in ips_from_db:
                print(ip)
                if len(sys.argv) < 3 or sys.argv[2].upper() != "ALL":
                    sys.exit(0)
        sys.exit(app.exec_())


if __name__ == "__main__":
    main()
