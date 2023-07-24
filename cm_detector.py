from bson import ObjectId
from startup import mongo
from pymongo import ReturnDocument
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


def check_and_update_detectors_state(user_from_cookie):
    user = mongo.users.find_one({"_id": ObjectId(user_from_cookie["id"])})

    updated = False
    updated_detectors = []

    for detector in user["detectors"]:
        if "delay" not in detector["detector_config"].keys():
            updated_detectors.append(detector)
            continue

        # TODO: if the detector_id is the _id: ObjectId, then its good ig
        logs_obj = mongo.logs.find_one(
            {"detector_id": detector["detector_id"]}
        )

        photo_time = detector["detector_config"]["delay"]

        last_log = logs_obj["logs"][-1]
        delay_time = photo_time * 0.01 * 3600 * 1000

        if datetime.now().timestamp() - last_log["timestamp"].timestamp() > delay_time:
            updated = True
            if detector["state"] != "sleep":
                detector["state"] = "sleep"
        updated_detectors.append(detector)

    if updated:
        updated_user = mongo.users.find_one_and_update(
            {"_id": ObjectId(user_from_cookie["id"])},
            {"$set": {"detectors": updated_detectors}},
            return_document=ReturnDocument.AFTER
        )
        return updated_user

    return user
