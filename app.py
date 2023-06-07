from startup import app
import endpoints_detector
import endpoints_client

@app.route("/")
def hello_world():
    return "<p>Szia Lajos!</p>"