import threading
import time
import tkinter as tk
from time import sleep
from tkinter import filedialog, messagebox, scrolledtext
import subprocess
import os
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

driver = None  # global driver instance

# Packages to uninstall
FREETV_UAT_PACKAGE = "tv.freetv.androidtv.uat"
FREETV_PROD_PACKAGE = "tv.freetv.androidtv"


def connect_appium():
    global driver
    if driver:
        output_text.insert(tk.END, "Already connected to Appium.\n")
        return

    ip = ip_entry.get()
    if not ip:
        messagebox.showerror("Error", "Please enter IP address.")
        return

    desired_caps = {
        "platformName": "Android",
        "deviceName": "Android Device",
        "appPackage": "tv.freetv.androidtv",
        "appActivity": "pl.atende.mobile.tv.ui.gui.main.activity.MainActivity",  # adjust if needed
        "automationName": "UiAutomator2",
        "noReset": True,
    }

    def init_driver():
        global driver
        try:
            output_text.insert(tk.END, f"Connecting to Appium server at http://{ip}:4723/wd/hub ...\n")
            driver = webdriver.Remote(f"http://{ip}:4723/wd/hub", desired_caps)
            output_text.insert(tk.END, "Connected to Appium server!\n")
        except Exception as e:
            output_text.insert(tk.END, f"Error connecting to Appium: {e}\n")

    threading.Thread(target=init_driver).start()


def press_digit(digit: str):
    global driver
    if not driver:
        output_text.insert(tk.END, "Error: Appium driver not connected.\n")
        return

    button_ids = {
        "0": "tv.freetv.androidtv:id/keypadButtonZero",
        "1": "tv.freetv.androidtv:id/keypadButtonOne",
        "2": "tv.freetv.androidtv:id/keypadButtonTwo",
        "3": "tv.freetv.androidtv:id/keypadButtonThree",
        "4": "tv.freetv.androidtv:id/keypadButtonFour",
        "5": "tv.freetv.androidtv:id/keypadButtonFive",
        "6": "tv.freetv.androidtv:id/keypadButtonSix",
        "7": "tv.freetv.androidtv:id/keypadButtonSeven",
        "8": "tv.freetv.androidtv:id/keypadButtonEight",
        "9": "tv.freetv.androidtv:id/keypadButtonNine",
    }

    btn_id = button_ids.get(digit)
    if not btn_id:
        output_text.insert(tk.END, f"Invalid digit: '{digit}'\n")
        return

    try:
        element = driver.find_element(AppiumBy.ID, btn_id)
        element.click()
        output_text.insert(tk.END, f"Pressed digit '{digit}'\n")
    except Exception as e:
        output_text.insert(tk.END, f"Failed pressing digit '{digit}': {e}\n")


def run_adb_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        return result.stdout.strip()
    except Exception as e:
        return str(e)


def connect_device():
    show_press_effect(connect_btn)
    ip = ip_entry.get()
    if not ip:
        messagebox.showerror("Error", "Please enter IP address.")
        return
    output = run_adb_command(["adb", "connect", f"{ip}:5555"])
    output_text.insert(tk.END, output + "\n")


def disconnect_device():
    show_press_effect(disconnect_btn)
    output = run_adb_command(["adb", "disconnect"])
    output_text.insert(tk.END, output + "\n")


def list_devices():
    show_press_effect(list_btn)
    output = run_adb_command(["adb", "devices"])
    output_text.insert(tk.END, output + "\n")


def select_apk():
    show_press_effect(select_btn)
    filepath = filedialog.askopenfilename(filetypes=[("APK files", "*.apk")])
    if filepath:
        if not filepath.endswith(".apk"):
            messagebox.showerror("Error", "Selected file is not an APK.")
            return
        apk_path.set(filepath)


def install_apk():
    show_press_effect(install_btn)
    path = apk_path.get()
    if not path or not os.path.isfile(path):
        messagebox.showerror("Error", "No APK selected.")
        return
    output = run_adb_command(["adb", "install", path])
    output_text.insert(tk.END, output + "\n")


