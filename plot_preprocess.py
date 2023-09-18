import datetime

import pandas as pd
import numpy as np

from cm_config import PLOT_COLOR, TYPE_COLORS
from startup import mongo
from cm_models import Detector, Location
from cm_types import error_response


def prepare_detector_lineplot_data(detector: Detector):
    value_id = detector.detector_id

    if len(detector.logs) == 0:
        return None
    df = pd.DataFrame.from_records([log.get_json() for log in detector.logs])
    df["date"] = df["timestamp"].map(
            lambda x: x.strftime("%m.%d-%H:%M"))
    df[value_id] = df["value"].rolling(2).apply(
        lambda x: np.round(x.iloc[1] - x.iloc[0], 3)).fillna(0)

    reformatted_data = df[["date", value_id]].to_dict(orient="records")

    return reformatted_data

def prepare_location_lineplot_data(location: Location):
    #TODO: implement this
    return NotImplemented


def prepare_piechart_data(detectors):
    pie_data = {}

    current_month = datetime.datetime.now().month
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

def make_config(detector_ids):

    lines = [{
      "type": "monotone",
      "dataKey": detector_id,
      "stroke": "#82ca9d"} for detector_id in detector_ids]

    return {
        "type": "dashboard",
        "containerWidth": "100%",
        "containerHeight": "100%",
        "chartwidth": 50,
        "chartheight": 0,
        "chartmargin": {
            "top": 5,
            "right": 30,
            "left": 20,
            "bottom": 5
        },
        "yaxis": {
            "type": "number"
        },
        "xaxis": {
            "datakey": "date"
        },""
        "cartesiangrid": {
            "strokedasharray": "3 3"
        },
        "tooltip": {
            "enable": True
        },
        "legend": {
            "enable": True
        },
        "lines": lines

    }

def monthly_stat_by_type(location: Location, type: str):
    detectors: list[dict | None]  = [mongo.detectors.find_one({"_id": detector.id}) for detector in location.detectors if detector.type == type]
    if detectors == []:
        return error_response("monthly_stat_by_type", "no detector found")

    current_month = datetime.datetime.now().month

    values  = [detector_consumption_by_month(Detector(detector), current_month) for detector in detectors if detector is not None]

    return sum(values)

def monthly_stat(location: Location):
    types = ["water", "electricity", "gas"]

    current_month = datetime.datetime.now().month

    result = []
    for i in range(5):
        monthly_result = {}
        for type in types:
            detectors: list[dict | None]  = [mongo.detectors.find_one({"_id": detector.id}) for detector in location.detectors if detector.type == type]
            if detectors == []:
                return error_response("monthly_stat", "no detector found")

            values  = [detector_consumption_by_month(Detector(detector), current_month - i) * detector["detector_config"]["cost"] for detector in detectors if detector is not None]
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

