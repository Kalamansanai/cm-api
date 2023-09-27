import logging
import os
from dotenv import dotenv_values

config = dotenv_values("library/.env")

MODE = config["MODE"]
APP_HOST = config["APP_HOST"]
APP_PORT = config["APP_PORT"]
MONGO_URI = config["MONGO_URI"] 

if MODE == "dev":
    DB_NAME = "test_1"
elif MODE == "prod":
    DB_NAME = "cm_prod"
elif MODE == "demo":
    DB_NAME = "cm_demo"
elif MODE == "test":
    DB_NAME = "cm_test"

        
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

IMAGE_PATH = config["IMAGE_PATH"]

DETECTOR_CONFIG = {
    "quality": 12,
    "resolution": 5,
    "flash_time": 500,
    "timeout": 10000
}

LOG_PATH = (
    "library/api_log.log"
)

JWT_SECRET = config["JWT_SECRET"]
JWT_COOKIE_KEY = "cm-user-token"
SESSION_PERSISTANCE_TIME = 1800 if MODE == "prod" else 30000000
SESSION_COOKIE_HTTPS_ONLY = False
SESSION_KEY_SALT = config["SESSION_KEY_SALT"]

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
        if MODE == "prod":
            print(msg)
        else:
            _logger.debug(msg)

    def info(msg: str):
        if MODE == "prod":
            print(msg)
        else:
            _logger.info(msg)

    def warning(msg: str):
        if MODE == "prod":
            print(msg)
        else:
            _logger.warning(msg)

    def error(msg: str):
        if MODE == "prod":
            print(msg)
        else:
            _logger.error(msg)


PLOT_COLOR = "hsl(101, 70%, 50%)"

TYPE_COLORS = {
    "electricity": "hsl(104, 70%, 50%)",
    "water": "hsl(229, 70%, 50%)",
    "gas": "hsl(344, 70%, 50%)"
}
