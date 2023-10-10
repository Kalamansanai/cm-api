import datetime

import pytest

from api.diagrams import detector_lineplot
def test_make_config():
    detector_ids = ["64537"]
    expectedOutput = {
      "type": "monotone",
      "dataKey": "64537",
      "stroke": "#82ca9d"}
    response = detector_lineplot.make_config(detector_ids)
    assert len(response["lines"]) == 1
    assert response["lines"][0]["type"] == expectedOutput["type"]
    assert response["lines"][0]["dataKey"] == expectedOutput["dataKey"]
    assert response["lines"][0]["stroke"] == expectedOutput["stroke"]
def test_prepare_detector_lineplot_data_calculate():
    input = [{
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
        }
    ]
    assert detector_lineplot.prepare_detector_lineplot_data(input)[1] == 5
def test_prepare_detector_lineplot_data_calculate_without_measurement():
    input = [{
        "location_id": 1,
        "detector_id": 1,
        "type": "water",
        "timestamp": datetime.datetime.now(),
        "value": None
    },
    {
        "location_id": 1,
        "detector_id": 1,
        "type": "water",
        "timestamp": datetime.datetime.now(),
        "value": None
    }
    ]
    with pytest.raises(TypeError):
        detector_lineplot.prepare_detector_lineplot_data(input)
def test_prepare_detector_lineplot_data_date_view():
    input = [{
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
        "timestamp": datetime.datetime(2023,6,24,10,40),
        "value": 10
    }
    ]
    assert detector_lineplot.prepare_detector_lineplot_data(input)["date"] == "2023.06-10:40"

