from sqlmodel import Field, SQLModel
from pydantic import validator
from typing import Optional
from datetime import datetime

from utils.validators import validate_note_title


class NoteBase(SQLModel, table=False):
    title: str
    description: str

    @validator('title')
    def title_must_be_captialized(cls, title):
        validate_note_title(title)
        return title
