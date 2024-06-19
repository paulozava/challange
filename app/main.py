import psycopg
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return "Good morninig Vietnam!"


@app.get("/hello/{username}")
def get_hello(username: str):
    with psycopg.connect(
        "host=0.0.0.0 port=5432 dbname=hello user=root password=pantera!!!"
    ) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM hello.usernames")
            # cur.execute("SELECT * from information_schema.schemata;")
            user = cur.fetchall()
            conn.commit()
    return {"bull": user}
