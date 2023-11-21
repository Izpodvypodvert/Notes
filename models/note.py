from sqlmodel import Field, Relationship
from pydantic import UUID4
from typing import TYPE_CHECKING
from datetime import datetime

from models.category import Category
from schemas.note_schema import TitleDescriptionBase
from schemas.user_schema import UserRelatedBase

if TYPE_CHECKING:
    from models.user import User


class Note(UserRelatedBase, TitleDescriptionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    user: "User" = Relationship(
        back_populates="notes",
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "Note.user_id==User.id",
        })
    created_at: datetime = Field(default_factory=datetime.utcnow)
    category_id: UUID4 | None = Field(
        default=None, foreign_key="category.id")
    category: Category = Relationship(back_populates="notes")
