# 📱 Android QA Tool

A powerful PySide6 desktop tool for Android TV (ATV) **and** Android phones — built for QA engineers, automation testers, and developers to install APKs, control devices, collect logs, and speed up validation.

![screenshot](./assets/Android-qa-tool.png)

---

## ✨ Features

- 🚀 **ADB Management** – Connect via IP/USB, list devices, install/uninstall APKs, reboot
- 🧹 **App Data Controls** – One-click **Clear Data** (UAT / Prod) and **Kill App**
- 🎮 **RCU Dialog** – Send key events (Up/Down/Left/Right/OK/Back/Home, etc.) from a virtual remote
- 🤖 **Appium Server Control** – **Start / Kill Appium** from the UI (default `0.0.0.0:4723`)
- 🔁 **Env Helpers** – Streamline **UAT ↔ PROD** actions (install/launch/kill/connect)
- 🔎 **Utilities** – Get device IP, background app (HOME), log viewer with **Clear** & export
- 🖥️ **Multi-Device Support** – Target devices by IP/serial
- 🧩 **Clean UI** – Minimal PySide6 interface focused on daily QA tasks

---

## 🖼️ UI Preview

> Matches the current UI: two input fields at the top, **four** functional columns (**General / Prod Version / UAT Version / Appium Server**), a log panel, and a large red **Clear QA Tool Log** button.

```text
┌────────────────────────────────────────────────────────────────────────────────────────────┐
│ Enter IP:    [_____________________________________]   [ Connect to Device ] [ Disconnect ]│
│ Enter Phone: [_____________________________________]   [ Connect to Account ]              │
├────────────────────────────────────────────────────────────────────────────────────────────┤
│  General                 │   Prod Version               │   UAT Version         │ Appium Server │
│ ──────────────────────── │ ──────────────────────────── │ ───────────────────── │ ───────────── │
│ [ List Devices ]         │ [ Uninstall FreeTV Prod ]   │ [ Uninstall FreeTV ]  │ [ Start Appium ] │
│ [ Select APK ]           │ [ Launch FreeTV Prod   ]     │ [ Launch FreeTV UAT ] │ [ Kill Appium  ] │
│ [ Install APK ]          │ [ Clear Data (Prod)     ]    │ [ Clear Data (UAT) ]  │                 │
│ [ Reboot Device ]        │ [ Kill FreeTV App       ]    │                        │                 │
│ [ Get Device IP ]        │                              │                        │                 │
│ [ Go Background (HOME) ] │                              │                        │                 │
│ [ Open RCU Control ]     │                              │                        │                 │
├──────────────────────────────────────────── Log Output ─────────────────────────────────────┤
│                                                                                              │
│                                                                                              │
└──────────────────────────────────────────────────────────────────────────────────────────────┘
[                                     Clear QA Tool Log                                        ]
