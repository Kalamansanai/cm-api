from startup import app
import endpoints_detector
import endpoints_client
import endpoints_user
from cm_config import APP_HOST, APP_PORT


if __name__ == "__main__":
    app.run(host=APP_HOST, port=APP_PORT)
