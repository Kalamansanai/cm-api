from startup import app
import endpoints_detector
import endpoints_client
import endpoints_user
from cm_config import APP_HOST, APP_PORT, MODE

@app.route("/")
def hello_w():
    return "Szia Lajos" 


if __name__ == "__main__":
    if MODE == "prod":
        # TODO: use a real server, not the build in
        app.run(host=APP_HOST, port=APP_PORT, ssl_context=('library/cert.pem', 'library/privkey.pem'))
    else:
        app.run(host=APP_HOST, port=APP_PORT)
