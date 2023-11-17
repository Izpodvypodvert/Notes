from sqlmodel import Field, Relationship
from pydantic import UUID4
from typing import Optional, TYPE_CHECKING
from datetime import datetime

from models.category import Category
from schemas.note_schema import TitleDescriptionBase
from schemas.user_schema import UserRelatedBase

if TYPE_CHECKING:
    from models.user import User


class Note(UserRelatedBase, TitleDescriptionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user: "User" = Relationship(back_populates="notes")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    category_id: Optional[UUID4] = Field(
        default=None, foreign_key="category.id")
    category: Category = Relationship(back_populates="notes")
