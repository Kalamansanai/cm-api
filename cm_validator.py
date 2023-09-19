import numpy as np
from cm_config import Logger
from startup import mongo
import time
from domain.detector import Detector


# TODO
def validate(detector: Detector, new_value):
    if new_value != None:
        return True
    else:
        return False
