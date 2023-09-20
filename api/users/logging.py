from startup import app, mongo
from api.api_utils import success_response, error_response, validate_json, hash as _hash, set_cookie_time, auth_token
from flask import abort, make_response
from cm_config import JWT_COOKIE_KEY, SESSION_PERSISTANCE_TIME
import jwt
from cm_config import JWT_SECRET

@app.route("/login", methods=["POST"])
def login():
    email, password = validate_json(["email", "password"])
    user = mongo.users.find_one({"email": email})
    if user is None:
        return abort(401)
    if not user["password_salt"] or not user["password_hash"]:
        return error_response("/login", "password error")

    hash = _hash(password + user["password_salt"])
    if user["password_hash"] != hash:
        return error_response("/login", "invalid password")

    return create_set_cookie_response(user=user)


@app.route("/logout", methods=["GET"])
def logout():
    user = auth_token()
    if user is None:
        return abort(401)

    response = make_response(success_response(
        "logout successfully"
    ))

    return set_cookie_time(response, 0)

def create_set_cookie_response(user: dict):

    user_id_string = str(user["_id"])

    user_data = {
        "id": user_id_string,
        "email": user["email"]
    }

    token = jwt.encode(payload=user_data, key=JWT_SECRET)

    response = make_response({
        "result": "ok",
        "data": token
        }
        )

    response.set_cookie(
        key=JWT_COOKIE_KEY,
        value=token,
        max_age=SESSION_PERSISTANCE_TIME,
        secure=True,
        samesite="None"
    )
    return response
