import numpy as np
from cm_config import Logger
from cm_models import Detector
from startup import mongo
import time


# TODO
def validate(detector: Detector, new_value):
    if new_value != None:
        if len(detector.logs) > 0 and new_value < detector.logs[-1]:
            return False 
        return True
    else:
        return False
