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
def test_prepare_lineplot_data():
    pass
