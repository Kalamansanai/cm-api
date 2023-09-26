from datetime import datetime
from flask import request
from domain.detector_image import DetectorImage
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
from api import detector_id_validation_required

#TODO: detector validation required
@app.route("/send_image/<detector_id>", methods=["POST"])
@detector_id_validation_required
def send_image(detector_id):
    img_raw = request.files["image"]
    img = Image.open(img_raw)

    detector_raw = mongo.detectors.find_one({"detector_id": detector_id})
    if detector_raw is None:
        return error_response("detector is not found")
    detector = Detector(detector_raw)

    error = None

    log_data = _detector.detect(
        np.array(img), detector.detector_config.char_num, detector.detector_config.coma_position, detector_id)

    is_valid = V.validate(detector, log_data)

    if is_valid:
        new_log = Log({"location_id": detector.location_id, "detector_id": detector_id, "type": detector.type, "timestamp": datetime.now(), "value": log_data})
        mongo.logs.insert_one(new_log.get_json())
        # detector.logs.append(new_log)
    else:
        return error_response("detected value is not valid")

    img_path = f"library/images/{detector_id}.png"

    mongo.images.insert_one({
            "detector_id": detector_id,
            "img_path":img_path
        })

    mongo.detectors.find_one_and_update(
        {"detector_id": detector_id},
        {"$set": detector.get_db()}
    )

    # location_raw = mongo.locations.find_one(
    #     {"_id": ObjectId(detector.location_id)},
    # )
    # if(location_raw is None):
    #     return error_response("location is not found")
    #
    # location = Location(location_raw)
    #
    # new_value = (log_data - detector.logs[-1].value) * detector.detector_config.cost
    # location.add_monthly_log(detector, new_value)

    return success_response("success") if error is None else error_response(error)
