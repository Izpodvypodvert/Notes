from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from fastapi_users.password import PasswordHelper

from models.note import Note
from models.user import User


# If you run the application from a container
# DATABASE_URL = 'postgresql+asyncpg://postgres:postgres@db:5432/foo'
DATABASE_URL = 'postgresql+asyncpg://postgres:postgres@localhost:5432/foo'

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def create_notes():
    async with AsyncSessionLocal() as session:

        helper = PasswordHelper()
        user = User(
            email='user@example.com',
            hashed_password=helper.hash('password'),
            is_active=True,
            is_verified=True,
            is_superuser=True
        )
        session.add(user)
        await session.commit()

        note_1 = Note(
            title="utils",
            description="write a custom validator and a custom error",
            user_id=user.id
        )
        note_2 = Note(
            title="add a readme",
            description="describe how to deploy the project locally",
            user_id=user.id
        )
        note_3 = Note(
            title="Alembic",
            description="configure alembic",
            user_id=user.id
        )
        note_4 = Note(
            title="Security",
            description="move sensitive data in .env file",
            user_id=user.id
        )

        session.add_all([note_1, note_2, note_3, note_4])
        await session.commit()


async def main():
    # await create_db_and_tables()
    await create_notes()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
