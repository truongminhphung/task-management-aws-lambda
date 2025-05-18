import os

class Config:
    """
    Configuration class for the application.
    """
    DB_HOST = os.environ.get("DB_HOST")
    DB_NAME = os.environ.get("DB_NAME")
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_PORT = os.environ.get("DB_PORT", "5432")  # Default to 5432 if not set

    JWT_SECRET = os.environ.get("JWT_SECRET")

    S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")

    @classmethod
    def get_db_connection_string(cls):
        """
        Returns the database connection string.
        """
        return f"postgresql://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_HOST}:{cls.DB_PORT}/{cls.DB_NAME}"
    
    @classmethod
    def get_jwt_secret(cls):
        """
        Returns the JWT secret key.
        """
        return cls.JWT_SECRET
    

# create a singleton instance of the Config class
config = Config()
