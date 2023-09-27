from startup import app, mongo
from cm_config import MODE
from api.api_utils import success_response, error_response, validate_json 
from domain.location import Location 
from domain.detector import create_detector_for_mongo, detector_valid
from api import login_required

from bson.objectid import ObjectId


@app.route("/add_detector", methods=["POST"])
@login_required
def add_detector_to_user(_):
    (location_id, detector_id, type, detector_name, char_num, coma_position) = validate_json(
        ["location_id", "detector_id", "type", "detector_name", "char_num", "coma_position"]
    )

    location_raw = mongo.locations.find_one({"_id": ObjectId(location_id)})
    if location_raw is None:
        return error_response("location is not found")
    location = Location(location_raw) 

    # if MODE == "prod" and not detector_valid(detector_id):
    #     return error_response("This detector ID is not valid.")

    if not detector_id_unique(location_id, detector_id):
        return error_response("A detector is already registered with this id !")

    new_detector = create_detector_for_mongo(detector_id, location_id, detector_name, char_num, coma_position, type) 

    detector_id = mongo.detectors.insert_one(new_detector).inserted_id
    if detector_id is None:
        return error_response("adding detector failed")

    new_detector["_id"] = detector_id
    mongo.locations.find_one_and_update(
        {"_id": ObjectId(location_id)},
        {"$push": {"detectors": new_detector}}
    )

    return success_response( str(detector_id))

def detector_id_unique(location_id: str, detector_id: str):
    detectors = mongo.detectors.find({"location_id": location_id})
    for detector in detectors:
        if detector["detector_id"] == detector_id:
            return False
    return True
