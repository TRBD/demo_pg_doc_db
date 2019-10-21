"""
Context manager for database connection
"""
from demo_importlib import contextmanager, psycopg2
from config import PG_CONN_STRING


@contextmanager
def pg_connection():
    pg_conn = psycopg2.connect(PG_CONN_STRING)
    yield pg_conn
    pg_conn.close()
