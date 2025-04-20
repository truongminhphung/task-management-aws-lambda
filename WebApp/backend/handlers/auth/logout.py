import json
from commonUtil.constants.http_status import http_status
from commonUtil.constants.app_constants import app_constants
from commonUtil.constants.error_messages import error_messages
from commonUtil.response_helpers import create_error_response, create_success_response


def lambda_handler(event, context):
    """
    AWS Lambda handler for POST /logout endpoint.
    Clears the JWT cookie to log the user out.

    Args:
        event (dict): The Lambda event object containing request details.
        context (object): The Lambda context object providing runtime information.

    Returns:
        dict: A response object with status code, body, and headers.
    """
    try:
        # Define the cookie with immediate expiration to delete it
        cookie = (
            "token=; "  # Clear the token value
            "HttpOnly; "  # Security attribute
            f"Path={app_constants.COOKIE_PATH}; "  # Match the cookie's original path
            "Max-Age=0; "  # Expire immediately
            f"SameSite={app_constants.COOKIE_SAMESITE}"  # Match original SameSite policy
        )
        return create_success_response(
            http_status.OK,
            "Logout successful",
            additional_headers={
                "Set-Cookie": cookie,  # Set the cookie in the response
                "Content-Type": "application/json"
            }
        )
        
    except Exception as e:
        # Handle any exceptions that may occur
        return create_error_response(http_status.INTERNAL_SERVER_ERROR, error_messages.INTERNAL_ERROR.format(str(e)))
    