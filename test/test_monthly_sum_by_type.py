from api.diagrams import monthly_sum_by_type
import datetime
def test_monthly_sum_calculate_with_sortingMultipleTypes():
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
        }
    ]
    assert monthly_sum_by_type.monthly_sum_by_type(input, "water") == 10
    assert monthly_sum_by_type.monthly_sum_by_type(input, "gas") == 20
    assert monthly_sum_by_type.monthly_sum_by_type(input, "electricity") == 30
def test_monthly_sum_calculate_with_previousMonths():
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
    assert monthly_sum_by_type.monthly_sum_by_type(input, "water") == 10
    assert monthly_sum_by_type.monthly_sum_by_type(input, "gas") == 20
    assert monthly_sum_by_type.monthly_sum_by_type(input, "electricity") == 30
