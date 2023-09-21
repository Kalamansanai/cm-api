from startup import app
from api.api_utils import auth_token, success_response, make_response
from cm_config import JWT_COOKIE_KEY
from api import login_required

from flask import request, abort

@app.route("/logout", methods=["GET"])
@login_required
def logout(_):
    response = make_response(success_response(
        "logout successfully"
    ))

    #TODO: need refactor. bad naming.
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
