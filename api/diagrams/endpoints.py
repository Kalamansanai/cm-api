from bson.objectid import ObjectId
from domain.detector import Detector
from domain.location import Location

from startup import app, mongo
from cm_types import error_response, success_response
import cm_utils
from plot_preprocess import prepare_detector_lineplot_data, prepare_location_lineplot_data, prepare_piechart_data, make_config, monthly_stat_by_type, monthly_stat
from flask import abort


@app.route("/get_logs_for_plot_by_detector/<detector_id>", methods=["GET"])
def get_logs_for_plot_by_detector(detector_id):
    user_data = cm_utils.auth_token()
    if user_data is None:
        return abort(401)

    detector_raw = mongo.detectors.find_one({"detector_id": detector_id})
    if detector_raw is None:
        return error_response("/get_logs_for_plot_by_detector", "detector is None")
    detector = Detector(detector_raw)

    data = prepare_detector_lineplot_data(detector)
    config = make_config([detector_id])
    
    return success_response( {
        "data": data,
        "config": config
        })


@app.route("/get_location_pie/<location_id>", methods=["GET"])
def get_location_pie(location_id):
    user_data = cm_utils.auth_token()
    if user_data is None:
        return abort(401)

    detectors_raw = mongo.detectors.find({"location_id": location_id})
    detectors = [Detector(detector_row) for detector_row in detectors_raw]

    return success_response(prepare_piechart_data(detectors))


@app.route("/get_detector_with_logs/<detector_id>", methods=["GET"])
def get_detector_with_logs(detector_id):
    user_data = cm_utils.auth_token()
    if user_data is None:
        return abort(401)

    detector_raw = mongo.detectors.find_one({"detector_id": detector_id})
    if detector_raw is None:
        return error_response("/get_detector_with_logs", "detector is None")
    detector = Detector(detector_raw)

    return success_response( detector.get_json())


@app.route("/get_location_monthly_stat_by_type/<location_id>", methods=["POST"])
def get_location_monthly_stat_by_type(location_id):
    user_data = cm_utils.auth_token()
    if user_data is None:
        return abort(401)

    (type, ) = cm_utils.validate_json(["type"]) 

    location_raw = mongo.locations.find_one({"_id": ObjectId(location_id)})
    if location_raw is None:
        return error_response("/get_location_monthly_stat_by_type", "location is not found")
    location = Location(location_raw)

    stat = monthly_stat_by_type(location, type)
    
    return success_response( stat)


@app.route("/get_location_monthly_sums/<location_id>", methods=["POST"])
def get_monthly_sums(location_id):
    
    location_raw = mongo.locations.find_one({"_id": ObjectId(location_id)})
    if location_raw is None:
        return error_response("/get_location_monthly_sums", "location is not found")
    location = Location(location_raw)

    stats = monthly_stat(location)

    return success_response(stats)
