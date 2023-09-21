from startup import app, mongo
from domain.detector import Detector
from domain.location import Location
from api.api_utils import error_response, success_response, validate_json
from api import login_required

import pandas as pd
from datetime import datetime
from bson.objectid import ObjectId

@app.route("/get_location_monthly_sum_by_type/<location_id>", methods=["POST"])
@login_required
def get_location_monthly_sum_by_type(_, location_id):
    (type, ) = validate_json(["type"]) 

    location_raw = mongo.locations.find_one({"_id": ObjectId(location_id)})
    if location_raw is None:
        return error_response("/get_location_monthly_stat_by_type", "location is not found")
    location = Location(location_raw)

    stat = monthly_sum_by_type(location, type)
    if stat is None:
        return error_response("", "error")
    
    return success_response( stat)

def monthly_sum_by_type(location: Location, type: str):
    detectors: list[dict | None]  = [mongo.detectors.find_one({"_id": detector.id}) for detector in location.detectors if detector.type == type]
    if detectors == []:
        return None

    current_month = datetime.now().month

    values  = [Detector(detector).consumption_by_month(current_month ) for detector in detectors if detector is not None]

    return sum(values)
