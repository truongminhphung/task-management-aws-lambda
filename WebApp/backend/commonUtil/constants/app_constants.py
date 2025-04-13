
# Application-specific constants
class AppConstants:
    JWT_EXPIRATION_TIME = 86400  # 24 hours in seconds
    JWT_ALGORITHM = "HS256"  # JWT signing algorithm
    MIN_USERNAME_LENGTH = 3  # Minimum length for usernames
    MAX_USERNAME_LENGTH = 20  # Maximum length for usernames
    MIN_PASSWORD_LENGTH = 8  # Minimum length for passwords
    MAX_PASSWORD_LENGTH = 20  # Maximum length for passwords
    COOKIE_PATH = "/"  # Path for the cookie
    COOKIE_SAMESITE = "Strict"  # SameSite attribute for the cookie


# singleton instance for application constants
app_constants = AppConstants()