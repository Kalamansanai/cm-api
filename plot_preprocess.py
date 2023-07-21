from cm_config import PLOT_COLOR


def line_data(data: dict):
    new_data = []

    new_data.append({
        "id": data["detector_id"],
        "color": PLOT_COLOR,
        "data": [{
            "x": log["timestamp"],
            "y": log["value"]
        } for log in data["logs"]]
    })

    return new_data


def bar_data(data: dict):
    new_data = []


def pie_data(data: dict):
    new_data = []


def adapt_data(type: str, data: dict):
    if type == "line":
        return line_data(data)
    elif type == "bar":
        return bar_data(data)
    elif type == "pie":
        return pie_data(data)
