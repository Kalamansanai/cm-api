from datetime import datetime

from flask import request
from startup import app, mongo

from PIL import Image
import PIL

from cm_config import IMAGE_PATH, DETECTOR_CONFIG, Logger
from cm_types import success_response, error_response
import cm_utils
import random
from datetime import datetime

from library.detector import Detector


detector = Detector("library/plates.pt", "library/plates.pt")


def generate_mock_data():
    return {"timestamp": datetime.now().timestamp(), "value": random.random(0, 10)}


@app.route("/send_image/<detector_id>", methods=["POST"])
def send_image(detector_id):
    try:
        img = Image.open(request.files["image"])
        img.save(f"{IMAGE_PATH}/{datetime.now().timestamp()}.png")

        # image processing(now its just mocking)
        log_data = detector.detect(img, 8, 3)

        mongo.logs.find_one_and_update(
            {"detector_id": detector_id},
            {"$push": {"logs": log_data}}
        )

        return success_response("/send_image", "success")
    except BaseException as err:
        return error_response("/send_image", f"Unexpected {err=}, {type(err)=}")


@app.route("/get_config")
def get_config():
    try:
        return success_response("/get_config", DETECTOR_CONFIG)
    except BaseException as err:
        return error_response("/get_config", f"Unexpected {err=}, {type(err)=}")


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

        log_id = mongo.logs.insert_one({
            "detector_id": detector_id,
            "logs": []
        }).inserted_id

        new_detector = {
            "detector_id": detector_id,
            "detector_name": detector_name,
            "detector_config": {},
            "type": type
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
