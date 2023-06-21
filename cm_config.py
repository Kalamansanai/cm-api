import logging

PRODUCTION = False

MONGO_URI = "mongodb+srv://dev:kiskacsa@cluster0.fb9cr7y.mongodb.net/?retryWrites=true&w=majority"

IMAGE_PATH = "images"

DETECTOR_CONFIG = {
    "test" : "test"
}

LOG_PATH = (
    ""
    if PRODUCTION
    else "api_log.log" 
)

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