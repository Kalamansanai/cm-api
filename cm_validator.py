import numpy as np
from cm_config import Logger
from startup import mongo
from datetime import datetime
from sklearn.linear_model import LinearRegression
import time

model = LinearRegression()

# TODO: Limit historical data.
# NOTE: Ha megváltozik a detektálási intervallum, akkor nem pontos


def validate(detector, new_value, threshold=0.2):
    try:
        new_value = int(new_value)
    except ValueError:
        Logger.info("int(new_value)")
        return False

    current_time = round(time.time() * 1000)

    X = []
    y = []
    for log in detector["logs"]:
        X.append(int(log["timestamp"].timestamp() * 1000))
        y.append(log["value"])

    if len(X) < 2:  # Can not do much with that
        Logger.info("Validator --- len < 2")
        return True

    if new_value < y[-1]:
        Logger.info("Validator --- new_value < y[-1]")
        return False

    X = np.array(X)
    y = np.array(y)

    model.fit(X.reshape(-1, 1), y)

    predicted_value = model.predict(np.array([[current_time]]))

    diff = abs(new_value - predicted_value)
    average = (new_value + predicted_value) / 2
    percent_diff = (diff / average) * 100

    return True if percent_diff <= threshold else False
