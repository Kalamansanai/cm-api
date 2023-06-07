from datetime import datetime

from flask import request, abort
from startup import app

from PIL import Image 
import PIL

from cm_config import IMAGE_PATH, DETECTOR_CONFIG
from cm_types import success_response, error_response

@app.route("/send_image", methods=["POST"])
def send_image():
    try:
        img = Image.open(request.json["image"])
        img.save(f"{IMAGE_PATH}/{datetime.now()}")
        return success_response("success")
    except BaseException as err:
        return error_response(f"(try-except)send_image --- Unexpected {err=}, {type(err)=}")

@app.route("/get_current_time")
def get_current_time():
    try:
        return success_response(datetime.now())
    except BaseException as err:
        return error_response(f"(try-except)get_current_time --- Unexpected {err=}, {type(err)=}")

@app.route("/get_config")
def get_config():
    try:
        return success_response(DETECTOR_CONFIG)
    except BaseException as err:
        return error_response(f"(try-except)get_config --- Unexpected {err=}, {type(err)=}")

@app.route("/set_config")
def set_config():
    try:
        #TODO: implement setting
        return success_response("success")
    except BaseException as err:
        return error_response(f"(try-except)set_config --- Unexpected {err=}, {type(err)=}")