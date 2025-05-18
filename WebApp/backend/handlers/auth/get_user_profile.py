import jwt
import logging
import json
import base64
import boto3

from commonUtil.response_helpers import create_error_response, create_success_response
from commonUtil.constants.error_messages import error_messages
from commonUtil.constants.http_status import http_status
from commonUtil.auth import validate_jwt, extract_token_from_cookie
from commonUtil.db import get_cursor
from commonUtil.config import config


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    """
    AWS Lambda handler for GET /profile endpoint.
    Retrieves the user's profile information.

    Args:
        event (dict): The Lambda event object containing request details.
        context (object): The Lambda context object providing runtime information.

    Returns:
        dict: A response object with status code, body, and headers.
    """
    
    try:
        # Authentication - Extract and validate token
        token = extract_token_from_cookie(event.get("headers", {}))
        if not token:
            return create_error_response(http_status.UNAUTHORIZED, error_messages.MISSING_AUTH_TOKEN)
        
        try:
            payload = validate_jwt(token, config.JWT_SECRET)
            user_id = payload.get("user_id")
            if not user_id:
                return create_error_response(http_status.UNAUTHORIZED, error_messages.INVALID_CREDENTIALS)
        except jwt.ExpiredSignatureError:
            return create_error_response(http_status.UNAUTHORIZED, error_messages.JWT_EXPIRED)
        except jwt.InvalidTokenError:
            return create_error_response(http_status.UNAUTHORIZED, error_messages.JWT_INVALID)
        
        # Fetch user profile from the database
        with get_cursor() as cursor:
            cursor.execute(
                """SELECT u.email, u.username, up.profile_image_url 
                FROM users u LEFT JOIN user_profiles up ON u.user_id = up.user_id
                WHERE u.user_id = %s""",
                (user_id,)
            )
            user_profile = cursor.fetchone()
            if not user_profile:
                return create_error_response(http_status.NOT_FOUND, error_messages.USER_NOT_FOUND)
        email, username, profile_image_url = user_profile
        # Decode the base64 image if it exists
        if profile_image_url:
            s3_client = boto3.client("s3")
            bucket_name = config.S3_BUCKET_NAME
            object_key = f"profile_images/{user_id}.jpg"
            try:
                response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
                profile_image_data = response["Body"].read()
                profile_image_url = f"data:image/jpeg;base64,{base64.b64encode(profile_image_data).decode('utf-8')}"
            except Exception as e:
                logger.error(f"Error fetching image from S3: {str(e)}")
                return create_error_response(http_status.INTERNAL_SERVER_ERROR, error_messages.INTERNAL_ERROR.format(str(e)))
        else:
            profile_image_url = None
        
        result = create_success_response(http_status.OK, {
            "email": email,
            "username": username,
            "profile_image_url": profile_image_url
        })
        return result
    except Exception as e:
        logger.error(f"Error fetching user profile: {str(e)}")
        return create_error_response(http_status.INTERNAL_SERVER_ERROR, error_messages.INTERNAL_ERROR.format(str(e)))
    