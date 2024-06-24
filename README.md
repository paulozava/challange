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

## Solution

### How to run

#### Requirements

- Docker
- Docker Compose
- Terraform (for AWS deployment)
- AWS CLI (for AWS deployment)

#### Local

use the following command to run the application locally:

```bash
docker compose up
```

if you need to run tests, use the following command:

```bash
docker compose restart -t 10 test
```

#### AWS

use the following command on the root of the folder to deploy the application to AWS:

```bash
terraform init
terraform apply
```

#### Commands

### System Diagram

### Decision log

- **Python**: Python is a common language nowadays, almost all SRE/DevOps professional knows at least the basics of it. This widespread familiarity will facilitate the improvement and maintenance of the code.

- **FastAPI**: FastAPI is a modern web framework for building APIs with Python. With it, I expect to create a production-level API quickly, complete with logging and testing capabilities.

- **PostgreSQL**: I chose PostgreSQL because it is a widely-used database known for its good performance and ease of use. Additionally, it is adopted by companies like Revolut.

- **Case-sensitive Username**: I opted to make usernames case-sensitive, meaning "John" and "john" will be treated as different users. The requirements do not specify that usernames should be case-insensitive.

- **ASCII-only Username**: For simplicity, I chose to allow only ASCII letters in usernames.

- **Username Character Limit**: To keep things simple, I decided to limit usernames to 100 characters.

- **Pluralized Message for Days**: I chose to pluralize the message for the number of days instead of using "day(s)" to make it more readable for users.

- **Running Tests in a Container**: I decided to create a container to run the tests. Although the container setup is not perfect when restarting tests, I opted to keep it as is for now. If this were a production resource, it would make sense to spend more time improving it.

- **AWS**: I chose AWS as the cloud provider because it is the one I have the most experience with.

- **Terraform and Local State**: I used Terraform to create the Infrastructure as Code (IaC) resources. However, I kept the state local for convenience. In a production environment, the state should be stored remotely.

- **Aurora PostgreSQL**:

  - I chose Aurora PostgreSQL because it is a managed service with good performance and scalability.
  - I left the database without delete protection since this is a test environment. In production, delete protection should be enabled, along with the latest backup features.
  - I used hardcoded credentials for convenience, but in production, they should be stored in a secret manager like AWS Secrets Manager or HashiCorp Vault.

- **ECS**: I chose ECS because it is a managed service with good performance and scalability. Additionally, it is easy to integrate with Application Load Balancer (ALB).

- **Release the code with terraform**: My idea here is to have a simple way to deploy the infra stack and test the application. I decide to not add an pipeline step to this because I simply do not know anything about your infra. In a production environment, the code should be released with a CI/CD pipeline.

### TODO

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
- [x] Create the infrastructure
  - [x] Create a Postgres database on AWS RDS
  - [x] Create a ECS cluster
  - [x] Create a self-signed certificate to allow https
  - [x] Create an ALB to expose the ECS function
- [x] Deploy the application to AWS
- [] Create a system diagram
- [] Write documentation about how to use the code
- [] Write configuration scripts for building and no-downtime production deployment of this application, keeping in mind aspects that an SRE would have to consider.?
