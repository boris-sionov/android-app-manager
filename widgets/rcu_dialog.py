from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QSizePolicy
)
from PySide6.QtCore import Qt, QSize

from core.constants import RCU_KEYCODES, BUTTON_STYLE

# Labels to display on buttons
DISPLAY_LABELS = {
    # D-Pad
    "UP": "↑",
    "DOWN": "↓",
    "LEFT": "←",
    "RIGHT": "→",
    "OK": "●",            # or "⏎"

    # System
    "BACK": "↩",
    "HOME": "⌂",

    # Volume & Channel
    "VOLUME_UP": "＋",
    "VOLUME_DOWN": "－",
    "MUTE": "🔇",
    "CHANNEL_UP": "CH↑",
    "CHANNEL_DOWN": "CH↓",
}


class RCUDialog(QDialog):
    """
    Google/Android TV-like RCU layout (Back under LEFT, Home under RIGHT):

          ↑
      ←   ●   →
      ↩   ↓   ⌂

    ＋             CH↑
    －     🔇      CH↓
    """

    def __init__(self, log_func, adb, parent=None):
        super().__init__(parent)
        self.log = log_func
        self.adb = adb
        self.setWindowTitle("RCU Control")
        self._init_ui()
        # lock window to its content (prevents extra gaps)
        self.setFixedSize(self.sizeHint())

    # ---------- UI ----------

    def _init_ui(self) -> None:
        root = QVBoxLayout(self)
        root.setContentsMargins(10, 10, 10, 10)
        root.setSpacing(8)

        # Common helpers
        def circular_btn(name: str, size: QSize) -> QPushButton:
            """Round button with fixed size."""
            code = RCU_KEYCODES[name]
            text = DISPLAY_LABELS.get(name, name)
            b = QPushButton(text)
            b.setToolTip(name.replace("_", " ").title())
            radius = min(size.width(), size.height()) // 2
            b.setStyleSheet(
                BUTTON_STYLE +
                f"QPushButton {{ font-size: 18px; min-width: {size.width()}px; "
                f"max-width: {size.width()}px; min-height: {size.height()}px; "
                f"max-height: {size.height()}px; border-radius: {radius}px; }}"
            )
            b.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            b.clicked.connect(lambda _=False, n=name, k=code: self._send_key(n, k))
            return b

        def pill_btn(name: str, size: QSize) -> QPushButton:
            """Rounded-rect button (for VOLUME/CHANNEL)."""
            code = RCU_KEYCODES[name]
            text = DISPLAY_LABELS.get(name, name)
            b = QPushButton(text)
            b.setToolTip(name.replace("_", " ").title())
            radius = min(size.width(), size.height()) // 2  # pill-ish
            b.setStyleSheet(
                BUTTON_STYLE +
                f"QPushButton {{ font-size: 18px; min-width: {size.width()}px; "
                f"max-width: {size.width()}px; min-height: {size.height()}px; "
                f"max-height: {size.height()}px; border-radius: {radius}px; }}"
            )
            b.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            b.clicked.connect(lambda _=False, n=name, k=code: self._send_key(n, k))
            return b

        # Sizes
        dpad_size = QSize(52, 52)         # round D-pad & OK
        sys_size = QSize(48, 48)          # round Back/Home/Mute
        col_btn_size = QSize(56, 40)      # pill style for volume/channel

        # === D-Pad cluster (3x3 grid) with Back/Home on bottom corners ===
        dpad = QGridLayout()
        dpad.setHorizontalSpacing(6)
        dpad.setVerticalSpacing(6)

        # Row 0
        dpad.addWidget(circular_btn("UP", dpad_size),     0, 1, alignment=Qt.AlignmentFlag.AlignCenter)

        # Row 1
        dpad.addWidget(circular_btn("LEFT", dpad_size),   1, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        dpad.addWidget(circular_btn("OK", dpad_size),     1, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        dpad.addWidget(circular_btn("RIGHT", dpad_size),  1, 2, alignment=Qt.AlignmentFlag.AlignCenter)

        # Row 2 (Back under Left, Home under Right, Down in middle)
        dpad.addWidget(circular_btn("BACK", sys_size),    2, 0, alignment=Qt.AlignmentFlag.AlignCenter)
        dpad.addWidget(circular_btn("DOWN", dpad_size),   2, 1, alignment=Qt.AlignmentFlag.AlignCenter)
        dpad.addWidget(circular_btn("HOME", sys_size),    2, 2, alignment=Qt.AlignmentFlag.AlignCenter)

        root.addLayout(dpad)

        # === Bottom: Volume (left) | Mute (center) | Channel (right) ===
        bottom = QHBoxLayout()
        bottom.setContentsMargins(0, 0, 0, 0)
        bottom.setSpacing(24)

        # Volume column (left)
        vol_col = QVBoxLayout()
        vol_col.setSpacing(10)
        vol_col.addWidget(pill_btn("VOLUME_UP", col_btn_size), alignment=Qt.AlignmentFlag.AlignCenter)
        vol_col.addWidget(pill_btn("VOLUME_DOWN", col_btn_size), alignment=Qt.AlignmentFlag.AlignCenter)

        # Channel column (right)
        ch_col = QVBoxLayout()
        ch_col.setSpacing(10)
        ch_col.addWidget(pill_btn("CHANNEL_UP", col_btn_size), alignment=Qt.AlignmentFlag.AlignCenter)
        ch_col.addWidget(pill_btn("CHANNEL_DOWN", col_btn_size), alignment=Qt.AlignmentFlag.AlignCenter)

        bottom.addLayout(vol_col)
        bottom.addStretch(1)
        bottom.addWidget(circular_btn("MUTE", sys_size), alignment=Qt.AlignmentFlag.AlignCenter)
        bottom.addStretch(1)
        bottom.addLayout(ch_col)

        root.addLayout(bottom)

    # ---------- Send Keys ----------

    def _send_key(self, name: str, code: int) -> None:
        """Always send a normal keyevent."""
        try:
            out = self.adb.keyevent(code)
            self.log(f"RCU: {name} ({code}) → {out}")
        except Exception as e:
            self.log(f"RCU ERROR sending {name} ({code}): {e}", "ERROR")
