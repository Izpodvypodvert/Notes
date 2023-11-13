import os
from dotenv import load_dotenv

from sqlmodel import SQLModel
from fastapi_users.password import PasswordHelper

from dependencies.db import engine, AsyncSessionLocal
from models.note import Note
from models.user import User


load_dotenv('.env')
SUPERUSER_EMAIL = os.environ['SUPERUSER_EMAIL']
SUPERUSER_PASSWORD = os.environ['SUPERUSER_PASSWORD']


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def create_user(
    email: str,
    password: str,
    verified: bool = False,
    superuser: bool = False
) -> User:
    async with AsyncSessionLocal() as session:
        helper = PasswordHelper()
        user = User(
            email=email,
            hashed_password=helper.hash(password),
            is_active=True,
            is_verified=verified,
            is_superuser=superuser
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


async def create_user_notes(user: User):
    async with AsyncSessionLocal() as session:
        notes = [
            Note(
                title="utils",
                description="write a custom validator and a custom error",
                user_id=user.id
            ),
            Note(
                title="add a readme",
                description="describe how to deploy the project locally",
                user_id=user.id
            ),
            Note(
                title="Alembic",
                description="configure alembic",
                user_id=user.id
            ),
            Note(
                title="Security",
                description="move sensitive data in .env file",
                user_id=user.id
            )
        ]
        session.add_all(notes)
        await session.commit()


async def main():
    user = await create_user(
        SUPERUSER_EMAIL,
        SUPERUSER_PASSWORD,
        verified=True,
        superuser=True
    )
    await create_user_notes(user)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
