from functools import wraps
from api.api_utils import auth_token, error_response

def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        user_data = auth_token()
        if user_data is None:
            return error_response("/add_detector", "no user signed in")
        return func(user_data, *args, **kwargs)
    return decorated_function
