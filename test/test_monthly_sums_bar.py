import datetime
from api.diagrams import monthly_sums_bar
def test_monthly_stat():
    input_logs = [{
        "location_id": "1",
        "detector_id": "1",
        "type": "water",
        "timestamp": datetime.datetime.now().month,
        "value": 2
    },
        {
            "location_id": "1",
            "detector_id": "2",
            "type": "water",
            "timestamp": datetime.datetime.now().month,
            "value": 10
        },
        {
            "location_id": "1",
            "detector_id": "2",
            "type": "water",
            "timestamp": datetime.datetime.now().month,
            "value": 20
        },
        {
            "location_id": "1",
            "detector_id": "2",
            "type": "water",
            "timestamp": datetime.datetime.now().month,
            "value": 30
        },
        {
            "location_id": "1",
            "detector_id": "1",
            "type": "gas",
            "timestamp": datetime.datetime.now().month,
            "value": 2
        },
        {
            "location_id": "1",
            "detector_id": "2",
            "type": "electricity",
            "timestamp": datetime.datetime.now().month,
            "value": 10
        },
        {
            "location_id": "1",
            "detector_id": "2",
            "type": "gas",
            "timestamp": datetime.datetime.now().month,
            "value": 20
        },
        {
            "location_id": "1",
            "detector_id": "2",
            "type": "electricity",
            "timestamp": 7,
            "value": 30
        }
    ]
    response = monthly_sums_bar.monthly_stat(input_logs)
    for data in response:
        for (key, value) in data:
            if key == "water":
                assert value == 28
            if key == "electricity":
                assert value == 0
            if key == "gas":
                assert value == 18
