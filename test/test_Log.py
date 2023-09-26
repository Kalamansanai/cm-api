import datetime

from domain.log import Log
def test_get_json():
    test_log_json = {
        "location_id": 2,
        "detector_id": 3,
        "type": "test",
        "timestamp": datetime.datetime.now(),
        "value": 1
    }
    test_Log = Log(test_log_json)
    response = test_Log.get_json()
    assert response["location_id"] == 2
    assert response["detector_id"] == 3
    assert response["type"] == "test"
    assert response["timestamp"] == datetime.datetime.now()
    assert response["value"] == 1

