def make_config(detector_ids):

    lines = [{
      "type": "monotone",
      "dataKey": detector_id,
      "stroke": "#82ca9d"} for detector_id in detector_ids]

    return {
        "type": "dashboard",
        "containerWidth": "100%",
        "containerHeight": "100%",
        "chartWidth": 50,
        "chartHeight": 0,
        "chartMargin": {
            "top": 5,
            "right": 30,
            "left": 20,
            "bottom": 5
        },
        "yAxis": {
            "type": "number"
        },
        "xAxis": {
            "datakey": "date"
        },""
        "cartesianGrid": {
            "strokeDashArray": "3 3"
        },
        "tooltip": {
            "enable": True
        },
        "legend": {
            "enable": True
        },
        "lines": lines

    }
