from cm_config import MODE
from domain.detector import detector_valid

from functools import wraps
from api.api_utils import auth_token, error_response

def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        user_data = auth_token()
        if user_data is None:
            return error_response("no user signed in")
        return func(user_data, *args, **kwargs)
    return decorated_function

def detector_id_validation_required(func):
    """ Only usable if the func get the detector_id in paramaters """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if MODE == "prod" and not detector_valid(*args, **kwargs):
            return error_response("detector is not valid")
        return func(*args, **kwargs)
    return decorated_function
