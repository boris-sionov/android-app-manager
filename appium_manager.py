from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from constants import KEYPAD_SUFFIX


class AppiumManager:
    def __init__(self, log_func):
        self.driver = None
        self.log = log_func

    def init_driver(self, package, activity):
        if self.driver:
            try:
                self.driver.quit()
                self.log("Previous Appium session ended.")
            except Exception as e:
                self.log(f"Error closing Appium driver: {e}")
        options = UiAutomator2Options()
        options.platform_name = "Android"
        options.device_name = "Android Device"
        options.app_package = package
        options.app_activity = activity
        options.no_reset = True
        self.driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
        self.log(f"Appium driver initialized for {package}")

    def connect_to_account(self, number):
        if not self.driver:
            self.log("Driver is not initialized.")
            return

        wait = WebDriverWait(self.driver, 2)

        for digit in number:
            button_id = f"tv.freetv.androidtv:id/keypadButton{KEYPAD_SUFFIX[digit]}"
            self.log(f"Clicking button for digit '{digit}' with ID '{button_id}'")
            try:
                el = wait.until(EC.element_to_be_clickable((AppiumBy.ID, button_id)))
                el.click()
            except Exception as e:
                self.log(f"Failed to press digit {digit}: {e}")

        for _ in range(5):
            self.driver.press_keycode(20)  # DOWN

        self.driver.press_keycode(22)  # RIGHT
        self.driver.press_keycode(66)  # ENTER

        self.driver.quit()
        self.driver = None
        self.log("Appium session ended.")
