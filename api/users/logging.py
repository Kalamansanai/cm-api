from startup import app, mongo
import cm_utils
from cm_types import success_response, error_response
from flask import abort, make_response

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
        "logout successfully"
    ))

    return cm_utils.set_cookie_time(response, 0)
