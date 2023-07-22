from hashlib import sha256
from secrets import token_hex
from time import time
from flask import abort, request, make_response
import jwt

from cm_config import JWT_SECRET, JWT_COOKIE_KEY
from cm_types import success_response


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


def create_set_cookie_response(user: dict):
    user_data = {key: value for key,
                 value in user.items() if key in ["creation_time", "name", "email"]}

    token = jwt.encode(payload=user_data, key=JWT_SECRET)

    response = make_response(success_response(
        "create_set_cookie_response", token))

    # TODO: make the token persistent
    response.set_cookie(
        key=JWT_COOKIE_KEY,
        value=token,
        max_age=None,
        secure=True,
        samesite="None"
    )
    return response


def set_cookie_time(time):

    token = request.cookies.get(JWT_COOKIE_KEY)

    response = make_response(success_response(
        "set_cookie_time", token
    ))

    response.set_cookie(
        key=JWT_COOKIE_KEY,
        value=token,
        max_age=0,
        secure=True,
        samesite="None"
    )

    return response


def create_delete_cookie_response():
    response = make_response(success_response(
        "/create_delete_cookie_token", "successfully logged out"))
    response.delete_cookie(JWT_COOKIE_KEY)
    return response


def auth_token():
    token = request.cookies.get(JWT_COOKIE_KEY)

    if token is None:
        return None

    value = jwt.decode(token, key=JWT_SECRET, algorithms=["HS256",])
    return value
