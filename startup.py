from flask import Flask
from flask_cors import CORS
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import certifi
from cm_config import DB_NAME

from cm_config import PRODUCTION, MONGO_URI
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

ca = certifi.where()
mongo = MongoClient(MONGO_URI, tlsCAFile=ca)[DB_NAME]

ALLOWED_ORIGINS = ["*"] if PRODUCTION else ["*"]
CORS(app, resources={"/*": {"origins": ALLOWED_ORIGINS}},
     supports_credentials=True)
