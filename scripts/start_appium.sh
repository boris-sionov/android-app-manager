#!/usr/bin/env bash
set -euo pipefail

# Start Appium server if not already running.
# macOS/Linux compatible.

APPIUM_BIN="${APPIUM_BIN:-appium}"
HOST="${APPIUM_HOST:-127.0.0.1}"
PORT="${APPIUM_PORT:-4723}"

# Check if appium binary is available
if ! command -v "$APPIUM_BIN" >/dev/null 2>&1; then
  echo "Error: '$APPIUM_BIN' not found in PATH. Install Appium or set APPIUM_BIN."
  exit 1
fi

# If already running, exit gracefully
if curl -s "http://${HOST}:${PORT}/status" >/dev/null 2>&1; then
  echo "Appium already running at ${HOST}:${PORT}"
  exit 0
fi

# Start in background, silencing output
nohup "$APPIUM_BIN" --address "$HOST" --port "$PORT" >/dev/null 2>&1 &
sleep 1

# Verify it started
if curl -s "http://${HOST}:${PORT}/status" >/dev/null 2>&1; then
  echo "Appium started at ${HOST}:${PORT}"
  exit 0
else
  echo "Failed to start Appium at ${HOST}:${PORT}"
  exit 1
fi
