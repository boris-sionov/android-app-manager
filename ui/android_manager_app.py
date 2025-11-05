from __future__ import annotations

from datetime import datetime
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFileDialog, QMessageBox

from core.logger import logger
from core.constants import (
    APPIUM_HOST,
    APPIUM_PORT,
    FREETV_PROD_PACKAGE,
    FREETV_UAT_PACKAGE,
)

from controllers.android_manager_controller import AndroidManagerController
from ui.sections.top_bar import TopBar
from ui.sections.actions_grid import ActionsGrid
from ui.sections.log_panel import LogPanel
from ui.dialogs.confirm_dialog import ConfirmDialog
from widgets.rcu_dialog import RCUDialog  # Option A: widgets outside /ui


class AndroidManagerApp(QWidget):
    """
    Main window (thin). Owns UI composition and signal wiring.
    All heavy logic (ADB/Appium/account flow) is delegated to AndroidManagerController.
    """

    def __init__(self) -> None:
        super().__init__()

        # --- Window ---
        self.setWindowTitle("Android QA Tool")
        self.resize(1200, 800)

        # --- State ---
        self._apk_path: str = ""

        # --- UI sections ---
        self._root = QVBoxLayout(self)
        self.top_bar = TopBar(parent=self)
        self.actions = ActionsGrid(parent=self)
        self.log_panel = LogPanel(parent=self)

        self._root.addWidget(self.top_bar)
        self._root.addWidget(self.actions)
        self._root.addWidget(self.log_panel)

        # --- Controller ---
        self.controller = AndroidManagerController(
            log_cb=self.log_output,
            app_host=APPIUM_HOST,
            app_port=APPIUM_PORT,
            parent=self,
        )

        self._wire_signals()

    # ========================= Wire-up ========================= #
    def _wire_signals(self) -> None:
        # Top bar
        self.top_bar.sigConnectDevice.connect(self._connect_device)
        self.top_bar.sigDisconnectDevice.connect(self._disconnect_device)
        self.top_bar.sigConnectAccount.connect(self._connect_account)

        # Actions grid — General
        self.actions.sigListDevices.connect(self._list_devices)
        self.actions.sigSelectApk.connect(self._select_apk)
        self.actions.sigInstallApk.connect(self._install_apk)
        self.actions.sigRebootDevice.connect(self._reboot_device)
        self.actions.sigGetDeviceIp.connect(self._get_device_ip)
        self.actions.sigGoHome.connect(
            lambda: self.controller.go_home(device_ip=self.top_bar.current_ip())
        )
        self.actions.sigOpenRcu.connect(self._open_rcu)

        # Actions grid — PROD
        self.actions.sigUninstallProd.connect(
            lambda: self._confirm_and(
                action=lambda: self.controller.uninstall_package(
                    FREETV_PROD_PACKAGE, device_ip=self.top_bar.current_ip()
                ),
                title="Confirm Uninstall",
                message=(
                    "Uninstalling this app will remove it completely from the device.\n\n"
                    "Do you want to continue?"
                ),
            )
        )
        self.actions.sigLaunchProd.connect(
            lambda: self._launch_activity(
                "tv.freetv.androidtv/pl.atende.mobile.tv.ui.gui.main.activity.MainActivity"
            )
        )
        self.actions.sigConnectAccountProd.connect(self._connect_account)
        self.actions.sigClearDataProd.connect(
            lambda: self._confirm_and(
                action=lambda: self.controller.clear_data(
                    FREETV_PROD_PACKAGE, device_ip=self.top_bar.current_ip()
                ),
                title="Confirm Clear Data",
                message=(
                    "This action will clear all app data.\n"
                    "You will be disconnected from your account and all stored data will be removed.\n\n"
                    "Do you want to continue?"
                ),
            )
        )
        self.actions.sigKillProd.connect(
            lambda: self._confirm_and(
                action=lambda: self.controller.kill_app(
                    FREETV_PROD_PACKAGE, device_ip=self.top_bar.current_ip()
                ),
                title="Confirm Kill App",
                message="This will immediately stop the app from running.\n\nDo you want to continue?",
            )
        )

        # Actions grid — UAT
        self.actions.sigUninstallUat.connect(
            lambda: self._confirm_and(
                action=lambda: self.controller.uninstall_package(
                    FREETV_UAT_PACKAGE, device_ip=self.top_bar.current_ip()
                ),
                title="Confirm Uninstall",
                message=(
                    "Uninstalling this app will remove it completely from the device.\n\n"
                    "Do you want to continue?"
                ),
            )
        )
        self.actions.sigLaunchUat.connect(
            lambda: self._launch_activity(
                "tv.freetv.androidtv.uat/pl.atende.mobile.tv.ui.gui.main.activity.MainActivity"
            )
        )
        self.actions.sigClearDataUat.connect(
            lambda: self._confirm_and(
                action=lambda: self.controller.clear_data(
                    FREETV_UAT_PACKAGE, device_ip=self.top_bar.current_ip()
                ),
                title="Confirm Clear Data",
                message=(
                    "This action will clear all app data.\n"
                    "You will be disconnected from your account and all stored data will be removed.\n\n"
                    "Do you want to continue?"
                ),
            )
        )

        # Actions grid — Appium
        self.actions.sigStartAppium.connect(self._start_appium)
        self.actions.sigKillAppium.connect(self._kill_appium)

    # ========================= UI Helpers ========================= #
    def log_output(self, text: str, level: str = "INFO") -> None:
        """
        Central logging: prints to python logger and to the UI log panel with timestamp.
        """
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{ts}] [{level}] {text}"
        if level.upper() == "ERROR":
            logger.error(text)
        elif level.upper() in ("WARN", "WARNING"):
            logger.warning(text)
        else:
            logger.info(text)

        self.log_panel.append_line(line)

    def _error(self, title: str, text: str) -> None:
        QMessageBox.critical(self, title, text)

    def _confirm_and(self, *, action, title: str, message: str) -> None:
        if ConfirmDialog.ask(self, title=title, message=message):
            try:
                action()
            except Exception as e:
                self._error("Error", str(e))

    # ========================= Top Bar Actions ========================= #
    def _connect_device(self) -> None:
        ip = self.top_bar.current_ip()
        if not ip:
            self._error("Error", "Please enter IP.")
            return
        self.controller.connect_device(ip)

    def _disconnect_device(self) -> None:
        self.controller.disconnect_device()

    def _connect_account(self) -> None:
        phone = self.top_bar.current_phone()
        if not phone:
            self._error("Error", "Please enter phone number (e.g., 05XXXXXXXX).")
            return
        self.controller.connect_account(
            phone=phone,
            device_ip=self.top_bar.current_ip(),
        )

    # ========================= Actions Grid Handlers ========================= #
    def _list_devices(self) -> None:
        self.controller.list_devices()

    def _select_apk(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Select APK", "", "APK Files (*.apk)")
        if not path:
            return
        if not path.endswith(".apk"):
            self._error("Error", "Not an APK file.")
            return
        self._apk_path = path
        self.log_output(f"APK selected: {path}")

    def _install_apk(self) -> None:
        if not self._apk_path:
            self._error("Error", "No APK selected.")
            return
        self.controller.install_apk(self._apk_path, device_ip=self.top_bar.current_ip())

    def _reboot_device(self) -> None:
        self.controller.reboot_device(device_ip=self.top_bar.current_ip())

    def _get_device_ip(self) -> None:
        ip = self.controller.get_device_ip()
        if isinstance(ip, str) and ip and "not found" not in ip.lower():
            self.top_bar.set_ip(ip)
        self.log_output(f"Detected IP: {ip}")

    def _open_rcu(self) -> None:
        dialog = RCUDialog(self.log_output, self.controller.adb_manager, self)
        dialog.setModal(False)
        dialog.show()
        dialog.raise_()
        dialog.activateWindow()

    def _launch_activity(self, package_activity: str) -> None:
        self.controller.launch_activity(
            package_activity=package_activity,
            device_ip=self.top_bar.current_ip(),
        )

    # ========================= Appium Controls ========================= #
    def _start_appium(self) -> None:
        self.controller.start_appium()

    def _kill_appium(self) -> None:
        self.controller.kill_appium()
