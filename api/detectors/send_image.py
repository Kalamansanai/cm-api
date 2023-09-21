from datetime import datetime
from flask import request
from domain.location import Location
from domain.detector import Detector
from domain.log import Log
from startup import app, mongo
from PIL import Image
import pandas as pd
import numpy as np
from bson.objectid import ObjectId
import cm_validator as V
from detector import _Detector
_detector = _Detector("library/plates.pt", "library/numbers.pt")
from api.api_utils import success_response, error_response
from api import login_required

#TODO: detector validation required
@app.route("/send_image/<detector_id>", methods=["POST"])
def send_image(detector_id):
    img_raw = request.files["image"]
    img = Image.open(img_raw)

    detector_raw = mongo.detectors.find_one({"detector_id": detector_id})
    if detector_raw is None:
        return error_response("/send_image", "detector is not found")
    detector = Detector(detector_raw)

    error = None

    log_data = _detector.detect(
        np.array(img), detector.detector_config.charNum, detector.detector_config.comaPosition, detector_id)

    is_valid = V.validate(detector, log_data)

    if is_valid:
        new_log = Log({"timestamp": datetime.now(), "value": log_data})
        detector.logs.append(new_log)
    else:
        return error_response("/set_image", "detected value is not valid")

    detector.img_path = f"library/images/{detector_id}.png"

    mongo.detectors.find_one_and_update(
        {"detector_id": detector_id},
        {"$set": detector.get_db()}
    )

    location_raw = mongo.locations.find_one(
        {"_id": ObjectId(detector.location_id)},
    )
    if(location_raw is None):
        return error_response("/send_image", "location is not found")

    location = Location(location_raw)

    new_value = (log_data - detector.logs[-1].value) * detector.detector_config.cost
    location.add_monthly_log(detector, new_value)

    return success_response("success") if error is None else error_response("/send_image", error)
