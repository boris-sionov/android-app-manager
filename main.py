import sys
from PySide6.QtWidgets import QApplication
from ui.android_manager_app import AndroidManagerApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AndroidManagerApp()
    window.resize(1200, 800)
    window.show()
    sys.exit(app.exec())
