from startup import app
import endpoints_client
from cm_config import APP_HOST, APP_PORT, MODE

from api.detectors import send_image, add_detector, basic, export
from api.users import register, logging, endpoints

@app.route("/")
def hello_w():
    return "Szia Lajos" 


if __name__ == "__main__":
    if MODE == "prod":
        # TODO: use a real server, not the build in
        app.run(host=APP_HOST, port=APP_PORT, ssl_context=('library/cert.pem', 'library/privkey.pem'))
    else:
        app.run(host=APP_HOST, port=APP_PORT)
