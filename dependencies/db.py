import os
from dotenv import load_dotenv

from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker


load_dotenv('.env')
TEST = os.environ["TEST"] == "True"
DATABASE_URL = os.environ['DATABASE_URL'] if not TEST else os.environ['TEST_DATABASE_URL']

engine = create_async_engine(DATABASE_URL, echo=False, future=True)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session
