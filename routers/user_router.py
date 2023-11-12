from fastapi import APIRouter, HTTPException

from dependencies.user import auth_backend, fastapi_users
from schemas.user import UserCreate, UserUpdate, UserRead

router = APIRouter()

router.include_router(
    # В роутер аутентификации
    # передается объект бэкенда аутентификации.
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix='/users',
    tags=['users'],
)


@router.delete(
    '/users/{id}',
    tags=['users'],
    deprecated=True
)
def delete_user(id: str):
    """Переопределен метод удаления пользователя, чтобы никто, даже суперпользователь,
    не мог отправить запрос на удаление пользователя.
    При необходимости пользоветеля можно деактивировать is_active=False"""
    raise HTTPException(
        status_code=405,
        detail="Удаление пользователей запрещено!"
    )
