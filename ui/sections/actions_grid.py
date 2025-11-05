from __future__ import annotations

from PySide6.QtCore import Qt, Signal, SignalInstance
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton

from core.constants import BUTTON_STYLE


class ActionsGrid(QWidget):
    # General
    sigListDevices = Signal()
    sigSelectApk = Signal()
    sigInstallApk = Signal()
    sigRebootDevice = Signal()
    sigGetDeviceIp = Signal()
    sigOpenRcu = Signal()
    sigGoHome = Signal()
    # PROD
    sigUninstallProd = Signal()
    sigLaunchProd = Signal()
    sigConnectAccountProd = Signal()
    sigClearDataProd = Signal()
    sigKillProd = Signal()
    # UAT
    sigUninstallUat = Signal()
    sigLaunchUat = Signal()
    sigClearDataUat = Signal()
    # Appium
    sigStartAppium = Signal()
    sigKillAppium = Signal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self._build_ui()

    # -------------------- UI -------------------- #
    def _build_ui(self) -> None:
        grid = QGridLayout(self)
        grid.setSpacing(10)
        grid.setContentsMargins(0, 10, 0, 10)

        # ==== GENERAL COLUMN ====
        grid.addWidget(QLabel("<b>General</b>"), 0, 0)
        grid.addWidget(self._btn("List Devices", self.sigListDevices), 1, 0)
        grid.addWidget(self._btn("Select APK", self.sigSelectApk), 2, 0)
        grid.addWidget(self._btn("Install APK", self.sigInstallApk), 3, 0)
        grid.addWidget(self._btn("Reboot Device", self.sigRebootDevice), 4, 0)
        grid.addWidget(self._btn("Get Device IP", self.sigGetDeviceIp), 5, 0)
        grid.addWidget(self._btn("Go Background (HOME)", self.sigGoHome), 6, 0)
        grid.addWidget(self._btn("Open RCU Control", self.sigOpenRcu), 7, 0)

        # ==== PROD COLUMN ====
        grid.addWidget(QLabel("<b>Prod Version</b>"), 0, 1)
        grid.addWidget(self._btn("Uninstall FreeTV Prod", self.sigUninstallProd), 1, 1)
        grid.addWidget(self._btn("Launch FreeTV Prod", self.sigLaunchProd), 2, 1)
        grid.addWidget(self._btn("Clear Data (Prod)", self.sigClearDataProd), 3, 1)
        grid.addWidget(self._btn("Kill FreeTV App", self.sigKillProd), 4, 1)

        # ==== UAT COLUMN ====
        grid.addWidget(QLabel("<b>UAT Version</b>"), 0, 2)
        grid.addWidget(self._btn("Uninstall FreeTV UAT", self.sigUninstallUat), 1, 2)
        grid.addWidget(self._btn("Launch FreeTV UAT", self.sigLaunchUat), 2, 2)
        grid.addWidget(self._btn("Clear Data (UAT)", self.sigClearDataUat), 3, 2)

        # ==== APPIUM COLUMN ====
        grid.addWidget(QLabel("<b>Appium Server</b>"), 0, 3)
        grid.addWidget(self._btn("Start Appium Server", self.sigStartAppium), 1, 3)
        grid.addWidget(self._btn("Kill Appium Server", self.sigKillAppium), 2, 3)

    # -------------------- Helper -------------------- #
    def _btn(self, text: str, signal_obj: SignalInstance) -> QPushButton:
        btn = QPushButton(text)
        btn.setFixedWidth(250)
        btn.setFixedHeight(35)
        btn.setStyleSheet(BUTTON_STYLE)
        # Use the QtCore enum path PyCharm likes:
        btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        btn.clicked.connect(signal_obj.emit)
        return btn
