from startup import app, mongo
from cm_types import error_response, success_response
import cm_utils
from plot_preprocess import prepare_lineplot_data, prepare_piechart_data


@app.route("/get_logs_for_plot/<detector_id>", methods=["POST"])
def get_logs_for_plot(detector_id):
    user_data = cm_utils.auth_token()
    if user_data is None:
        return error_response("/get_user_pie", "no user signed in")

    logs = mongo.logs.find_one({"detector_id": detector_id})

    return success_response("get_logs_for_plot", prepare_lineplot_data(logs))


@app.route("/get_user_pie", methods=["GET"])
def get_user_pie():
    user_data = cm_utils.auth_token()
    if user_data is None:
        return error_response("/get_user_pie", "no user signed in")

    user = mongo.users.find_one(
        {"email": user_data["email"]}
    )

    return success_response("get_user_pie", prepare_piechart_data(user))
