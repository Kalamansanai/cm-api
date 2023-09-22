from bson.objectid import ObjectId
from startup import app, mongo
from cm_config import DETECTOR_CONFIG
from flask import abort, send_file
from api.api_utils import success_response, error_response, validate_json
from domain.detector import Detector
from api import login_required, detector_id_validation_required

@app.route("/get_detector_with_logs/<detector_id>", methods=["GET"])
@login_required
def get_detector_with_logs(_, detector_id):
    detector_raw = mongo.detectors.find_one({"detector_id": detector_id})
    if detector_raw is None:
        return error_response("detector is None")
    detector = Detector(detector_raw)

    return success_response( detector.get_json())

@app.route("/get_detector_config/<detector_id>")
@detector_id_validation_required
def get_detector_config(detector_id):
    detector = mongo.detectors.find_one(
        {"detector_id": detector_id}
    )

    if detector is None:
        return error_response("detector has not added to any user yet !")

    config = detector["detector_config"]
    config.update(DETECTOR_CONFIG)

    return config


@app.route("/set_detector_config/<detector_id>", methods=["POST"])
@login_required
def set_detector_config(_, detector_id):

    (new_config,) = validate_json(["new_config"])

    mongo.detectors.update_one(
        {"detector_id": detector_id},
        {"$set": {"detector_config": new_config}}
    )

    return success_response("config updates successfully")

@app.route("/detector/<detector_id>", methods=["DELETE"])
@login_required
def delete_detector(user_data, detector_id):
    mongo.detectors.delete_one({"_id": ObjectId(detector_id)})

    mongo.locations.find_one_and_update(
        {"user_id": ObjectId(user_data["id"])},
        {"$pull": {"detectors": {"_id": ObjectId(detector_id)}}}
    )

    return success_response("detector deleted successfully")


@app.route("/get_detector_img/<detector_id>", methods=["GET"])
@login_required
def get_detector_img(_, detector_id):

    detector = mongo.detectors.find_one({"detector_id": detector_id})
    if detector is None:
        return error_response("detector is None")

    try:
        return send_file(detector["img_path"], as_attachment=True)
    except:
        return abort(400)
