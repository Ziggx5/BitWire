import requests
import os
from packaging import version
from PySide6.QtCore import QObject, Signal

class UpdateChecker(QObject):
    update_found = Signal(str)

    def __init__(self):
        super().__init__()
        self.current_release = "1.6.0"
        self.url = "https://api.github.com/repos/Ziggx5/BiteWire/releases"

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
                        break
            return None

        except:
            return None