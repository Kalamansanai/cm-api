from startup import app
from startup import mongo
from domain.user import User
from api.api_utils import success_response, auth_token, validate_json
from api import login_required

from flask import request, abort
from bson.objectid import ObjectId


@app.route("/user", methods=["GET"])
@login_required
def get_user(user_cookie):
    user = mongo.users.find_one({"_id": ObjectId(user_cookie["id"])})
    user = User(user)

    return success_response(user.get_json())


@app.route("/user", methods=["DELETE"])
@login_required
def delete_users(_):
    # TODO: delete all of its detectors

    name = request.json["name"]
    mongo.users.delete_one({"name": name})
    
    return success_response("User successfully deleted.")


@app.route("/set_config", methods=["POST"])
@login_required
def set_user_config(user_data):
    (new_config, ) = validate_json(["new_config"])

    mongo.users.update_one({"email": user_data['email']}, {
        "$set": {"config": new_config}})

    return success_response("config updated successfully")
