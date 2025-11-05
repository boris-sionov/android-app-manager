import logging
from logging.handlers import TimedRotatingFileHandler
import os

# === Constants ===
LOG_DIR = "logs"
LOG_FILE = "android_manager.log"

# Ensure log folder exists
os.makedirs(LOG_DIR, exist_ok=True)

# === Logger setup ===
logger = logging.getLogger("AndroidManager")
logger.setLevel(logging.DEBUG)

# === File handler (daily rotation) ===
file_handler = TimedRotatingFileHandler(
    filename=os.path.join(LOG_DIR, LOG_FILE),
    when="midnight",
    backupCount=7,
    encoding="utf-8"
)
file_handler.setLevel(logging.DEBUG)

# === Console handler ===
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# === Formatter ===
formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# === Attach handlers only once ===
if not logger.handlers:
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
