from domain.detector import Detector
from startup import app, mongo
from api.api_utils import error_response, success_response
from api import login_required

@app.route("/get_detectors_by_location/<location_id>", methods=["GET"])
@login_required
def get_detectors_by_location(_, location_id):
    detectors_raw = mongo.detectors.find({"location_id":location_id})
    if detectors_raw is None:
        return error_response("no detector found")

    detectors_resp = [Detector(detector_raw).get_json() for detector_raw in detectors_raw]

    return success_response(detectors_resp)
