import json
from constants.app_constants import app_constants
from constants.http_status import http_status

def create_error_response(status_code, error_message):
    """
    Create a standardized error response
    """
    return {
        "statusCode": status_code,
        "body": json.dumps({"error": error_message}),
        "headers": get_default_headers()
    }

def create_success_response(status_code, body, additional_headers=None):
    """
    Create a standardized success response
    """
    headers = get_default_headers()
    if additional_headers:
        headers.update(additional_headers)
    
    return {
        "statusCode": status_code,
        "body": json.dumps(body),
        "headers": headers
    }

def get_default_headers():
    """
    Get default headers for API responses including CORS settings
    """
    return {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",  # Adjust as needed for CORS
        "Access-Control-Allow-Credentials": "true"
    }

def generate_auth_cookie(jwt_token):
    """
    Generate a standardized authentication cookie string
    """
    return (
        f"token={jwt_token}; "
        "HttpOnly; "
        f"Path={app_constants.COOKIE_PATH}; "
        f"Max-age={app_constants.JWT_EXPIRATION_TIME}; "
        f"SameSite={app_constants.COOKIE_SAMESITE}; "
    )