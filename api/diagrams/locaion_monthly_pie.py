from startup import app, mongo
from api.api_utils import success_response, auth_token
from domain.detector import Detector
from cm_config import TYPE_COLORS
from api import login_required

from flask import abort
from datetime import datetime
import numpy as np
import pandas as pd

@app.route("/get_location_pie/<location_id>", methods=["GET"])
@login_required
def get_location_pie(_, location_id):
    detectors_raw = mongo.detectors.find({"location_id": location_id})
    detectors = [Detector(detector_row) for detector_row in detectors_raw]

    return success_response(prepare_piechart_data(detectors))

def prepare_piechart_data(detectors):
    pie_data = {}

    current_month = datetime.now().month
    for detector in detectors:
        monthly_cost = detector_consumption_by_month(detector, current_month) * detector.detector_config.cost
        if detector.type in pie_data.keys():
            pie_data[detector.type] = pie_data[detector.type] + \
                float(monthly_cost)
        else:
            pie_data[detector.type] = float(
               monthly_cost) 

    reformatted_data = []
    for key in pie_data.keys():
        reformatted_data.append(
            {
                "id": key,
                "label": key,
                "value": np.round(pie_data[key], 3),
                "color": TYPE_COLORS[key]
            }
        )

    return reformatted_data

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
