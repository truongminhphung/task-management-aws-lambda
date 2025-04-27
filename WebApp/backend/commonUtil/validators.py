import re
from datetime import datetime

from commonUtil.constants.app_constants import app_constants, TaskStatus
from commonUtil.constants.error_messages import error_messages
from commonUtil.constants.http_status import http_status

def validate_login_input(username, password):
    """
    Validate the login input.
    :param username: The username provided by the user.
    :param password: The password provided by the user.
    :return: None if valid else an error message.
    """

    if not username or not password:
        return error_messages.MISSING_FIELDS
    
    if len(username) < app_constants.MIN_USERNAME_LENGTH or len(username) > app_constants.MAX_USERNAME_LENGTH:
        return error_messages.INVALID_USERNAME
    
    if len(password) < app_constants.MIN_PASSWORD_LENGTH or len(password) > app_constants.MAX_PASSWORD_LENGTH:
        return error_messages.INVALID_PASSWORD
    
    if not any(char.isdigit() for char in password):
        return error_messages.PASSWORD_NO_DIGIT
    
    if not any(char.isalpha() for char in password):
        return error_messages.PASSWORD_NO_LETTER
    
    # if not any(char in "!@#$%^&*()-_=+[]{};:,.<>?/" for char in password):
    #     return error_messages.PASSWORD_NO_SPECIAL
    
    return None

def validate_task_input(description, due_date, status):
    """
    Validate the task input.
    :param description: The task description.
    :param due_date: The due date of the task.
    :param status: The status of the task.
    :return: None if valid else an error message.
    """

    if not description:
        return error_messages.MISSING_DESCRIPTION
    
    if len(description) < 1 or len(description) > 255:
        return error_messages.INVALID_DESCRIPTION
    
    if due_date and not re.match(r'^\d{4}-\d{2}-\d{2}$', due_date):
        return error_messages.INVALID_DUE_DATE
    if datetime.strptime(due_date, '%Y-%m-%d') < datetime.now():
        return error_messages.DUE_DATE_IN_PAST
    
    if status not in [status.value for status in TaskStatus]:
        return error_messages.INVALID_TASK_STATUS
    