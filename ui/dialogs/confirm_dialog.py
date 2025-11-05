from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
from PySide6.QtGui import QCursor


class ConfirmDialog(QDialog):
    @staticmethod
    def ask(parent, *, title: str, message: str) -> bool:
        dlg = ConfirmDialog(parent, title, message)
        return dlg.exec() == QDialog.DialogCode.Accepted

    def __init__(self, parent, title: str, message: str) -> None:
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setFixedSize(420, 260)

        self.setStyleSheet("""
            QDialog { background-color: #2E2E2E; border-radius: 8px; }
            QLabel { color: white; }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        title_label = QLabel("Are you sure?")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("QLabel { font-size: 18px; font-weight: bold; color: white; }")
        layout.addWidget(title_label)

        msg_label = QLabel(message)
        msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        msg_label.setWordWrap(True)
        msg_label.setMinimumHeight(80)
        msg_label.setStyleSheet("QLabel { font-size: 13px; color: #DDDDDD; }")
        layout.addWidget(msg_label)

        btn_row = QHBoxLayout()
        btn_row.setSpacing(40)
        btn_row.setAlignment(Qt.AlignmentFlag.AlignCenter)

        yes_btn = QPushButton("Yes")
        yes_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        yes_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px 30px;
                font-size: 14px;
                border-radius: 8px;
            }
            QPushButton:hover { background-color: #45A049; }
            QPushButton:pressed { background-color: #2E7D32; }
        """)

        no_btn = QPushButton("No")
        no_btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        no_btn.setStyleSheet("""
            QPushButton {
                background-color: #F44336;
                color: white;
                padding: 8px 30px;
                font-size: 14px;
                border-radius: 8px;
            }
            QPushButton:hover { background-color: #D32F2F; }
            QPushButton:pressed { background-color: #B71C1C; }
        """)

        btn_row.addWidget(no_btn)
        btn_row.addWidget(yes_btn)
        layout.addLayout(btn_row)

        yes_btn.clicked.connect(self.accept)
        no_btn.clicked.connect(self.reject)
