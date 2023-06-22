from flask import make_response, request
from startup import app
from cm_types import success_response, error_response, user_data
from cm_mongo import test_db as _test_db
from startup import mongo
from cm_config import Logger
import cm_utils


@app.route("/test_db")
def test_db():
    return success_response("/get_data", _test_db())


@app.route("/user", methods=["POST"])
def add_user():
    try:
        name, email, password = cm_utils.validate_json(
            ["name", "email", "password"])

        user = mongo.cm_test.users.find_one({"email": email})
        if user is not None:
            return error_response("/user", "email already registered")
        user: dict = {}

        salt = cm_utils.create_token()
        hash = cm_utils.hash(password + salt)

        user = user_data(cm_utils.utc_now(), name, email,
                         salt, hash, cm_utils.create_token())

        id = mongo.cm_test.users.insert_one(user).inserted_id

        # TODO: need to make the verification email send

        return success_response("/add_user", f"{id}")
    except BaseException as err:
        return error_response("/add_user", f"Unexpected {err=}, {type(err)=}")


@app.route("/user", methods=["GET"])
def get_user():
    try:
        name = request.json["name"]
        user = mongo.cm_test.users.find_one({"name": name})
        return success_response("/get_user", {"id": str(user["_id"]), "username": user["name"], "age": user["age"]})
    except BaseException as err:
        return error_response("/get_user", f"Unexpected {err=}, {type(err)=}")


@app.route("/user", methods=["DELETE"])
def delete_users():
    try:
        name = request.json["name"]
        mongo.cm_test.users.delete_one({"name": name})
        return success_response("/delete_user", "User successfully deleted.")
    except BaseException as err:
        return error_response("/delete_user", f"Unexpected {err=}, {type(err)=}")


@app.route("/users", methods=["GET"])
def get_users():
    try:
        name = request.json["name"]
        users = mongo.cm_test.users.find({"name": name})
        users_res = {"users": []}
        for user in users:
            users_res["users"].append(
                {"id": str(user["_id"]), "username": user["name"], "age": user["age"]})
        return success_response("/get_user", users_res)

    except BaseException as err:
        return error_response("/get_users", f"Unexpected {err=}, {type(err)=}")


@app.route("/login", methods=["POST"])
def login():
    try:
        email, password = cm_utils.validate_json(["email", "password"])
        user = mongo.cm_test.users.find_one({"email": email})
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

        response = cm_utils.create_delete_cookie_token()
        return response
    except BaseException as err:
        return error_response("/logout", f"Unexpected {err=}, {type(err)=}")
