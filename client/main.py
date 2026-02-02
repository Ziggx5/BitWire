from PySide6.QtWidgets import QApplication
from client_modules.loading_screen import LoadingScreen

def main():
    app = QApplication()
    window = LoadingScreen()
    window.show()
    window.update_progress_bar()
    app.exec()

if __name__ == "__main__":
    main()