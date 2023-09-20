from startup import app, mongo
from domain.detector import Detector
from domain.location import Location
from api.api_utils import error_response, auth_token, success_response, validate_json

import pandas as pd
from datetime import datetime
from flask import abort
from bson.objectid import ObjectId

@app.route("/get_location_monthly_stat_by_type/<location_id>", methods=["POST"])
def get_location_monthly_stat_by_type(location_id):
    user_data = auth_token()
    if user_data is None:
        return abort(401)

    (type, ) = validate_json(["type"]) 

    location_raw = mongo.locations.find_one({"_id": ObjectId(location_id)})
    if location_raw is None:
        return error_response("/get_location_monthly_stat_by_type", "location is not found")
    location = Location(location_raw)

    stat = monthly_stat_by_type(location, type)
    
    return success_response( stat)

def detector_consumption_by_month(detector: Detector, month: int):
    data = [log.get_json() for log in detector.logs]
    if data == []:
        return 0

    df = pd.DataFrame.from_dict(data)
    df["month"] = pd.DatetimeIndex(df["timestamp"]).month

    df = df.loc[(df["month"] == month)]

    if df.empty:
        return 0

    return df.iloc[-1]["value"] - df.iloc[0]["value"]


def monthly_stat_by_type(location: Location, type: str):
    detectors: list[dict | None]  = [mongo.detectors.find_one({"_id": detector.id}) for detector in location.detectors if detector.type == type]
    if detectors == []:
        return error_response("monthly_stat_by_type", "no detector found")

    current_month = datetime.now().month

    values  = [detector_consumption_by_month(Detector(detector), current_month) for detector in detectors if detector is not None]

    return sum(values)
