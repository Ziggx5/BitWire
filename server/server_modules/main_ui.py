from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import threading
from server_modules.data_manipulation import local_data_file, copy_to_data_dir, files_check
from server_modules.server import ChatServer
from server_modules.system_tray import TrayManager
from server_modules.load_assets import file_root

class MainUi(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("BiteWire Server")
        self.setStyleSheet("background-color : #0e1117;")
        self.setFixedSize(400, 500)
        self.tray = TrayManager(self)
        self.chat_server = ChatServer()
        self.chat_server.uptime_signal.connect(self.update_timer)
        local_data_file()
        image_path = file_root()
        self.files = files_check()

        layout = QVBoxLayout(self)

        ssl_box = QGroupBox("SSL Certificate Files")
        ssl_box_layout = QVBoxLayout()
        certificate_file_layout = QHBoxLayout()
        key_file_layout = QHBoxLayout()

        databases_box = QGroupBox("Database files")
        database_files_layout = QVBoxLayout()
        users_database_layout = QHBoxLayout()
        messages_database_layout = QHBoxLayout()

        server_control_box = QGroupBox("Server Control")
        server_control_box_layout = QVBoxLayout()
        server_status_layout = QHBoxLayout()
        server_uptime_layout = QHBoxLayout()
        server_buttons_layout = QHBoxLayout()

        server_folder_layout = QHBoxLayout()

        certificate_file_label = QLabel("Certificate file:")
        self.certificate_file_input = QLineEdit()
        #self.certificate_file_button = QPushButton("Browse...")
        #self.certificate_file_button.clicked.connect(lambda: self.send_file_path("certificate"))

        key_file_label = QLabel("Key file:")
        self.key_file_input = QLineEdit()
        #self.key_file_button = QPushButton("Browse...")
        #self.key_file_button.clicked.connect(lambda: self.send_file_path("key"))

        users_database_file_label = QLabel("Users database file:")
        self.users_database_file_input = QLineEdit()
        #self.users_database_file_button = QPushButton("Browse...")
        #self.users_database_file_button.clicked.connect(lambda: self.send_file_path("users_database"))

        messages_database_file_label = QLabel("Messages database file:")
        self.messages_database_file_input = QLineEdit()
        #self.messages_database_file_button = QPushButton("Browse...")
        #self.messages_database_file_button.clicked.connect(lambda: self.send_file_path("messages_database"))

        self.start_server_button = QPushButton("Start Server")
        self.start_server_button.clicked.connect(self.start_server)
        self.stop_server_button = QPushButton("Stop Server")
        self.stop_server_button.clicked.connect(self.stop_server)
        self.stop_server_button.setEnabled(False)

        server_status_label = QLabel("Server Status:")
        self.server_status_state = QLabel("Stopped")

        server_uptime_label = QLabel("Server Uptime")
        self.server_uptime_time = QLabel("Time")

        server_folder_button = QPushButton()
        server_folder_button.setIcon(QIcon(f"{image_path}/folder.png"))
        server_folder_button.setIconSize(QSize(15, 15))
        server_folder_button.setFixedSize(35, 35)

        certificate_file_layout.addWidget(certificate_file_label)
        certificate_file_layout.addWidget(self.certificate_file_input)
        #certificate_file_layout.addWidget(self.certificate_file_button)

        key_file_layout.addWidget(key_file_label)
        key_file_layout.addWidget(self.key_file_input)
        #key_file_layout.addWidget(self.key_file_button)

        ssl_box_layout.addLayout(certificate_file_layout)
        ssl_box_layout.addLayout(key_file_layout)

        ssl_box.setLayout(ssl_box_layout)

        users_database_layout.addWidget(users_database_file_label)
        users_database_layout.addWidget(self.users_database_file_input)
        #users_database_layout.addWidget(self.users_database_file_button)

        messages_database_layout.addWidget(messages_database_file_label)
        messages_database_layout.addWidget(self.messages_database_file_input)
        #messages_database_layout.addWidget(self.messages_database_file_button)

        database_files_layout.addLayout(users_database_layout)
        database_files_layout.addLayout(messages_database_layout)

        databases_box.setLayout(database_files_layout)

        server_status_layout.addWidget(server_status_label)
        server_status_layout.addWidget(self.server_status_state)

        server_uptime_layout.addWidget(server_uptime_label)
        server_uptime_layout.addWidget(self.server_uptime_time)

        server_buttons_layout.addWidget(self.start_server_button)
        server_buttons_layout.addWidget(self.stop_server_button)

        server_control_box_layout.addLayout(server_status_layout)
        server_control_box_layout.addLayout(server_uptime_layout)
        server_control_box_layout.addLayout(server_buttons_layout)

        server_folder_layout.addStretch()
        server_folder_layout.addWidget(server_folder_button)

        server_control_box.setLayout(server_control_box_layout)

        layout.addWidget(ssl_box)
        layout.addWidget(databases_box)
        layout.addWidget(server_control_box)
        layout.addLayout(server_folder_layout)

        self.fill_inputs(self.files)

    def fill_inputs(self, files):
        for file_path in files:
            if file_path.endswith(".crt"):
                self.certificate_file_input.setText(file_path)

            elif file_path.endswith(".key"):
                self.key_file_input.setText(file_path)

            elif file_path.endswith(".db"):
                self.users_database_file_input.setText(file_path)

    def send_file_path(self, file_type):
        if file_type == "certificate":
            file_path, _ = QFileDialog.getOpenFileName(self, "Select file", "", "Certificate files (*.crt)")

        elif file_type == "key":
            file_path, _ = QFileDialog.getOpenFileName(self, "Select file", "", "Key files (*.key)")

        elif file_type == "users_database":
            file_path, _ = QFileDialog.getOpenFileName(self, "Select file", "", "Database files (*.db)")

        elif file_type == "messages_database":
            file_path, _ = QFileDialog.getOpenFileName(self, "Select file", "", "Database files (*.db)")

        if not file_path:
            return

        copied_file_path = copy_to_data_dir(file_path)

        if file_type == ".crt":
            self.certificate_file_input.setText(copied_file_path)

        elif file_type == ".key":
            self.key_file_input.setText(copied_file_path)

        elif file_type == ".db":
            self.database_file_input.setText(copied_file_path)

    def start_server(self):
        if not self.certificate_file_input.text() or not self.key_file_input.text():
            return

        threading.Thread(target = self.chat_server.start, daemon = True).start()

        self.server_status_state.setText("Running")
        self.start_server_button.setEnabled(False)
        QTimer.singleShot(2000, lambda: self.stop_server_button.setEnabled(True))

        self.certificate_file_input.setEnabled(False)
        self.key_file_input.setEnabled(False)
        self.database_file_input.setEnabled(False)
        #self.key_file_button.setEnabled(False)
        #self.database_file_button.setEnabled(False)
        #self.certificate_file_button.setEnabled(False)
        self.tray.set_server_status("Running")

    def stop_server(self):
        self.chat_server.stop()
        self.server_status_state.setText("Stopped")
        self.stop_server_button.setEnabled(False)
        QTimer.singleShot(2000, lambda: self.start_server_button.setEnabled(True))

        self.certificate_file_input.setEnabled(True)
        self.key_file_input.setEnabled(True)
        self.database_file_input.setEnabled(True)
        #self.key_file_button.setEnabled(True)
        #self.database_file_button.setEnabled(True)
        #self.certificate_file_button.setEnabled(True)
        self.tray.set_server_status("Stopped")

        self.update_timer(0, 0, 0)
    
    def update_timer(self, hours, minutes, seconds):
        self.server_uptime_time.setText(f"{hours:02}:{minutes:02}:{seconds:02}")
        self.tray.set_server_uptime(hours, minutes, seconds)
        
    def closeEvent(self, event):
        event.ignore()
        self.hide()