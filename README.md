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

- Python
- FastAPI
- Syncronous code
- Postgres
- Secrets on environment variables
- Accepted date format: YYYY-MM-DD
- Terraform and local state
- AWS
- Lambda
- ALB
- 201 instead of 204 when user is created

## TODO

- [x] Create a local database:
  - [x] Create table hello with the fields:
    - [x] id
    - [x] username
    - [x] dateOfBirth
  - [x] Create a connection pool
  - [] Bootstrap database when schema is not available
- [] Create a FastAPI app with the endpoints:
  - [] PUT /hello/<username>
    - [] Evaluate put request
      - [] Validate username is only letters
      - [x] Validate the date format is valid
      - [x] Validate date is before today
    - [] Save the user in the database
    - [] Return:
      - [] 201 Created if the user is created
      - [] 204 No Content if user is updated
      - [] 400 Bad Request if any validation fail with the error in the message
      - [] 500 Internal Server Error if save on the database fails
  - [] GET /hello/<username>
    - [] Evaluate get request username is only letters
    - [] Get the user from the database
    - [] Return:
      - [] 200 OK with the message:
        - [] "Hello, <username>! Your birthday is in N day(s)" if the birthday is not today
        - [] "Hello, <username>! Happy birthday!" if the birthday is today
      - [] 404 Not Found if the user is not found
      - [] 500 Internal Server Error if get on the database fails
- [x] Create a Dockerfile
- [x] Create a docker-compose file
- [] Local tests
  - [] Unit tests
  - [] Integration tests with testcontainers
- [] Create the infrastructure
  - [] Create a Postgres database on AWS RDS
  - [] Create a Lambda function
  - [] Create a self-signed certificate to allow https
  - [] Create an ALB to expose the Lambda function
- [] Deploy the application to AWS
- [] Create a system diagram
- [] Write documentation about how to use the code
- [] Write configuration scripts for building and no-downtime production deployment of this application, keeping in mind aspects that an SRE would have to consider.?
