import psycopg2
from contextlib import contextmanager

DB_CONFIG = {
    "host": "microservice-db",
    "port": "5432",
    "dbname": "appdb",
    "user": "appuser",
    "password": "apppass"
}

@contextmanager
def get_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    try:
        yield conn
    finally:
        conn.close()
