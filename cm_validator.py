import numpy as np
from cm_config import Logger
from cm_models import Detector
from startup import mongo
import time


def validate(detector: Detector, new_value):
    X = []
    y = []
    for log in detector.logs:
        X.append(int(log.timestamp.timestamp() * 1000))
        y.append(log.value)

    if len(X) < 1:
        Logger.info("Validator - There is no data yet")
        return True

    if new_value < y[-1]:
        Logger.info("Validator - Value greater than previous")
        return False

    return True
