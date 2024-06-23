# challange

## Requirements

1.  Design and code a simple "Hello World" application that exposes the following
    HTTP-based APIs:

    ```
    Description: Saves/updates the given user’s name and date of birth in the database.
    Request: PUT /hello/<username> { "dateOfBirth": "YYYY-MM-DD" }
    Response: 204 No Content
    ```

    Note:

    - <username> must contain only letters.

    - YYYY-MM-DD must be a date before the today date.

    ```
    Description: Returns hello birthday message for the given user
    Request: Get /hello/<username>
    Response: 200 OK
    ```

    Response Examples:
    A. If username’s birthday is in N days:

    ```json
    { "message": "Hello, <username>! Your birthday is in N day(s)" }
    ```

    B. If username’s birthday is today:

    ```json
    { "message": "Hello, <username>! Happy birthday!" }
    ```

    Note: Use storage/database of your choice.

2.  Produce a system diagram of your solution deployed to either AWS or GCP (it's not required to support both cloud platforms).

3.  Write configuration scripts for building and no-downtime production deployment of this application, keeping in mind aspects that an SRE would have to consider.

### Implicit requirements:

1. The code produced by you is expected to be of high quality.
2. The solution must have tests, runnable locally, and deployable to the cloud.
3. Use common sense.

## Decision log

- Python: Python is a common langue nowdays, so common that every SRE/DevOps know at least the basics of it, so it will be easier to improve and maintain the code.
- FastAPI: FastAPI is a modern web framework for building APIs with Python. With it I expect to create the api with production level very fast, with logging and testing.
- Syncronous code: I choose to use syncronous code to make the code easier to understand and maintain.
- Postgres: I choose to use Postgres because it is a common database, with good performance, easy to use and adopted by Revolut.
- Username will be case sensitive: I choose to make the username case sensitive, that means that "John" and "john" are different users. The requirements do not specify that the username should be case insensitive.
- Username will allow only ASCII letters: For simplicity I choose to allow only ASCII letters in the username.
- Username have max 100 characters: Same as above, for simplicity I choose to limit the username to 100 characters.
- Get message with the number of days: I choose to pluralize the message intead of use the "day(s)" so it will be more readable for the user.
- Running tests on container: I choose to create a container to run the tests, however it is not in perfect stage during restart the test, I decide to keep this as is for now, probably if this was a production resource, it makes sense to expend more time on improving that.
- AWS
- Terraform and local state
- ECR public repository
- Aurora Postgres:
  - I choose to use Aurora Postgres because it is a managed service, with good performance and scalability.
  - I left the database with no delete protection, because it is a test environment, in production it should be enabled. The same for last backup.
  - I use credentials in code just for convinience, in production it should be stored in a secret manager like AWS Secrets or Hashcorp Vault.
- ECS
- ALB

## TODO

- [x] Create a local database:
  - [x] Create table hello with the fields:
    - [x] id
    - [x] username
    - [x] dateOfBirth
  - [x] Create a connection pool
  - [] Bootstrap database when schema is not available
- [x] Create a FastAPI app with the endpoints:
  - [x] PUT /hello/<username>
    - [x] Evaluate put request
      - [x] Validate username is only letters
      - [x] Validate the date format is valid
      - [x] Validate date is before today
    - [x] Save the user in the database
    - [x] Return:
      - [x] 204 No Content if user is created/updated
      - [?] 400 Bad Request if any validation fail with the error in the message
      - [x] 500 Internal Server Error if save on the database fails
  - [x] GET /hello/<username>
    - [x] Evaluate get request username is only letters
    - [x] Get the user from the database
    - [x] Return:
      - [x] 200 OK with the message:
        - [x] "Hello, <username>! Your birthday is in N day(s)" if the birthday is not today
        - [x] "Hello, <username>! Happy birthday!" if the birthday is today
      - [x] 404 Not Found if the user is not found
      - [x] 500 Internal Server Error if get on the database fails
- [x] Create a Dockerfile
- [x] Create a docker-compose file
- [x] Local tests
- [] Create the infrastructure
  - [] Create a Postgres database on AWS RDS
  - [] Create a Lambda function
  - [] Create a self-signed certificate to allow https
  - [] Create an ALB to expose the Lambda function
- [] Deploy the application to AWS
- [] Create a system diagram
- [] Write documentation about how to use the code
- [] Write configuration scripts for building and no-downtime production deployment of this application, keeping in mind aspects that an SRE would have to consider.?
