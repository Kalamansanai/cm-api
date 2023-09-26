import datetime

from domain.log import Log
def test_get_json():
    test_log_json = {
        "timestamp": datetime.datetime.now(),
        "value": 1
    }
    test_Log = Log(test_log_json)
    response = test_Log.get_json()
    assert response["timestamp"] == datetime.datetime.now()
    assert response["value"] == 1

