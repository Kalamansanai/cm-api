from startup import app, mongo
from api.api_utils import success_response, error_response
from domain.detector import Detector
from api import login_required

import pandas as pd
import numpy as np

@app.route("/get_logs_for_plot_by_detector/<detector_id>", methods=["GET"])
@login_required
def get_logs_for_plot_by_detector(_, detector_id):
    detector_raw = mongo.detectors.find_one({"detector_id": detector_id})
    if detector_raw is None:
        return error_response("detector is None")
    detector = Detector(detector_raw)

    data = prepare_detector_lineplot_data(detector)
    config = make_config([detector_id])
    
    return success_response( {
        "data": data,
        "config": config
        })

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
