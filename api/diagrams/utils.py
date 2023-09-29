def make_config(line_keys: list[str]):

    lines = [{
      "type": "monotone",
      "dataKey": line_key,
      "stroke": "#82ca9d"} for line_key in line_keys]

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
            "datakey": "day"
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
