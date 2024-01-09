import datetime
from api.diagrams import linechart_with_prev_month
def test_prepare_detector_lineplot_data_multipleDays_inOneMonth():
    input = [
    {
        "location_id": 1,
        "detector_id": 1,
        "type": "water",
        "timestamp": datetime.datetime(2023, 6, 24, 10, 10),
        "value": 5
    },
    {
        "location_id": 1,
        "detector_id": 1,
        "type": "water",
        "timestamp": datetime.datetime(2023, 6, 24, 10, 10),
        "value": 10
    }
    ]
    response = linechart_with_prev_month.prepare_detector_lineplot_data(input)
    assert response["date"] == "06.24-10:10"
    assert response[1] == 5
def test_prepare_detector_lineplot_data_multipleDays_inMultipleMonth():
    input = [
        {
            "location_id": 1,
            "detector_id": 1,
            "type": "water",
            "timestamp": datetime.datetime(2023, 6, 24, 10, 10),
            "value": 5
        },
        {
            "location_id": 1,
            "detector_id": 1,
            "type": "water",
            "timestamp": datetime.datetime(2023, 6, 25, 10, 10),
            "value": 10
        },
        {
            "location_id": 1,
            "detector_id": 1,
            "type": "water",
            "timestamp": datetime.datetime(2023, 7, 24, 10, 10),
            "value": 15
        },
        {
            "location_id": 1,
            "detector_id": 1,
            "type": "water",
            "timestamp": datetime.datetime(2023, 8, 24, 10, 10),
            "value": 10
        }
    ]
    response = linechart_with_prev_month.prepare_detector_lineplot_data(input)
    assert response["date"] == "07.24-10:10"
    assert response[1] == 15
