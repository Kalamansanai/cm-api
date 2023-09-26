from startup import app, mongo
from api.api_utils import success_response, error_response
from domain.log import Log
from api import login_required

import pandas as pd
import numpy as np

@app.route("/get_logs_for_plot_by_detector/<detector_id>", methods=["GET"])
@login_required
def get_logs_for_plot_by_detector(_, detector_id):
    logs_raw = list(mongo.logs.find({"detector_id": detector_id}))
    if logs_raw == []:
        return error_response("no log found")

    data = prepare_detector_lineplot_data(logs_raw)
    config = make_config([detector_id])
    
    return success_response( {
        "data": data,
        "config": config
        })

def prepare_detector_lineplot_data(logs: list[dict]):
    value_id = logs[0]["detector_id"]

    df = pd.DataFrame.from_records(logs)
    df["date"] = df["timestamp"].map(
            lambda x: x.strftime("%m.%d-%H:%M"))
    df[value_id] = df["value"].rolling(2).apply(
        lambda x: np.round(x.iloc[1] - x.iloc[0], 3)).fillna(0)

    reformatted_data = df[["date", value_id]].to_dict(orient="records")

    return reformatted_data

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
        "yAxis": {
            "type": "number"
        },
        "xAxis": {
            "datakey": "date"
        },""
        "cartesianGrid": {
            "strokeDashArray": "3 3"
        },
        "tooltip": {
            "enable": True
        },
        "legend": {
            "enable": True
        },
        "lines": lines

    }
