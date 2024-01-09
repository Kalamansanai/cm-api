import datetime
from api.diagrams import locaion_monthly_pie
def test_prepare_piechart_data_calculate_with_MultipleMeasurements_inOneMonth():
    input = [
        {
            "location_id": 1,
            "detector_id": 1,
            "type": "water",
            "timestamp": datetime.datetime.now(),
            "value": 5
        },
        {
            "location_id": 1,
            "detector_id": 1,
            "type": "water",
            "timestamp": datetime.datetime.now(),
            "value": 10
        },
        {
            "location_id": 1,
            "detector_id": 1,
            "type": "gas",
            "timestamp": datetime.datetime.now(),
            "value": 10
        },
        {
            "location_id": 1,
            "detector_id": 1,
            "type": "gas",
            "timestamp": datetime.datetime.now(),
            "value": 20
        },
        {
            "location_id": 1,
            "detector_id": 1,
            "type": "electricity",
            "timestamp": datetime.datetime.now(),
            "value": 5
        },
        {
            "location_id": 1,
            "detector_id": 1,
            "type": "electricity",
            "timestamp": datetime.datetime.now(),
            "value": 30
        },
    ]
    response = locaion_monthly_pie.prepare_piechart_data(input)
    for restype in response:
        for name in restype:
            if name["id"] == "water":
                assert name["value"] == 10
            if name["id"] == "gas":
                assert name["value"] == 20
            if name["id"] == "electricity":
                assert name["value"] == 30
def test_prepare_piechart_data_calculate_with_previousMonths():
    input = [
        {
            "location_id": 1,
            "detector_id": 1,
            "type": "water",
            "timestamp": datetime.datetime(2023, 7, 24, 10, 10),
            "value": 5
        },
        {
            "location_id": 1,
            "detector_id": 1,
            "type": "water",
            "timestamp": datetime.datetime.now(),
            "value": 5
        },
        {
            "location_id": 1,
            "detector_id": 1,
            "type": "water",
            "timestamp": datetime.datetime.now(),
            "value": 10
        },
        {
            "location_id": 1,
            "detector_id": 1,
            "type": "gas",
            "timestamp": datetime.datetime(2023, 7, 24, 10, 10),
            "value": 14
        },
        {
            "location_id": 1,
            "detector_id": 1,
            "type": "gas",
            "timestamp": datetime.datetime.now(),
            "value": 10
        },
        {
            "location_id": 1,
            "detector_id": 1,
            "type": "gas",
            "timestamp": datetime.datetime.now(),
            "value": 20
        },
        {
            "location_id": 1,
            "detector_id": 1,
            "type": "electricity",
            "timestamp": datetime.datetime.now(),
            "value": 5
        },
        {
            "location_id": 1,
            "detector_id": 1,
            "type": "electricity",
            "timestamp": datetime.datetime.now(),
            "value": 30
        },
    ]
    response = locaion_monthly_pie.prepare_piechart_data(input)
    for restype in response:
        for name in restype:
            if name["id"] == "water":
                assert name["value"] == 10
            if name["id"] == "gas":
                assert name["value"] == 20
            if name["id"] == "electricity":
                assert name["value"] == 30

