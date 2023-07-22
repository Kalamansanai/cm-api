from cm_config import PLOT_COLOR
import datetime
from startup import mongo
import pandas as pd


def prepare_lineplot_data(data: dict):
    new_data = []

    new_data.append({
        "id": data["detector_id"],
        "color": PLOT_COLOR,
        "data": [{
            "x": log["timestamp"],
            "y": log["value"]
        } for log in data["logs"]]
    })

    return new_data


def prepare_piechart_data(user: dict):
    pie_data = {}
    for detector in user["detectors"]:
        if detector["type"] in pie_data.keys():
            pie_data[detector["type"]] = pie_data[detector["type"]] + \
                float(structure_detector_pie_data(detector))
        else:
            pie_data[detector["type"]] = float(
                structure_detector_pie_data(detector))

    return pie_data


def structure_detector_pie_data(detector):
    data = mongo.logs.find_one(
        {"detector_id": detector["detector_id"]}
    )["logs"]

    current_month = datetime.datetime.now().month

    df = pd.DataFrame.from_dict(data)
    df["month"] = pd.DatetimeIndex(df["timestamp"]).month

    df = df.loc[(df["month"] == current_month)]

    monthly_consumption = df.iloc[-1]["value"] - df.iloc[0]["value"]

    return monthly_consumption * detector["cost"]
