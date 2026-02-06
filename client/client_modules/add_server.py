from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from client_modules.save_server import save_server_handler
from client_modules.load_servers import server_loader

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
        name = self.server_name.text()
        ip_address = self.ip_address.text()

        if name and ip_address:
            save_server_handler(name, ip_address)
            self.on_cancel()
            self.close()
            server_loader()
        else:
            QMessageBox.warning(
                self,
                "Something went wrong.",
                "Please enter server name and IP address."
            )