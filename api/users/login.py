from startup import app, mongo
from api.api_utils import error_response, validate_json
from domain.user import User
from cm_config import JWT_COOKIE_KEY, SESSION_PERSISTANCE_TIME
from cm_config import JWT_SECRET

import jwt
from flask import abort, make_response

@app.route("/login", methods=["POST"])
def login():
    email, password = validate_json(["email", "password"])
    user_raw = mongo.users.find_one({"email": email})
    if user_raw is None:
        return abort(401)

    user = User(user_raw)

    if not user.same_password(password):
        return error_response("invalid password")

    return create_set_cookie_response(user)

def create_set_cookie_response(user: User):

    token = jwt.encode(payload={
        "id": str(user.id),
        "email": user.email
    }, key=JWT_SECRET)

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
