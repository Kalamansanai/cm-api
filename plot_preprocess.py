import datetime

import pandas as pd
import numpy as np

from cm_config import PLOT_COLOR, TYPE_COLORS
from startup import mongo
from cm_models import Detector, Location


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
    for detector in detectors:
        if detector["type"] in pie_data.keys():
            pie_data[detector["type"]] = pie_data[detector["type"]] + \
                float(_structure_detector_pie_data(detector))
        else:
            pie_data[detector["type"]] = float(
                _structure_detector_pie_data(detector))

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


def _structure_detector_pie_data(detector):
    data = detector["logs"]
    if data == []:
        return 0

    current_month = datetime.datetime.now().month

    df = pd.DataFrame.from_dict(data)
    df["month"] = pd.DatetimeIndex(df["timestamp"]).month

    df = df.loc[(df["month"] == current_month)]

    if df.empty:
        return 0

    monthly_consumption = df.iloc[-1]["value"] - df.iloc[0]["value"]

    return monthly_consumption * detector["detector_config"]["cost"]


def make_config(detector_ids):

    lines = [{
      "type": "monotone",
      "dataKey": detector_id,
      "stroke": "#82ca9d"} for detector_id in detector_ids]

    return {
        "type": "dashboard",
        "containerWidth": "100%",
        "containerHeight": "100%",
        "chartWidth": 50,
        "chartHeight": 0,
        "chartMargin": {
            "top": 5,
            "right": 30,
            "left": 20,
            "bottom": 5
        },
        "YAxis": {
            "type": "number"
        },
        "XAxis": {
            "dataKey": "date"
        },""
        "CartesianGrid": {
            "strokeDashArray": "3 3"
        },
        "Tooltip": {
            "enable": True
        },
        "Legend": {
            "enable": True
        },
        "Lines": lines

    }
