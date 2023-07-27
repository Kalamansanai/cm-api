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

detector = Detector("library/plates.pt", "library/plates.pt")


@app.route("/send_image/<detector_id>", methods=["POST"])
def send_image(detector_id):
    img = request.files["image"]
    img = Image.open(img)

    user = mongo.users.find_one(
        {"detectors.detector_id": detector_id}
    )

    detectors = user["detectors"]
    for det in detectors:
        if det["detector_id"] == detector_id:
            config = det["detector_config"]

    number_length, coma_position = config["charNum"], config["comaPosition"]

    log_data = detector.detect(np.array(img), number_length, coma_position)

    is_valid = V.validate(detector_id, round(time.time() * 1000), log_data)

    if log_data == None and is_valid:
        return success_response("send_image", "success_none")

    log = {"timestamp": datetime.now(), "value": int(log_data)}
    mongo.logs.find_one_and_update(
        {"detector_id": detector_id},
        {"$push": {"logs": log}}
    )

    return success_response("/send_image", "success")


@app.route("/add_detector", methods=["POST"])
def add_detector_to_user():
    user_data = cm_utils.auth_token()
    if user_data is None:
        return error_response("/add_detector", "no user signed in")

    (detector_id, type, detector_name, cost) = cm_utils.validate_json(
        ["detector_id", "type", "detector_name", "cost"]
    )

    if id_uniqueness(user_data["email"], detector_id):
        return error_response("/add_detector", "A detector is already registered with this id !")

    mongo.logs.insert_one({
        "detector_id": detector_id,
        "logs": []
    }).inserted_id

    new_detector = {
        "detector_id": detector_id,
        "detector_name": detector_name,
        "detector_config": {},
        "type": type,
        "state": "init",
        "cost": cost
    }

    mongo.users.update_one(
        {"_id": ObjectId(user_data["id"])},
        {'$push': {"detectors": new_detector}}
    )

    return success_response("/add_detector", "detector added successfully")


@app.route("/get_detector_config/<detector_id>")
def get_detector_config(detector_id):
    user = mongo.users.find_one(
        {"detectors.detector_id": detector_id}
    )

    if user is None:
        return error_response("/get_detector_config", "detector has not added to any user yet !")

    detectors = user["detectors"]
    for det in detectors:
        if det["detector_id"] == detector_id:
            config = det["detector_config"]

    config.update(DETECTOR_CONFIG)

    return config


@app.route("/set_detector_config/<detector_id>", methods=["POST"])
def set_detector_config(detector_id):
    user_data = cm_utils.auth_token()
    if user_data is None:
        return error_response("/add_detector", "no user signed in")

    (new_config,) = cm_utils.validate_json(["new_config"])

    mongo.users.update_one(
        {"detectors.detector_id": detector_id},
        {"$set": {"detectors.$.detector_config": new_config}}
    )

    return success_response("/set_detector_config", "config updates successfully")


@app.route("/detector/<detector_id>", methods=["DELETE"])
def delete_detector(detector_id):
    user_data = cm_utils.auth_token()
    if user_data is None:
        return error_response("/add_detector", "no user signed in")

    mongo.logs.delete_one({"detector_id": detector_id})

    mongo.users.update_one(
        {"_id": ObjectId(user_data["id"])},
        {"$pull": {"detectors": {"detector_id": detector_id}}})

    return success_response("/delete_detector", "detector deleted successfully")


@app.route("/detector/<detector_id>/export")
def export_detector_log(detector_id):
    logs = mongo.logs.find_one({"detector_id": detector_id})

    logs_table = pd.DataFrame.from_records(logs["logs"])

    with tempfile.TemporaryDirectory() as tmpdirname:
        tmppath = os.path.join(tmpdirname, f"{str(datetime.now())}.csv")
        with open(tmppath, 'w') as tmpfile:
            logs_table.to_csv(tmpfile.name, index=False)
            mimetype = "text/csv"

        return send_file(tmppath, mimetype=mimetype, as_attachment=True)


@app.route("/detector/<detector_id>/check_state")
def detector_check_state(detector_id):
    changed = check_and_update_detectors_state(detector_id)
    return success_response("/detector/check_state", changed)