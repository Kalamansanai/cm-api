from startup import app, mongo
import cm_utils
from flask import abort
from cm_types import success_response, error_response
from domain.location import Location
from bson.objectid import ObjectId

@app.route("/get_location", methods=["GET"])
def get_location():
    user_data = cm_utils.auth_token()
    if user_data is None:
        return abort(401)

    location_raw = mongo.locations.find_one(
        {"user_id": ObjectId(user_data["id"])})
    if location_raw is None:
        return error_response("/get_location", "location is None")
    location = Location(location_raw)

    return success_response( location.get_json())
