import subprocess
import os
from core.logger import logger


class AdbManager:
    def __init__(self, log_func):
        self.log = log_func

    def run(self, command, device_ip=None):
        """Execute ADB command, optionally targeting a specific device IP."""
        if device_ip:
            command = ["adb", "-s", f"{device_ip}:5555"] + command[1:]
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            output = result.stdout.strip()
            if result.stderr:
                logger.warning(f"ADB stderr: {result.stderr.strip()}")
            return output
        except Exception as e:
            logger.exception("ADB command failed")
            return str(e)

    def connect(self, ip):
        self.log(f"Connecting to device at IP: {ip}")
        return self.run(["adb", "connect", f"{ip}:5555"])

    def disconnect(self):
        self.log("Disconnecting all ADB devices")
        return self.run(["adb", "disconnect"])

    def list_devices(self):
        return self.run(["adb", "devices"])

    def reboot_device(self, device_ip=None):
        self.log(f"Rebooting device: {device_ip or 'default'}")
        return self.run(["adb", "reboot"], device_ip)

    def install_apk(self, apk_path, device_ip=None):
        self.log(f"Installing APK on device {device_ip or 'default'}: {apk_path}")
        if not apk_path or not os.path.isfile(apk_path):
            error_msg = "APK path is invalid or file not found."
            logger.warning(error_msg)
            return error_msg
        return self.run(["adb", "install", apk_path], device_ip)

    def uninstall_package(self, package, device_ip=None):
        self.log(f"Uninstalling package '{package}' on device {device_ip or 'default'}")
        return self.run(["adb", "uninstall", package], device_ip)

    def launch_app(self, package_activity, device_ip=None):
        self.log(f"Launching app '{package_activity}' on device {device_ip or 'default'}")
        return self.run(["adb", "shell", "am", "start", "-n", package_activity], device_ip)

    def kill_app(self, package, device_ip=None):
        self.log(f"Killing app '{package}' on device {device_ip or 'default'}")
        return self.run(["adb", "shell", "am", "force-stop", package], device_ip)

    def keyevent(self, code, device_ip=None):
        self.log(f"Sending keyevent {code} to device {device_ip or 'default'}")
        return self.run(["adb", "shell", "input", "keyevent", str(code)], device_ip)

    def get_device_ip(self):
        result = self.run(["adb", "shell", "ip", "-f", "inet", "addr", "show", "wlan0"])
        lines = result.splitlines()
        for line in lines:
            line = line.strip()
            if line.startswith("inet "):
                ip_address = line.split()[1].split("/")[0]
                return ip_address
        warning_msg = "IP address not found."
        logger.warning(warning_msg)
        return warning_msg

    def clear_data(self, package, device_ip=None):
        """Clear all app data for the given package (equivalent to Settings > Storage > Clear data)."""
        self.log(f"Clearing data for package '{package}' on device {device_ip or 'default'}")
        out = self.run(["adb", "shell", "pm", "clear", package], device_ip)

        if out.strip().lower().startswith("success"):
            return f"Data cleared for {package}."
        return f"Clear data result for {package}: {out}"
