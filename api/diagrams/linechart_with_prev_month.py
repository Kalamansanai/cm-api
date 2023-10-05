from datetime import datetime
from api.diagrams.utils import make_config
from startup import app, mongo
from api.api_utils import success_response, error_response
from api import login_required

import polars as pl


@app.route("/linechart_with_prev_month/<location_id>", methods=["GET"])
@login_required
def linechart_with_prev_month(_, location_id):
    logs_raw = list(mongo.logs.find({"location_id": location_id}))
    if logs_raw == []:
        return error_response("no log found")

    data_list = prepare_detector_lineplot_data(logs_raw)
    config_list = [make_config(["prev", "current"]) for _ in data_list]

    return success_response(
        [
            {"data": data, "config": config}
            for (data, config) in zip(data_list, config_list)
        ]
    )


def prepare_detector_lineplot_data(logs: list[dict]):
    _df = pl.from_dicts(logs)

    current_month = datetime.now().month

    result = []
    for type in ["water", "electricity", "gas"]:
        df = _df
        df = (
            df.with_columns(
                [
                    pl.col("timestamp").dt.day().alias("day"),
                    pl.col("timestamp").dt.month().alias("month"),
                    pl.when((df["type"].shift() == df["type"]))
                    .then(
                        (df["value"] - df["value"].shift()).fill_null(strategy="zero")
                    )
                    .otherwise(0)
                    .alias("consumption"),
                ]
            )
            .filter(
                (df["type"] == type)
                & (
                    (df["timestamp"].dt.month() == current_month)
                    | (df["timestamp"].dt.month() == current_month - 1)
                )
            )
            .group_by(["month", "day"])
            .agg(pl.col("consumption").sum())
            .sort(["month", "day"])
        )

        df_current = df.filter(pl.col("month") == current_month)
        df_prev = df.filter(pl.col("month") == current_month - 1)

        result.append(
            df_current.join(df_prev, on="day", how="outer")
            .select(["day", "consumption", "consumption_right"])
            .rename({"consumption": "current", "consumption_right": "prev"})
            .to_dicts()
        )

    return result
