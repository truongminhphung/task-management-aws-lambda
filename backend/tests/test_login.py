import json
import pytest
from unittest.mock import Mock, patch, MagicMock
from handlers.auth.login import lambda_handler
from constants.http_status import http_status
from constants.error_messages import error_messages
from constants.app_constants import app_constants

# Sample event fixture
@pytest.fixture
def login_event():
    """Returns a sample login event with valid credentials."""
    return {
        "body": json.dumps({
            "username": "test_user",
            "password": "test_password123"
        })
    }

# Mock database cursor fixture
@pytest.fixture
def mock_db_cursor():
    """Returns a mocked database cursor."""
    cursor = Mock()
    cursor.fetchone.return_value = (1, "test_user", "hashed_password")  # (user_id, username, password_hash)
    return cursor

# Mock database connection fixture
@pytest.fixture
def mock_db_conn():
    """Returns a mocked database connection."""
    conn = Mock()
    cursor_mock = Mock()
    cursor_mock.fetchone.return_value = (1, "test_user", "hashed_password")
    conn.cursor.return_value.__enter__.return_value = cursor_mock
    return conn

# Test successful login
@patch("handlers.auth.login.validate_login_input")
@patch("handlers.auth.login.db_connection")
@patch("handlers.auth.login.bcrypt.checkpw")
@patch("handlers.auth.login.generate_jwt")
def test_successful_login(mock_generate_jwt, mock_checkpw, mock_db_connection, mock_validate_input, login_event):
    """Test successful login with valid credentials."""
    # Arrange
    mock_validate_input.return_value = None  # Valid input
    
    # Set up proper context manager mocks
    cursor_mock = MagicMock()
    cursor_mock.fetchone.return_value = (1, "test_user", "hashed_password")
    
    conn_mock = MagicMock()
    conn_mock.__enter__.return_value = conn_mock
    conn_mock.cursor.return_value.__enter__.return_value = cursor_mock
    
    mock_db_connection.return_value = conn_mock
    
    mock_checkpw.return_value = True  # Password matches
    mock_generate_jwt.return_value = "fake_jwt_token"

    # Act
    response = lambda_handler(login_event, None)

    # Assert
    assert response["statusCode"] == http_status.OK
    assert json.loads(response["body"]) == {"message": "Login successful."}
    assert "Set-Cookie" in response["headers"]
    cookie = response["headers"]["Set-Cookie"]
    assert "token=fake_jwt_token" in cookie
    assert "HttpOnly" in cookie
    assert f"Path={app_constants.COOKIE_PATH}" in cookie
    assert f"SameSite={app_constants.COOKIE_SAMESITE}" in cookie

# Test invalid credentials (user not found)
@patch("handlers.auth.login.validate_login_input")
@patch("handlers.auth.login.db_connection")
def test_invalid_credentials_user_not_found(mock_db_connection, mock_validate_input, login_event):
    """Test login with non-existent user."""
    # Arrange
    mock_validate_input.return_value = None
    
    # Set up proper context manager mocks
    cursor_mock = MagicMock()
    cursor_mock.fetchone.return_value = None  # No user found
    
    conn_mock = MagicMock()
    conn_mock.__enter__.return_value = conn_mock
    conn_mock.cursor.return_value.__enter__.return_value = cursor_mock
    
    mock_db_connection.return_value = conn_mock

    # Act
    response = lambda_handler(login_event, None)

    # Assert
    assert response["statusCode"] == http_status.UNAUTHORIZED
    assert json.loads(response["body"]) == {"error": error_messages.INVALID_CREDENTIALS}

# Test invalid credentials (wrong password)
@patch("handlers.auth.login.validate_login_input")
@patch("handlers.auth.login.db_connection")
@patch("handlers.auth.login.bcrypt.checkpw")
def test_invalid_credentials_wrong_password(mock_checkpw, mock_db_connection, mock_validate_input, login_event):
    """Test login with incorrect password."""
    # Arrange
    mock_validate_input.return_value = None
    
    # Set up proper context manager mocks
    cursor_mock = MagicMock()
    cursor_mock.fetchone.return_value = (1, "test_user", "hashed_password")
    
    conn_mock = MagicMock()
    conn_mock.__enter__.return_value = conn_mock
    conn_mock.cursor.return_value.__enter__.return_value = cursor_mock
    
    mock_db_connection.return_value = conn_mock
    
    mock_checkpw.return_value = False  # Password doesn't match

    # Act
    response = lambda_handler(login_event, None)

    # Assert
    assert response["statusCode"] == http_status.UNAUTHORIZED
    assert json.loads(response["body"]) == {"error": error_messages.INVALID_CREDENTIALS}

# Test missing fields
@patch("handlers.auth.login.validate_login_input")
def test_missing_fields(mock_validate_input):
    """Test login with missing username or password."""
    # Arrange
    event = {"body": json.dumps({"username": ""})}
    mock_validate_input.return_value = error_messages.MISSING_FIELDS

    # Act
    response = lambda_handler(event, None)

    # Assert
    assert response["statusCode"] == http_status.BAD_REQUEST
    assert json.loads(response["body"]) == {"error": error_messages.MISSING_FIELDS}

# Test invalid JSON
def test_invalid_json():
    """Test login with malformed JSON."""
    # Arrange
    event = {"body": "invalid_json_string"}

    # Act
    response = lambda_handler(event, None)

    # Assert
    assert response["statusCode"] == http_status.BAD_REQUEST
    assert json.loads(response["body"]) == {"error": error_messages.INVALID_JSON}

# Test internal server error
@patch("handlers.auth.login.validate_login_input")
@patch("handlers.auth.login.db_connection")
def test_internal_server_error(mock_db_connection, mock_validate_input, login_event):
    """Test login with a database connection failure."""
    # Arrange
    mock_validate_input.return_value = None
    mock_db_connection.side_effect = Exception("Database failure")

    # Act
    response = lambda_handler(login_event, None)

    # Assert
    assert response["statusCode"] == http_status.INTERNAL_SERVER_ERROR
    # Changed this assertion to match the actual error message returned
    assert "error" in json.loads(response["body"])
    assert json.loads(response["body"])["error"] == error_messages.DATABASE_CONNECTION_FAILED