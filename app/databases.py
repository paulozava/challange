import os

import psycopg

DEFAULT_DB = {
    "host": "0.0.0.0",
    "port": 5432,
    "name": "hello",
    "user": "root",
    "password": "pantera!!!",
}


def get_db_connection():
    conn = psycopg.connect(
        f"host={os.getenv('APP_DB_HOST', DEFAULT_DB['host'])} port={os.getenv('APP_DB_PORT', DEFAULT_DB['port'])} dbname={os.getenv('APP_DB_NAME', DEFAULT_DB['name'])} user={os.getenv('APP_DB_USER', DEFAULT_DB['user'])} password={os.getenv('APP_DB_PASSWORD', DEFAULT_DB['password'])}",
        autocommit=True,
    )
    return conn
