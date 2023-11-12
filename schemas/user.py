from fastapi_users import schemas
from pydantic import UUID4


class UserRead(schemas.BaseUser[UUID4]):
    """Cхема с базовыми полями модели пользователя (кроме пароля):
    id, email, is_active, is_superuser, is_verified."""


class UserCreate(schemas.BaseUserCreate):
    """Cхема для создания пользователя. Обязательно должны быть переданы email и password.
    Любые другие поля, передаваемые в запросе на создание пользователя, будут проигнорированы."""


class UserUpdate(schemas.BaseUserUpdate):
    """Cхема для обновления объекта пользователя. Cодержит все базовые поля модели пользователя (в том числе и пароль).
    Все поля опциональны. Если запрос передаёт обычный пользователь (а не суперюзер), то поля is_active, is_superuser,
    is_verified исключаются из набора данных: эти три поля может изменить только суперюзер"""
