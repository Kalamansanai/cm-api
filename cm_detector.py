from startup import mongo
from datetime import datetime


def id_uniqueness(user_email, detector_id):
    user = mongo.users.find_one(
        {"email": user_email}
    )

    detectors = user["detectors"]

    for detector in detectors:
        if detector["detector_id"] == detector_id:
            return True

    return False


def check_state(detector_id):
    # TODO: refactor this, this func needs to be used in several places in the code,
    # so its need to be as optimal as it can (now it has two db query)
    logs_obj = mongo.logs.find_one(
        {"detector_id": detector_id}
    )

    user = mongo.users.find_one(
        {"detectors.detector_id": detector_id}
    )

    for det in user["detectors"]:
        if det["detector_id"] == detector_id:
            photo_time = det["detector_config"]["delay"]

    last_log = logs_obj["logs"][-1]
    delay_time = photo_time * 3600 * 1000

    if datetime.now().timestamp() - last_log["timestamp"] > delay_time:
        mongo.users.update_one(
            {"detectors.detector_id": detector_id},
            {"$set": {"detectors.$.state": "sleep"}}
        )
        return True
    return False
