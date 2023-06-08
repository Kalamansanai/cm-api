from cm_config import Logger


def error_response(data, endpoint):
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