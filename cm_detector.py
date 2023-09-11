from cm_models import Detector, Log
from startup import mongo
from datetime import datetime


def id_uniqueness(location_id, detector_id):
    detectors = mongo.detectors.find({"location_id": location_id})

    for detector in detectors:
        if detector["detector_id"] == detector_id:
            return True

    return False


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