def uninstall_freetv_uat():
    show_press_effect(uninstall_freetv_uat_btn)
    output = run_adb_command(["adb", "uninstall", FREETV_UAT_PACKAGE])
    output_text.insert(tk.END, f"Uninstalled {FREETV_UAT_PACKAGE}: {output}\n")


def uninstall_freetv_prod():
    show_press_effect(uninstall_freetv_prod_btn)
    output = run_adb_command(["adb", "uninstall", FREETV_PROD_PACKAGE])
    output_text.insert(tk.END, f"Uninstalled {FREETV_PROD_PACKAGE}: {output}\n")


def launch_freetv_prod():
    show_press_effect(launch_freetv_prod_btn)
    output = run_adb_command([
        "adb",
        "shell",
        "am",
        "start",
        "-n",
        "tv.freetv.androidtv/pl.atende.mobile.tv.ui.gui.main.activity.MainActivity"
    ])
    output_text.insert(tk.END, f"Launched FreeTV Prod App:\n{output}\n")


def launch_freetv_uat():
    show_press_effect(launch_freetv_uat_btn)
    output = run_adb_command([
        "adb",
        "shell",
        "am",
        "start",
        "-n",
        "tv.freetv.androidtv.uat/pl.atende.mobile.tv.ui.gui.main.activity.MainActivity"
    ])
    output_text.insert(tk.END, f"Launched FreeTV UAT App:\n{output}\n")


def show_press_effect(button):
    original_bg = button.cget("background")
    button.config(background="lightblue")
    root.after(300, lambda *args: button.config(background=original_bg))


def connect_to_account():
    show_press_effect(auto_connect_btn)

    output1 = run_adb_command(["adb", "shell", "input", "keyevent", "21"])  # LEFT
    output_text.insert(tk.END, f"Sent LEFT key: {output1}\n")

    output2 = run_adb_command(["adb", "shell", "input", "keyevent", "66"])  # OK
    output_text.insert(tk.END, f"Sent OK key: {output2}\n")

    global driver

    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.device_name = "Android Device"
    options.app_package = "tv.freetv.androidtv"
    options.app_activity = "tv.freetv.androidtv.MainActivity"
    options.no_reset = True

    output_text.insert(tk.END, "Connecting to Appium server at http://127.0.0.1:4723 ...\n")

    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

    digit_to_id_suffix = {
        "0": "Zero",
        "1": "One",
        "2": "Two",
        "3": "Three",
        "4": "Four",
        "5": "Five",
        "6": "Six",
        "7": "Seven",
        "8": "Eight",
        "9": "Nine",
    }

    number = phone_number.get()
    if not number:
        messagebox.showerror("Error", "Please enter phone number.")
        return

    wait = WebDriverWait(driver, 2)

    for digit in number:
        button_id = f"tv.freetv.androidtv:id/keypadButton{digit_to_id_suffix[digit]}"
        output_text.insert(tk.END, f"Trying to press digit '{digit}' with ID '{button_id}'\n")

        element = wait.until(
            EC.element_to_be_clickable((AppiumBy.ID, button_id))
        )
        element.click()
        output_text.insert(tk.END, f"Pressed digit '{digit}'\n")

    output3 = run_adb_command(["adb", "shell", "input", "keyevent", "20"])  # DOWN
    output_text.insert(tk.END, f"Sent LEFT key: {output3}\n")
    output3 = run_adb_command(["adb", "shell", "input", "keyevent", "20"])  # DOWN
    output_text.insert(tk.END, f"Sent LEFT key: {output3}\n")
    output3 = run_adb_command(["adb", "shell", "input", "keyevent", "20"])  # DOWN
    output_text.insert(tk.END, f"Sent LEFT key: {output3}\n")
    output3 = run_adb_command(["adb", "shell", "input", "keyevent", "20"])  # DOWN
    output_text.insert(tk.END, f"Sent LEFT key: {output3}\n")
    output3 = run_adb_command(["adb", "shell", "input", "keyevent", "20"])  # DOWN
    output_text.insert(tk.END, f"Sent LEFT key: {output3}\n")
    output3 = run_adb_command(["adb", "shell", "input", "keyevent", "22"])  # RIGHT
    output_text.insert(tk.END, f"Sent LEFT key: {output3}\n")

    time.sleep(1)

    output4 = run_adb_command(["adb", "shell", "input", "keyevent", "66"])  # ENTER
    output_text.insert(tk.END, f"Sent ENTER key: {output4}\n")



