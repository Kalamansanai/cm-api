from hashlib import sha256
from secrets import token_hex
from time import time
from flask import abort, request

from cm_config import Logger


def validate_json(*keys, json=None) -> "tuple":
    if json is None:
        json = request.get_json()

    # if json is None or any([key not in json for key in keys]):
    #     abort(400, "invalid body format")

    return (json[key] for key in keys)

def create_token():
    return token_hex(32)  # create 256bit hex token

def hash(text):
    return sha256(bytes(text, "UTF-8")).hexdigest()

def utc_now():
    return int(time())