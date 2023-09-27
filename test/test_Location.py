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
        "detectors":[{
                "_id": 1,
                "location_id": 2,
                "detector_id": "3",
                "detector_name": "test",
                "type": "test",
                "state": "init",
                "detector_config": {"char_num": 544}
        }],
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
    assert response["detectors"][0]["_id"] == 1
    assert response["monthly_logs"][0]["month"] == 6
def test_get_json(testLocation_json):
    test_Location = Location(testLocation_json)
    response = test_Location.get_json()
    assert response["id"] == "1"
    assert response["user_id"] == "2"
    assert response["name"] == "test"
    assert response["detectors"][0]["id"] == "1"
    assert response["monthly_logs"][0]["month"] == 6
def test_id_unique(testLocation_json):
    test_Location = Location(testLocation_json)
    id_true = "2"
    id_false = "3"
    response_true = test_Location.id_unique(id_true)
    response_false = test_Location.id_unique(id_false)
    assert response_true is True
    assert response_false is False
