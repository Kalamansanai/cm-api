from datetime import datetime

from flask import request, send_file
from cm_models import Detector, Location, Log
from startup import app, mongo

from PIL import Image
import tempfile
import os
import pandas as pd

from cm_config import DETECTOR_CONFIG, IMAGE_PATH, MODE
from cm_types import success_response, error_response
import cm_utils
from detector import _Detector
from cm_detector import check_and_update_detectors_state, id_uniqueness, detector_valid

import numpy as np
import json
from bson.objectid import ObjectId

import cm_validator as V

# TODO: refactor this
_detector = _Detector("library/plates.pt", "library/numbers.pt")


@app.route("/send_image/<detector_id>", methods=["POST"])
def send_image(detector_id):
    img_raw = request.files["image"]
    img = Image.open(img_raw)

    img_path = f"{IMAGE_PATH}/test.png"
    img.save(img_path)

    detector_raw = mongo.detectors.find_one({"detector_id": detector_id})
    if detector_raw is None:
        return error_response("/send_image", "detector is not found")
    detector = Detector(detector_raw)

    error = None

    log_data = _detector.detect(
        np.array(img), detector.detector_config.charNum, detector.detector_config.comaPosition)

    is_valid = V.validate(detector, log_data)

    if is_valid:
        new_log = Log({"timestamp": datetime.now(), "value": log_data})
        detector.logs.append(new_log)
    else:
        return error_response("/set_image", "detected value is not valid")

    detector.img_path = img_path

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

    return success_response("/send_image", "success") if error is None else error_response("/send_image", error)


@app.route("/add_detector", methods=["POST"])
def add_detector_to_user():
    user_data = cm_utils.auth_token()
    if user_data is None:
        return error_response("/add_detector", "no user signed in")

    (location_id, detector_id, type, detector_name) = cm_utils.validate_json(
        ["location_id", "detector_id", "type", "detector_name"]
    )


    if MODE == "prod" and not detector_valid(detector_id):
        return error_response("/add_detector", "This detector ID is not valid.")

    if id_uniqueness(location_id, detector_id):
        return error_response("/add_detector", "A detector is already registered with this id !")

    new_detector = {
        "detector_id": detector_id,
        "location_id": location_id,
        "detector_name": detector_name,
        "detector_config": {
            "delay": 86400000,  # a day
            "cost": 1,
            "flash": 0
        },
        "type": type,
        "state": "init",
        "logs": [],
        "img_path": ""
    }

    detector_id = mongo.detectors.insert_one(new_detector).inserted_id
    if detector_id is None:
        return error_response("add_detector", "detector not added because of some problem")

    new_detector["_id"] = detector_id
    mongo.locations.find_one_and_update(
        {"_id": ObjectId(location_id)},
        {"$push": {"detectors": new_detector}}
    )

    return success_response("/add_detector", str(detector_id))


@app.route("/get_detector_config/<detector_id>")
def get_detector_config(detector_id):
    detector = mongo.detectors.find_one(
        {"detector_id": detector_id}
    )

    if detector is None:
        return error_response("/get_detector_config", "detector has not added to any user yet !")

    config = detector["detector_config"]
    config.update(DETECTOR_CONFIG)

    return config


@app.route("/set_detector_config/<detector_id>", methods=["POST"])
def set_detector_config(detector_id):
    user_data = cm_utils.auth_token()
    if user_data is None:
        return error_response("/add_detector", "no user signed in")

    (new_config,) = cm_utils.validate_json(["new_config"])

    mongo.detectors.update_one(
        {"detector_id": detector_id},
        {"$set": {"detector_config": new_config}}
    )

    return success_response("/set_detector_config", "config updates successfully")


@app.route("/detector/<detector_id>", methods=["DELETE"])
def delete_detector(detector_id):
    user_data = cm_utils.auth_token()
    if user_data is None:
        return error_response("/add_detector", "no user signed in")

    mongo.detectors.delete_one({"_id": ObjectId(detector_id)})

    mongo.locations.find_one_and_update(
        {"user_id": ObjectId(user_data["id"])},
        {"$pull": {"detectors": {"_id": ObjectId(detector_id)}}}
    )

    return success_response("/delete_detector", "detector deleted successfully")


@app.route("/detector/<detector_id>/export")
def export_detector_log(detector_id):
    detector = mongo.detectors.find_one({"_id": ObjectId(detector_id)})

    logs_table = pd.DataFrame.from_records(detector["logs"])

    with tempfile.TemporaryDirectory() as tmpdirname:
        tmppath = os.path.join(tmpdirname, f"{str(datetime.now())}.csv")
        with open(tmppath, 'w') as tmpfile:
            logs_table.to_csv(tmpfile.name, index=False)
            mimetype = "text/csv"

        return send_file(tmppath, mimetype=mimetype, as_attachment=True)


@app.route("/detector/<detector_id>/check_state")
def detector_check_state(detector_id):
    detector = mongo.detectors.find_one({"detector_id": detector_id})
    changed = check_and_update_detectors_state(detector)
    return success_response("/detector/check_state", changed)


@app.route("/get_all_detectors", methods=["GET"])
def get_all_detectors():
    user_data = cm_utils.auth_token()  
    if user_data is None:
        return error_response("/get_all_detectors", "no user signed in")
    
    user_id = user_data["id"]  
    
    location = mongo.locations.find_one({"user_id": ObjectId(user_id)})
    
    if location is None:
        return error_response("/get_all_detectors", "No location found for the user.")
    
    detectors = location.get("detectors", [])
    return success_response("/get_all_detectors", detectors)
