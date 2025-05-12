import jwt
import json
import logging
from uuid import uuid4

from commonUtil.response_helpers import create_error_response, create_success_response
from commonUtil.constants.error_messages import error_messages
from commonUtil.constants.http_status import http_status
from commonUtil.constants.app_constants import TaskStatus
from commonUtil.db import get_cursor # Import get_cursor instead of get_db_session
from commonUtil.validators import validate_task_input
from commonUtil.auth import validate_jwt
from commonUtil.config import config

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, _context):
    """
    AWS Lambda handler for POST /tasks endpoint.
    Creates a new task for the authenticated user.

    Args:
        event (dict): The Lambda event object containing request details.
        context (object): The Lambda context object providing runtime information.

    Returns:
        dict: A response object with status code, body, and headers.
    """

    try:
        # Parse and validate request data
        body = json.loads(event["body"])
        description = body.get("description")
        due_date = body.get("due_date")  # YYYY-MM-DD format
        status = body.get("status", TaskStatus.PENDING.value)

        # Validate input parameters
        validation_error = validate_task_input(description, due_date, status)
        if validation_error:
            return create_error_response(http_status.BAD_REQUEST, validation_error)
        
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
        
        # Create the task in database
        try:
            with get_cursor() as cursor:
                # Insert task and get ID in one transaction
                task_id = str(uuid4().hex)  # Generate a unique task ID
                # Use a parameterized query to prevent SQL injection
                cursor.execute(
                    "INSERT INTO tasks (task_id, user_id, description, due_date, status) VALUES (%s, %s, %s, %s, %s)",
                    (task_id, user_id, description, due_date, status)
                )
                cursor.connection.commit()
                
                # task_id = cursor.fetchone()[0]
                # return create_success_response(http_status.CREATED, {"task_id": task_id})
                cursor.execute(
                    "SELECT task_id, description, due_date, status, created_at FROM tasks WHERE task_id = %s",
                    (task_id,)
                )

                task = cursor.fetchone()
            
            # Transform to a dictionary for the response
            task_data = {
                "task_id": task[0],
                "description": task[1],
                "due_date": task[2].isoformat() if task[2] else None,
                "status": task[3],
                "created_at": task[4].isoformat() if task[4] else None
            }
            
            # Commit the transaction to ensure the data is saved
            
            return create_success_response(http_status.CREATED, {"task": task_data})
        except Exception as e:
            logger.error(f"Database error creating task: {e}")
            return create_error_response(
                http_status.INTERNAL_SERVER_ERROR, 
                error_messages.TASK_CREATION_FAILED
            )

    except Exception as e:
        logger.error(f"Error creating task: {e}")
        return create_error_response(
            http_status.INTERNAL_SERVER_ERROR, 
            error_messages.INTERNAL_ERROR.format(str(e))
        )

def extract_token_from_cookie(event):
    """Extract JWT token from request cookies."""
    auth_header = event.get("headers", {}).get("Cookie")
    if not auth_header:
        return None
        
    for cookie in auth_header.split(";"):
        if cookie.strip().startswith("token="):
            return cookie.strip().split("=")[1]
    return None
