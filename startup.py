import os

from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient

import certifi

from cm_config import MONGO_URI, MODE, DB_NAME, IMAGE_PATH

if(not os.path.exists(os.path.join(IMAGE_PATH, "images"))):
     os.mkdir(os.path.join(IMAGE_PATH, "images"))


app = Flask(__name__)

ca = certifi.where()
mongo = MongoClient(MONGO_URI, tlsCAFile=ca)[DB_NAME]

ALLOWED_ORIGINS = ["*"] 
if MODE == "dev":
     ALLOWED_ORIGINS = ["*"]
elif MODE == "prod":
     ALLOWED_ORIGINS = ["*"]
elif MODE == "demo":
     ALLOWED_ORIGINS = ["*"]

CORS(app, resources={"/*": {"origins": ALLOWED_ORIGINS}},
     supports_credentials=True)
