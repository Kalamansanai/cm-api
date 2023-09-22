from startup import app, mongo
from domain.detector import Detector
from domain.log import Log
from datetime import datetime
from api.api_utils import success_response, error_response
from api import login_required

@app.route("/detector/<detector_id>/check_state")
@login_required
def detector_check_state(_, detector_id):
    detector_raw: dict | None = mongo.detectors.find_one({"detector_id": detector_id})
    if detector_raw is None:
        return error_response("no detector found")
    changed = check_and_update_detectors_state(detector_raw)
    return success_response(changed)

#TODO: refactor to user entity(detector.check_and_update_state())
def check_and_update_detectors_state(detector: Detector):
    changed = False

    if detector.detector_config.delay == "":
        return "no delay set"
    elif len(detector.logs) == 0:
        return "there is no log on this detector"

    photo_time = detector.detector_config.delay

    last_log: Log = detector.logs[-1]
    delay_time = photo_time * 0.01 * 3600 * 1000

    if datetime.now().timestamp() * 1000 - last_log.timestamp.timestamp() > delay_time:
        if detector.state != "sleep":
            # TODO: maybe if there is a lot of detectors, update_many could be better
            mongo.detectors.update_one(
                {"_id": detector.id},
                {"$set": {"state": "sleep"}}
            )
            changed = True

    return changed
