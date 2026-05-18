import requests
import os
from packaging import version
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class UpdateChecker(QWidget):
    update_found = Signal(str)

    def __init__(self):
        super().__init__()
        self.current_release = "1.7.0"
        self.url = "https://api.github.com/repos/Ziggx5/BiteWire/releases"
        #self.on_cancel = on_cancel

        self.setFixedSize(500, 350)
        self.setStyleSheet("background-color: transparent;")

        update_page_layout = QVBoxLayout(self)

        self.update_label = QLabel("Update Available")
        self.update_label.setStyleSheet("font-size: 22px; font-weight: 600;")

        self.name_label = QLabel()

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

        update_page_layout.addWidget(self.update_label)
        update_page_layout.addWidget(self.name_label)
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
                        self.name_label.setText(f"BiteWire {self.current_release} => {latest_release}")
                        break
            return None

        except:
            return None