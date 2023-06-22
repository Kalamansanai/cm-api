from hashlib import sha256
from secrets import token_hex
from time import time
from flask import abort, request, make_response
import jwt

from cm_config import Logger, JWT_SECRET, JWT_COOKIE_KEY, SESSION_COOKIE_HTTPS_ONLY
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
        secure=SESSION_COOKIE_HTTPS_ONLY
    )
    return response
