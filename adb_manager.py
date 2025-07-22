import subprocess
import os


class AdbManager:
    def __init__(self, log_func):
        self.log = log_func

    def run(self, command):
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            return result.stdout.strip()
        except Exception as e:
            return str(e)

    def connect(self, ip):
        return self.run(["adb", "connect", f"{ip}:5555"])

    def disconnect(self):
        return self.run(["adb", "disconnect"])

    def list_devices(self):
        return self.run(["adb", "devices"])

    def reboot_device(self):
        return self.run(["adb", "reboot"])

    def install_apk(self, apk_path):
        if not apk_path or not os.path.isfile(apk_path):
            return "APK path is invalid or file not found."
        return self.run(["adb", "install", apk_path])

    def uninstall_package(self, package):
        return self.run(["adb", "uninstall", package])

    def launch_app(self, package_activity):
        return self.run(["adb", "shell", "am", "start", "-n", package_activity])

    def kill_app(self, package):
        return self.run(["adb", "shell", "am", "force-stop", package])

    def keyevent(self, code):
        return self.run(["adb", "shell", "input", "keyevent", str(code)])
