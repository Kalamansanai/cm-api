from bson.objectid import ObjectId
from startup import app, mongo
import tempfile
import os
from datetime import datetime
from flask import send_file
import pandas as pd
from api.api_utils import error_response
from api import login_required

@app.route("/detector/<detector_id>/export")
@login_required
def export_detector_log(_,detector_id):
    detector_raw: dict | None = mongo.detectors.find_one({"_id": ObjectId(detector_id)})
    if detector_raw is None:
        return error_response("no detector found!")

    logs_table = pd.DataFrame.from_records(detector_raw["logs"])

    with tempfile.TemporaryDirectory() as tmpdirname:
        tmppath = os.path.join(tmpdirname, f"{str(datetime.now())}.csv")
        with open(tmppath, 'w') as tmpfile:
            logs_table.to_csv(tmpfile.name, index=False)
            mimetype = "text/csv"

        return send_file(tmppath, mimetype=mimetype, as_attachment=True)
