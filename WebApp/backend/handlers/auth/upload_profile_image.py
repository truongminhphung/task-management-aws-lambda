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


def process_image_data(image_data):
    """Process and decode base64 image data."""
    try:
        # Remove "data:image/jpeg;base64," prefix and decode
        image_bytes = base64.b64decode(image_data.split(",")[1])
        return image_bytes
    except Exception as e:
        logger.error(f"Error decoding image data: {str(e)}")
        raise ValueError("Invalid image data format")


def upload_image_to_s3(image_bytes, user_id):
    """Upload image to S3 and return the image URL."""
    try:
        s3_client = boto3.client('s3')
        bucket_name = config.S3_BUCKET_NAME
        object_key = f"profile_images/{user_id}.jpg"
        
        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=image_bytes,
            ContentType="image/jpeg",
            ACL="public-read"
        )
        
        image_url = f"https://{bucket_name}.s3.amazonaws.com/{object_key}"
        logger.info(f"Image uploaded successfully: {image_url}")
        return image_url
    except Exception as e:
        logger.error(f"Error uploading to S3: {str(e)}")
        raise


def update_profile_image_url(user_id, image_url):
    """Update the user's profile image URL in the database."""
    with get_cursor() as cursor:
        cursor.execute(
            "UPDATE user_profiles SET profile_image_url = %s WHERE user_id = %s",
            (image_url, user_id)
        )
        cursor.connection.commit()
        if cursor.rowcount == 0:
            raise ValueError("Failed to update profile image URL in database")


def lambda_handler(event, context):
    """
    Lambda function to handle the upload of a profile image.
    
    This function processes a request to update a user's profile image. It:
    1. Authenticates the user via JWT token
    2. Extracts the base64 encoded image from the request
    3. Uploads the image to S3
    4. Updates the user's profile record with the new image URL
    
    Args:
        event (dict): API Gateway Lambda Proxy Input Format containing request data
                     including headers and body with the image data
        context (object): Lambda Context runtime methods and attributes
    
    Returns:
        dict: API Gateway Lambda Proxy Output Format containing response with
              status code, headers, and body (success or error message)
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

        # Parse request data
        body = json.loads(event["body"])
        image_data = body.get("image")
        if not image_data:
            return create_error_response(http_status.BAD_REQUEST, error_messages.MISSING_IMAGE_DATA)
        
        # Process image data
        try:
            image_bytes = process_image_data(image_data)
        except ValueError:
            return create_error_response(http_status.BAD_REQUEST, error_messages.INVALID_IMAGE_DATA)
        
        # Upload to S3
        try:
            image_url = upload_image_to_s3(image_bytes, user_id)
        except Exception as e:
            logger.error(f"S3 upload error: {str(e)}")
            return create_error_response(http_status.INTERNAL_SERVER_ERROR, error_messages.INTERNAL_ERROR.format("Failed to upload image"))
        
        # Update database
        try:
            update_profile_image_url(user_id, image_url)
        except ValueError:
            return create_error_response(http_status.INTERNAL_SERVER_ERROR, error_messages.PROFILE_UPDATE_FAILED)
        
        return create_success_response(http_status.OK, {"message": "Profile image uploaded successfully.", "image_url": image_url})
    
    except Exception as e:
        logger.error(f"Error uploading profile image: {str(e)}")
        return create_error_response(http_status.INTERNAL_SERVER_ERROR, error_messages.INTERNAL_ERROR.format(str(e)))
