def error_response(data):
    """
    Generic error response
    """
    return {"result": "error", "data": data}


def success_response(data):
    """
    Generic success response
    """
    return {"result": "ok", "data": data}