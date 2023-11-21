# FastAPI Notes Application

This is a simple CRUD asynchronous application for managing notes, built with FastAPI, SQLModel, and PostgreSQL. It features user authentication and allows users to create, read, update, and delete notes.
This project uses a custom version of fastapi-cache2, modified to suit specific requirements. The primary reason for this customization is the incompatibility of the pendulum library, a dependency in the standard fastapi-cache2, with Python 3.12. See [customization details below](#customization-details).

## Features

-   User registration and authentication
-   CRUD operations for notes
-   Notes are private to users
-   Asynchronous database operations
-   Containerized PostgreSQL database
-   Endpoint caching with Redis
-   Asynchronous Email Dispatch with Celery
-   Task Monitoring with Flower

## Additional Features

Asynchronous Email Dispatch with Celery and Flower
This project leverages Celery, an asynchronous task queue, along with Flower for monitoring, to handle the dispatch of emails containing user Notes. Redis is used as the broker for these tasks.

Celery: Used for managing asynchronous tasks, specifically for sending emails in the background.
Flower: An accompanying tool for Celery that provides monitoring capabilities, allowing visibility into the task queue and performance.
Redis: Acts as a message broker for Celery, queuing the email tasks created by the application.

## Technology Stack

-   **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
-   **SQLModel**: SQL databases in Python with asyncio, made easy with a combination of SQLAlchemy for query building and Pydantic for data validation.
-   **PostgreSQL**: An open source object-relational database system with over 30 years of active development.
-   **Alembic**: A lightweight database migration tool for usage with the SQLAlchemy Database Toolkit for Python.
-   **Redis**: An advanced key-value store, often used as a cache and message broker, with support for data structures such as strings, hashes, lists, sets, and sorted sets with range queries.
-   **Pytest**: A powerful tool for testing Python code, providing a simple and flexible framework for writing and executing tests.
-   **Celery**: An asynchronous task queue/job queue based on distributed message passing, focused on real-time operation and supporting scheduling.
-   **Flower**: A web-based tool for monitoring and administrating Celery clusters, providing insights into tasks and worker status.

## Getting Started

### Prerequisites

-   Python 3.12
-   Docker
-   Docker Compose (for running PostgreSQL container)

### Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/Izpodvypodvert/Notes.git
    cd Notes
    ```

2. Сreate a `.env` file in the root directory of the project:

```plaintext
    Settings for connecting to the main PostgreSQL database
    POSTGRES_USER=postgres # PostgreSQL username
    POSTGRES_PASSWORD=postgres # PostgreSQL user password
    POSTGRES_DB=foo # Name of the main database
    HOST=localhost # Change it to db for development in docker
    DATABASE_URL=postgresql+asyncpg://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${HOST}:5432/${POSTGRES_DB}

    Settings for connecting to the PostgreSQL test database
    TEST_POSTGRES_USER=postgres_test # Username for the test database
    TEST_POSTGRES_PASSWORD=postgres_test # Password for the test database user
    POSTGRES_TEST_DB=test_db # Name of the test database
    TEST_DATABASE_URL=postgresql+asyncpg://${TEST_POSTGRES_USER}:${TEST_POSTGRES_PASSWORD}@${HOST}:5433/${POSTGRES_TEST_DB}

    Superuser credentials
    SUPERUSER_EMAIL=user@example.com # Superuser email
    SUPERUSER_PASSWORD=password # Superuser password

    General settings
    TEST=False # Flag for running in main mode with main db
    SECRET=SECRET # Secret key of the application

    Redis settings
    REDIS_DOCKER=localhost # Change it to redis for development in docker
    REDIS_URL=redis://${REDIS_DOCKER}:6379

    Smtp settings
    SMTP_HOST=smtp.gmail.com
    SMTP_PORT=465
    SMTP_USER=your_email@gmail.com
    SMTP_PASSWORD=hehe hehe hehe hehe
```

3. Run the services defined in docker-compose.yml using the following command:
    ```sh
    docker-compose up -d
    ```
4. If you need to perform initial database setup or create a superuser, use the following command:
    ```sh
    docker exec fastapi_app python -m utils.initial_data
    ```
    After starting the FastAPI server, you can visit http://127.0.0.1:8000/docs to see the Swagger UI and interact with the API.

### How to start testing

1. Don't forget to set the test flag to True:
    ```sh
    TEST=True # Flag for running in test mode with test db
    ```
2. Start the PostgreSQL container with test db:
    ```sh
    docker-compose -f docker-compose.test.yml up
    ```
3. Run the tests:
    ```sh
    pytest
    ```

## Customization Details

### Removal of Pendulum Dependency

-   The standard `fastapi-cache2` relies on `pendulum` for date and time handling.
-   As `pendulum` does not support Python 3.12, it has been removed from our custom implementation.
-   Instead, Python's native `datetime` module is utilized for handling date and time.

### Custom Converters

The following custom converters have been implemented to replace `pendulum` functionality:

```python
CONVERTERS = {
    "date": lambda x: datetime.date.fromisoformat(x),
    "datetime": lambda x: datetime.datetime.fromisoformat(x),
    "decimal": Decimal,
}
```

### Endpoint Caching: read_notes

-   The endpoint read_notes is specifically optimized for caching.
-   Caching is personalized: each user's notes are cached individually.
-   The cache for a user's notes is invalidated upon any modification (creation, update, or deletion) of their notes.
