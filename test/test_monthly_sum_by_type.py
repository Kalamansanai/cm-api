from api.diagrams import monthly_sum_by_type
import datetime
def test_monthly_sum():
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
        "detector_id": "1",
        "type": "gas",
        "timestamp": datetime.datetime.now(),
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
    input_water = "water"
    input_gas = "gas"
    input_electricity = "electricity"
    assert monthly_sum_by_type.monthly_sum_by_type(input_logs,input_water) == 28
    assert monthly_sum_by_type.monthly_sum_by_type(input_logs,input_gas) == 18
    assert monthly_sum_by_type.monthly_sum_by_type(input_logs,input_electricity) == 20
