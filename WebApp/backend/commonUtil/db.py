import psycopg2
from contextlib import contextmanager

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
    
    Usage:
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