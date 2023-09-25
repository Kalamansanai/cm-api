from startup import app, mongo
from api.api_utils import success_response, error_response 
from cm_config import TYPE_COLORS
from api import login_required

import polars as pl

@app.route("/get_location_pie/<location_id>", methods=["GET"])
@login_required
def get_location_pie(_, location_id):
    logs_raw = list(mongo.logs.find({"location_id": location_id}))
    if logs_raw == []:
        return error_response("no log found")
    
    return success_response(prepare_piechart_data(logs_raw))

def prepare_piechart_data(logs: list[dict]):
    pie_data = {}

    df = pl.from_dicts(logs)

    df = df.with_columns((df['value'] - df['value'].shift()).alias("consumption"))

    grouped = df.group_by('type').agg(pl.col('consumption').sum())
    print(grouped)

    reformatted_data = []
    for type in grouped.rows():
        name = type[0]
        value = type[1]
        reformatted_data.append(
            {
                "id": name,
                "label": value,
                "value": round(value, 3),
                "color": TYPE_COLORS[name]
            }
        )
            
    return reformatted_data


