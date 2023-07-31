from bson.objectid import ObjectId
from cm_config import Logger

from startup import app, mongo
from cm_types import error_response, success_response
import cm_utils
from plot_preprocess import prepare_lineplot_data, prepare_piechart_data


@app.route("/get_logs_for_plot/<detector_id>", methods=["POST"])
def get_logs_for_plot(detector_id):
    user_data = cm_utils.auth_token()
    if user_data is None:
        return error_response("/get_user_pie", "no user signed in")

    logs = mongo.detectors.find_one({"detector_id": detector_id})

    return success_response("get_logs_for_plot", prepare_lineplot_data(logs))


@app.route("/get_user_pie", methods=["GET"])
def get_user_pie():
    user_data = cm_utils.auth_token()
    if user_data is None:
        return error_response("/get_user_pie", "no user signed in")

    detectors = mongo.detectors.find({"user_id": user_data["id"]})

    return success_response("get_user_pie", prepare_piechart_data(detectors))


@app.route("/get_detectors_by_user/<user_id>", methods=["GET"])
def get_detectors_by_user(user_id):
    user_data = cm_utils.auth_token()
    if user_data is None:
        return error_response("/get_detectors_by_user", "no user signed in")

    def wrap_detector(detector):
        ignored_fields = ["_id", "user_id", "logs"]
        detector_filtered = {key: value for key,
                             value in detector.items() if key not in ignored_fields}
        return detector_filtered

    detectors_raw = mongo.detectors.find({"user_id": user_id})
    detectors = list(map(wrap_detector, detectors_raw))

    return success_response("/get_detectors_by_user", detectors)


@app.route("/get_detector/<detector_id>", methods=["GET"])
def get_detector(detector_id):
    detector_raw = mongo.detectors.find_one({"detector_id": detector_id})

    ignored_fields = ["_id", "user_id", ]
    detector_filtered = {key: value for key,
                         value in detector_raw.items() if key not in ignored_fields}

    return success_response("/get_detector", detector_filtered)
