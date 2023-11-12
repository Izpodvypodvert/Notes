from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager, FastAPIUsers, UUIDIDMixin, InvalidPasswordException
)
from fastapi_users_db_sqlmodel import SQLModelUserDatabaseAsync

from fastapi_users.authentication import (
    AuthenticationBackend, BearerTransport, JWTStrategy
)
from pydantic import UUID4
from sqlmodel.ext.asyncio.session import AsyncSession

from dependencies.db import get_async_session
from models.user import User
from schemas.user import UserCreate


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLModelUserDatabaseAsync(session=session, user_model=User)


bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    """Определяем стратегию: хранение токена в виде JWT."""
    return JWTStrategy(secret='SECRET', lifetime_seconds=3600)


# Создаём объект бэкенда аутентификации с выбранными параметрами.
auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(UUIDIDMixin, BaseUserManager[User, UUID4]):
    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        if len(password) < 3:
            raise InvalidPasswordException(
                reason='Password should be at least 3 characters'
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason='Password should not contain e-mail'
            )

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        """Метод для действий после успешной регистрации пользователя."""
        print(f'Пользователь {user.email} зарегистрирован.')


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, UUID4](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
