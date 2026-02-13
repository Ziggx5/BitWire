from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
import requests

class Login(QWidget):
    def __init__(self, on_cancel):
        super().__init__()

        self.on_cancel = on_cancel

        login_page = QVBoxLayout(self)

        login_label = QLabel("Login")
        login_label.setFont(QFont("Courier New", 20))
        login_label.setStyleSheet("color: #a5a8ad;")

        self.cancel = QPushButton("Cancel")
        self.confirm = QPushButton("Confirm")
        self.cancel.clicked.connect(self.on_cancel)


