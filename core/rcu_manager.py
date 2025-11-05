from __future__ import annotations

from typing import Iterable, Union

from core.constants import RCU_KEYCODES
from core.adb_manager import AdbManager

KeyName = Union[str, int]


class RcuManager:
    """
    Thin helper over ADB for Android TV remote-like actions.

    - Accepts either key *names* (e.g., "UP", "DOWN", "LEFT", "RIGHT", "OK", "BACK", "HOME")
      or raw Android keycodes (ints).
    - Provides small convenience wrappers for common actions and sequences.
    """

    def __init__(self, adb: AdbManager, log_func):
        self.adb = adb
        self.log = log_func

    # ---------- Core ----------

    def _resolve_code(self, key: KeyName) -> int:
        """Translate a key name or return an int keycode as-is. Raises on unknown name."""
        if isinstance(key, int):
            return key
        name = str(key).upper().strip()
        if name in RCU_KEYCODES:
            return RCU_KEYCODES[name]
        raise ValueError(f"Unknown RCU key name: {key}")

    def press(self, key: KeyName, times: int = 1, device_ip: str | None = None) -> None:
        """Press a key N times."""
        code = self._resolve_code(key)
        times = max(1, int(times))
        for _ in range(times):
            out = self.adb.keyevent(code, device_ip=device_ip)
            self.log(f"RCU press {key} ({code}) → {out}")

    def press_sequence(self, keys: Iterable[KeyName], device_ip: str | None = None) -> None:
        """Press a series of keys in order."""
        for k in keys:
            self.press(k, device_ip=device_ip)

    # ---------- Convenience ----------

    def up(self, times: int = 1, device_ip: str | None = None) -> None:
        self.press("UP", times, device_ip)

    def down(self, times: int = 1, device_ip: str | None = None) -> None:
        self.press("DOWN", times, device_ip)

    def left(self, times: int = 1, device_ip: str | None = None) -> None:
        self.press("LEFT", times, device_ip)

    def right(self, times: int = 1, device_ip: str | None = None) -> None:
        self.press("RIGHT", times, device_ip)

    def ok(self, times: int = 1, device_ip: str | None = None) -> None:
        self.press("OK", times, device_ip)

    def back(self, times: int = 1, device_ip: str | None = None) -> None:
        self.press("BACK", times, device_ip)

    def home(self, times: int = 1, device_ip: str | None = None) -> None:
        self.press("HOME", times, device_ip)

    def recents(self, times: int = 1, device_ip: str | None = None) -> None:
        """Open App Switcher / Recents (KEYCODE_APP_SWITCH = 187) if defined in constants; otherwise use raw code."""
        if "RECENTS" in RCU_KEYCODES:
            self.press("RECENTS", times, device_ip)
        else:
            self.press(187, times, device_ip)

    # ---------- Higher-level flows ----------

    def focus_and_confirm_left_option(self, device_ip: str | None = None) -> None:
        """Move focus LEFT once, then OK."""
        self.left(1, device_ip=device_ip)
        self.ok(1, device_ip=device_ip)

    def confirm_with_down_then_ok(self, downs: int = 4, device_ip: str | None = None) -> None:
        """
        Navigate DOWN N times and then press OK.
        Default used by the login flow: DOWN x4, then OK.
        """
        self.down(downs, device_ip=device_ip)
        self.ok(1, device_ip=device_ip)
