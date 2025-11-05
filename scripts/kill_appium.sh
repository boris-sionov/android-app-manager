#!/usr/bin/env bash
set -euo pipefail

# Kill all running Appium server processes
# macOS/Linux compatible.

if pgrep -f "appium" >/dev/null 2>&1; then
  echo "Killing running Appium server(s)..."
  pkill -f "appium"
  sleep 1
  echo "Appium server(s) terminated."
else
  echo "No active Appium server process found."
fi
