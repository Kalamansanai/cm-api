from hashlib import sha256

import pytest

from api import api_utils
from time import time
def test_error_response():
    data = {
        "type": "monotone",
        "dataKey": "65423"
    }
    response = api_utils.error_response(data)
    assert response["result"] == "error"
    assert response["data"]["type"] == "monotone"
    assert response["data"]["dataKey"] == "65423"
def test_success_response_without_token():
    data = {
        "type": "monotone",
        "dataKey": "65423"
    }
    with pytest.raises(Exception):
        api_utils.success_response(data)
def test_validate_json_without_json():
    data = ["keys", "test"]
    with pytest.raises(Exception):
        api_utils.validate_json(data)
def test_create_token():
    token = api_utils.create_token()
    assert len(token) == 64
def test_hash():
    text = "test"
    test = sha256(bytes("test", "UTF-8")).hexdigest()
    response = api_utils.hash(text)
    assert test == response
def test_utc_now():
    now = int(time())
    assert api_utils.utc_now() == now
def test_auth_token_without_token():
    with pytest.raises(Exception):
        api_utils.auth_token()
