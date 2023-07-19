import logging
import os

PRODUCTION = False

APP_HOST = "0.0.0.0"
APP_PORT = "3000"

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = "cm_prod" if PRODUCTION else "cm_dev"

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

IMAGE_PATH = "images"

DETECTOR_CONFIG = {
    "quality": 12,
    "resolution": 9,
    "flash_time": 500,
    "timeout": 10000
}

LOG_PATH = (
    ""
    if PRODUCTION
    else "api_log.log"
)

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_COOKIE_KEY = "cm-user-token"
SESSION_PERSISTANCE_TIME = 31536000  # 1 year max cookie age
SESSION_COOKIE_HTTPS_ONLY = False
SESSION_KEY_SALT = os.getenv("SESSION_KEY_SALT")

_logger = logging.Logger("cm-logger", level=logging.DEBUG)
_fh = logging.FileHandler(LOG_PATH)
_fh.setFormatter(
    logging.Formatter(
        fmt="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
)
_fh.setLevel(logging.INFO)
_logger.addHandler(_fh)


class Logger:
    def debug(msg: str):
        _logger.debug(msg)

    def info(msg: str):
        _logger.info(msg)

    def warning(msg: str):
        _logger.warning(msg)

    def error(msg: str):
        _logger.error(msg)


PLOT_COLOR = "hsl(101, 70%, 50%)"
