import psycopg2
from contextlib import contextmanager
from .config import config # Import config

def get_db_connection(host, database, user, password, port=5432):
    """
    Establishes a connection to the PostgreSQL database.
    """
    try:
        conn = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )
        return conn
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

@contextmanager
def db_connection(host, database, user, password, port=5432):
    """
    Context manager for database connections.
    Automatically closes the connection when exiting the context.
    
    Example:
        with db_connection(host, database, user, password) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users")
                results = cursor.fetchall()
    """
    conn = None
    try:
        conn = get_db_connection(host, database, user, password, port)
        if not conn:
            raise Exception("Failed to establish database connection")
        yield conn
    finally:
        if conn:
            conn.close()

# Database session context manager with automatic config
@contextmanager
def get_db_session():
    """
    Provides a database connection using application config.
    
    Example:
        with get_db_session() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users")
                results = cursor.fetchall()
    """
    db_params = {
        'host': config.DB_HOST,
        'database': config.DB_NAME,
        'user': config.DB_USER,
        'password': config.DB_PASSWORD,
        'port': config.DB_PORT,
    }
    
    with db_connection(**db_params) as conn:
        yield conn

@contextmanager
def get_cursor():
    """
    Provides a database cursor with automatic connection handling.
    
    Example:
        with get_cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            results = cursor.fetchall()
    """
    with get_db_session() as conn:
        with conn.cursor() as cursor:
            yield cursor