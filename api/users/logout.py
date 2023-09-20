from startup import app
from api.api_utils import auth_token, success_response, make_response
from cm_config import JWT_COOKIE_KEY

from flask import request, abort

@app.route("/logout", methods=["GET"])
def logout():
    user = auth_token()
    if user is None:
        return abort(401)

    response = make_response(success_response(
        "logout successfully"
    ))

    return set_cookie_time(response)

def set_cookie_time(response):
    token = request.cookies.get(JWT_COOKIE_KEY)

    response.set_cookie(
        key=JWT_COOKIE_KEY,
        value=token,
        max_age=0,
        secure=True,
        samesite="None"
    )

    return response
