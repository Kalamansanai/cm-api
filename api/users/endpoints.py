from flask import request, abort
from startup import app
from cm_types import success_response
from startup import mongo
import cm_utils
from bson.objectid import ObjectId
from cm_config import SESSION_PERSISTANCE_TIME, Logger 
from domain.user import User


@app.route("/user", methods=["GET"])
def get_user():
    user_cookie = cm_utils.auth_token()
    if user_cookie is None:
        abort(401)

    user = mongo.users.find_one({"_id": ObjectId(user_cookie["id"])})
    user = User(user)

    return success_response(user.get_json())


@app.route("/user", methods=["DELETE"])
def delete_users():
    # TODO: delete all of its detectors
    user = cm_utils.auth_token()
    if user is None:
        return abort(401)

    name = request.json["name"]
    mongo.users.delete_one({"name": name})
    
    return success_response("User successfully deleted.")




@app.route("/set_config", methods=["POST"])
def set_user_config():
    (new_config, ) = cm_utils.validate_json(["new_config"])
    user_data = cm_utils.auth_token()
    if user_data is None:
        return abort(401)

    mongo.users.update_one({"email": user_data['email']}, {
        "$set": {"config": new_config}})

    return success_response("config updated successfully")
