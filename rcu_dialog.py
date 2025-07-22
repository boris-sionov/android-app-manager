from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QGridLayout, QPushButton
from PySide6.QtCore import Qt
from constants import RCU_KEYCODES, RCU_POSITIONS, BUTTON_STYLE


class RCUDialog(QDialog):
    def __init__(self, log_func, adb, parent=None):
        super().__init__(parent)
        self.log = log_func
        self.adb = adb
        self.setWindowTitle("RCU Control")
        self.setFixedSize(300, 300)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("<b>Remote Control Unit (RCU)</b>")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        grid = QGridLayout()
        for label, key in RCU_KEYCODES.items():
            btn = QPushButton(label)
            btn.setStyleSheet(BUTTON_STYLE)
            btn.clicked.connect(lambda _, k=key: self.send_key(k))
            row, col = RCU_POSITIONS[label]
            grid.addWidget(btn, row, col)

        layout.addLayout(grid)

    def send_key(self, code):
        output = self.adb.keyevent(code)
        self.log(f"Sent keyevent {code}: {output}")
