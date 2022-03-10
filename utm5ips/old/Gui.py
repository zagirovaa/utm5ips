#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from PyQt5.QtWidgets import QWidget, QFormLayout, QLabel, QComboBox


class Window(QWidget):
    """
    Class for creating QT5 forms with comboboxes
    filled with free addresses in given subnets
    """

    def __init__(self):
        """ Constructor """

        super().__init__()
        self.setWindowTitle("UTM5 Free IPs")
        self.layout = QFormLayout()

    def fix_size(self):
        """ Function makes window non-resisable """

        self.setMaximumSize(self.width(), self.height())
        self.setMinimumSize(self.width(), self.height())

    def add_subnet(self, subnet, addresses):
        """
        Function fills list of free ip addresses in combobox

        :param subnet: Subnet of free addresses
        :type subnet: str

        :param addresses: List of free addresses of the subnet
        :type addresses: List[str]
        """

        label = QLabel(subnet)
        combobox = QComboBox()
        combobox.addItems(addresses)
        self.layout.addRow(label, combobox)
        self.setLayout(self.layout)
