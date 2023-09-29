
from datetime import datetime
from api.diagrams.utils import make_config
from startup import app, mongo
from api.api_utils import success_response, error_response
from api import login_required

import polars as pl

@app.route("/get_logs_for_plot_by_location/<location_id>", methods=["GET"])
# @login_required
def get_logs_for_plot_by_location(location_id):
    logs_raw = list(mongo.logs.find({"location_id": location_id}))
    if logs_raw == []:
        return error_response("no log found")

    data_list = prepare_detector_lineplot_data(logs_raw)
    config_list = [make_config(["current"]) for data in data_list]

    print(data_list)
    return success_response(
            [ 
                {
                    "data": data,
                    "config": config
                } for (data, config) in zip(data_list, config_list)
            ]
        )

def prepare_detector_lineplot_data(logs: list[dict]):
    df = pl.from_dicts(logs)

    current_month = datetime.now().month

    df = df.sort("type").filter((df["timestamp"].dt.month() == current_month) | (df["timestamp"].dt.month() == current_month - 1))

    df = df.with_columns(
            [
                df["timestamp"].dt.day().alias("day"),
                df["timestamp"].dt.month().alias("month")
            ])

    df = df.with_columns(
            pl.when((df["type"].shift() == df["type"]))
            .then((df["value"] - df["value"].shift()).fill_null(strategy="zero"))
            .otherwise(0)
            .alias("current")
        )

    df = df.group_by(["type", "month", "day"]).agg(pl.col("current").sum())
    df = df.sort(["month", "day"])

    data = [
            df.select(["month", "day", "current"]).filter(df["type"] == "water").to_dicts(),
            df.select(["month", "day", "current"]).filter(df["type"] == "electricity").to_dicts(),
            df.select(["month", "day", "current"]).filter(df["type"] == "gas").to_dicts()
        ]

    return data 
    
