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
    return jwt.decode(payload, secret, algorithms=[app_constants.JWT_ALGORITHM])


def extract_token_from_cookie(headers):
    """Extract JWT token from request cookies or Authorization header."""
    # Check if token is in cookies
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
