from cm_config import Logger
from cm_models import User
from cm_utils import utc_now, create_token

def error_response(endpoint: str, data):
    """
    Generic error response
    """
    Logger.error(f"error response - endpoint: {endpoint} - data: {data}")
    return {"result": "error", "data": data}


def success_response(endpoint: str, data):
    """
    Generic success response
    """
    Logger.info(f"success response - endpoint: {endpoint} - data: {data}")
    return {"result": "ok", "data": data}


def user_data(name: str, email: str, password_salt: str, password_hash: str):
    return {
        "creation_time": utc_now(),
        "name": name,
        "email": email,
        "password_salt": password_salt,
        "password_hash": password_hash,
        "email_verification_token": create_token()
    }