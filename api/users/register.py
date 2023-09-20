from startup import app, mongo
import cm_utils
from cm_types import error_response, success_response, user_data

@app.route("/register", methods=["POST"])
def add_user():
    name, email, password = cm_utils.validate_json(
        ["name", "email", "password"])

    user = mongo.users.find_one({"email": email})
    if user is not None:
        return error_response("/user", "email already registered")
    user: dict = {}

    salt = cm_utils.create_token()
    hash = cm_utils.hash(password + salt)

    user = user_data(cm_utils.utc_now(), name, email,
                     salt, hash, cm_utils.create_token())

    user_id = mongo.users.insert_one(user).inserted_id

    location = {
        "user_id": user_id,
        "name": "init",
        "detectors": [],
        "monthly_logs": []
    }
    mongo.locations.insert_one(location)

    # TODO: need to make the verification email send

    return success_response(f"{id}")
