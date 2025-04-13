import json
import pytest
from unittest.mock import patch
from handlers.auth.logout import lambda_handler
from constants.http_status import http_status
from constants.error_messages import error_messages
from constants.app_constants import app_constants

# Sample event fixture
@pytest.fixture
def logout_event():
    """Returns a sample logout event."""
    return {}

# Test successful logout
def test_successful_logout(logout_event):
    """Test that logout returns successful response with cookie cleared."""
    # Act
    response = lambda_handler(logout_event, None)
    # Assert
    assert response["statusCode"] == http_status.OK
    assert json.loads(response["body"]) == "Logout successful"
    
    # Check cookie header
    assert "Set-Cookie" in response["headers"]
    cookie = response["headers"]["Set-Cookie"]
    assert "token=" in cookie  # Token should be emptied
    assert "HttpOnly" in cookie
    assert f"Path={app_constants.COOKIE_PATH}" in cookie
    assert "Max-Age=0" in cookie  # Cookie should expire immediately
    assert f"SameSite={app_constants.COOKIE_SAMESITE}" in cookie
    
    # Check content type header
    assert response["headers"]["Content-Type"] == "application/json"

# Test internal server error handling
@patch("handlers.auth.logout.create_success_response")
def test_internal_server_error(mock_create_success_response, logout_event):
    """Test error handling when an exception occurs."""
    # Arrange
    mock_create_success_response.side_effect = Exception("Unexpected error")
    
    # Act
    response = lambda_handler(logout_event, None)
    
    # Assert
    assert response["statusCode"] == http_status.INTERNAL_SERVER_ERROR
    error_message = json.loads(response["body"])["error"]
    assert error_message.startswith(error_messages.INTERNAL_ERROR.split("{}")[0])
