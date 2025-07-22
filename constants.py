FREETV_UAT_PACKAGE = "tv.freetv.androidtv.uat"
FREETV_PROD_PACKAGE = "tv.freetv.androidtv"

KEYPAD_SUFFIX = {
    "0": "Zero", "1": "One", "2": "Two", "3": "Three", "4": "Four",
    "5": "Five", "6": "Six", "7": "Seven", "8": "Eight", "9": "Nine"
}

RCU_KEYCODES = {
    "UP": 19, "DOWN": 20, "LEFT": 21, "RIGHT": 22, "BACK": 4, "OK": 66
}

RCU_POSITIONS = {
    "UP": (0, 1), "LEFT": (1, 0), "OK": (1, 1),
    "RIGHT": (1, 2), "DOWN": (2, 1), "BACK": (3, 1)
}

BUTTON_STYLE = """
QPushButton {
    background-color: #2196F3;
    color: white;
    padding: 10px 20px;
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
