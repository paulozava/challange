from typing import Annotated

from fastapi import Body, FastAPI, Path

from app.databases import get_db_connection
from app.date_of_birth_model import DateOfBirth
from app.username_model import Username

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
def put_hello(
    username: Annotated[
        str,
        Path(
            title="Username of the user",
            description="The username of the user",
            pattern="^[a-zA-Z]+$",
        ),
    ],
    dateOfBirth: Annotated[DateOfBirth, Body(embed=False)],
):
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
