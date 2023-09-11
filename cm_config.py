import logging
import os

MODE = os.getenv("MODE")

APP_HOST: str | None = os.getenv("APP_HOST")
APP_PORT: str | None = os.getenv("APP_PORT")

MONGO_URI = os.getenv("MONGO_URI")

if MODE == "dev":
    DB_NAME = "cm_dev"
elif MODE == "prod":
    DB_NAME = "cm_prod"
elif MODE == "demo":
    DB_NAME = "cm_demo"

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

IMAGE_PATH = os.getenv("IMAGE_PATH")

DETECTOR_CONFIG = {
    "quality": 12,
    "resolution": 5,
    "flash_time": 500,
    "timeout": 10000
}

LOG_PATH = (
    "library/api_log.log"
)

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_COOKIE_KEY = "cm-user-token"
SESSION_PERSISTANCE_TIME = 1800  # 30 minutes
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

TYPE_COLORS = {
    "electricity": "hsl(104, 70%, 50%)",
    "water": "hsl(229, 70%, 50%)",
    "gas": "hsl(344, 70%, 50%)"
}
