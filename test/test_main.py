import os
import sys
from datetime import date
from random import choices, randrange
from string import ascii_letters

from app.main import app
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../app")))
client = TestClient(app)

ERROR_MSG = "Failed for {}, expected {} got {}"


def test_health_path():
    """Test the health path"""
    response = client.get("/-/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_all_path():
    """Test the all path"""
    response = client.get("/-/all")
    assert response.status_code == 200


# test for get username
def test_get_username_success_found():
    """Test the get username path with valid users - return 200"""
    test_cases = [
        ("John", date(1990, 1, 1)),
        ("Mary", date(1990, 11, 1)),
        ("Jane", date(1990, 1, 21)),
    ]
    for username, date_of_birth in test_cases:
        response = client.get(f"/hello/{username}")
        assert response.status_code == 200
        r = response.json()
        if r["message"].endswith("birthday!"):
            assert r == {"message": f"Hello, {username}! Happy birthday!"}
        else:
            birthday_delta = date.today() - date(
                date.today().year, date_of_birth.month, date_of_birth.day
            )
            assert r == {
                "message": f"Hello, {username}! Your birthday is in {birthday_delta.days} day{'' if birthday_delta.days == 1 else 's'}",
            }


def test_get_username_valid_not_found():
    """Test the get username path with valid users that were not put - return 404"""
    test_cases = [
        "john",
        "mAry",
        "ane",
    ]

    expected_staus_code = 404

    for username in test_cases:
        response = client.get(f"/hello/{username}")
        assert response.status_code == expected_staus_code, ERROR_MSG.format(
            username, expected_staus_code, response.status_code
        )
        expected_json = {"detail": f"User {username} not found"}
        assert response.json() == expected_json, ERROR_MSG.format(
            username, expected_json, response.json()
        )


# receive an invalid user - return 422
# invalid users:
# - string with special characters
# - string with numbers
# - string with emoji
def test_get_username_invalid():
    """Test the get username path with invalid users - return 422"""
    expected_staus_code = 422
    expected_message = "String should match pattern '^[a-zA-Z]+$'"
    test_cases = [
        "mary ann",
        "anne_daniels",
        "j0hn",
        "!mary",
        "mary!",
        "!mary$",
        "123",
        "çñè",
        "🎉",
    ]

    for username in test_cases:
        response = client.get(f"/hello/{username}")
        status_code = response.status_code
        message = response.json()["detail"][0]["msg"]
        assert status_code == expected_staus_code, ERROR_MSG.format(
            username, expected_staus_code, status_code
        )
        assert message == expected_message, ERROR_MSG.format(
            username, expected_message, message
        )


# test for put username


# receive a valid user and a valid date of birth - return 204
def test_put_username_valid():
    """Test the put username path with valid users - return 204"""
    expected_staus_code = 204
    test_cases = [
        ("John", date(1990, 1, 1)),
        ("Mary", date(1990, 11, 1)),
        ("Jane", date(1990, 1, 21)),
    ]
    random_username = [
        ("".join(choices(ascii_letters, k=randrange(1, 100))), date(1990, 1, 1))
        for _ in range(100)
    ]
    test_cases.extend(random_username)
    for username, date_of_birth in test_cases:
        response = client.put(
            f"/hello/{username}",
            json={"dateOfBirth": date_of_birth.strftime("%Y-%m-%d")},
        )
        status_code = response.status_code
        assert status_code == expected_staus_code, ERROR_MSG.format(
            username, expected_staus_code, status_code
        )


# receive an invalid user - return 422
# invald users:
# - empty string
# - string with special characters
# - string with numbers
# - string with emoji
def test_put_username_invalid():
    """Test the put username path with invalid users - return 422"""
    expected_staus_code = 422
    expected_message = "String should match pattern '^[a-zA-Z]+$'"
    test_cases = [
        ("mary ann", date(1990, 1, 1)),
        ("anne_daniels", date(1990, 1, 1)),
        ("j0hn", date(1990, 1, 1)),
        ("!mary", date(1990, 1, 1)),
        ("mary!", date(1990, 1, 1)),
        ("!mary$", date(1990, 1, 1)),
        ("123", date(1990, 1, 1)),
        ("çñè", date(1990, 1, 1)),
        ("🎉", date(1990, 1, 1)),
    ]

    for username, date_of_birth in test_cases:
        response = client.put(
            f"/hello/{username}",
            json={"dateOfBirth": date_of_birth.strftime("%Y-%m-%d")},
        )
        status_code = response.status_code
        message = response.json()["detail"][0]["msg"]
        assert status_code == expected_staus_code, ERROR_MSG.format(
            username, expected_staus_code, status_code
        )
        assert message == expected_message, ERROR_MSG.format(
            username, expected_message, message
        )


# receive an username bigger than 100 characters - return 422
def test_put_username_big100():
    """Test the put username path with users bigger than 100 characters - return 422"""
    expected_staus_code = 422
    expected_message = "Username should have at most 100 characters"
    test_cases = [
        ("".join(choices(ascii_letters, k=randrange(100, 10000))), date(1990, 1, 1))
        for _ in range(100)
    ]

    for username, date_of_birth in test_cases:
        response = client.put(
            f"/hello/{username}",
            json={"dateOfBirth": date_of_birth.strftime("%Y-%m-%d")},
        )
        status_code = response.status_code
        message = response.json()["detail"]
        assert status_code == expected_staus_code, ERROR_MSG.format(
            username, expected_staus_code, status_code
        )
        assert message == expected_message, ERROR_MSG.format(
            username, expected_message, message
        )


# receive an invalid date of birth - return 422
# invalid date of birth:
# - empty date
# - date with special characters
# - date without the correct format
# - date with emoji
# - date of date bigger than today
# - date of a date with year less than 9999
def test_put_date_of_birth_invalid():
    """Test the put username path with invalid date of birth - return 422"""
    expected_staus_code = 422
    test_cases = [
        ("".join(choices(ascii_letters, k=randrange(100, 10000))), date(1990, 1, 1))
        for _ in range(100)
    ]
    test_cases = [
        ("John", ""),
        ("John", "1990-01-01!"),
        ("John", "01-01-1990"),
        ("John", "1-1-1990"),
        ("John", "1990/01/01"),
        ("John", "🎉"),
        ("John", "990-01-01"),
        ("John", "10000-01-01"),
        ("John", "9999-01-01"),
        ("John", date.today().strftime("%Y-%m-%d")),
    ]

    for username, date_of_birth in test_cases:
        response = client.put(
            f"/hello/{username}",
            json={"dateOfBirth": date_of_birth},
        )
        status_code = response.status_code
        assert status_code == expected_staus_code, ERROR_MSG.format(
            date_of_birth, expected_staus_code, status_code
        )
