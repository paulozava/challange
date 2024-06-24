from contextlib import asynccontextmanager
from datetime import date
from typing import Annotated

from app.databases import bootstrap_db, get_db_connection
from app.models import DateOfBirth
from fastapi import Body, FastAPI, HTTPException, Path, status


@asynccontextmanager
async def lifespan(app: FastAPI):
    bootstrap_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/-/all")
def get_all_users():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM hello.usernames")
            user = cur.fetchall()
    return {"users": user}


@app.get("/-/health")
def get_health():
    return {"status": "ok"}


@app.get("/hello/{username}")
def get_hello(
    username: Annotated[
        str,
        Path(
            title="Username of the user",
            description="The username of the user",
            pattern="^[a-zA-Z]+$",
        ),
    ]
):

    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM hello.usernames WHERE username = %s", (username,)
            )
            user = cur.fetchall()
    if not user:
        raise HTTPException(status_code=404, detail=f"User {username} not found")
    elif len(user) > 1:
        raise HTTPException(
            status_code=418,
            detail="We have more than one user with the same username, I will prepare a tea and we can try again",
        )
    else:
        _, username, dateOfBirth = tuple(user[0])
        birthday_delta = date.today() - date(
            date.today().year, dateOfBirth.month, dateOfBirth.day
        )
        if birthday_delta.days == 0:
            return {"message": f"Hello, {username}! Happy birthday!"}
        else:
            return {
                "message": f"Hello, {username}! Your birthday is in {birthday_delta.days} day{'' if birthday_delta.days == 1 else 's'}",
            }


@app.put("/hello/{username}", status_code=status.HTTP_204_NO_CONTENT)
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
    if len(username) > 100:
        raise HTTPException(
            status_code=422,
            detail="Username should have at most 100 characters",
        )
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO hello.usernames (username, dateOfBirth) VALUES (%s, %s) ON CONFLICT (username) DO UPDATE SET dateOfBirth = EXCLUDED.dateOfBirth",
                (username, dateOfBirth.dateOfBirth),
            )
