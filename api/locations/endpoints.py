from startup import app, mongo
from flask import abort
from domain.location import Location
from bson.objectid import ObjectId
from api.api_utils import auth_token, error_response, success_response

@app.route("/get_location", methods=["GET"])
def get_location():
    user_data = auth_token()
    if user_data is None:
        return abort(401)

    location_raw = mongo.locations.find_one(
        {"user_id": ObjectId(user_data["id"])})
    if location_raw is None:
        return error_response("/get_location", "location is None")
    location = Location(location_raw)

    return success_response( location.get_json())
