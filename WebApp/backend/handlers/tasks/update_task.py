import logging
import jwt
from datetime import datetime
import json

from commonUtil.response_helpers import create_error_response, create_success_response
from commonUtil.constants.error_messages import error_messages
from commonUtil.constants.http_status import http_status
from commonUtil.constants.app_constants import TaskStatus
from commonUtil.db import get_cursor
from commonUtil.auth import validate_jwt
from commonUtil.config import config
from commonUtil.auth import extract_token_from_cookie


logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    AWS Lambda handler for PATCH /tasks/{task_id} endpoint.
    Updates a task for the authenticated user.
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
        
        # Parse and validate request data
        try:
            body = json.loads(event["body"])
        except json.JSONDecodeError:
            return create_error_response(http_status.BAD_REQUEST, error_messages.INVALID_JSON)
        if not body:
            return create_error_response(http_status.BAD_REQUEST, error_messages.MISSING_REQUEST_BODY)
        
        # validate input parameters
        
        description = body.get("description")
        due_date = body.get("due_date")  # YYYY-MM-DD format
        status = body.get("status")
        # Validate input parameters
        if due_date:
            validation_error = validate_due_date(due_date)
            if validation_error:
                return create_error_response(http_status.BAD_REQUEST, validation_error)
        if status and status not in [s.value for s in TaskStatus]:
            return create_error_response(http_status.BAD_REQUEST, error_messages.INVALID_TASK_STATUS)
        
        with get_cursor() as cursor:
            # Check if the task exists and belongs to the user
            cursor.execute(
                "SELECT task_id FROM tasks WHERE task_id = %s AND user_id = %s",
                (task_id, user_id)
            )
            task = cursor.fetchone()
            
            if not task:
                return create_error_response(http_status.NOT_FOUND, error_messages.TASK_NOT_FOUND)
            
            # Update the task in the database
            update_query = """
                UPDATE tasks 
                SET description = COALESCE(%s, description), 
                    due_date = COALESCE(%s, due_date), 
                    status = COALESCE(%s, status) 
                WHERE task_id = %s AND user_id = %s
            """
            cursor.execute(
                update_query,
                (description, due_date, status, task_id, user_id)
            )
            
            # Commit the changes
            cursor.connection.commit()
            if cursor.rowcount == 0:
                return create_error_response(http_status.NOT_FOUND, error_messages.TASK_UPDATE_FAILED)
            # Fetch the updated task
            cursor.execute(
                "SELECT task_id, description, due_date, status FROM tasks WHERE task_id = %s",
                (task_id,)
            )
            task = cursor.fetchone()
            if not task:
                return create_error_response(http_status.NOT_FOUND, error_messages.TASK_NOT_FOUND)
            # Transform to a dictionary for the response
            task_data = {
                "task_id": task[0],
                "description": task[1],
                "due_date": task[2].isoformat() if task[2] else None,
                "status": task[3]
            }
            return create_success_response(http_status.OK, task_data)
    except Exception as e:
        logger.error(f"Error updating task: {str(e)}")
        return create_error_response(http_status.INTERNAL_SERVER_ERROR, error_messages.INTERNAL_ERROR.format(str(e)))
        
        
def validate_due_date(due_date):
    """Validate the due date format and check if it's in the past."""
    try:
        due_date_obj = datetime.strptime(due_date, "%Y-%m-%d")
        if due_date_obj < datetime.now():
            return error_messages.DUE_DATE_IN_PAST
        return None
    except ValueError:
        return error_messages.INVALID_DATE_FORMAT
