from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from client_modules.add_server_ui import AddServerUi
from client_modules.data_manipulation import delete_server, server_loader
from client_modules.networking import ChatHandler
from client_modules.tray_manager import TrayManager
from client_modules.path_finder import file_root
from client_modules.login_ui import Login
from client_modules.identity_ui import AddIdentityUi

class MainUi(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("BiteWire")
        self.setStyleSheet("""
        QWidget {
            background-color: #0e1117;
        }
        
        QScrollBar:vertical {
            background-color: transparent;
            width: 6px;
        }

        QScrollBar::handle:vertical {
            background-color: #374151;     
            border-radius: 3px;      
        }

        QScrollBar::handle:vertical:hover {
            background-color: #4b5563;
        }
        """)
        self.showMaximized()

        self.add_server_window = AddServerUi(self.add_server_window_show_main_ui)
        self.chat_handler = ChatHandler()
        self.chat_handler.message_received.connect(self.client_display_message)
        self.chat_handler.users_received.connect(self.add_users)
        self.chat_handler.server_status.connect(self.server_close_message)

        self.login_server_window = Login(self.login_server_window_show_main_ui, self.on_success_login, self.chat_handler)
        self.identity_window = AddIdentityUi(self.identity_window_show_main_ui)
        self.tray = TrayManager(self)
        self.image_path = file_root()

        self.overlay = QWidget(self)
        self.overlay.setStyleSheet("background-color: rgba(0, 0, 0, 150);")
        self.overlay.setGeometry(0, 0, self.width(), self.height())

        self.overlay_layout = QVBoxLayout(self.overlay)

        popup_background_container = QWidget()
        popup_background_container.setObjectName("container")
        popup_background_container.setStyleSheet("""
            QWidget#container {
                    background-color: #161b22;
                    border-radius: 12px;
                    border: 1px solid rgba(255, 255, 255, 0.05);
            }
        """)
        self.popup_background_container_layout = QVBoxLayout(popup_background_container)

        self.overlay_layout.addWidget(popup_background_container, alignment = Qt.AlignCenter)

        self.add_server_window.hide()
        self.identity_window.hide()

        main_root_layout = QHBoxLayout(self)
        main_root_layout.setSpacing(0)
        main_root_layout.setContentsMargins(0, 0, 0, 0)

        left_container = QVBoxLayout()

        server_frame = QFrame(self)
        server_frame.setStyleSheet("background-color: #111827; border: none;")

        self.server_layout = QVBoxLayout(server_frame)
        self.server_layout.setAlignment(Qt.AlignTop)
        self.server_layout.setSpacing(3)

        user_frame = QFrame(self)
        user_frame.setObjectName("container")
        user_frame.setStyleSheet("""
            QFrame#container {
                background: transparent;
                border: 1px solid #30363d;
            }
        """)
        self.user_frame_layout = QHBoxLayout(user_frame)

        main_frame = QFrame(self)
        main_frame.setStyleSheet("background: transparent; border: none;")

        self.main_layout_horizontal = QHBoxLayout(main_frame)
        self.main_layout_horizontal.setContentsMargins(0, 0, 0, 0)

        self.main_layout_vertical = QVBoxLayout()
        self.main_layout_vertical.setSpacing(8)
        self.main_layout_horizontal.addLayout(self.main_layout_vertical)

        upper_frame = QFrame(self)
        upper_frame.setStyleSheet("background-color: #111827; border-bottom: 1px solid rgba(255, 255, 255, 0.05);")

        self.upper_layout = QHBoxLayout(upper_frame)

        logo_frame = QFrame(self)
        logo_frame.setStyleSheet("background: #111827; border: none;")

        self.logo_layout = QHBoxLayout(logo_frame)

        self.BiteWire_label = QLabel("BiteWire")
        self.BiteWire_label.setStyleSheet("color: #a5a8ad; border: none; font-size: 30px;")
        
        self.logo_layout.addWidget(self.BiteWire_label, alignment = Qt.AlignCenter)

        self.add_server_label = QLabel("All servers")
        self.add_server_label.setStyleSheet("color: white; border: none; font-size: 17px;")

        self.add_button = QPushButton("+")
        self.add_button.setStyleSheet("""
            QPushButton {
                color: white;
                background-color: #3b82f6;
                border-radius: 8px;
                font-weight: 700;
                border: 2px solid #ffffff;
                font-size: 20px;
            }
            
            QPushButton:hover {
                background-color: #2563eb;
            }

            QPushButton:pressed {
                background-color: #1d4ed8;
            }
        """)
        self.add_button.setFixedSize(35, 35)
        self.add_button.clicked.connect(lambda: self.show_popup(self.add_server_window))
        self.add_button.setCursor(Qt.PointingHandCursor)
        self.reload_servers()

        self.upper_layout.addWidget(self.add_server_label)
        self.upper_layout.addStretch()
        self.upper_layout.addWidget(self.add_button)

        self.username_label = QLabel("User")

        self.new_user_button = QPushButton()
        self.new_user_button.setFixedSize(30, 30)
        self.new_user_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 6px;
            }

            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.08)
            }

            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.15)
            }
        """)
        self.new_user_button.clicked.connect(lambda: self.show_popup(self.identity_window))
        self.new_user_button.setIcon(QIcon(f"{self.image_path}/identity.png"))
        self.new_user_button.setIconSize(QSize(30, 30))
        self.new_user_button.setCursor(Qt.PointingHandCursor)
        self.settings_button = QPushButton()
        self.settings_button.setIcon(QIcon(f"{self.image_path}/settings.png"))
        self.settings_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 6px;
            }

            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.08)
            }

            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.15)
            }
        """)

        self.settings_button.setIconSize(QSize(18, 18))
        self.settings_button.setFixedSize(30, 30)
        self.settings_button.setCursor(Qt.PointingHandCursor)

        self.user_picture = QLabel()
        self.user_picture.setFixedSize(30, 30)
        self.user_picture.setStyleSheet("background-color: white; border-radius: 15px")
        self.pixmap = QPixmap(f"{self.image_path}/user_picture_placeholder.png").scaled(30, 30, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.user_picture.setPixmap(self.pixmap)
        self.user_frame_layout.addWidget(self.user_picture)
        self.user_frame_layout.addWidget(self.username_label)
        self.user_frame_layout.addWidget(self.new_user_button)
        self.user_frame_layout.addWidget(self.settings_button)

        left_container.addWidget(logo_frame)
        left_container.addWidget(upper_frame)
        left_container.addWidget(server_frame, 1)
        left_container.addWidget(user_frame)

        main_root_layout.addLayout(left_container, 1)
        main_root_layout.addWidget(main_frame, 5)

    def add_server_window_show_main_ui(self):
        self.add_server_window.hide()
        self.overlay.hide()
        self.reload_servers()

    def login_server_window_show_main_ui(self):
        self.login_server_window.hide()
        self.overlay.hide()
        self.reload_servers()

    def reload_servers(self):
        while self.server_layout.count():
            item = self.server_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        server_list = server_loader()
        for server in server_list:
            server_button = ServerButton(server["name"], server["ip_address"], self.login_page_popup, self.server_delete_data)
            self.server_layout.addWidget(server_button)

    def client_display_message(self, username, content, time):
        message_widget = MessageWidget(username, content, time, f"{self.image_path}/user_picture_placeholder.png")
        self.chat_layout.addWidget(message_widget)

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

    def login_page_popup(self, item):
        server_address = item.ip
        server_name = item.name
        self.login_server_window.get_server_info(server_address, server_name)
        self.show_popup(self.login_server_window)
    
    def on_success_login(self, username, server_name):
        self.username_label.setText(username)

        header = QFrame()
        header.setStyleSheet("""
            background-color: #161b22;
            border-bottom: 1px solid white;
        """)
        header.setFixedHeight(45)

        header_layout = QHBoxLayout(header)

        self.server_name_label = QLabel(server_name)
        self.server_name_label.setStyleSheet("""
            color: #e6edf3;
            font-size: 16px;
            font-weight: 600;
            border: none;
        """)

        header_layout.addWidget(self.server_name_label)
        header_layout.addStretch()

        self.chat_container = QFrame()

        self.chat_layout = QVBoxLayout(self.chat_container)
        self.chat_layout.setSpacing(12)
        self.chat_layout.setContentsMargins(0, 0, 0, 0)
        self.chat_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)
        
        scroll = QScrollArea()
        scroll.setStyleSheet("border: none;")
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.chat_container)

        scroll_container = QWidget()
        scroll_container.setStyleSheet("border: none;")
        scroll_layout = QVBoxLayout(scroll_container)
        scroll_layout.setContentsMargins(12, 12, 12, 12)

        scroll_layout.addWidget(scroll)

        self.message_input = QTextEdit()
        self.message_input.setFixedHeight(50)
        self.message_input.setPlaceholderText("Type a message...")
        self.message_input.installEventFilter(self)
        self.message_input.setStyleSheet("""
            QTextEdit {
                border-radius: 10px;
                border: 1px solid #1e293b;
                background-color: #0f172a;
                color: #e6edf3;
                padding: 10px;
            }

            QTextEdit:focus {
                border: 1px solid #3b82f6;
            }
        """)

        input_layout = QHBoxLayout()
        input_layout.setContentsMargins(5, 5, 5, 5)
        input_layout.addWidget(self.message_input)

        chat_wrapper = QFrame()

        chat_wrapper_layout = QVBoxLayout(chat_wrapper)
        chat_wrapper_layout.setContentsMargins(0, 0, 0, 0)
        chat_wrapper_layout.setSpacing(0)
        
        chat_wrapper_layout.addWidget(header)
        chat_wrapper_layout.addWidget(scroll_container)
        chat_wrapper_layout.addLayout(input_layout)

        self.all_users_container = QWidget()
        self.all_users_layout = QVBoxLayout(self.all_users_container)
        self.all_users_layout.setSpacing(5)
        self.all_users_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        all_users_scroll = QScrollArea()
        all_users_scroll.setStyleSheet("border-left: 1px solid white;")
        all_users_scroll.setWidget(self.all_users_container)
        all_users_scroll.setWidgetResizable(True)

        self.main_layout_horizontal.addWidget(chat_wrapper, 5)
        self.main_layout_horizontal.addWidget(all_users_scroll, 1)
        self.message_input.setFocus()

    def server_delete_data(self, item):
        self.server_address = item.ip
        delete_server(self.server_address)
        self.reload_servers()

    def identity_window_show_main_ui(self):
        self.identity_window.hide()
        self.overlay.hide()

    def show_popup(self, widget):
        while self.popup_background_container_layout.count():
            item = self.popup_background_container_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)

        self.popup_background_container_layout.addWidget(widget)
        self.overlay.setGeometry(0, 0, self.width(), self.height())
        self.overlay.raise_()
        self.overlay.show()
        widget.show()

    def add_users(self, users):
        for user in users:
            user_widget = UserWidget(user, f"{self.image_path}/user_picture_placeholder.png")
            self.all_users_layout.addWidget(user_widget)
    
    def eventFilter(self, obj, event):
        if obj == self.message_input and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Return:
                self.client_send_message()
                return True
        return False     

    def server_close_message(self, message):
        QMessageBox.warning(self, "Server Message", message)
        self.message_input.setEnabled(False)

