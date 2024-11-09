# Organization Management API

This project provides RESTful FastAPIs for organization management where an admin can perform the following tasks:

1. Create an Organization with some information, including an admin user.
2. Retrieve an organization by its name.
3. Admin login with JWT token generation.

## Features

- **Create Organization**: Admin can create an organization with email, password, and name. A dynamic database is created for the organization in the backend, and the information is stored in a master database.
- **Get Organization**: Retrieve organization information by name.
- **Admin Login**: Admin can log in and get a JWT token for subsequent authenticated requests.


### Prerequisites

1. Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)

## Docker Setup

- Run below script to set up your system for local development using docker:

```bash
./app/scripts/docker-dev.sh  # Enter password when asked
```

Now run the below commands to run services in Docker:

```bash
# Build container images for api and db
docker-compose build

# Start all services in the background
docker-compose up --detach
```

`docker-compose up` will start the following services:

- `db` (PostgreSql)
- `api` (FastAPi app)

If you want to access the docker container of a particular service, you can do so by running:

```bash
# interactive shell session on an already-running service
docker-compose exec -it <service> bash
# For example, to access `api` service interactive shell
docker-compose exec -it api bash
# Run unit tests
docker-compose exec api bash ./run_tests.sh
```

Other useful commands:

```bash
# View logs of a specific service/container
docker-compose logs <service>
# Stream container logs on host
docker-compose logs api -f --tail 50
# Start a specific service only instead of all
docker-compose up api --detach
# Stop an already running service
docker-compose down api
```


## API Endpoints

### 1. Create Organization
- **Endpoint**: `POST /org/create`
- **Description**: Create an organization with an admin user.
- **Payload**:
    ```json
    {
        "email": "admin@example.com",
        "password": "adminpassword",
        "organization_name": "MyOrganization"
    }
    ```

### 2. Get Organization By Name
- **Endpoint**: `GET /org/get`
- **Description**: Retrieve organization information by organization name.
- **Query Parameter**: `organization_name`
- **Example Request**:
    ```
    GET /org/get?organization_name=MyOrganization
    ```

### 3. Admin Login
- **Endpoint**: `POST /admin/login`
- **Description**: Admin login to get a JWT token.
- **Payload**:
    ```json
    {
        "email": "admin@example.com",
        "password": "adminpassword"
    }
    ```
- **Response**:
    ```json
    {
        "access_token": "your_jwt_token",
        "token_type": "bearer"
    }
    ```

## Python

We use

- Python ~= 3.9
- pip ~= 24.3.x (https://pypi.org/project/pip/)

### Installation

Use [PyEnv](https://github.com/pyenv/pyenv) to install and use Python 3.9.x.

## API Documentation

http://dev.navatech.ai:8000/docs

