import datetime
from api.diagrams import locaion_monthly_pie

def test_prepare_piechart_data():
    input_logs = [{
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
    }]
    response = locaion_monthly_pie.prepare_piechart_data(input_logs)
    for data in response:
        if data["id"] == "water":
            assert data["label"] == 8
