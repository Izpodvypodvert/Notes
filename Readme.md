# FastAPI Notes Application

This is a simple CRUD application for managing notes, built with FastAPI, SQLModel, and PostgreSQL. It features user authentication and allows users to create, read, update, and delete notes.

## Features

-   User registration and authentication
-   CRUD operations for notes
-   Notes are private to users
-   Asynchronous database operations
-   Containerized PostgreSQL database

## Technology Stack

-   **FastAPI**: A modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
-   **SQLModel**: SQL databases in Python with asyncio, made easy with a combination of SQLAlchemy for query building and Pydantic for data validation.
-   **PostgreSQL**: An open source object-relational database system with over 30 years of active development.
-   **Alembic**: A lightweight database migration tool for usage with the SQLAlchemy Database Toolkit for Python.

## Getting Started

### Prerequisites

-   Python 3.7+
-   Docker
-   Docker Compose (for running PostgreSQL container)

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/Izpodvypodvert/Notes.git
    cd Notes
    ```
2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```
4. Start the PostgreSQL container:
    ```sh
    docker-compose up -d
    ```
5. Run the Alembic migrations to the latest version (optional, if you have made changes to the models):
    ```sh
    alembic upgrade head
    ```
6. Add notes to db and create superuser:
    ```sh
    python -m utils.initial_data
    ```
7. Start the FastAPI server:
    ```sh
    uvicorn main:app --reload
    ```
    Usage
    After starting the FastAPI server, you can visit http://127.0.0.1:8000/docs to see the Swagger UI and interact with the API.
