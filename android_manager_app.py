import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit,
    QFileDialog, QTextEdit, QMessageBox, QGridLayout
)
from PySide6.QtCore import Qt
from adb_manager import AdbManager
from appium_manager import AppiumManager
from rcu_dialog import RCUDialog
from constants import (
    FREETV_PROD_PACKAGE, FREETV_UAT_PACKAGE,
    BUTTON_STYLE
)


class AndroidManagerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.output_text = None
        self.apk_label = None
        self.phone_entry = None
        self.ip_entry = None
        self.setWindowTitle("Android APK Manager")
        self.apk_path = ""
        self.adb = AdbManager(self.log_output)
        self.appium = AppiumManager(self.log_output)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.ip_entry = QLineEdit()
        self.phone_entry = QLineEdit()
        self.apk_label = QLabel("")
        self.output_text = QTextEdit(readOnly=True)

        layout.addWidget(QLabel("Android Device IP:"))
        layout.addWidget(self.ip_entry)

        layout.addWidget(QLabel("Phone Number:"))
        layout.addWidget(self.phone_entry)

        grid = QGridLayout()

        # General
        grid.addWidget(QLabel("<b>General</b>"), 0, 0)
        grid.addWidget(self.btn("Connect", self.connect_device), 1, 0)
        grid.addWidget(self.btn("Disconnect", self.disconnect_device), 2, 0)
        grid.addWidget(self.btn("List Devices", self.list_devices), 3, 0)
        grid.addWidget(self.btn("Select APK", self.select_apk), 4, 0)
        grid.addWidget(self.btn("Install APK", self.install_apk), 5, 0)
        grid.addWidget(self.btn("Reboot Device", self.reboot_device), 6, 0)
        grid.addWidget(self.btn("Open RCU Control", self.open_rcu_window), 7, 0)

        # Prod
        grid.addWidget(QLabel("<b>Prod Version</b>"), 0, 1)
        grid.addWidget(self.btn("Uninstall FreeTV Prod", lambda: self.uninstall(FREETV_PROD_PACKAGE)), 1, 1)
        grid.addWidget(self.btn("Launch FreeTV Prod", lambda: self.launch("tv.freetv.androidtv/pl.atende.mobile.tv.ui.gui.main.activity.MainActivity")), 2, 1)
        grid.addWidget(self.btn("Connect to Account", self.connect_to_account), 3, 1)
        grid.addWidget(self.btn("Kill FreeTV App", lambda: self.kill(FREETV_PROD_PACKAGE)), 4, 1)

        # UAT
        grid.addWidget(QLabel("<b>UAT Version</b>"), 0, 2)
        grid.addWidget(self.btn("Uninstall FreeTV UAT", lambda: self.uninstall(FREETV_UAT_PACKAGE)), 1, 2)
        grid.addWidget(self.btn("Launch FreeTV UAT", lambda: self.launch("tv.freetv.androidtv.uat/pl.atende.mobile.tv.ui.gui.main.activity.MainActivity")), 2, 2)

        layout.addLayout(grid)
        layout.addWidget(self.apk_label)
        layout.addWidget(QLabel("<b>Log Output</b>"))
        layout.addWidget(self.output_text)

        clear_btn = QPushButton("Clear Log")
        clear_btn.setStyleSheet("""
        QPushButton {
            background-color: #f44336;
            color: white;
            padding: 10px 20px;
            font-size: 14px;
            border-radius: 6px;
        }
        QPushButton:hover {
            background-color: #d32f2f;
        }
        QPushButton:pressed {
            background-color: #b71c1c;
        }
        """)
        clear_btn.clicked.connect(self.output_text.clear)
        layout.addWidget(clear_btn)

    def btn(self, text, handler):
        b = QPushButton(text)
        b.setStyleSheet(BUTTON_STYLE)
        b.clicked.connect(handler)
        return b

    def log_output(self, text):
        self.output_text.append(text)
        self.output_text.verticalScrollBar().setValue(
            self.output_text.verticalScrollBar().maximum()
        )

    def connect_device(self):
        ip = self.ip_entry.text()
        if not ip:
            QMessageBox.critical(self, "Error", "Please enter IP.")
            return
        self.log_output(self.adb.connect(ip))

    def disconnect_device(self):
        self.log_output(self.adb.disconnect())

    def list_devices(self):
        self.log_output(self.adb.list_devices())

    def reboot_device(self):
        self.log_output(self.adb.reboot_device())

    def select_apk(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select APK", "", "APK Files (*.apk)")
        if path:
            if path.endswith(".apk"):
                self.apk_path = path
                self.apk_label.setText(path)
            else:
                QMessageBox.critical(self, "Error", "Not an APK file.")

    def install_apk(self):
        result = self.adb.install_apk(self.apk_path)
        self.log_output(result)

    def uninstall(self, package):
        result = self.adb.uninstall_package(package)
        self.log_output(f"Uninstalled {package}: {result}")

    def launch(self, activity):
        result = self.adb.launch_app(activity)
        self.log_output(f"Launched {activity}: {result}")

    def kill(self, package):
        result = self.adb.kill_app(package)
        self.log_output(f"Killed {package}: {result}")

    def connect_to_account(self):
        phone = self.phone_entry.text()
        if not phone:
            QMessageBox.critical(self, "Error", "Phone number required.")
            return
        for key in ["21", "66"]:  # LEFT, ENTER
            self.log_output(self.adb.keyevent(key))
        self.appium.init_driver("tv.freetv.androidtv", "tv.freetv.androidtv.MainActivity")
        self.appium.connect_to_account(phone)

    def open_rcu_window(self):
        dialog = RCUDialog(self.log_output, self.adb, self)
        dialog.exec()
