from flask import abort, request, make_response
from cm_detector import check_and_update_detectors_state
from cm_models import User
from startup import app
from cm_types import success_response, error_response, user_data
from startup import mongo
import cm_utils
from datetime import datetime
from bson.objectid import ObjectId
from cm_config import SESSION_PERSISTANCE_TIME, JWT_COOKIE_KEY, Logger 


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

    return success_response("/add_user", f"{id}")


@app.route("/user", methods=["GET"])
def get_user():
    user_cookie = cm_utils.auth_token()
    if user_cookie is None:
        abort(401)

    user = mongo.users.find_one({"_id": ObjectId(user_cookie["id"])})
    user = User(user)

    return success_response("/get_user", user.get_json())


@app.route("/user", methods=["DELETE"])
def delete_users():
    # TODO: delete all of its detectors
    user = cm_utils.auth_token()
    if user is None:
        return abort(401)

    name = request.json["name"]
    mongo.users.delete_one({"name": name})
    
    return success_response("/delete_user", "User successfully deleted.")


@app.route("/login", methods=["POST"])
def login():
    email, password = cm_utils.validate_json(["email", "password"])
    user = mongo.users.find_one({"email": email})
    if user is None:
        return abort(401)
    if not user["password_salt"] or not user["password_hash"]:
        return error_response("/login", "password error")

    hash = cm_utils.hash(password + user["password_salt"])
    if user["password_hash"] != hash:
        return error_response("/login", "invalid password")

    return cm_utils.create_set_cookie_response(user=user)


@app.route("/logout", methods=["GET"])
def logout():
    user = cm_utils.auth_token()
    if user is None:
        return abort(401)

    response = make_response(success_response(
        "/logout", "logout successfully"
    ))

    return cm_utils.set_cookie_time(response, 0)


@app.route("/set_config", methods=["POST"])
def set_user_config():
    (new_config, ) = cm_utils.validate_json(["new_config"])
    user_data = cm_utils.auth_token()
    if user_data is None:
        return abort(401)

    mongo.users.update_one({"email": user_data['email']}, {
        "$set": {"config": new_config}})

    return success_response("/set_config", "config updated successfully")
