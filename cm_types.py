from cm_config import Logger, JWT_COOKIE_KEY, SESSION_PERSISTANCE_TIME
from flask import make_response, request

def error_response(endpoint: str, data):
    # Logger.error(f"error response - endpoint: {endpoint} - data: {data}")
    return {"result": "error", "data": data}

def user_data(creation_time: str, name: str, email: str, password_salt: str, password_hash: str, token: str):
    return {
        "creation_time": creation_time,
        "name": name,
        "email": email,
        "password_salt": password_salt,
        "password_hash": password_hash,
        "email_verification_token": token,
        "config": {},
    }

def success_response(endpoint, data):
    token = request.cookies.get(JWT_COOKIE_KEY)

    response = make_response({"result": "ok", "data": data})

    response.set_cookie(
        key=JWT_COOKIE_KEY,
        value=token,
        max_age= SESSION_PERSISTANCE_TIME,
        secure=True,
        samesite="None"
    )

    return response
