from startup import app
import endpoints_detector
import endpoints_client
import endpoints_user

@app.route("/")
def hello_world():
    return "<p>Szia Lajos!</p>"