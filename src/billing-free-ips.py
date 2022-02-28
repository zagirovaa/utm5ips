#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from __future__ import annotations
from mysql.connector import MySQLConnection, Error
from configparser import ConfigParser
import ipaddress
import sys


SQL_QUERY: str = "SELECT ip FROM ip_groups WHERE is_deleted=0"


def read_db_config(filename: str = "config.ini", section: str = "mysql") -> Dict:
        """
        Функция считывает настройки подключенния к БД
        :параметр filename: имя файла конфигурации
        :параметр section: раздел конфигурации
        :возвращает словарь с настройками подключения
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
            raise Exception(
                "Раздел {0} в файле {1} не найден".format(section, filename))
        return db


def connect_to_db() -> MySQLConnection:
    """
    Function connects to database
    using parameters from config file
    and returns the connection
    """

    db_config = read_db_config()
    try:
        conn = MySQLConnection(**db_config)
        if conn.is_connected():
            return conn
    except Error as e:
        print(e)


def get_ips_from_db():
    """
    Function returns list of ip addresses from database
    """

    ips_from_db: List[str] = []
    conn = connect_to_db()
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
    """
    Application entry point
    """

    if len(sys.argv) > 1:
        subnet = ipaddress.ip_network(sys.argv[1])
        ips_from_db = get_ips_from_db()
        if len(ips_from_db) > 0:
            for ip in subnet.hosts():
                if ip not in ips_from_db:
                    print(ip)
                    if len(sys.argv) < 3 or sys.argv[2].upper() != "ALL":
                        sys.exit(0)
    else:
        print("Пример использования: ")
        print("python spareips.py 192.168.0.0/24 [all]")


if __name__ == "__main__":
    main()
