from flask import request, abort
from startup import app
from cm_types import success_response

data = {
    "2023.02.18.": 150,
    "2023.02.19.": 158,
    "2023.02.20.": 179,
    "2023.02.21.": 183,
    "2023.02.22.": 189,
    "2023.02.23.": 194,
    "2023.02.24.": 212,
    "2023.02.25.": 226,
}

@app.route("/get_data")
def get_data():
    return success_response(data)