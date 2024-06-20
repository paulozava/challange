import psycopg


def get_db_connection():
    conn = psycopg.connect(
        "host=0.0.0.0 port=5432 dbname=hello user=root password=pantera!!!",
        autocommit=True,
    )
    return conn
