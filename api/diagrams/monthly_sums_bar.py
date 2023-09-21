from domain.detector import Detector
from domain.location import Location
from api import login_required
from startup import app, mongo
from api.api_utils import success_response, error_response

from datetime import datetime
import pandas as pd
from bson.objectid import ObjectId


@app.route("/get_location_monthly_sums/<location_id>", methods=["POST"])
@login_required
def get_monthly_sums(_, location_id):
    
    location_raw = mongo.locations.find_one({"_id": ObjectId(location_id)})
    if location_raw is None:
        return error_response("/get_location_monthly_sums", "location is not found")
    location = Location(location_raw)

    stats = monthly_stat(location)

    return success_response(stats)


def monthly_stat(location: Location):
    types = ["water", "electricity", "gas"]

    current_month = datetime.now().month

    result = []
    for i in range(5):
        monthly_result = {}
        for type in types:
            detectors: list[dict | None]  = [mongo.detectors.find_one({"_id": detector.id}) for detector in location.detectors if detector.type == type]
            if detectors == []:
                return error_response("monthly_stat", "no detector found")

            values  = [Detector(detector).consumption_by_month(current_month - i) * detector["detector_config"]["cost"] for detector in detectors if detector is not None]
            monthly_result[type] = sum(values)

        result.append({
            "month": current_month - i, 
            "water":  monthly_result["water"], 
            "waterColor": "hsl(229, 70%, 50%)",
            "electricity": monthly_result["electricity"], 
            "electricityColor": "hsl(104, 70%, 50%)",
            "gas": monthly_result["gas"],
            "gasColor": "hsl(344, 70%, 50%)"})

    return result

