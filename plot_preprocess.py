from cm_config import PLOT_COLOR, TYPE_COLORS
import datetime
from startup import mongo
import pandas as pd


def reformat(data: dict, type):
    reformatted_data = []

    if type == "line":
        reformatted_data.append({
            "id": data["detector_id"],
            "color": PLOT_COLOR,
            "data": [{
                "x": log["timestamp"],
                "y": log["value"]
            } for log in data["logs"]]
        })
    elif type == "pie_cost":
        for key in data.keys():
            reformatted_data.append(
                {
                    "id": key,
                    "label": key,
                    "value": data[key],
                    "color": TYPE_COLORS[key]
                }
            )

    return reformatted_data


def prepare_lineplot_data(data: dict):
    reformatted_data = reformat(data, "line")

    return reformatted_data


def prepare_piechart_data(detectors):

    # TODO: refactor this for the new design

    pie_data = {}
    for detector in detectors:
        if detector["type"] in pie_data.keys():
            pie_data[detector["type"]] = pie_data[detector["type"]] + \
                float(_structure_detector_pie_data(detector))
        else:
            pie_data[detector["type"]] = float(
                _structure_detector_pie_data(detector))

    reformatted = reformat(pie_data, "pie_cost")

    return reformatted


def _structure_detector_pie_data(detector):
    data = detector["logs"]
    if data == []:
        return 0

    current_month = datetime.datetime.now().month

    df = pd.DataFrame.from_dict(data)
    df["month"] = pd.DatetimeIndex(df["timestamp"]).month

    df = df.loc[(df["month"] == current_month)]

    monthly_consumption = df.iloc[-1]["value"] - df.iloc[0]["value"]

    return monthly_consumption * detector["cost"]
