# Centralized stylesheet definitions for the PySide6 UI

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

DANGER_BUTTON_STYLE = """
QPushButton {
    background-color: #f44336;
    color: white;
    padding: 10px 20px;
    font-size: 14px;
    border-radius: 6px;
}
QPushButton:hover { background-color: #d32f2f; }
QPushButton:pressed { background-color: #b71c1c; }
"""

DIALOG_STYLE = """
QDialog {
    background-color: #2E2E2E;
    border-radius: 8px;
}
QLabel {
    color: white;
}
"""
