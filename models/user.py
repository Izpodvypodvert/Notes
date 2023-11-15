from fastapi_users_db_sqlmodel import SQLModelBaseUserDB
from typing import List, TYPE_CHECKING
from sqlmodel import Relationship


if TYPE_CHECKING:
    from models.note import Note


class User(SQLModelBaseUserDB, table=True):
    """The user's model."""
    notes: List["Note"] = Relationship(back_populates="user")
