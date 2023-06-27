import logging

PRODUCTION = False

MONGO_URI = "mongodb+srv://dev:kiskacsa@cluster0.fb9cr7y.mongodb.net/?retryWrites=true&w=majority"
DB_NAME = "cm_prod" if PRODUCTION else "cm_dev"

IMAGE_PATH = "images"

DETECTOR_CONFIG = {
    "test": "test"
}

LOG_PATH = (
    ""
    if PRODUCTION
    else "api_log.log"
)

JWT_SECRET = "szialajosJNDSnjsdnjsnJNDSJNDJSnjsndjsnJSNDKJNSNDSJnd"
JWT_COOKIE_KEY = "cm-user-token"
SESSION_PERSISTANCE_TIME = 31536000  # 1 year max cookie age
SESSION_COOKIE_HTTPS_ONLY = False
SESSION_KEY_SALT = "6670c7a914efe3ed2d8b4c83660252aa6ec3df21e2fbcb296d1c07511670defa"

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
