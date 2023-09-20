from startup import app, mongo
from domain.user import data_for_db_creation
from api.api_utils import success_response, error_response, validate_json, create_token, hash as _hash, utc_now

@app.route("/register", methods=["POST"])
def add_user():
    name, email, password = validate_json(
        ["name", "email", "password"])

    user = mongo.users.find_one({"email": email})
    if user is not None:
        return error_response("/user", "email already registered")

    #TODO: refactor this to the user entity(create_user)
    user: dict = {}
    salt = create_token()
    hash = _hash(password + salt)
    user = data_for_db_creation(utc_now(), name, email,
                     salt, hash, create_token())

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
