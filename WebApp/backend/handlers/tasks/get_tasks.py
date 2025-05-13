import jwt
import logging
import json

from commonUtil.response_helpers import create_error_response, create_success_response
from commonUtil.constants.error_messages import error_messages
from commonUtil.constants.http_status import http_status
from commonUtil.auth import validate_jwt
from commonUtil.db import get_cursor
from commonUtil.config import config


logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Lambda function handler to get tasks from the database.
    """
    try:
        # Extract token from cookie
        token = extract_token_from_cookie(event)
        if not token:
            return create_error_response(http_status.UNAUTHORIZED, error_messages.MISSING_AUTH_TOKEN)

        # Verify token and get user_id
        try:
            payload = validate_jwt(token, config.JWT_SECRET)
            user_id = payload.get("user_id")
            if not user_id:
                return create_error_response(http_status.UNAUTHORIZED, error_messages.INVALID_CREDENTIALS)
        except jwt.ExpiredSignatureError:
            return create_error_response(http_status.UNAUTHORIZED, error_messages.JWT_EXPIRED)
        except jwt.InvalidTokenError:
            return create_error_response(http_status.UNAUTHORIZED, error_messages.JWT_INVALID)

        # Fetch tasks from the database
        with get_cursor() as cursor:
            cursor.execute(
                "SELECT task_id, description, due_date, status FROM tasks WHERE user_id = %s",
                (user_id,)
            )
            tasks = cursor.fetchall()
        
        # Format tasks for response
        formatted_tasks = [
            {
                "task_id": task[0],
                "description": task[1],
                "due_date": task[2].isoformat() if task[2] else None,
                "status": task[3]
            }
            for task in tasks
        ]
        return create_success_response(http_status.OK, {"tasks": formatted_tasks})
    except Exception as e:
        logger.error(f"Error fetching tasks: {str(e)}")
        return create_error_response(http_status.INTERNAL_SERVER_ERROR, error_messages.INTERNAL_ERROR.format(str(e)))


def extract_token_from_cookie(event):
    """Extract JWT token from request cookies or Authorization header."""
    # Check if token is in cookies
    headers = event.get("headers", {})
    cookie_header = headers.get("Cookie") or headers.get("cookie")
    if cookie_header:
        for cookie in cookie_header.split(";"):
            if cookie.strip().startswith("token="):
                return cookie.strip().split("=")[1]
    
    # Check if token is in Authorization header (Bearer token)
    auth_header = headers.get("Authorization") or headers.get("authorization")
    if auth_header and auth_header.startswith("Bearer "):
        return auth_header[7:]  # Remove "Bearer " prefix
    
    return None
