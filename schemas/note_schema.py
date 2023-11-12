from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime


class NoteBase(SQLModel, table=False):
    title: str
    description: str
