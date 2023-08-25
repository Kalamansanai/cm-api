from bson.objectid import ObjectId
from flask import abort, send_file
from cm_config import Logger
from cm_models import Detector, Location

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


# @app.route("/get_detector/<detector_id>", methods=["GET"])
# def get_detector(detector_id):
#     user_data = cm_utils.auth_token()
#     if user_data is None:
#         return error_response("/get_detector", "no user signed in")
#     detector_raw = mongo.detectors.find_one({"detector_id": detector_id})
#     detector = Detector(detector_raw)

#     return success_response("/get_detector", detector.get_json(logs=False))


@app.route("/get_detector_with_logs/<detector_id>", methods=["GET"])
def get_detector_with_logs(detector_id):
    user_data = cm_utils.auth_token()
    if user_data is None:
        return error_response("/get_detector_with_logs", "no user signed in")

    detector_raw = mongo.detectors.find_one({"detector_id": detector_id})
    detector = Detector(detector_raw)

    return success_response("/get_detector_logs", detector.get_json())


@app.route("/get_detector_img/<detector_id>", methods=["GET"])
def get_detector_img(detector_id):
    user_data = cm_utils.auth_token()
    if user_data is None:
        return error_response("/get_detector_img", "no user signed in")

    print(detector_id)
    detector = mongo.detectors.find_one({"detector_id": detector_id})

    try:
        return send_file(detector["img_path"], as_attachment=True)
    except:
        return abort(400)


@app.route("/get_location", methods=["GET"])
def get_location():
    user_data = cm_utils.auth_token()
    if user_data is None:
        return error_response("/get_detector_img", "no user signed in")

    location_raw = mongo.locations.find_one(
        {"user_id": ObjectId(user_data["id"])})
    location = Location(location_raw)

    return success_response("/get_location", location.get_json())
