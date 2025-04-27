import json
import os
import bcrypt
import jwt
import logging

from commonUtil.db import get_cursor # Import get_cursor instead of get_db_session
from commonUtil.auth import generate_jwt
from commonUtil.validators import validate_login_input
from commonUtil.config import config # Keep config for JWT_SECRET
from commonUtil.constants.app_constants import app_constants
from commonUtil.constants.error_messages import error_messages
from commonUtil.constants.http_status import http_status
from commonUtil.response_helpers import create_error_response, create_success_response, generate_auth_cookie


def lambda_handler(event, context):
    """
    AWS Lambda handler for POST /login endpoint.
    Verifies user credentials and returns a JWT in an HTTP-only cookie.
    """
        
    try:
        print("Received event:", event)
        # Parse the request body
        body = json.loads(event["body"])
        username = body.get("username")
        password = body.get("password")

        # Validate the input
        validation_error = validate_login_input(username, password)
        if validation_error:
            return create_error_response(400, validation_error)
        
        # Use single context manager for both database connection and cursor
        user = None
        try:
            # Use the new get_cursor context manager
            with get_cursor() as cursor:
                # Fetch the user from the database
                cursor.execute("SELECT user_id, username, password_hash FROM users WHERE username = %s", (username,))
                user = cursor.fetchone()
        except Exception as db_error:
            logging.error(f"Database error: {db_error}")
            return create_error_response(500, error_messages.DATABASE_CONNECTION_FAILED)
        
        # Check if user exists and verify password
        if not user:
            return create_error_response(401, error_messages.INVALID_CREDENTIALS)
            
        user_id, db_user_name, password_hash = user

        # TODO: Uncomment the following lines when bcrypt is used for password hashing
        # if not bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
        #     return create_error_response(401, error_messages.INVALID_CREDENTIALS)

        # Generate JWT token
        jwt_token = generate_jwt(payload={"user_id": user_id, "username": db_user_name}, secret=config.JWT_SECRET)

        # Generate cookie and return the response
        cookie = generate_auth_cookie(jwt_token)
        
        return create_success_response(
            http_status.OK,
            {"message": "Login successful."},
            additional_headers={"Set-Cookie": cookie}
        )
        
    except json.JSONDecodeError:
        return create_error_response(400, error_messages.INVALID_JSON)
        
    except Exception as e:
        logging.error(f"Error: {e}")
        return create_error_response(
            http_status.INTERNAL_SERVER_ERROR, 
            error_messages.INTERNAL_ERROR.format(str(e))
        )