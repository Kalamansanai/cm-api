from domain.location import Location
from api import login_required
from startup import app, mongo
from api.api_utils import success_response, error_response

from datetime import datetime
from bson.objectid import ObjectId
import polars as pl


@app.route("/get_location_monthly_sums/<location_id>", methods=["POST"])
@login_required
def get_monthly_sums(_, location_id):
    logs_raw = list(mongo.logs.find({"location_id": location_id}))
    if len(logs_raw) == 0:
        return error_response("logs not found")

    table = monthly_stat(logs_raw)
    dict = table_to_dict(table)

    return success_response(dict)


def monthly_stat(logs):
    df = pl.from_dicts(logs)

    df = df.with_columns(
        (df["timestamp"].dt.month().alias("month")),
    )

    df = df.sort("type")

    df = df.with_columns(
        pl.when((df["type"].shift() == df["type"]))
        .then((df["value"] - df["value"].shift()) * df["cost"])
        .otherwise(0)
        .alias("consumption")
    )

    return df.group_by(["month", "type"]).agg(pl.col("consumption").sum())


def table_to_dict(table):
    reformatted_data = []
    for name, data in table.sort("month").group_by("month"):
        water_value = (
            data.filter(data["type"] == "water").rows()[0][2]
            if not data.filter(data["type"] == "water").is_empty()
            else 0
        )
        electricity_value = (
            data.filter(data["type"] == "electricity").rows()[0][2]
            if not data.filter(data["type"] == "electricity").is_empty()
            else 0
        )
        gas_value = (
            data.filter(data["type"] == "gas").rows()[0][2]
            if not data.filter(data["type"] == "gas").is_empty()
            else 0
        )

        reformatted_data.append(
            {
                "month": name,
                "water": water_value,
                "electricity": electricity_value,
                "gas": gas_value,
            }
        )

    return reformatted_data
