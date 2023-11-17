
from typing import TYPE_CHECKING, List

from sqlmodel import Relationship


from schemas.note_schema import TitleDescriptionBase
from schemas.user_schema import UserRelatedBase

if TYPE_CHECKING:
    from models.note import Note
    from models.user import User


class Category(UserRelatedBase, TitleDescriptionBase, table=True):
    """Сategory of notes."""
    notes: List["Note"] = Relationship(back_populates="category")
    user: "User" = Relationship(back_populates="categories")
