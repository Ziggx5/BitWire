import requests
import os
from packaging import version
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class UpdateChecker(QWidget):
    update_found = Signal(str)

    def __init__(self, image_path):
        super().__init__()
        self.current_release = "1.7.0"
        self.url = "https://api.github.com/repos/Ziggx5/BiteWire/releases"
        #self.on_cancel = on_cancel

        self.setFixedSize(550, 500)
        self.setStyleSheet("background-color: transparent;")

        update_page_layout = QVBoxLayout(self)
        header_page_horizontal_layout = QHBoxLayout()
        header_page_vertical_layout = QVBoxLayout()

        update_image_widget = QWidget()
        update_image_widget.setFixedSize(100, 100)
        update_image_widget.setStyleSheet("""
            QWidget {
                background-color: #2b2d30;
                border-radius: 50px;
            }
        """)

        update_image_layout = QVBoxLayout(update_image_widget)

        update_image = QLabel()
        update_image.setFixedSize(60, 60)
        update_image.setPixmap(QPixmap(f"{image_path}/update_now.png").scaled(60, 60, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation))

        update_image_layout.addWidget(update_image, alignment = Qt.AlignmentFlag.AlignCenter)

        update_label = QLabel("Update available")
        update_label.setStyleSheet("font-size: 22px; font-weight: 600;")

        subtitle_label = QLabel("A new version of BiteWire is ready to install.")
        subtitle_label.setStyleSheet("font-size: 14px; font-weight: 500; color: #b3b3b3;")

        version_widget = QWidget()
        version_widget.setFixedSize(130, 35)
        version_widget.setStyleSheet("""
            QWidget {
                background-color: rgba(59, 130, 245, 0.15);
                border-radius: 10px;
                border: 1px solid rgba(59, 130, 245, 0.4);
            }    
        """)

        version_widget_layout = QHBoxLayout(version_widget)
        version_widget_layout.setContentsMargins(10, 4, 10, 4)

        self.new_version_label = QLabel("version")
        self.new_version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.new_version_label.setStyleSheet("""
            QLabel {
                color: #60a5fa;
                font-size: 14px;
                font-weight: 600;
                background: transparent;
                border: none;
            }
        """)

        version_widget_layout.addWidget(self.new_version_label)

        header_page_vertical_layout.addWidget(update_label)
        header_page_vertical_layout.addWidget(subtitle_label)
        header_page_vertical_layout.addWidget(version_widget)

        header_page_horizontal_layout.addWidget(update_image_widget)
        header_page_horizontal_layout.addLayout(header_page_vertical_layout)


        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("border: none; background: transparent;")

        scroll_content = QWidget()

        scroll_layout = QVBoxLayout(scroll_content)

        self.description = QLabel("""
            - Added profile pictures
            - Added update popup
            - Fixed duplicated users list
            - Improved networking
            - Better UI performance
            - Added profile pictures
            - Added update popup
            - Fixed duplicated users list
            - Improved networking
            - Better UI performance
            - Added profile pictures
            - Added update popup
            - Fixed duplicated users list
            - Improved networking
            - Better UI performance
            - Added profile pictures
            - Added update popup
            - Fixed duplicated users list
            - Improved networking
            - Better UI performance
        """)
        self.description.setWordWrap(True)
        self.description.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.description.setStyleSheet("font-size: 18px;")

        scroll_layout.addWidget(self.description)
        scroll.setWidget(scroll_content)

        upper_line = QFrame()
        upper_line.setFrameShape(QFrame.Shape.HLine)
        upper_line.setStyleSheet("color: #30363d;")

        bottom_line = QFrame()
        upper_line.setFrameShape(QFrame.Shape.HLine)
        upper_line.setStyleSheet("color: #30363d;")

        update_page_layout.addLayout(header_page_horizontal_layout)
        update_page_layout.addWidget(upper_line)
        update_page_layout.addWidget(scroll)
        update_page_layout.addWidget(bottom_line)

    def check_update(self):
        response = requests.get(self.url)
        data = response.json()

        try:
            for release in data:
                tag = release["tag_name"]
                if tag.startswith("c"):
                    split_release = tag[1:]
                    if version.parse(split_release) > version.parse(self.current_release):
                        latest_release = split_release
                        self.update_found.emit(latest_release)
                        self.new_version_label.setText(f"Version {latest_release}")
                        break
            return None

        except:
            return None