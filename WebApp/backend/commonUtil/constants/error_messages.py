
# Centralized error messages with meaningful names
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
    MISSING_DESCRIPTION = "Task description is required"
    INVALID_DESCRIPTION = "Task description must be between 1 and 255 characters"
    INVALID_TASK_STATUS = "Invalid task status"
    INVALID_DUE_DATE = "Invalid due date format. Expected format: YYYY-MM-DD"
    DUE_DATE_IN_PAST = "Due date cannot be in the past"
    MISSING_AUTH_TOKEN = "Missing authentication token in request headers"
    JWT_EXPIRED = "JWT token has expired"
    JWT_INVALID = "JWT token is invalid"
    TASK_CREATION_FAILED = "Task creation failed"
    TASK_CREATION_SUCCESS = "Task created successfully"
    MISSING_TASK_ID = "Task ID is required"
    TASK_NOT_FOUND = "Task not found"
    TASK_UPDATE_FAILED = "Task update failed"
    TASK_DELETION_FAILED = "Task deletion failed"
    MISSING_REQUEST_BODY = "Missing request body"
    INVALID_DATE_FORMAT = "Invalid date format. Expected format: YYYY-MM-DD"

# Singleton instance for convenience
error_messages = ErrorMessages()