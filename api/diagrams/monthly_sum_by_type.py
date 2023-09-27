from startup import app, mongo
from api.api_utils import error_response, success_response, validate_json
from api import login_required

import polars as pl
from datetime import datetime

@app.route("/get_location_monthly_sum_by_type/<location_id>", methods=["POST"])
@login_required
def get_location_monthly_sum_by_type(_, location_id):
    (type, ) = validate_json(["type"]) 

    logs_raw = list(mongo.logs.find({"location_id": location_id}))
    if len(logs_raw) == 0:
        return error_response("logs not found")

    sum = monthly_sum_by_type(logs_raw, type)
    
    return success_response(sum)

def monthly_sum_by_type(logs, type: str):
    df = pl.from_dicts(logs)

    current_month = datetime.now().month

    df = df.filter(
            df["type"] == type
            )

    df = df.with_columns(
            pl.when((df["timestamp"].dt.month() == current_month))
            .then((df['value'] - df['value'].shift()))
            .otherwise(0)
            .alias("consumption")
        )

    return df["consumption"].sum()
