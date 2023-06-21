from flask import request
from startup import app
from cm_types import success_response, error_response, user_data
from cm_mongo import test_db as _test_db
from startup import mongo
from cm_config import Logger
from cm_utils import validate_json, create_token
import cm_utils


@app.route("/test_db")
def test_db():
    return success_response("/get_data", _test_db())


@app.route("/user", methods=["POST"])
def add_user():
    try:
        #TODO: would be better with validate_json bc the key validation, and more clean
        # name, email, password = validate_json(["name", "email", "password"])
        name = request.json["name"]
        email = request.json["email"]
        password = request.json["password"]
        
        user = mongo.cm_test.users.find_one({"email": email})
        if user is not None:
            return error_response("/user", "email already registered")
        user: dict = {}
        
        salt = create_token()
        hash = cm_utils.hash(password + salt)

        user = user_data(name, email, salt, hash)
        id = mongo.cm_test.users.insert_one(user).inserted_id

        #TODO: need to make the verification email send

        return success_response("/add_user", f"{id}")
    except BaseException as err:
        return error_response("/add_user", f"Unexpected {err=}, {type(err)=}" )

@app.route("/user", methods=["GET"])
def get_user():
    try:
        name = request.json["name"]
        user = mongo.cm_test.users.find_one({"name": name})
        return success_response("/get_user", {"id": str(user["_id"]), "username": user["name"], "age": user["age"]})
    except BaseException as err:
        return error_response("/get_user", f"Unexpected {err=}, {type(err)=}" )

@app.route("/user", methods=["DELETE"])
def delete_users():
    try:
        name = request.json["name"]
        mongo.cm_test.users.delete_one({"name": name})
        return success_response("/delete_user", "User successfully deleted.")
    except BaseException as err:
        return error_response("/delete_user", f"Unexpected {err=}, {type(err)=}" )
    
@app.route("/users", methods=["GET"])
def get_users():
    try:
        name = request.json["name"]
        users = mongo.cm_test.users.find({"name": name})
        users_res = {"users": []}
        for user in users:
            users_res["users"].append({"id": str(user["_id"]), "username": user["name"], "age": user["age"]})
        return success_response("/get_user", users_res)
        
    except BaseException as err:
        return error_response("/get_users", f"Unexpected {err=}, {type(err)=}" )