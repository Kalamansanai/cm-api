from startup import app, mongo
from domain.location import Location
from api.api_utils import error_response, success_response
from api import login_required

from bson.objectid import ObjectId


@app.route("/get_location", methods=["GET"])
@login_required
def get_location(user_data):
    location_raw = mongo.locations.find_one(
        {"user_id": ObjectId(user_data["id"])})
    if location_raw is None:
        return error_response("location is None")
    location = Location(location_raw)

    return success_response( location.get_json())
