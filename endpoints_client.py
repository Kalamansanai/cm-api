from flask import request, abort
from startup import app
from cm_types import success_response
import json


def load_data():
    with open('mock_data.json') as file:
        # Load the JSON data into a dictionary
        return json.load(file)


@app.route("/get_data")
def get_data():
    return success_response("/get_data", load_data())
