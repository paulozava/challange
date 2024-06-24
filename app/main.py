from contextlib import asynccontextmanager
from datetime import date
from typing import Annotated

from app.databases import bootstrap_db, get_db_connection
from app.models import DateOfBirth
from fastapi import Body, FastAPI, HTTPException, Path, status


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create the database schema if not done yet before the application starts"""
    bootstrap_db()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/-/all")
def get_all_users():
    """/-/all - GET - return all the users in the database"""
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM hello.usernames")
            user = cur.fetchall()
    return {"users": user}


@app.get("/-/health")
def get_health():
    """/-/health - GET - return 200 status ok as a healthcheck"""
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
    """/hello/{username} - GET - return a message with the number of days until the user's birthday or a happy birthday message"""
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
        _, username, date_of_birth = tuple(user[0])
        birthday_delta = date.today() - date(
            date.today().year, date_of_birth.month, date_of_birth.day
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
    """/hello/{username} - PUT - Add a new user or update the date of birth of an existing user"""
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
