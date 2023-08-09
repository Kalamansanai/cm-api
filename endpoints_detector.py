from datetime import datetime

from flask import request, send_file
from startup import app, mongo
import time

from PIL import Image
import tempfile
import os
import pandas as pd

from cm_config import DETECTOR_CONFIG
from cm_types import success_response, error_response
import cm_utils
from detector import Detector
from cm_detector import check_and_update_detectors_state, id_uniqueness

from datetime import datetime
import numpy as np
from bson.objectid import ObjectId

import cm_validator as V

_detector = Detector("library/plates.pt", "library/plates.pt")


@app.route("/send_image/<detector_id>", methods=["POST"])
def send_image(detector_id):
    img = request.files["image"]
    img = Image.open(img)

    detector = mongo.detectors.find_one({"detector_id": detector_id})

    config = detector["detector_config"]
    number_length, coma_position = config["charNum"], config["comaPosition"]

    log_data = _detector.detect(np.array(img), number_length, coma_position)

    if log_data == None:
        return success_response("send_image", "not detected a valid number")

    is_valid = V.validate(detector, log_data)

    if not is_valid:
        return success_response("send_image", "value is not valid")

    float_value = int(log_data) / (10 ** coma_position)
    new_log = {"timestamp": datetime.now(), "value": float_value}

    detector["logs"].append(new_log)

    mongo.detectors.find_one_and_update(
        {"detector_id": detector_id},
        {"$set": detector}
    )

    return success_response("/send_image", "success")


@app.route("/add_detector", methods=["POST"])
def add_detector_to_user():
    user_data = cm_utils.auth_token()
    if user_data is None:
        return error_response("/add_detector", "no user signed in")

    (detector_id, type, detector_name) = cm_utils.validate_json(
        ["detector_id", "type", "detector_name"]
    )

    if id_uniqueness(user_data["id"], detector_id):
        return error_response("/add_detector", "A detector is already registered with this id !")

    new_detector = {
        "detector_id": detector_id,
        "user_id": user_data["id"],
        "detector_name": detector_name,
        "detector_config": {
            "delay": 86400000,  # a day
            "cost": 1
        },
        "type": type,
        "state": "init",
        "logs": []
    }

    id = mongo.detectors.insert_one(new_detector).inserted_id
    if id is None:
        return error_response("add_detector", "detector not added because of some problem")

    return success_response("/add_detector", "detector added successfully")


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

    mongo.detectors.delete_one({"detector_id": detector_id})

    return success_response("/delete_detector", "detector deleted successfully")


@app.route("/detector/<detector_id>/export")
def export_detector_log(detector_id):
    detector = mongo.detectors.find_one({"detector_id": detector_id})

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
