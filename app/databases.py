import os

import psycopg


def get_db_connection():
    conn = psycopg.connect(
        f"host={os.getenv('APP_DB_HOST', '0.0.0.0')} port={os.getenv('APP_DB_PORT', 5432)} dbname={os.getenv('APP_DB_NAME', 'hello')} user={os.getenv('APP_DB_USER', 'root')} password={os.getenv('APP_DB_PASSWORD', 'pantera!!!')}",
        autocommit=True,
    )
    return conn
