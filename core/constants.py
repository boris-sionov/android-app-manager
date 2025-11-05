# --- Packages ---
FREETV_UAT_PACKAGE = "tv.freetv.androidtv.uat"
FREETV_PROD_PACKAGE = "tv.freetv.androidtv"

# --- Dial keypad mapping (for login) ---
KEYPAD_SUFFIX = {
    "0": "Zero", "1": "One", "2": "Two", "3": "Three", "4": "Four",
    "5": "Five", "6": "Six", "7": "Seven", "8": "Eight", "9": "Nine"
}

# --- RCU key mapping (Android TV) ---
# Arrows: UP=19, DOWN=20, LEFT=21, RIGHT=22
# Back=4, Home=3, OK=66 (ENTER; use 23 if you prefer DPAD_CENTER)
# Volume: UP=24, DOWN=25, MUTE=164
# Channels: UP=166, DOWN=167
RCU_KEYCODES = {
    "UP": 19,
    "DOWN": 20,
    "LEFT": 21,
    "RIGHT": 22,
    "OK": 66,
    "BACK": 4,
    "HOME": 3,

    "VOLUME_UP": 24,
    "MUTE": 164,
    "VOLUME_DOWN": 25,

    "CHANNEL_UP": 166,
    "CHANNEL_DOWN": 167,
}

# --- Grid positions (5 columns: 0..4) for the requested layout ---
#  row 0:  VOL+ (0)   ↑ (2)    CH+ (4)
#  row 1:  MUTE (0)  ←(1) ●(2) →(3)
#  row 2:  VOL- (0)  ↩(1) ↓(2) ⌂(3)    CH- (4)
RCU_POSITIONS = {
    "VOLUME_UP":   (0, 0),
    "UP":          (0, 2),
    "CHANNEL_UP":  (0, 4),

    "MUTE":        (1, 0),
    "LEFT":        (1, 1),
    "OK":          (1, 2),
    "RIGHT":       (1, 3),

    "VOLUME_DOWN": (2, 0),
    "BACK":        (2, 1),
    "DOWN":        (2, 2),
    "HOME":        (2, 3),
    "CHANNEL_DOWN":(2, 4),
}

# --- Shared button style ---
BUTTON_STYLE = """
QPushButton {
    background-color: #2196F3;
    color: white;
    padding: 10px 10px;  
    font-size: 14px;
    border-radius: 6px;
}
QPushButton:hover {
    background-color: #1976D2;
}
QPushButton:pressed {
    background-color: #0D47A1;
}
"""

# ---- Centralized defaults ----
APPIUM_HOST = "127.0.0.1"
APPIUM_PORT = 4723
LOG_DIR = "logs"
LOG_FILE = "android_manager.log"
LOG_PATH = f"{LOG_DIR}/{LOG_FILE}"

# ---- Login screen verification texts (Hebrew) ----
LOGIN_FIRST_TEXT  = "להצטרפות וקבלת חודש ניסיון בחינם"
LOGIN_SECOND_TEXT = "כניסה למנויים קיימים"
LOGIN_SCREEN_TEXTS = [LOGIN_FIRST_TEXT, LOGIN_SECOND_TEXT]
