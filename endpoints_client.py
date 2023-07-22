from startup import app, mongo
from cm_types import error_response, success_response
import cm_utils
from plot_preprocess import adapt_data


@app.route("/get_logs_for_plot/<detector_id>", methods=["POST"])
def get_logs_for_plot(detector_id):
    (plot_type,) = cm_utils.validate_json(["plot_type"])

    logs = mongo.logs.find_one({"detector_id": detector_id})
    logs_data = {key: value for key,
                 value in logs.items() if key not in ["_id"]}

    plot_data = adapt_data(plot_type, logs_data)

    return success_response("get_logs_for_plot", plot_data)
