from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from client_modules.add_server import AddServer
from client_modules.load_servers import server_loader
class MainUi(QWidget):
    def __init__(self):
        super().__init__()

        self.add_server_window = AddServer(self.show_main_ui)
        self.setWindowTitle("BitWire")
        self.setStyleSheet("background-color : #0e1117;")

        self.left_frame = QFrame(self)
        self.left_frame.setGeometry(0, 100, 200, 500)
        self.left_frame.setStyleSheet("background: transparent; border: 1px solid #737373")

        self.left_layout = QVBoxLayout(self.left_frame)
        self.left_layout.setAlignment(Qt.AlignTop)
        self.left_layout.setSpacing(1)

        self.right_frame = QFrame(self)
        self.right_frame.setGeometry(200, 0, 700, 600)
        self.right_frame.setStyleSheet("background: transparent; border: 1px solid #737373")

        self.right_layout = QVBoxLayout(self.right_frame)
        self.right_layout.setContentsMargins(10, 10, 10, 10)
        self.right_layout.setSpacing(8)

        self.upper_frame = QFrame(self)
        self.upper_frame.setGeometry(0, 50, 200, 50)
        self.upper_frame.setStyleSheet("background: transparent; border: 1px solid #737373")

        self.bitwire_label = QLabel("BitWire", self)
        self.bitwire_label.setFont(QFont("Courier New", 25))
        self.bitwire_label.setStyleSheet("color: #a5a8ad;")
        self.bitwire_label.move(30, 10)

        self.add_server_label = QLabel("All servers", self.upper_frame)
        self.add_server_label.setFont(QFont("Courier New", 11))
        self.add_server_label.setStyleSheet("color: white; border: none")
        self.add_server_label.move(10, 15)

        self.add_button = QPushButton("+", self.upper_frame)
        self.add_button.setFont(QFont("Courier New", 15, QFont.Bold))
        self.add_button.setStyleSheet("""
            QPushButton {
            color: white;
            background-color: #1f6feb;
            border-radius: 10px;
            border: 2px solid #ffffff;
            }
            
            QPushButton:hover {
                border-color: #58a6ff;
            }

            QPushButton:pressed {
            background-color: #1a5fd1;
            border-color: #1a5fd1;
            }
            
            """)
        self.add_button.setGeometry(150, 10, 32, 32)
        self.add_button.clicked.connect(self.open_add_server)
        self.reload_servers()

    def open_add_server(self):
        self.add_server_window.show()
        self.hide()

    def show_main_ui(self):
        self.add_server_window.close()
        self.show()
        self.reload_servers()

    def reload_servers(self):
        while self.left_layout.count():
            item = self.left_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        server_list = server_loader()
        for server in server_list:
            server_button = QPushButton(server["name"])
            server_button.setFixedHeight(35)
            server_button.setFont(QFont("Courier New", 12))
            server_button.setStyleSheet("""
                QPushButton {
                    text-align: left;
                    padding-left: 5px;
                    color: #a5a8ad;
                    background-color: transparent;
                    border-radius: 5px;
                }

                QPushButton:hover {
                    background-color: #333333;
                }
            """)
            self.left_layout.addWidget(server_button)
            server_button.clicked.connect(self.load_chat)
    
    def load_chat(self):
        while self.right_layout.count():
            item = self.right_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        message_input = QTextEdit()
        message_input.setFixedHeight(30)
        message_input.setPlaceholderText("Type a message...")
        message_input.setStyleSheet("""
            QTextEdit {
                border-radius: 10px;
                background-color: #1a1e24;
            }
        """)

        self.right_layout.addStretch()
        self.right_layout.addWidget(message_input)
