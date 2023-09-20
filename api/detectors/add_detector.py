from bson.objectid import ObjectId
from startup import app, mongo
from cm_config import MODE
import json
from api.api_utils import success_response, error_response, auth_token, validate_json 


@app.route("/add_detector", methods=["POST"])
def add_detector_to_user():
    user_data = auth_token()
    if user_data is None:
        return error_response("/add_detector", "no user signed in")

    (location_id, detector_id, type, detector_name, char_num, coma_position) = validate_json(
        ["location_id", "detector_id", "type", "detector_name", "char_num", "coma_position"]
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
            "flash": 0,
            "charNum": char_num,
            "comaPosition": coma_position
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

    return success_response( str(detector_id))

def id_uniqueness(location_id, detector_id):
    detectors = mongo.detectors.find({"location_id": location_id})

    for detector in detectors:
        if detector["detector_id"] == detector_id:
            return True

    return False


def detector_valid(detector_id: str):
    if detector_id not in json.load(open('library/detector_list.json'))["id"]:
        return False
