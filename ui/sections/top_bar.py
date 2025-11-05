from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QSizePolicy
from PySide6.QtGui import QCursor

from core.constants import BUTTON_STYLE


class TopBar(QWidget):
    sigConnectDevice = Signal()
    sigDisconnectDevice = Signal()
    sigConnectAccount = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.ip_entry = QLineEdit(self)
        self.phone_entry = QLineEdit(self)
        self._build_ui()

    def _build_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setAlignment(Qt.AlignmentFlag.AlignTop)
        root.setContentsMargins(0, 0, 0, 4)
        root.setSpacing(10)

        row_height = 35
        top_btn_width = 200

        root.addWidget(QLabel("Enter IP:"))
        ip_row = QHBoxLayout()
        ip_row.setAlignment(Qt.AlignmentFlag.AlignLeft)
        ip_row.setSpacing(12)

        self._style_lineedit(self.ip_entry, "e.g., 192.168.1.25", width=260, height=row_height)
        ip_row.addWidget(self.ip_entry)

        btn_connect = QPushButton("Connect to Device")
        self._style_button(btn_connect, width=top_btn_width, height=row_height)
        btn_connect.clicked.connect(self.sigConnectDevice.emit)
        ip_row.addWidget(btn_connect)

        btn_disconnect = QPushButton("Disconnect")
        self._style_button(btn_disconnect, width=top_btn_width, height=row_height)
        btn_disconnect.clicked.connect(self.sigDisconnectDevice.emit)
        ip_row.addWidget(btn_disconnect)
        root.addLayout(ip_row)

        root.addWidget(QLabel("Enter Phone:"))
        phone_row = QHBoxLayout()
        phone_row.setAlignment(Qt.AlignmentFlag.AlignLeft)
        phone_row.setSpacing(12)

        self._style_lineedit(self.phone_entry, "e.g., 0501234567", width=260, height=row_height)
        phone_row.addWidget(self.phone_entry)

        btn_connect_acc = QPushButton("Connect to Account")
        self._style_button(btn_connect_acc, width=top_btn_width, height=row_height)
        btn_connect_acc.clicked.connect(self.sigConnectAccount.emit)
        phone_row.addWidget(btn_connect_acc)
        root.addLayout(phone_row)

    @staticmethod
    def _style_lineedit(le: QLineEdit, placeholder: str, *, width: int, height: int) -> None:
        le.setPlaceholderText(placeholder)
        le.setFixedWidth(width)
        le.setFixedHeight(height)
        le.setStyleSheet("""
            QLineEdit {
                background-color: #2b2b2b;
                color: white;
                border: none;
                padding: 8px 12px;
                font-size: 13px;
                border-radius: 6px;
            }
        """)

    @staticmethod
    def _style_button(btn: QPushButton, *, width: int, height: int) -> None:
        btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn.setStyleSheet(BUTTON_STYLE)
        btn.setMinimumWidth(width)
        btn.setMaximumWidth(width)
        btn.setMinimumHeight(height)
        btn.setMaximumHeight(height)
        btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

    def current_ip(self) -> str:
        return self.ip_entry.text().strip()

    def set_ip(self, ip: str) -> None:
        self.ip_entry.setText(ip or "")

    def current_phone(self) -> str:
        return self.phone_entry.text().strip()
