import logging
import jwt

from commonUtil.response_helpers import create_error_response, create_success_response
from commonUtil.constants.error_messages import error_messages
from commonUtil.constants.http_status import http_status
from commonUtil.db import get_cursor
from commonUtil.auth import validate_jwt
from commonUtil.config import config
from commonUtil.auth import extract_token_from_cookie

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    AWS Lambda handler for DELETE /tasks/{task_id} endpoint.
    Deletes a task for the authenticated user.

    Args:
        event (dict): The Lambda event object containing request details.
        context (object): The Lambda context object providing runtime information.

    Returns:
        dict: A response object with status code, body, and headers.
    """
    
    try:
        # Extract task_id from path parameters
        task_id = event["pathParameters"].get("task_id")
        if not task_id:
            return create_error_response(http_status.BAD_REQUEST, error_messages.MISSING_TASK_ID)
        
        # Extract token from cookie
        token = extract_token_from_cookie(event.get("headers", {}))
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
        
        with get_cursor() as cursor:
            # Check if the task exists and belongs to the user
            cursor.execute(
                "SELECT task_id FROM tasks WHERE task_id = %s AND user_id = %s",
                (task_id, user_id)
            )
            task = cursor.fetchone()
            
            if not task:
                return create_error_response(http_status.NOT_FOUND, error_messages.TASK_NOT_FOUND)
            
            # Delete the task
            cursor.execute(
                "DELETE FROM tasks WHERE task_id = %s",
                (task_id,)
            )
            cursor.connection.commit()
            if cursor.rowcount == 0:
                return create_error_response(http_status.INTERNAL_SERVER_ERROR, error_messages.TASK_DELETION_FAILED)
            return create_success_response(http_status.OK, {"message": "Task deleted successfully."})
    except Exception as e:
        logger.error(f"Error deleting task: {str(e)}")
        return create_error_response(http_status.INTERNAL_SERVER_ERROR, error_messages.INTERNAL_ERROR.format(str(e)))
            
