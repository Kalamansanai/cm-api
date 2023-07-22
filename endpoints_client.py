from flask import request, abort
from cm_config import Logger
from startup import app, mongo
from cm_types import error_response, success_response
import json
import cm_utils
from plot_preprocess import prepare_lineplot_data, prepare_piechart_data


def load_data():
    with open('mock_data.json') as file:
        # Load the JSON data into a dictionary
        return json.load(file)


@app.route("/get_data")
def get_data():
    return success_response("/get_data", load_data())


@app.route("/get_logs/<detector_id>")
def get_logs(detector_id):
    try:
        user = cm_utils.auth_token()
        if user is None:
            return error_response("/logout", "no user signed in")

        logs = mongo.logs.find_one({"detector_id": detector_id})

        logs_data = {key: value for key,
                     value in logs.items() if key not in ["_id"]}

        return success_response("/get_logs", logs_data)

    except BaseException as err:
        return error_response("/get_logs", f"Unexpected {err=}, {type(err)=}")


@app.route("/get_logs_for_plot/<detector_id>", methods=["POST"])
def get_logs_for_plot(detector_id):
    try:
        user_data = cm_utils.auth_token()
        if user_data is None:
            return error_response("/get_user_pie", "no user signed in")

        logs = mongo.logs.find_one({"detector_id": detector_id})
        logs_data = {key: value for key,
                     value in logs.items() if key not in ["_id"]}

        plot_data = prepare_lineplot_data(logs_data)

        return success_response("get_logs_for_plot", plot_data)

    except BaseException as err:
        return error_response("/get_logs_for_plot", f"Unexpected {err=}, {type(err)=}")


@app.route("/get_user_pie", methods=["GET"])
def get_user_pie():
    user_data = cm_utils.auth_token()
    if user_data is None:
        return error_response("/get_user_pie", "no user signed in")

    user = mongo.users.find_one(
        {"email": user_data["email"]}
    )

    return success_response("get_user_pie", prepare_piechart_data(user))
