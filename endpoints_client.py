from bson.objectid import ObjectId
from flask import abort, send_file
from cm_config import Logger
from cm_models import Detector, Location

from startup import app, mongo
from cm_types import error_response, success_response
import cm_utils
from plot_preprocess import prepare_detector_lineplot_data, prepare_location_lineplot_data, prepare_piechart_data, make_config


@app.route("/get_logs_for_plot_by_detector/<detector_id>", methods=["GET"])
def get_logs_for_plot_by_detector(detector_id):
    user_data = cm_utils.auth_token()
    if user_data is None:
        return error_response("/get_user_pie", "no user signed in")

    detector_raw = mongo.detectors.find_one({"detector_id": detector_id})
    if detector_raw is None:
        return error_response("/get_logs_for_plot_by_detector", "detector is None")
    detector = Detector(detector_raw)

    data = prepare_detector_lineplot_data(detector)
    config = make_config([detector_id])
    
    return success_response("get_logs_for_plot", {
        "data": data,
        "config": config
        })


@app.route("/get_logs_for_plot_by_location/<location_id>", methods=["GET"])
def get_logs_for_plot_by_location(location_id):
    user_data = cm_utils.auth_token()
    if user_data is None:
        return error_response("/get_user_pie", "no user signed in")

    location_raw = mongo.locations.find_one({"_id": ObjectId(location_id)})
    if location_raw is None:
        return error_response("/get_logs_for_plot_by_location", "location is None")
    location = Location(location_raw)

    data = prepare_location_lineplot_data(location)
    #TODO: make_config gets all the detectors we want to make as a line 
    config = make_config([detector_id])
    
    return success_response("get_logs_for_plot", {
        "data": data,
        "config": config
        })

@app.route("/get_location_pie/<location_id>", methods=["GET"])
def get_location_pie(location_id):
    user_data = cm_utils.auth_token()
    if user_data is None:
        return error_response("/get_user_pie", "no user signed in")

    detectors = mongo.detectors.find({"location_id": location_id})

    return success_response("get_user_pie", prepare_piechart_data(detectors))


@app.route("/get_detector_with_logs/<detector_id>", methods=["GET"])
def get_detector_with_logs(detector_id):
    user_data = cm_utils.auth_token()
    if user_data is None:
        return error_response("/get_detector_with_logs", "no user signed in")

    detector_raw = mongo.detectors.find_one({"detector_id": detector_id})
    if detector_raw is None:
        return error_response("/get_detector_with_logs", "detector is None")
    detector = Detector(detector_raw)

    return success_response("/get_detector_logs", detector.get_json())


@app.route("/get_detector_img/<detector_id>", methods=["GET"])
def get_detector_img(detector_id):
    user_data = cm_utils.auth_token()
    if user_data is None:
        return error_response("/get_detector_img", "no user signed in")

    detector = mongo.detectors.find_one({"detector_id": detector_id})
    if detector is None:
        return error_response("/get_detector_with_logs", "detector is None")

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
    if location_raw is None:
        return error_response("/get_location", "location is None")
    location = Location(location_raw)

    return success_response("/get_location", location.get_json())
