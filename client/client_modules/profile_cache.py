from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import base64

class ProfileCache:
    def __init__(self):
        self.cache = {}

    def save(self, username, picture_bytes):
        decoded_bytes = base64.b64decode(picture_bytes)

        pixmap = QPixmap()
        pixmap.loadFromData(decoded_bytes)
        picture = pixmap.scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)

        icon = QPixmap(30, 30)
        icon.fill(Qt.GlobalColor.transparent)

        painter = QPainter(icon)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        path = QPainterPath()
        path.addEllipse(0, 0, 30, 30)

        painter.setClipPath(path)
        painter.drawPixmap(0, 0, picture)
        painter.end()

        self.cache[username] = icon

        print(self.cache)

    def get(self, username):
        print(self.cache)