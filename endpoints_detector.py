from datetime import datetime

from flask import request, send_file
from startup import app, mongo

from PIL import Image
import tempfile
import os
import pandas as pd

from cm_config import IMAGE_PATH, DETECTOR_CONFIG, Logger
from cm_types import success_response, error_response
import cm_utils
import random
from detector import Detector
from google_ocr import detect_text
from cm_detector import id_uniqueness, check_state

from datetime import datetime
import numpy as np


detector = Detector("library/plates.pt", "library/plates.pt")


def generate_mock_data():
    return {"timestamp": datetime.now().timestamp(), "value": random.random(0, 10)}


@app.route("/send_image/<detector_id>", methods=["POST"])
def send_image(detector_id):
    try:
        img = request.files["image"]
        img = Image.open(img)

        log_data = detector.detect(np.array(img), 8, 3)

        if log_data == None:
            return success_response("send_image", "success_none")

        log = {"timestamp": datetime.now().timestamp(), "value": int(log_data)}
        mongo.logs.find_one_and_update(
            {"detector_id": detector_id},
            {"$push": {"logs": log}}
        )

        return success_response("/send_image", "success")
    except BaseException as err:
        return error_response("/send_image", f"Unexpected {err=}, {type(err)=}")


@app.route("/set_config")
def set_config():
    try:
        return success_response("/set_config", "success")
    except BaseException as err:
        return error_response("/set_config", f"Unexpected {err=}, {type(err)=}")


@app.route("/add_detector", methods=["POST"])
def add_detector_to_user():
    try:
        user_data = cm_utils.auth_token()
        if user_data is None:
            return error_response("/add_detector", "no user signed in")

        (detector_id, type, detector_name) = cm_utils.validate_json(
            ["detector_id", "type", "detector_name"])

        if id_uniqueness(user_data["email"], detector_id):
            return error_response("/add_detector", "this detector id is already registered")

        log_id = mongo.logs.insert_one({
            "detector_id": detector_id,
            "logs": []
        }).inserted_id

        new_detector = {
            "detector_id": detector_id,
            "detector_name": detector_name,
            "detector_config": {},
            "type": type,
            "state": "init"
        }

        Logger.info(new_detector)

        mongo.users.update_one(
            {'email': user_data["email"]},
            {'$push': {"detectors": new_detector}}
        )

        return success_response("/add_detector", "detector added successfully")

    except BaseException as err:
        return error_response("/add_detector", f"Unexpected {err=}, {type(err)=}")


@app.route("/get_detector_config/<detector_id>")
def get_detector_config(detector_id):
    try:
        user = mongo.users.find_one(
            {"detectors.detector_id": detector_id}
        )

        detectors = {key: value for key,
                     value in user.items() if key in ["detectors"]}

        detectors = detectors["detectors"]
        for det in detectors:
            if det["detector_id"] == detector_id:
                config = det["detector_config"]

        config.update(DETECTOR_CONFIG)

        return config
    except BaseException as err:
        return error_response("/get_detector_config", f"Unexpected {err=}, {type(err)=}")


@app.route("/set_detector_config/<detector_id>", methods=["POST"])
def set_detector_config(detector_id):
    try:
        (new_config,) = cm_utils.validate_json(["new_config"])

        mongo.users.update_one(
            {"detectors.detector_id": detector_id},
            {"$set": {"detectors.$.detector_config": new_config}}
        )

        return success_response("/set_detector_config", "config updates successfully")
    except BaseException as err:
        return error_response("/set_detector_config", f"Unexpected {err=}, {type(err)=}")


@app.route("/detector/<detector_id>", methods=["DELETE"])
def delete_detector(detector_id):
    try:
        user_data = cm_utils.auth_token()
        if user_data is None:
            return error_response("/add_detector", "no user signed in")

        mongo.logs.delete_one({"detector_id": detector_id})

        mongo.users.update_one(
            {"detectors.detector_id": detector_id},
            {"$pull": {"detectors": {"detector_id": detector_id}}})

        return success_response("/delete_detector", "detector deleted successfully")
    except BaseException as err:
        return error_response("/delete_detector", f"Unexpected {err=}, {type(err)=}")


@app.route("/detector/<detector_id>/export")
def export_detector_log(detector_id):
    try:
        logs = mongo.logs.find_one({"detector_id": detector_id})

        logs_data = {key: value for key,
                     value in logs.items() if key == "logs"}

        logs_table = pd.DataFrame.from_records(logs_data)

        with tempfile.TemporaryDirectory() as tmpdirname:
            tmppath = os.path.join(tmpdirname, f"{str(datetime.now())}.csv")
            with open(tmppath, 'w') as tmpfile:
                logs_table.to_csv(tmpfile.name, index=False)
                mimetype = "text/csv"

            return send_file(tmppath, mimetype=mimetype, as_attachment=True)
    except BaseException as err:
        return error_response("/export_detector_log", f"Unexpected {err=}, {type(err)=}")


@app.route("/detector/<detector_id>/check_state")
def detector_check_state(detector_id):
    changed = check_state(detector_id)
    return success_response("asd", changed)
