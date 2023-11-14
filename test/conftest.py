import asyncio
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import AsyncClient

from main import app
from utils.initial_data import (
    get_test_user_token,
    create_test_user,
    delete_user,
    create_user_notes,
    delete_user_notes,
    create_db_and_tables,
    drop_db_and_tables
)


@pytest.fixture(scope="session")
async def setup_and_teardown_db():
    await create_db_and_tables()
    yield
    await drop_db_and_tables()


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def test_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client


@pytest_asyncio.fixture(scope="session")
async def test_user():
    test_user = await create_test_user()
    yield test_user
    await delete_user(test_user)


@pytest_asyncio.fixture()
async def clean_up_user(test_user):
    yield
    await delete_user(test_user)


@pytest_asyncio.fixture(scope="function")
async def notes(test_user):
    notes = await create_user_notes(test_user)
    yield notes
    await delete_user_notes(test_user)


async def get_headers(user):
    token = await get_test_user_token(user)
    headers = {'Authorization': f'Bearer {token}'}
    return headers
