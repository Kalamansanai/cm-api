from api.diagrams.utils import make_config
from startup import app, mongo
from api.api_utils import success_response, error_response
from api import login_required

import polars as pl

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

    df = pl.from_dicts(logs)

    df = df.with_columns(
            [
                df["timestamp"].dt.strftime("%m.%d-%H:%M").alias("date"),
                (df["value"] - df["value"].shift()).alias(value_id).fill_null(strategy="zero")
            ]
        )

    res = df.select(["date", value_id]).to_dicts()
    
    return res
