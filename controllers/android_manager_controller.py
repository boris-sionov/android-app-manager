from __future__ import annotations

import os
import socket
import subprocess
from typing import Callable, Optional

from PySide6.QtCore import QObject
from PySide6.QtWidgets import QMessageBox

from core.adb_manager import AdbManager
from core.appium_manager import AppiumManager
from core.constants import LOGIN_FIRST_TEXT, LOGIN_SECOND_TEXT, LOGIN_SCREEN_TEXTS
from core.logger import logger


class AndroidManagerController(QObject):
    def __init__(self, *, log_cb: Callable[[str, str], None], app_host: str, app_port: int, parent=None) -> None:
        super().__init__(parent)
        self._log_cb = log_cb
        self._host = app_host
        self._port = app_port
        self.adb_manager = AdbManager(self._log)
        self.appium_manager = AppiumManager(self._log, parent=self, host=self._host, port=self._port)

    # ---- logging helpers ----

    def _log(self, text: str, level: str = "INFO") -> None:
        try:
            self._log_cb(text, level)
        except Exception:
            pass

    @staticmethod
    def _popup_error(title: str, message: str) -> None:
        QMessageBox.critical(None, title, message)

    # ---- utils ----

    @staticmethod
    def _port_open(host: str, port: int, timeout: float = 0.35) -> bool:
        try:
            with socket.socket() as s:
                s.settimeout(timeout)
                return s.connect_ex((host, port)) == 0
        except OSError:
            return False

    @staticmethod
    def _has_connected_devices(adb_list_output: str) -> bool:
        lines = [ln for ln in adb_list_output.splitlines() if ln.strip() and not ln.startswith("List")]
        return any("\tdevice" in ln for ln in lines)

    @staticmethod
    def _valid_phone(phone: str) -> bool:
        phone = (phone or "").strip()
        return phone.startswith("05") and len(phone) in (10, 11) and phone.isdigit()

    # ---- ADB ops ----
    def connect_device(self, ip: str) -> None:
        if not ip:
            self._popup_error("Missing IP", "No IP provided.")
            logger.error("No IP provided.")
            return
        self._log(self.adb_manager.connect(ip))

    def disconnect_device(self) -> None:
        self._log(self.adb_manager.disconnect())

    def list_devices(self) -> None:
        self._log(self.adb_manager.list_devices())

    def reboot_device(self, *, device_ip: Optional[str] = None) -> None:
        self._log(self.adb_manager.reboot_device(device_ip=device_ip))

    def install_apk(self, apk_path: str, *, device_ip: Optional[str] = None) -> None:
        if not apk_path or not apk_path.endswith(".apk"):
            self._popup_error("Invalid APK", "Invalid APK path.")
            logger.error("Invalid APK path.")
            return
        self._log(self.adb_manager.install_apk(apk_path, device_ip=device_ip))

    def launch_activity(self, *, package_activity: str, device_ip: Optional[str] = None) -> None:
        res = self.adb_manager.launch_app(package_activity, device_ip=device_ip)
        self._log(f"Launch result: {res}")

    def uninstall_package(self, package: str, *, device_ip: Optional[str] = None) -> None:
        res = self.adb_manager.uninstall_package(package, device_ip=device_ip)
        self._log(f"Uninstalled {package}: {res}")

    def kill_app(self, package: str, *, device_ip: Optional[str] = None) -> None:
        res = self.adb_manager.kill_app(package, device_ip=device_ip)
        self._log(f"Killed {package}: {res}")

    def clear_data(self, package: str, *, device_ip: Optional[str] = None) -> None:
        res = self.adb_manager.clear_data(package, device_ip=device_ip)
        self._log(f"Data cleared for {package}: {res}")

    def get_device_ip(self) -> str:
        return self.adb_manager.get_device_ip()

    # add near other ADB ops
    def go_home(self, *, device_ip: Optional[str] = None) -> None:
        """Send HOME key to a device to background the current app."""
        self._log(f"Sending HOME to {device_ip or 'default'}")
        res = self.adb_manager.keyevent(3, device_ip=device_ip)  # 3 = KEYCODE_HOME
        self._log(f"HOME result: {res}")

    # ---- Appium lifecycle ----
    def start_appium(self) -> None:
        try:
            if self._port_open(self._host, self._port):
                self._log(f"Appium already running on {self._host}:{self._port}")
                return
            start_script = os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts", "start_appium.sh")
            if os.path.exists(start_script):
                subprocess.Popen(["bash", start_script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                self._log("Attempted to start Appium via scripts/start_appium.sh")
            else:
                subprocess.Popen(["appium"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                self._log("Appium server start requested (direct).")
        except Exception as e:
            self._popup_error("Appium Error", f"Failed to start Appium server:\n{e}")
            logger.error("Failed to start Appium server: %s", e)

    def kill_appium(self) -> None:
        try:
            kill_script = os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts", "kill_appium.sh")
            if os.path.exists(kill_script):
                subprocess.call(["bash", kill_script])
                self._log("Requested Appium stop via scripts/kill_appium.sh")
            else:
                subprocess.call(["pkill", "-f", "appium"])
                self._log("Appium server kill requested (pkill).")
        except Exception as e:
            self._popup_error("Appium Error", f"Failed to kill Appium server:\n{e}")
            logger.error("Failed to kill Appium server: %s", e)

    # ---- Account flow ----
    def connect_account(self, *, phone: str, device_ip: Optional[str] = None) -> None:
        # 0) Phone validation
        if not self._valid_phone(phone):
            self._popup_error("Invalid Phone Number", "Incorrect phone number.")
            logger.error("Incorrect phone number.")
            return

        # 1) Device connected?
        devices_output = self.adb_manager.list_devices()
        if not self._has_connected_devices(devices_output):
            self._popup_error("No Device", "No device connected. Please connect a device first.")
            logger.error("No device connected.")
            return

        # 2) Appium up?
        if not self._port_open(self._host, self._port):
            self._popup_error("Appium Not Running", "Appium server is not running.")
            logger.error("Appium server is not running.")
            return

        # 3) Create Appium session WITHOUT launching the app
        #    Provide package/activity only as metadata; auto_launch=False ensures no launch.
        self.appium_manager.init_driver(
            package="tv.freetv.androidtv",
            activity="pl.atende.mobile.tv.ui.gui.main.activity.MainActivity",
            auto_launch=False,
        )
        if not getattr(self.appium_manager, "driver", None):
            return

        # 4) Verify FreeTV in foreground; if not, ask user to open it
        if not self.appium_manager.is_package_in_foreground("tv.freetv.androidtv"):
            self._popup_error(
                "Open FreeTV",
                "FreeTV is not open on the device.\n\nPlease open the FreeTV app on the Android TV, then press 'Connect to Account' again."
            )
            logger.warning("FreeTV not in foreground when connecting to account.")
            return

        # 5) Verify Login screen (quick)
        if not self.appium_manager.verify_login_screen_fast(LOGIN_SCREEN_TEXTS, max_wait_ms=1200):
            self._popup_error("Login Screen Missing", "Could not detect the login screen.")
            logger.error("Login screen not detected.")
            return

        # 6) Report focused button text
        focused_text = self.appium_manager.get_focused_element_text()
        if focused_text:
            self._log(f"Currently focused: {focused_text}")
        else:
            self._log("No focused element detected.", "WARN")

        # 7) Move to the second button and press OK
        if not self.appium_manager.focus_second_and_enter(LOGIN_FIRST_TEXT, LOGIN_SECOND_TEXT):
            self._popup_error(
                "Cannot Focus Button",
                "Could not highlight the 'כניסה למנויים קיימים' button. Check the login screen and try again."
            )
            logger.error("Could not focus 'כניסה למנויים קיימים' button.")
            return

        # 8) Proceed to keypad entry
        self._log(f"Connecting to account with phone: {phone}")
        self.appium_manager.connect_to_account(phone)
