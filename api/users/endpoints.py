from flask import request, abort
from startup import app
from startup import mongo
from bson.objectid import ObjectId
from domain.user import User
from api.api_utils import success_response, auth_token, validate_json


@app.route("/user", methods=["GET"])
def get_user():
    user_cookie = auth_token()
    if user_cookie is None:
        abort(401)

    user = mongo.users.find_one({"_id": ObjectId(user_cookie["id"])})
    user = User(user)

    return success_response(user.get_json())


@app.route("/user", methods=["DELETE"])
def delete_users():
    # TODO: delete all of its detectors
    user = auth_token()
    if user is None:
        return abort(401)

    name = request.json["name"]
    mongo.users.delete_one({"name": name})
    
    return success_response("User successfully deleted.")




@app.route("/set_config", methods=["POST"])
def set_user_config():
    (new_config, ) = validate_json(["new_config"])
    user_data = auth_token()
    if user_data is None:
        return abort(401)

    mongo.users.update_one({"email": user_data['email']}, {
        "$set": {"config": new_config}})

    return success_response("config updated successfully")
