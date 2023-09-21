from startup import app, mongo
from domain.detector import Detector
from domain.location import Location
from api.api_utils import error_response, auth_token, success_response, validate_json
from api import login_required

import pandas as pd
from datetime import datetime
from flask import abort
from bson.objectid import ObjectId

@app.route("/get_location_monthly_stat_by_type/<location_id>", methods=["POST"])
@login_required
def get_location_monthly_stat_by_type(_, location_id):
    (type, ) = validate_json(["type"]) 

    location_raw = mongo.locations.find_one({"_id": ObjectId(location_id)})
    if location_raw is None:
        return error_response("/get_location_monthly_stat_by_type", "location is not found")
    location = Location(location_raw)

    stat = monthly_stat_by_type(location, type)
    
    return success_response( stat)

def monthly_stat_by_type(location: Location, type: str):
    detectors: list[dict | None]  = [mongo.detectors.find_one({"_id": detector.id}) for detector in location.detectors if detector.type == type]
    if detectors == []:
        return error_response("monthly_stat_by_type", "no detector found")

    current_month = datetime.now().month

    values  = [Detector(detector).consumption_by_month(current_month ) for detector in detectors if detector is not None]

    return sum(values)
