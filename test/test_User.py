import datetime
import pytest
from api.api_utils import hash as _hash

from domain.user import User
@pytest.fixture()
def testUser():
    return {
        "_id": 1,
        "creation_time": datetime.datetime.now(),
        "name": "test",
        "email": "test@gmail.com",
        "password_salt": "43224",
        "password_hash": _hash("same" + "43224"),
        "config": ""
    }
def test_get_json(testUser):
    test_User = User(testUser)
    response = test_User.get_json()
    assert response["id"] == "1"
    assert response["creation_time"] == datetime.datetime.now()
    assert response["name"] == "test"
    assert response["email"] == "test@gmail.com"
    assert response["config"] == ""
    with pytest.raises(Exception):
        assert response["password_salt"] == "43224"
def test_same_password(testUser):
    test_User = User(testUser)
    test_password_good = "test"
    test_password_same = "same"
    response_false = test_User.same_password(test_password_good)
    response_true = test_User.same_password(test_password_same)
    assert response_false is False
    assert response_true is True



