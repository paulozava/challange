from typing import Annotated

from fastapi import Body, FastAPI

from app.databases import get_db_connection
from app.date_of_birth_model import DateOfBirth

app = FastAPI()


@app.get("/")
def read_root():
    return "Good morninig Vietnam!"


@app.get("/hello/{username}")
def get_hello(username: str):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM hello.usernames")
            user = cur.fetchall()
    return {"bull": user}


@app.put("/hello/{username}")
def put_hello(username: str, dateOfBirth: Annotated[DateOfBirth, Body(embed=False)]):
    # with get_db_connection() as conn:
    #     with conn.cursor() as cur:
    #         cur.execute(
    #             "INSERT INTO hello.usernames (username, dateOfBirth) VALUES (%s, %s)",
    #             (username, "2021-01-01"),
    #         )
    return {
        "username": username,
        "dateOfBirth": dateOfBirth.dateOfBirth,
    }
