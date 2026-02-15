from PySide6.QtWidgets import *
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from client_modules.save_server import save_server_handler
from client_modules.load_servers import server_loader
from client_modules.networking import ChatHandler

class AddServer(QWidget):
    def __init__(self, on_cancel):
        super().__init__()

        self.on_cancel = on_cancel
        self.stacked = QStackedLayout(self)
        self.chat_handler = ChatHandler(self)

        self.add_page = QWidget()
        add_layout = QVBoxLayout(self.add_page)

        add_server_title = QLabel("Add server")
        add_server_title.setFont(QFont("Courier New", 20))
        add_server_title.setStyleSheet("color: #a5a8ad;")

        server_name_title = QLabel("Server name:")
        server_name_title.setFont(QFont("Courier New", 20))
        server_name_title.setStyleSheet("color: #a5a8ad;")

        server_address_title = QLabel("Server address:")
        server_address_title.setFont(QFont("Courier New", 20))
        server_address_title.setStyleSheet("color: #a5a8ad;")

        self.server_name_input = QLineEdit()
        self.ip_address_input = QLineEdit()

        self.cancel = QPushButton("Cancel")
        self.confirm = QPushButton("Confirm")
        self.confirm.clicked.connect(self.add_server_check_entries)
        self.cancel.clicked.connect(self.on_cancel)

        add_layout.addWidget(add_server_title)
        add_layout.addWidget(server_name_title)
        add_layout.addWidget(self.server_name_input)
        add_layout.addWidget(server_address_title)
        add_layout.addWidget(self.ip_address_input)
        add_layout.addWidget(self.cancel)
        add_layout.addWidget(self.confirm)
        self.stacked.addWidget(self.add_page)

        self.register_page = QWidget()
        register_layout = QVBoxLayout(self.register_page)

        register_label = QLabel("Register")
        register_label.setFont(QFont("Courier New", 20))
        register_label.setStyleSheet("color: #a5a8ad;")

        username_label = QLabel("Username")
        username_label.setFont(QFont("Courier New", 20))
        username_label.setStyleSheet("color: #a5a8ad;")

        self.username_input = QLineEdit()

        password_label = QLabel("Password")
        password_label.setFont(QFont("Courier New", 20))
        password_label.setStyleSheet("color: #a5a8ad;")

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        self.cancel = QPushButton("Cancel")
        self.confirm = QPushButton("Confirm")
        self.confirm.clicked.connect(self.register_check_entries)
        self.cancel.clicked.connect(self.on_cancel)

        register_layout.addWidget(register_label)
        register_layout.addWidget(username_label)
        register_layout.addWidget(self.username_input)
        register_layout.addWidget(password_label)
        register_layout.addWidget(self.password_input)
        register_layout.addWidget(self.cancel)
        register_layout.addWidget(self.confirm)
        self.stacked.addWidget(self.register_page)

    def add_server_check_entries(self):
        self.name = self.server_name_input.text()
        self.ip_address = self.ip_address_input.text()

        if self.name and self.ip_address:
            self.stacked.setCurrentWidget(self.register_page)
            server_loader()
        else:
            QMessageBox.warning(
                self,
                "Something went wrong.",
                "Please enter server name and IP address."
            )

    def register_check_entries(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if username and password:
            print(self.ip_address)
            save_server_handler(self.name, self.ip_address)
            self.chat_handler.register(username, password, self.ip_address)
            self.on_cancel()
            self.stacked.setCurrentWidget(self.add_page)
            self.close()
        else:
            QMessageBox.warning(
                self,
                "Something went wrong.",
                "Please enter username and password."
            )