# GUI setup
root = tk.Tk()
root.title("Android APK Manager")

ip_label = tk.Label(root, text="Android Device IP:")
ip_label.pack()

ip_entry = tk.Entry(root, width=30)
ip_entry.pack()
ip_entry.bind("<Return>", lambda event: connect_device())

phone_label = tk.Label(root, text="Phone Number:")
phone_label.pack()

phone_number = tk.StringVar()
phone_entry = tk.Entry(root, width=30, textvariable=phone_number)
phone_entry.pack()

apk_path = tk.StringVar()

BUTTON_WIDTH = 22
columns_frame = tk.Frame(root)
columns_frame.pack(pady=10)

# ============= COLUMN 1: GENERAL =============
general_label = tk.Label(columns_frame, text="General", font=("Arial", 12, "bold"))
general_label.grid(row=0, column=0, pady=2)

connect_btn = tk.Button(columns_frame, text="Connect", width=BUTTON_WIDTH, command=connect_device)
connect_btn.grid(row=1, column=0, padx=5, pady=2)

disconnect_btn = tk.Button(columns_frame, text="Disconnect", width=BUTTON_WIDTH, command=disconnect_device)
disconnect_btn.grid(row=2, column=0, padx=5, pady=2)

list_btn = tk.Button(columns_frame, text="List Devices", width=BUTTON_WIDTH, command=list_devices)
list_btn.grid(row=3, column=0, padx=5, pady=2)

select_btn = tk.Button(columns_frame, text="Select APK", width=BUTTON_WIDTH, command=select_apk)
select_btn.grid(row=4, column=0, padx=5, pady=2)

install_btn = tk.Button(columns_frame, text="Install APK", width=BUTTON_WIDTH, command=install_apk)
install_btn.grid(row=5, column=0, padx=5, pady=2)

connect_appium_btn = tk.Button(columns_frame, text="Connect Appium", width=BUTTON_WIDTH, command=connect_appium)
connect_appium_btn.grid(row=6, column=0, padx=5, pady=2)

# ============= COLUMN 2: PROD =============
prod_label = tk.Label(columns_frame, text="Prod Version", font=("Arial", 12, "bold"))
prod_label.grid(row=0, column=1, pady=2)

uninstall_freetv_prod_btn = tk.Button(columns_frame, text="Uninstall FreeTV Prod", width=BUTTON_WIDTH, command=uninstall_freetv_prod)
uninstall_freetv_prod_btn.grid(row=1, column=1, padx=5, pady=2)

launch_freetv_prod_btn = tk.Button(columns_frame, text="Launch FreeTV Prod", width=BUTTON_WIDTH, command=launch_freetv_prod)
launch_freetv_prod_btn.grid(row=2, column=1, padx=5, pady=2)

auto_connect_btn = tk.Button(columns_frame, text="Connect to autoconnect account", width=BUTTON_WIDTH, command=connect_to_account)
auto_connect_btn.grid(row=3, column=1, padx=5, pady=2)

# ============= COLUMN 3: UAT =============
uat_label = tk.Label(columns_frame, text="UAT Version", font=("Arial", 12, "bold"))
uat_label.grid(row=0, column=2, pady=2)

uninstall_freetv_uat_btn = tk.Button(columns_frame, text="Uninstall FreeTV UAT", width=BUTTON_WIDTH, command=uninstall_freetv_uat)
uninstall_freetv_uat_btn.grid(row=1, column=2, padx=5, pady=2)

launch_freetv_uat_btn = tk.Button(columns_frame, text="Launch FreeTV UAT", width=BUTTON_WIDTH, command=launch_freetv_uat)
launch_freetv_uat_btn.grid(row=2, column=2, padx=5, pady=2)

apk_label = tk.Label(root, textvariable=apk_path, fg="blue", wraplength=400)
apk_label.pack()

output_text = scrolledtext.ScrolledText(root, width=80, height=15)
output_text.pack(pady=5)

root.mainloop()
