import uuid
from sqlmodel import Field
from typing import Optional
from pydantic import UUID4
from datetime import datetime

from schemas.note_schema import NoteBase


class Note(NoteBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: UUID4 = Field(
        default_factory=uuid.uuid4,
        nullable=False)

    def __repr__(self):
        return f'{self.title}'
