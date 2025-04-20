
# Centralized error messages with meaningful names
"""
    if not username or not password:
        return error_messages.MISSING_FIELDS
    
    if len(username) < 3 or len(username) > 20:
        return "Username must be between 3 and 20 characters."
    
    if len(password) < 8 or len(password) > 20:
        return "Password must be between 8 and 20 characters."
    
    if not any(char.isdigit() for char in password):
        return "Password must contain at least one digit."
    
    if not any(char.isalpha() for char in password):
        return "Password must contain at least one letter."
    
    # if not any(char in "!@#$%^&*()-_=+[]{};:,.<>?/" for char in password):
    #     return "Password must contain at least one special character."
    
    return None
"""
class ErrorMessages:
    INVALID_CREDENTIALS = "Invalid username or password"
    INVALID_JSON = "Invalid JSON format"
    MISSING_FIELDS = "Username and password are required"
    INVALID_USERNAME = "Username must be between 3 and 20 characters"
    INVALID_PASSWORD = "Password must be between 8 and 20 characters"
    PASSWORD_NO_DIGIT = "Password must contain at least one digit"
    PASSWORD_NO_LETTER = "Password must contain at least one letter"
    PASSWORD_NO_SPECIAL = "Password must contain at least one special character"
    USER_NOT_FOUND = "User not found"
    USER_ALREADY_EXISTS = "User already exists"
    DATABASE_CONNECTION_FAILED = "Database connection failed"
    USER_CREATION_FAILED = "User creation failed"
    USER_UPDATE_FAILED = "User update failed"
    USER_DELETION_FAILED = "User deletion failed"
    INTERNAL_ERROR = "Internal server error: {}"  # Placeholder for dynamic error details


# Singleton instance for convenience
error_messages = ErrorMessages()