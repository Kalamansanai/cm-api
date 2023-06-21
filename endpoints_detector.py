from datetime import datetime

from flask import request
from startup import app

from PIL import Image 
import PIL

from cm_config import IMAGE_PATH, DETECTOR_CONFIG
from cm_types import success_response, error_response

@app.route("/send_image", methods=["POST"])
def send_image():
    try:
        img = Image.open(request.files["image"])
        img.save(f"{IMAGE_PATH}/{datetime.now()}.png")
        return success_response("/send_image", "success")
    except BaseException as err:
        return error_response("/send_image", f"Unexpected {err=}, {type(err)=}")

@app.route("/get_config")
def get_config():
    try:
        return success_response("/get_config", DETECTOR_CONFIG)
    except BaseException as err:
        return error_response("/get_config", f"Unexpected {err=}, {type(err)=}")

@app.route("/set_config")
def set_config():
    try:
        #TODO: implement setting
        return success_response("/set_config", "success")
    except BaseException as err:
        return error_response("/set_config", f"Unexpected {err=}, {type(err)=}")