#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from __future__ import annotations
from PyQt5.QtWidgets import QWidget, QListWidget, QMessageBox


class Gui(QWidget):
    """
    Pass
    """

    def __init__(self) -> None:
        """
        Pass
        """

        super().__init__()
        self.resize(171, 231)
        self.setMinimumSize(171, 231)
        self.setMaximumSize(171, 231)
        self.setWindowTitle("UTM5 Free IPs")
        self.lst_addresses = QListWidget(self)
        self.lst_addresses.setGeometry(10, 10, 151, 211)
        self.lst_addresses.setObjectName("lst_addresses")
        self.show()
    
    def show_dialog(self, title: str = "Default", message: str = "Default text message") -> None:
        """
        Функция выводит диалоговое окно с текстовым
        сообщением, заданным в качестве параметра для функции
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
    
