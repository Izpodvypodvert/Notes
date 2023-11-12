from fastapi_users_db_sqlmodel import SQLModelBaseUserDB


class User(SQLModelBaseUserDB, table=True):
    """Модель пользователя."""
