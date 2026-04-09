from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QSharedMemory
from PySide6.QtGui import QIcon
from server_modules.main_ui import MainUi
from server_modules.load_assets import app_icon
import sys

shared_memory = QSharedMemory("BiteWire_Server")

def main():
    if not shared_memory.create(1):
        sys.exit(0)

    app = QApplication()
    app.setWindowIcon(QIcon(app_icon()))
    window = MainUi()
    window.show()
    app.exec()

if __name__ == "__main__":
    main()