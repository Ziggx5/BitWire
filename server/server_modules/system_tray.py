from PySide6.QtWidgets import QSystemTrayIcon, QMenu, QApplication, QLabel
from PySide6.QtGui import QIcon, QAction
from server_modules.images_path import file_root
import webbrowser

class TrayManager:
    def __init__(self, parent):
        self.parent = parent

        picture_path = file_root()

        self.tray_icon = QSystemTrayIcon(QIcon(f"{picture_path}/tray_icon.png"), self.parent)
        self.tray_icon.setToolTip("BiteWire Server")

        menu = QMenu()

        github_link_action = QAction("Github Repository", self.tray_icon)
        github_link_action.triggered.connect(self.open_link)

        open_action = QAction("Open BiteWire Server", self.tray_icon)
        open_action.triggered.connect(self.parent.show)

        close_action = QAction("Close BiteWire Server", self.tray_icon)
        close_action.triggered.connect(self.exit_app)

        self.server_status = QAction("Stopped", self.tray_icon)
        self.server_status.setEnabled(False)

        self.server_uptime = QAction("00:00:00", self.tray_icon)
        self.server_uptime.setEnabled(False)

        menu.addAction(github_link_action)
        menu.addSeparator()
        menu.addAction(self.server_status)
        menu.addAction(self.server_uptime)
        menu.addAction(open_action)
        menu.addAction(close_action)
        
        self.tray_icon.setContextMenu(menu)
        self.tray_icon.activated.connect(self.parent.show)
        self.tray_icon.show()

    def open_link(self):
        webbrowser.open("https://github.com/Ziggx5/BiteWire")

    def exit_app(self):
        self.tray_icon.hide()
        QApplication.quit()

    def set_server_status(self, status):
        self.server_status.setText(status)
    
    def set_server_uptime(self, hours, minutes, seconds):
        self.server_uptime.setText(f"{hours:02}:{minutes:02}:{seconds:02}")