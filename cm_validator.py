import numpy as np
from startup import mongo
from datetime import datetime
from sklearn.linear_model import LinearRegression

model = LinearRegression()

# TODO: Limit historical data.
# NOTE: Ha megváltozik a detektálási intervallum, akkor nem pontos
def validate(id, time, value, threshold=0.2):
    X = []
    y = []
    for log in mongo.logs.find_one({"detector_id": id})["logs"]:
        X.append(int(log["timestamp"].timestamp() * 1000))
        y.append(log["value"])

    if len(X) < 2: # Can not do much with that
        return True

    if value < y[-1]:
        return False

    X = np.array(X)
    y = np.array(y)

    model.fit(X.reshape(-1, 1), y)

    predicted_value = model.predict(np.array([[time]]))

    diff = abs(value - predicted_value)
    average = (value + predicted_value) / 2
    percent_diff = (diff / average) * 100

    return True if percent_diff <= threshold else False