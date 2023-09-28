import datetime
from api.diagrams import monthly_sums_bar
def test_monthly_stat():
    input_logs = [{
            "location_id": "1",
            "detector_id": "2",
            "type": "electricity",
            "timestamp": datetime.datetime(2020, 5, 17),
            "value": 2
        },
        {
            "location_id": "1",
            "detector_id": "2",
            "type": "electricity",
            "timestamp": datetime.datetime(2020, 5, 17),
            "value": 10
        },
        {
            "location_id": "1",
            "detector_id": "2",
            "type": "gas",
            "timestamp": datetime.datetime(2020, 5, 17),
            "value": 10
        },
        {
            "location_id": "1",
            "detector_id": "1",
            "type": "water",
            "timestamp": datetime.datetime.now(),
            "value": 2
        },
        {
            "location_id": "1",
            "detector_id": "2",
            "type": "water",
            "timestamp": datetime.datetime.now(),
            "value": 10
        },
        {
            "location_id": "1",
            "detector_id": "2",
            "type": "water",
            "timestamp": datetime.datetime.now(),
            "value": 20
        },
        {
            "location_id": "1",
            "detector_id": "2",
            "type": "water",
            "timestamp": datetime.datetime.now(),
            "value": 30
        },
        {
            "location_id": "1",
            "detector_id": "2",
            "type": "gas",
            "timestamp": datetime.datetime.now(),
            "value": 20
        },
        {
            "location_id": "1",
            "detector_id": "2",
            "type": "electricity",
            "timestamp": datetime.datetime.now(),
            "value": 30
        }
    ]
    response = monthly_sums_bar.monthly_stat(input_logs)
    for data in response:
        if data["month"] == 5:
            assert data["water"] == 0
            assert data["gas"] == 0
            assert data["electricity"] == 8
        if data["month"] == 9:
            assert data["water"] == 28
            assert data["gas"] == 10
            assert data["electricity"] == 20
