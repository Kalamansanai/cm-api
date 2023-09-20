from startup import app
from cm_config import APP_HOST, APP_PORT, MODE

from api.detectors import endpoints, send_image, add_detector, export, check_state
from api.users import register, endpoints, login, logout
from api.diagrams import detector_lineplot, locaion_monthly_pie, monthly_sum_by_type, monthly_sums_bar
from api.locations import endpoints

@app.route("/")
def hello_w():
    return "Szia Lajos" 


if __name__ == "__main__":
    if MODE == "prod":
        # TODO: use a real server, not the build in
        app.run(host=APP_HOST, port=APP_PORT, ssl_context=('library/cert.pem', 'library/privkey.pem'))
    else:
        app.run(host=APP_HOST, port=APP_PORT)
