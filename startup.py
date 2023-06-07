from flask import Flask
from flask_cors import CORS
from cm_config import PRODUCTION

app = Flask(__name__)

ALLOWED_ORIGINS = ["https://tenderquery.com/*"] if PRODUCTION else ["*"]
CORS(app, resources={"/*": {"origins": ALLOWED_ORIGINS}})