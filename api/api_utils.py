from flask import request, make_response, abort
from cm_config import JWT_COOKIE_KEY, JWT_SECRET, SESSION_PERSISTANCE_TIME
from hashlib import sha256
from secrets import token_hex
from time import time
import jwt

def error_response(data):
    return {"result": "error", "data": data}


def success_response(data):
    token = request.cookies.get(JWT_COOKIE_KEY)

    response = make_response({"result": "ok", "data": data})

    if token is None:
        return response

    response.set_cookie(
        key=JWT_COOKIE_KEY,
        value=token,
        max_age= SESSION_PERSISTANCE_TIME,
        secure=True,
        samesite="None"
    )

    return response

def validate_json(keys: "list[str]") -> "tuple":
    json = request.get_json()
    if json is None or any([key not in json for key in keys]):
        abort(400, "invalid body format")
    return (json[key] for key in keys)


def create_token():
    return token_hex(32)  # create 256bit hex token


def hash(text):
    return sha256(bytes(text, "UTF-8")).hexdigest()


def utc_now():
    return int(time())


def auth_token():
    token = request.cookies.get(JWT_COOKIE_KEY)

    if token is None:
        return None

    value = jwt.decode(token, key=JWT_SECRET, algorithms=["HS256",])
    return value
