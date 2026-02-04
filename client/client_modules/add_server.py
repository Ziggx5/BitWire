from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont

class AddServer(QWidget):
    def __init__(self, on_cancel):
        super().__init__()

        self.on_cancel = on_cancel

        layout = QVBoxLayout(self)

        add_server_title = QLabel("Add server")
        add_server_title.setFont(QFont("Courier New", 20))
        add_server_title.setStyleSheet("color: #a5a8ad;")

        server_name_title = QLabel("Server name:")
        server_name_title.setFont(QFont("Courier New", 20))
        server_name_title.setStyleSheet("color: #a5a8ad;")

        server_address_title = QLabel("Server address:")
        server_address_title.setFont(QFont("Courier New", 20))
        server_address_title.setStyleSheet("color: #a5a8ad;")

        self.server_name = QLineEdit()
        self.ip_address = QLineEdit()

        self.cancel = QPushButton("Cancel")
        self.confirm = QPushButton("Confirm")

        self.cancel.clicked.connect(self.on_cancel)

        layout.addWidget(add_server_title)
        layout.addWidget(server_name_title)
        layout.addWidget(self.server_name)
        layout.addWidget(server_address_title)
        layout.addWidget(self.ip_address)
        layout.addWidget(self.cancel)
        layout.addWidget(self.confirm)

        self.confirm.clicked.connect(self.check_entries)

    def check_entries(self):
        if self.server_name.text() == "" and self.ip_address.text() == "":
            print("Working")
