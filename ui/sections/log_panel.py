from __future__ import annotations

from datetime import datetime
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton

from core.constants import LOG_PATH


class LogPanel(QWidget):
    """
    Encapsulates the log output UI:
      - Title label
      - Read-only QTextEdit (auto-scroll when already at bottom)
      - 'Clear QA Tool Log' button that clears the file and the UI

    Public API:
      - append_line(text: str)
      - clear()
    """

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        self.output = QTextEdit(self)
        self.output.setReadOnly(True)

        root = QVBoxLayout(self)
        root.setAlignment(Qt.AlignmentFlag.AlignTop)  # <- explicit enum scope to satisfy PyCharm
        root.setContentsMargins(0, 8, 0, 0)
        root.setSpacing(6)

        root.addWidget(QLabel("<b>Log Output</b>"))
        root.addWidget(self.output)

        btn_clear = QPushButton("Clear QA Tool Log", self)
        btn_clear.setStyleSheet(
            """
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
        )
        btn_clear.clicked.connect(self.clear)
        root.addWidget(btn_clear)

    def append_line(self, text: str) -> None:
        """
        Append a line to the log box. If the scrollbar is already at the bottom,
        keep it pinned after appending.
        """
        scrollbar = self.output.verticalScrollBar()
        at_bottom = scrollbar.value() == scrollbar.maximum()
        self.output.append(text)
        if at_bottom:
            scrollbar.setValue(scrollbar.maximum())

    def clear(self) -> None:
        """
        Clear the on-disk log file (LOG_PATH) and the UI text area.
        """
        try:
            log_path = Path(LOG_PATH)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            log_path.write_text("", encoding="utf-8")
        except Exception as e:
            self.output.clear()
            self.append_line(
                f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [ERROR] Error clearing logs: {e}"
            )
            return

        self.output.clear()
        self.append_line(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [INFO] Logs cleared.")
