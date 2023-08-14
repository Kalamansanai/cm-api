from bson.objectid import ObjectId
from flask import abort, send_file
from cm_config import Logger

from startup import app, mongo
from cm_types import error_response, success_response
import cm_utils
from plot_preprocess import prepare_lineplot_data, prepare_piechart_data


@app.route("/get_logs_for_plot/<detector_id>", methods=["GET"])
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

    detectors_raw = mongo.detectors.find({"user_id": user_id})
    detectors = list(map(lambda x: cm_utils.wrap_detector(x, ["_id", "user_id", "logs"]),
                     detectors_raw))

    return success_response("/get_detectors_by_user", detectors)


@app.route("/get_detector/<detector_id>", methods=["GET"])
def get_detector(detector_id):
    user_data = cm_utils.auth_token()
    if user_data is None:
        return error_response("/get_detector", "no user signed in")
    detector_raw = mongo.detectors.find_one({"detector_id": detector_id})

    detector_filtered = cm_utils.wrap_detector(
        detector_raw, ["_id", "user_id", "logs"])

    return success_response("/get_detector", detector_filtered)


@app.route("/get_detector_with_logs/<detector_id>", methods=["GET"])
def get_detector_with_logs(detector_id):
    user_data = cm_utils.auth_token()
    if user_data is None:
        return error_response("/get_detector_with_logs", "no user signed in")

    detector_raw = mongo.detectors.find_one({"detector_id": detector_id})
    detector_filtered = cm_utils.wrap_detector(
        detector_raw, ["_id", "user_id"])

    return success_response("/get_detector_logs", detector_filtered)


@app.route("/get_detector_img/<detector_id>", methods=["GET"])
def get_detector_img(detector_id):
    user_data = cm_utils.auth_token()
    if user_data is None:
        return error_response("/get_detector_img", "no user signed in")

    detector = mongo.detectors.find_one({"detector_id": detector_id})

    try:
        return send_file(detector["image_path"], as_attachment=True)
    except:
        return abort(400)