class ServerButton(QFrame):
    def __init__(self, name, ip, on_click, on_delete):
        super().__init__()

        self.name = name
        self.ip = ip
        self.on_click = on_click
        self.on_delete = on_delete

        self.setFixedHeight(40)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            QFrame {
                background-color: #1e1e2f;
                border-radius: 10px;
                border: 1px solid #3f3f4a;
            }

            QFrame:hover {
                background-color: #333333;
            }
        """)

        layout = QHBoxLayout(self)

        self.label = QLabel()
        self.label.setFixedWidth(180)
        self.label.setStyleSheet("""
            QLabel {
                color: #a5a8ad;
                border: none;
                background: transparent;
                font-size: 15px;
            }
        """)

        self.resize_server_name()

        self.delete_button = QPushButton("X")
        self.delete_button.setFixedSize(20, 20)
        self.delete_button.setStyleSheet("""
            QPushButton {
                border: none;
                color: #8c8c8c;
                background: transparent;
            }

            QPushButton:hover {
                color: #bababa;
            }
        """)

        layout.addWidget(self.label)
        layout.addStretch()
        layout.addWidget(self.delete_button)

        self.mousePressEvent = self.frame_clicked
        self.delete_button.clicked.connect(self.delete_button_clicked)
    
    def resize_server_name(self):
        metrics = QFontMetrics(self.label.font())
        resize_name = metrics.elidedText(self.name, Qt.ElideRight, self.label.width())
        self.label.setText(resize_name)

    def frame_clicked(self, event):
        self.on_click(self)

    def delete_button_clicked(self):
        self.on_delete(self)

class MessageWidget(QWidget):
    def __init__(self, username, message, time, image):
        super().__init__() 
        self.setObjectName("message_container")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet("""
            #message_container {
                background-color: #111827;
                border-radius: 12px;
            }
        """)

        layout = QHBoxLayout(self)
        
        icon = QLabel()
        icon.setStyleSheet("background-color: white; border-radius: 15px;")
        pixmap = QPixmap(image).scaled(35, 35, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        mask = QBitmap(35, 35)
        mask.fill(Qt.color0)
        painter = QPainter(mask)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.color1)
        painter.drawEllipse(0, 0, 35, 35)
        painter.end()
        pixmap.setMask(mask)
        icon.setPixmap(pixmap)
        icon.setFixedSize(35, 35)

        right_layout = QVBoxLayout()

        left_layout = QVBoxLayout()

        top_row = QHBoxLayout()

        username = QLabel(username)
        username.setStyleSheet("color: #58a6ff; font-weight: 500; font-size: 15px;")

        time = QLabel(time)
        time.setStyleSheet("color: #58a6ff; font-weight: 500; font-size: 10px;")

        message = QLabel(message)
        message.setWordWrap(True)
        message.setStyleSheet("color: #e6edf3;")

        right_layout.addLayout(top_row)
        right_layout.addWidget(message)

        left_layout.addWidget(icon, alignment = Qt.AlignTop)

        top_row.addWidget(username)
        top_row.addWidget(time)

        layout.addLayout(left_layout)
        layout.addSpacing(10)
        layout.addLayout(right_layout)

class UserWidget(QWidget):
    def __init__(self, username, image):
        super().__init__()

        self.setObjectName("userwidget")
        self.setAttribute(Qt.WA_StyledBackground, True)

        self.setStyleSheet("""
            #userwidget {
                background-color: rgba(255, 255, 255, 0.05);
                border-radius: 8px;
                padding: 5px; 
                border: none;           
            }

            #userwidget:hover {
                background-color: #1f2933;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        icon = QLabel("icon")
        icon.setStyleSheet("background-color: white; border-radius: 15px; border: none;")
        icon.setFixedSize(30, 30)

        pixmap = QPixmap(image).scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
        mask = QBitmap(30, 30)
        mask.fill(Qt.color0)

        painter = QPainter(mask)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(Qt.color1)
        painter.drawEllipse(0, 0, 30, 30)
        painter.end()

        pixmap.setMask(mask)

        icon.setPixmap(pixmap)

        username_label = QLabel(username)
        username_label.setStyleSheet("font-size: 15px; border: none;")
        username_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon_layout = QVBoxLayout()
        username_label_layout = QVBoxLayout()
        username_label_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        icon_layout.addWidget(icon)
        username_label_layout.addWidget(username_label)

        layout.addLayout(icon_layout)
        layout.addLayout(username_label_layout)