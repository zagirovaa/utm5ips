#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from __future__ import annotations
from typing import List
from PyQt5.QtWidgets import QWidget, QFormLayout, QLabel, QComboBox


class Window(QWidget):
    """ Class for creating QT5 form with listbox element """

    def __init__(self) -> None:
        """ Constructor """

        super().__init__()
        self.setWindowTitle("UTM5 Free IPs")
        self.layout = QFormLayout()

    def add_subnet(self, subnet: str, addresses: List[str]) -> None:
        label = QLabel("{}".format(subnet))
        combobox = QComboBox()
        combobox.addItems(addresses)
        self.layout.addRow(label, combobox)
        self.setLayout(self.layout)
