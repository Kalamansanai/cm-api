import pytest
from domain.detector import Detector
from domain.location import Monthly_log,Location,Consumption_values
import test.test_Detector
@pytest.fixture()
def testLocation_json():
    return {
        "_id": 1,
        "user_id": "2",
        "name": "test",
        "monthly_logs": [{"month": 6,
                         "values": {"water": 100,
                                    "electricity": 120,
                                    "gas": 230
                        }
        }]
    }
def test_get_db(testLocation_json):
    test_Location = Location(testLocation_json)
    response = test_Location.get_db()
    assert response["user_id"] == "2"
    assert response["name"] == "test"
    assert response["monthly_logs"][0]["month"] == 6
def test_get_json(testLocation_json):
    test_Location = Location(testLocation_json)
    response = test_Location.get_json()
    assert response["id"] == "1"
    assert response["user_id"] == "2"
    assert response["name"] == "test"
    assert response["monthly_logs"][0]["month"] == 6

