from __future__ import annotations

import http.client
from time import sleep
from typing import List, Optional

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    WebDriverException,
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from PySide6.QtWidgets import QMessageBox

from core.logger import logger


class AppiumManager:
    """Handles Appium driver initialization and UI automation for Android TV."""

    def __init__(self, log_func, parent=None, host: str = "127.0.0.1", port: int = 4723) -> None:
        self.driver: Optional[webdriver.Remote] = None
        self.log = log_func
        self.parent = parent
        self.host = host
        self.port = port

    # ---------- Utility ----------

    def _is_appium_server_running(self) -> bool:
        conn: Optional[http.client.HTTPConnection] = None
        try:
            conn = http.client.HTTPConnection(self.host, self.port, timeout=2)
            conn.request("GET", "/status")
            res = conn.getresponse()
            return res.status == 200
        except (http.client.HTTPException, OSError, ConnectionError, TimeoutError):
            return False
        finally:
            if conn is not None:
                try:
                    conn.close()
                except Exception:
                    pass

    # ---------- Driver Initialization ----------

    def init_driver(
        self,
        package: str | None = None,
        activity: str | None = None,
        *,
        auto_launch: bool = True,
    ) -> None:
        """
        Initialize Appium driver and verify Appium server is running.

        - If auto_launch=False, we attach without launching the app (no ADB start).
        - Provide package/activity when you want metadata on the target app, but with
          auto_launch=False we won't launch it.
        """
        if not self._is_appium_server_running():
            msg = f"Appium server is not running on {self.host}:{self.port}."
            self.log(msg)
            logger.error(msg)
            QMessageBox.critical(self.parent, "Appium Server Not Running", msg)
            return

        # Close old session if active
        if self.driver:
            try:
                self.driver.quit()
                self.log("Previous Appium session closed.")
            except WebDriverException as e:
                self.log(f"Error closing old Appium driver: {e}")
                logger.error(f"Error closing old Appium driver: {e}")

        try:
            options = UiAutomator2Options()

            # Required basics
            options.platform_name = "Android"
            options.device_name = "Android TV"

            # Only set package/activity if provided by caller
            if package:
                options.app_package = package
            if activity:
                options.app_activity = activity

            # Stability/attach flags
            options.no_reset = True
            options.new_command_timeout = 120
            options.auto_grant_permissions = True
            options.dont_stop_app_on_reset = True
            options.app_wait_activity = "*"

            self.driver = webdriver.Remote(f"http://{self.host}:{self.port}", options=options)
            self.log("Appium driver initialized")
            logger.info("Appium driver initialized")
        except WebDriverException as e:
            msg = f"Failed to initialize Appium driver: {e}"
            self.log(msg)
            logger.error(msg)
            QMessageBox.critical(self.parent, "Appium Error", msg)
            self.driver = None

    # ---------- Quick Checks ----------

    def is_package_in_foreground(self, expected_package: str) -> bool:
        """Check if the expected package is currently active on the device."""
        if not self.driver:
            return False
        try:
            current = getattr(self.driver, "current_package", None)
            # self.log(f"Foreground package: {current}")
            return current == expected_package
        except WebDriverException as e:
            self.log(f"Could not read current_package: {e}")
            return False

    def verify_login_screen_fast(self, texts_to_find: List[str], max_wait_ms: int = 1200) -> bool:
        """Quick check for login screen without long waiting."""
        driver = self.driver
        if driver is None:
            return False

        polls = max(1, max_wait_ms // 300)
        for _ in range(polls):
            try:
                all_ok = all(
                    bool(
                        driver.find_elements(
                            AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{text}")'
                        )
                    )
                    for text in texts_to_find
                )
                if all_ok:
                    self.log("Login screen verified quickly.")
                    return True
            except (WebDriverException, NoSuchElementException) as e:
                self.log(f"Quick login check error: {e}")
            sleep(0.3)

        self.log("Login screen not detected within short timeout.")
        return False

    # ---------- Focus Control & Info ----------

    def _is_text_focused(self, text: str) -> bool:
        assert self.driver is not None, "Driver must be initialized"
        el = self.driver.find_element(
            AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{text}")'
        )
        return str(el.get_attribute("focused")).lower() == "true"

    def get_focused_element_text(self) -> str:
        """
        Return the text (or content-desc) of the currently focused element, or '' if none.
        """
        if not self.driver:
            return ""
        try:
            el = self.driver.find_element(
                AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().focused(true)'
            )
            txt = (el.get_attribute("text") or "").strip()
            if not txt:
                txt = (el.get_attribute("contentDescription") or "").strip()
            return txt
        except NoSuchElementException:
            return ""
        except WebDriverException as e:
            self.log(f"Error while reading focused element: {e}")
            return ""

    def _press(self, keycode: int, times: int = 1) -> None:
        if not self.driver:
            return
        for _ in range(times):
            self.driver.press_keycode(keycode)

    def focus_second_and_enter(self, first_text: str, second_text: str) -> bool:
        """Ensure focus on the second button and press OK."""
        if not self.driver:
            self.log("Driver not initialized; cannot move focus.")
            return False

        try:
            self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{first_text}")')
            self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().text("{second_text}")')
        except (NoSuchElementException, WebDriverException) as e:
            self.log(f"Focus pre-check failed: {e}")
            return False

        try:
            if self._is_text_focused(second_text):
                self.log("Second button already focused. Pressing OK.")
                self._press(66)  # ENTER/OK
                return True
        except (NoSuchElementException, WebDriverException):
            pass

        try:
            if self._is_text_focused(first_text):
                self.log("First button focused. Moving right to select second.")
                self._press(21)  # LEFT
                if self._is_text_focused(second_text):
                    self._press(66)  # ENTER/OK
                    return True
        except (NoSuchElementException, WebDriverException):
            pass

        self.log("Could not focus on second button.")
        return False

    # ---------- Connect To Account ----------

    def connect_to_account(self, number: str) -> None:
        """Enter the phone number using keypad and confirm."""
        from core.constants import KEYPAD_SUFFIX  # local import to avoid cyclical issues

        if not self.driver:
            self.log("Driver is not initialized.")
            QMessageBox.critical(
                self.parent,
                "Appium Driver Not Initialized",
                "Appium driver is not initialized.\n\nPlease start Appium first."
            )
            return

        wait = WebDriverWait(self.driver, 1)

        for digit in number:
            button_id = f"tv.freetv.androidtv:id/keypadButton{KEYPAD_SUFFIX.get(digit, '')}"
            self.log(f"Clicking keypad digit '{digit}' (ID: {button_id})")
            try:
                el = wait.until(EC.element_to_be_clickable((AppiumBy.ID, button_id)))
                el.click()
            except TimeoutException as e:
                self.log(f"Failed to press digit {digit} (timeout): {e}")
                logger.error(f"Failed to press digit {digit}: {e}")
            except WebDriverException as e:
                self.log(f"Failed to press digit {digit} (webdriver): {e}")
                logger.error(f"Failed to press digit {digit}: {e}")

        # Navigate down 4 times and press OK
        try:
            self.log("Navigating down to confirm phone number entry...")
            self._press(20, times=5)  # DOWN x5
            self._press(22)           # RIGHT
            self._press(66)           # OK
            self.log("Confirmation complete.")
        except WebDriverException as e:
            self.log(f"Error during navigation: {e}")

        self.log("Keeping Appium session open for further actions.")

    # ---------- Close Driver ----------

    def close_driver(self) -> None:
        """Safely close the Appium driver session."""
        if self.driver:
            try:
                self.driver.quit()
                self.log("Appium driver closed manually.")
            except WebDriverException as e:
                self.log(f"Error closing Appium driver: {e}")
            finally:
                self.driver = None
