"""Database utilities for the application"""

import os

import psycopg

DEFAULT_DB = {
    "host": "0.0.0.0",
    "port": 5432,
    "name": "hello",
    "user": "root",
    "password": "pantera!!!",
}


def bootstrap_db():
    """Create the schema and table if they don't exist and insert a user if it doesn't exist"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
            CREATE SCHEMA IF NOT EXISTS hello;
            CREATE TABLE IF NOT EXISTS hello.usernames(
               id SERIAL PRIMARY KEY,
               username TEXT NOT NULL UNIQUE,
               dateOfBirth DATE NOT NULL
            );

            INSERT INTO hello.usernames (username, dateOfBirth) VALUES ('Arlindolando', '7960-11-01') ON CONFLICT (username) DO NOTHING;
            """
            )


def get_db_connection():
    """Return a connection to the database"""
    conn = psycopg.connect(
        f"host={os.getenv('APP_DB_HOST', DEFAULT_DB['host'])} port={os.getenv('APP_DB_PORT', DEFAULT_DB['port'])} dbname={os.getenv('APP_DB_NAME', DEFAULT_DB['name'])} user={os.getenv('APP_DB_USER', DEFAULT_DB['user'])} password={os.getenv('APP_DB_PASSWORD', DEFAULT_DB['password'])}",
        autocommit=True,
    )
    return conn
