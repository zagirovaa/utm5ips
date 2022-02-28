#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from __future__ import annotations
from PyQt5.QtWidgets import QWidget, QListWidget, QMessageBox


class Gui(QWidget):
    """ Class for creating QT5 form with listbox element """

    def __init__(self) -> None:
        """ Constructor """

        super().__init__()
        self.resize(171, 231)
        self.setMinimumSize(171, 231)
        self.setMaximumSize(171, 231)
        self.setWindowTitle("UTM5 Free IPs")
        self.lst_addresses = QListWidget(self)
        self.lst_addresses.setGeometry(10, 10, 151, 211)
        self.lst_addresses.setObjectName("lst_addresses")
        self.show()

    def show_dialog(self, title: str = "Default",
                    message: str = "Default text message") -> None:
        """
        Function shows a dialogbox with given title and message

        :param title: Dialogbox title
        :type title: str

        :param message: Dialogbox message
        :type message: str
        """

        if title.strip() == "":
            title = "Default title"
        if message.strip() == "":
            message = "Default text message"
        dialog = QMessageBox()
        dialog.setIcon(QMessageBox.Information)
        dialog.setWindowTitle(title)
        dialog.setText(message)
        dialog.exec()
