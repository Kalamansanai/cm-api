from startup import app, mongo
from api.api_utils import success_response, error_response, validate_json
from api import login_required


@app.route("/change_cost/<detector_id>", methods=["POST"])
@login_required
def change_cost_by_detector_id(detector_id):
    (new_cost,) = validate_json(["new_cost"])

    result = change_cost(detector_id, new_cost)

    if result.matched_count < 1:
        return error_response("not found any log with thid detector id")

    return success_response("cost changed succesfully")


def change_cost(detector_id, new_cost):
    return mongo.logs.update_many(
        {"detector_id": detector_id}, {"$set": {"cost": new_cost}}
    )
