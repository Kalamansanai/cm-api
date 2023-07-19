from startup import mongo


def id_uniqueness(user_email, detector_id):
    user = mongo.users.find_one(
        {"email": user_email}
    )

    detectors = user["detectors"]

    for detector in detectors:
        if detector["detector_id"] == detector_id:
            return True

    return False
