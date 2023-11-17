from sqlmodel import Field, SQLModel
from pydantic import validator

from utils.validators import validate_title


class TitleDescriptionBase(SQLModel, table=False):
    title: str = Field(max_length=200)
    description: str

    @validator('title')
    def title_validate(cls, title):
        validate_title(title)
        return title

    def __repr__(self):
        return f'{self.title}'
