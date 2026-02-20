from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from client_modules.add_server import AddServer
from client_modules.load_servers import server_loader
from client_modules.networking import ChatHandler
from client_modules.tray_manager import TrayManager
from client_modules.login import Login

class MainUi(QWidget):
    def __init__(self):
        super().__init__()

        self.active_server = None

        self.add_server_window = AddServer(self.add_server_window_show_main_ui)
        self.login_server_window = Login(self.login_server_window_show_main_ui, self.on_success_login)
        self.chat_handler = ChatHandler(self.client_display_message)
        self.tray = TrayManager(self)

        self.setWindowTitle("BitWire")
        self.setStyleSheet("background-color : #0e1117;")
        self.setFixedSize(900, 600)

        self.server_frame = QFrame(self)
        self.server_frame.setGeometry(0, 100, 200, 500)
        self.server_frame.setStyleSheet("background: transparent; border: 1px solid #737373")

        self.server_layout = QVBoxLayout(self.server_frame)
        self.server_layout.setAlignment(Qt.AlignTop)
        self.server_layout.setSpacing(1)

        self.main_frame = QFrame(self)
        self.main_frame.setGeometry(200, 0, 700, 600)
        self.main_frame.setStyleSheet("background: transparent; border: 1px solid #737373")

        self.main_layout = QVBoxLayout(self.main_frame)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(8)

        self.upper_frame = QFrame(self)
        self.upper_frame.setGeometry(0, 50, 200, 50)
        self.upper_frame.setStyleSheet("background: transparent; border: 1px solid #737373")

        self.server_button_group = QButtonGroup(self)
        self.server_button_group.setExclusive(True)

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

    def add_server_window_show_main_ui(self):
        self.add_server_window.close()
        self.show()
        self.reload_servers()

    def login_server_window_show_main_ui(self):
        self.login_server_window.close()
        self.show()
        self.reload_servers()

    def reload_servers(self):
        while self.server_layout.count():
            item = self.server_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        server_list = server_loader()
        for server in server_list:
            server_button = QPushButton(server["name"])
            server_button.setCheckable(True)
            server_button.setProperty("name", server["name"])
            server_button.setProperty("ip", server["ip_address"])
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

                QPushButton:checked {
                    background-color: #333333;
                }

                QPushButton:pressed {
                    background-color: #262626;
                }
            """)
            self.server_layout.addWidget(server_button)
            self.server_button_group.addButton(server_button)
            server_button.clicked.connect(self.load_chat)
    
    def load_chat(self):
        self.active_server = None
        while self.main_layout.count():
            item = self.main_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
        
        self.server_button = self.sender()
        
        if self.server_button == self.active_server:
            return
        
        if self.active_server:
            self.active_server.setEnabled(True)
            
        self.server_button.setEnabled(False)
        self.active_server = self.server_button
        
        self.server_address = self.server_button.property("ip")
        self.login_page()

    def client_display_message(self, message):
        self.chat_view.append(message)

    def client_send_message(self):
        message = self.message_input.toPlainText().strip()
        if not message:
            self.message_input.setFocus()
            return
        self.chat_handler.send_message(message)
        self.message_input.clear()
        self.message_input.setFocus()

    def closeEvent(self, event):
        event.ignore()
        self.hide()

    def login_page(self):
        self.login_server_window.get_ip_address(self.server_address)
        self.login_server_window.show() 
        self.hide()
    
    def on_success_login(self, username, ip_address):
        self.chat_view = QTextBrowser()
        self.chat_view.verticalScrollBar().setSingleStep(10)
        self.chat_view.setStyleSheet("""
            QTextBrowser {
                background-color: #0d1117;
                color: #e6edf3;
                padding: 10px;
                font-size: 14px;
            }
            QScrollBar:vertical {
                background: transparent;
                width: 15px;
                border-radius: 6px;
            }

            QScrollBar:handle:vertical {
                background-color: #333e4f;
                border-radius: 6px;
            }

            QScrollBar:handle:vertical:hover {
                background-color: #4d5d75;
            }

            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                background-color: transparent;
                border: transparent;
            }
        """)

        self.message_input = QTextEdit()
        self.message_input.setFixedHeight(40)
        self.message_input.setPlaceholderText("Type a message...")
        self.message_input.setStyleSheet("""
            QTextEdit {
                border-radius: 10px;
                background-color: #1a1e24;
                color: #e6edf3;
                padding: 5px 5px;
                border: 1px solid #3b4657;
            }

            QTextEdit:focus {
                border: 1px solid #505f75;
            }
        """)

        self.send_message = QPushButton(">")
        self.send_message.setFixedSize(30, 30)
        self.send_message.clicked.connect(self.client_send_message)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.message_input)
        input_layout.addWidget(self.send_message)

        self.main_layout.addWidget(self.chat_view)
        self.main_layout.addLayout(input_layout)
        self.message_input.setFocus()
        self.chat_handler.connect_to_server(self.server_address)