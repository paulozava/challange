import psycopg


def get_db_connection():
    conn = psycopg.connect(
        "host=postgres port=5432 dbname=hello user=root password=pantera!!!",
        autocommit=True,
    )
    return conn
