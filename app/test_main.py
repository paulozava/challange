from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_path():
    response = client.get("/-/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# test for put


# receive a valid user and a valid date of birth - return 204
def test_put_hello_username_happy():
    test_cases = [
        ("John", "1990-01-01"),
        ("Mary", "1990-11-01"),
        ("Jane", "1990-01-21"),
    ]
    for username, date_of_birth in test_cases:
        response = client.get(f"/hello/{username}")
        assert response.status_code == 200
        assert response.json() == {}


# receive an invalid user - return 422
# invald users:
# - empty string
# - string with special characters
# - string with numbers
# - string with emoji

# receive an invalid date of birth - return 422
# invalid date of birth:
# - empty date
# - date with special characters
# - date without the correct format
# - date with emoji
# - date of date bigger than today
# - date of a date with year less than 1000
# - date of a date with year less than 9999
