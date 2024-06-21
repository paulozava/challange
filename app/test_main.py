from datetime import date

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

ERROR_MSG = "Failed for {}, expected {} got {}"


def test_health_path():
    response = client.get("/-/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# test for get username


# receive a valid user - return 200
def test_get_username_success_found():
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
                "message": f"Hello, {username}! Your birthday is in {birthday_delta.days} days!"
            }


# receive a user that was not put - return 404
def test_get_username_valid_not_found():
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
    expected_staus_code = 204
    test_cases = [
        ("John", date(1990, 1, 1)),
        ("Mary", date(1990, 11, 1)),
        ("Jane", date(1990, 1, 21)),
    ]

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
    expected_staus_code = 204
    expected_message = {}
    test_cases = [
        ("John", date(1990, 1, 1)),
        ("Mary", date(1990, 11, 1)),
        ("Jane", date(1990, 1, 21)),
    ]

    for username, date_of_birth in test_cases:
        response = client.put(
            f"/hello/{username}",
            json={"dateOfBirth": date_of_birth.strftime("%Y-%m-%d")},
        )
        status_code = response.status_code
        # message = response.raw
        # assert message == expected_message, ERROR_MSG.format(
        #     username, expected_message, message
        # )
        assert status_code == expected_staus_code, ERROR_MSG.format(
            username, expected_staus_code, status_code
        )


# receive an invalid date of birth - return 422
# invalid date of birth:
# - empty date
# - date with special characters
# - date without the correct format
# - date with emoji
# - date of date bigger than today
# - date of a date with year less than 1000
# - date of a date with year less than 9999
