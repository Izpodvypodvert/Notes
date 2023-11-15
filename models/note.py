import uuid
from sqlmodel import Field, Relationship
from typing import Optional, TYPE_CHECKING
from pydantic import UUID4
from datetime import datetime


from schemas.note_schema import NoteBase

if TYPE_CHECKING:
    from models.user import User


class Note(NoteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: UUID4 = Field(default_factory=uuid.uuid4, foreign_key="user.id")
    user: "User" = Relationship(back_populates="notes")

    def __repr__(self):
        return f'{self.title}'
