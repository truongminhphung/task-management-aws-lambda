from commonUtil.constants.app_constants import app_constants
from commonUtil.constants.error_messages import error_messages

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