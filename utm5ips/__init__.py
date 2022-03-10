#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import sys
from argparse import ArgumentParser
import logging


# Used in logging module
APP_NAME = os.path.splitext(os.path.basename(sys.argv[0]))[0]
# Logging configuration section
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(threadName)s] [%(levelname)s] - %(message)s",
    handlers=[
        logging.FileHandler("{0}/{1}.log".format(os.getcwd(), APP_NAME)),
        logging.StreamHandler(sys.stdout)
    ]
)

# Used in arguments parsing module
DESCRIPTION = """The script searches for free
ip addresses in NetUp UTM5 billing system."""
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
