import jwt
import time
from commonUtil.constants.app_constants import app_constants


def generate_jwt(payload, secret) -> str:
    """
    Generates a JWT token with a 24-hour expiration time.
    """
    # Set the expiration time to 24 hours from now
    expiration_time = int(time.time()) + app_constants.JWT_EXPIRATION_TIME # 24 hours in seconds
    payload["exp"] = expiration_time
    # Generate the JWT token
    token = jwt.encode(payload, secret, algorithm=app_constants.JWT_ALGORITHM)
    return token

def validate_jwt(payload, secret):
    """Validates a JWT and returns the decoded payload."""
    