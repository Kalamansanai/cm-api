from cm_config import Logger


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


def user_data(creation_time: str, name: str, email: str, password_salt: str, password_hash: str, token: str):
    return {
        "creation_time": creation_time,
        "name": name,
        "email": email,
        "password_salt": password_salt,
        "password_hash": password_hash,
        "email_verification_token": token,
        "config": {}
    }
