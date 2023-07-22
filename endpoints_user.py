from flask import request
from startup import app
from cm_types import success_response, error_response, user_data
from startup import mongo
import cm_utils
from datetime import datetime


@app.route("/register", methods=["POST"])
def add_user():
    try:
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

        id = mongo.users.insert_one(user).inserted_id

        # TODO: need to make the verification email send

        return success_response("/add_user", f"{id}")
    except BaseException as err:
        return error_response("/add_user", f"Unexpected {err=}, {type(err)=}")


@app.route("/user", methods=["GET"])
def get_user():
    try:
        user = cm_utils.auth_token()
        if user is None:
            return error_response("/get_user", "no user signed in")

        user = mongo.users.find_one({"email": user["email"]})

        ignored_fields = ["_id", "password_hash",
                          "password_salt", "email_verification_token"]
        user_data = {key: value for key,
                     value in user.items() if key not in ignored_fields}

        return success_response("/get_user", user_data)
    except BaseException as err:
        return error_response("/get_user", f"Unexpected {err=}, {type(err)=}")


@app.route("/user", methods=["DELETE"])
def delete_users():
    try:
        user = cm_utils.auth_token()
        if user is None:
            return error_response("/get_user", "no user signed in")

        name = request.json["name"]
        mongo.users.delete_one({"name": name})
        return success_response("/delete_user", "User successfully deleted.")
    except BaseException as err:
        return error_response("/delete_user", f"Unexpected {err=}, {type(err)=}")


@app.route("/login", methods=["POST"])
def login():
    try:
        email, password = cm_utils.validate_json(["email", "password"])
        user = mongo.users.find_one({"email": email})
        if user is None:
            return error_response("/login", "this email has not been registered")
        if not user["password_salt"] or not user["password_hash"]:
            return error_response("/login", "password error")

        hash = cm_utils.hash(password + user["password_salt"])
        if user["password_hash"] != hash:
            return error_response("/login", "invalid password")

        return cm_utils.create_set_cookie_response(user=user)

    except BaseException as err:
        return error_response("/login", f"Unexpected {err=}, {type(err)=}")


@app.route("/logout", methods=["GET"])
def logout():
    try:
        user = cm_utils.auth_token()
        if user is None:
            return error_response("/logout", "no user signed in")

        response = cm_utils.set_cookie_time(datetime.now())
        return response
    except BaseException as err:
        return error_response("/logout", f"Unexpected {err=}, {type(err)=}")


@app.route("/set_config", methods=["POST"])
def set_user_config():
    try:
        (new_config, ) = cm_utils.validate_json(["new_config"])
        user_data = cm_utils.auth_token()
        if user_data is None:
            return error_response("/set_config", "no user signed in")

        mongo.users.update_one({"email": user_data['email']}, {
            "$set": {"config": new_config}})

        return success_response("/set_config", "config updated successfully")
    except BaseException as err:
        return error_response("/set_config", f"Unexpected {err=}, {type(err)=}")
