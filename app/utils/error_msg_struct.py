from fastapi.responses import JSONResponse

def fetch_error_message_struct(status_code, message=None):
   
    default_messages = {
        200: "The request was successful",
        400: "The request contains invalid parameters. Please review your request and try again.",
        404: "The requested resource could not be found. Please check the URL and try again.",
        409: "There was a conflict while processing your request. Please resolve the conflict and try again.",
        500: "An internal server error occurred. Please try again later.",
        503: "The service is currently unavailable. Please try again later."
    }
    
    # Use the custom message if provided, otherwise use the default
    error_message = message if message else default_messages.get(status_code, "An error occurred")
    
   
    error_msg = {
        "error": {
            "name": "error",
            "message": error_message,
            "reason": "",
            "type": "",
            "statusCode": str(status_code)
        }
    }
    success_msg={
        "success": {
            "message": error_message,
            "reason": "",
            "type": "",
            "statusCode": str(status_code)
        }
    }

    if status_code == 200:
        success_msg["success"]["reason"] = "Request successful"
        success_msg["success"]["type"] = "valid result"
    if status_code == 400:
        error_msg["error"]["reason"] = "The request contains invalid parameters. Please review your request and try again."
        error_msg["error"]["type"] = "Invalid input"
    elif status_code == 404:
        error_msg["error"]["reason"] = "The requested resource could not be found. Please check the URL and try again."
        error_msg["error"]["type"] = "Data not found"
    elif status_code == 409:
        error_msg["error"]["reason"] = "There was a conflict while processing your request. Please resolve the conflict and try again."
        error_msg["error"]["type"] = "Upstream Error"
    elif status_code == 500:
        error_msg["error"]["reason"] = "An internal server error occurred. Please try again later."
        error_msg["error"]["type"] = "Internal Server Error"
    elif status_code == 503:
        error_msg["error"]["reason"] = "The service is currently unavailable. Please try again later."
        error_msg["error"]["type"] = "Service Unavailable"
    
    if status_code == 200:
        return JSONResponse(content=success_msg, status_code=200)
    # Return the JSON response with the constructed error message and status code
    return JSONResponse(content=error_msg, status_code=status_code)