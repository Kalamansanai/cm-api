from startup import app, mongo
from api.api_utils import success_response, error_response
from domain.log import Log
from api import login_required


@app.route("/get_logs_by_detector/<detector_id>", methods=["GET"])
@login_required
def get_by_detector(_, detector_id):
    logs_raw = list(mongo.logs.find({"detector_id": detector_id}))
    if logs_raw == []:
        return error_response("no log found")
    logs = [Log(log_raw).get_json() for log_raw in logs_raw]

    return success_response(logs)
