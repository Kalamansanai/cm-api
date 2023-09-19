from bson.objectid import ObjectId
from startup import app, mongo
from cm_types import success_response, error_response
import cm_utils
from cm_config import DETECTOR_CONFIG
from cm_detector import check_and_update_detectors_state

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

    return success_response("config updates successfully")

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

    return success_response("detector deleted successfully")

@app.route("/detector/<detector_id>/check_state")
def detector_check_state(detector_id):
    detector_raw: dict | None = mongo.detectors.find_one({"detector_id": detector_id})
    if detector_raw is None:
        return error_response("check_state", "no detector found")
    changed = check_and_update_detectors_state(detector_raw)
    return success_response(changed)


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
    return success_response(detectors)
