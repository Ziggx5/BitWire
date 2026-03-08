from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPixmap
from client_modules.path_finder import file_root

class AddIdentityUi(QWidget):
    def __init__(self):
        super().__init__()

        #self.on_cancel = on_cancel
        self.picture_path = file_root()

        self.setWindowTitle("BitWire")
        self.setStyleSheet("background-color: #161b22")
        self.setFixedSize(500, 300)

        input_style = """
        QLineEdit {
            background-color: #0d1117;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 8px;
            color: #e6edf3;
            font-size: 15px;
        }
        """

        main_title = """
        QLabel {
            color: #e6edf3;
            font-size: 20px;
            font-weight: 600;
        }
        """
        
        add_identity_layout = QVBoxLayout(self)
        add_identity_layout.setSpacing(0)

        add_identity_upper_layout = QHBoxLayout()
        add_identity_left_layout = QVBoxLayout()
        add_identity_right_layout = QVBoxLayout()
        add_identity_lower_layout = QHBoxLayout()

        self.profile_picture_widget = QWidget()
        self.profile_picture_widget.setFixedSize(160, 160)
        self.profile_picture_widget.setStyleSheet("""
            QWidget { 
                background-color: #0d1117;
                border: 2px dashed #30363d;
                border-radius: 80px;
                color: #8b949e;
            }

            QWidget:hover {
            border: 2px solid #58a6ff;
            }
        """)
        profile_picture_layout = QVBoxLayout(self.profile_picture_widget)

        profile_picture = QLabel()
        profile_picture.setPixmap(QPixmap(f"{self.picture_path}/camera.png").scaled(80, 80))
        profile_picture.setStyleSheet("border: None; background-color: transparent;")

        profile_picture_subtitle = QLabel("Select photo")
        profile_picture_subtitle.setStyleSheet("border: None; background-color: transparent;")

        profile_picture_layout.setAlignment(Qt.AlignCenter)
        profile_picture_layout.addWidget(profile_picture)
        profile_picture_layout.addWidget(profile_picture_subtitle)

        title = QLabel("Add new identity")
        title.setStyleSheet(main_title)
        title.setFixedHeight(30)

        username_label = QLabel("Username")
        username_label.setFont(QFont("Courier New", 12))
        username_label.setStyleSheet("color: #a5a8ad;")
        username_label.setFixedHeight(20)
        self.username_input = QLineEdit()
        self.username_input.setStyleSheet(input_style)

        password_label = QLabel("Password")
        password_label.setFont(QFont("Courier New", 12))
        password_label.setStyleSheet("color: #a5a8ad;")
        password_label.setFixedHeight(20)

        self.password_input = QLineEdit()
        self.password_input.setStyleSheet(input_style)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setFixedSize(110, 35)
        self.cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #6e6e6e;
                font-weight: 600;
                border-radius: 5px;
                border: 1px solid #30363d;
            }
            QPushButton:hover {
                background-color: #878787;
            }
        """)

        self.confirm_button = QPushButton("Confirm")
        self.confirm_button.setFixedSize(110, 35)
        self.confirm_button.setStyleSheet("""
            QPushButton {
                background-color: #175723;
                font-weight: 600;
                border-radius: 5px;
                border: 1px solid #30363d;
            }

            QPushButton:hover {
                background-color: #1e732e;
            }
        """)

        self.all_identities_button = QPushButton("Identities")
        self.all_identities_button.setFixedSize(110, 35)
        self.all_identities_button.setStyleSheet("""
            QPushButton {
            background-color: #1f6feb;
            font-weight: 600;
            border-radius: 5px;
            border: 1px solid #30363d;
            }

            QPushButton:hover {
            background-color: #388bfd;
            }
        """)

        add_identity_left_layout.addWidget(self.profile_picture_widget)

        add_identity_right_layout.addWidget(title)
        add_identity_right_layout.addSpacing(10)
        add_identity_right_layout.addWidget(username_label)
        add_identity_right_layout.addSpacing(5)
        add_identity_right_layout.addWidget(self.username_input)
        add_identity_right_layout.addSpacing(10)
        add_identity_right_layout.addWidget(password_label)
        add_identity_right_layout.addSpacing(5)
        add_identity_right_layout.addWidget(self.password_input)

        add_identity_upper_layout.addLayout(add_identity_left_layout)
        add_identity_upper_layout.addSpacing(30)
        add_identity_upper_layout.addLayout(add_identity_right_layout)

        add_identity_lower_layout.addStretch()
        add_identity_lower_layout.addWidget(self.all_identities_button)
        add_identity_lower_layout.addSpacing(10)
        add_identity_lower_layout.addWidget(self.cancel_button)
        add_identity_lower_layout.addSpacing(10)
        add_identity_lower_layout.addWidget(self.confirm_button)

        add_identity_layout.addLayout(add_identity_upper_layout)
        add_identity_layout.addStretch()
        add_identity_layout.addLayout(add_identity_lower_layout)