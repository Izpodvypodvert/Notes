import uuid
from typing import TYPE_CHECKING

from fastapi_users import schemas
from pydantic import UUID4, validator
from sqlmodel import Field, Relationship, SQLModel

from utils.validators import validate_title


if TYPE_CHECKING:
    from models.user import User


class UserRead(schemas.BaseUser[UUID4]):
    """Schema with basic user model fields (except password):
    id, email address, is_active, is_superuser, is_verified."""


class UserCreate(schemas.BaseUserCreate):
    """Scheme for creating a user. Email and password must be transmitted.
    Any other fields passed in the user creation request will be ignored."""


class UserUpdate(schemas.BaseUserUpdate):
    """Schema for updating the user object. Contains all the basic fields of the user model (including the password).
    All fields are optional. If the request is sent by a regular user (and not a superuser), then the is_active, is_superuser fields,
    is_verified is excluded from the dataset: these three fields can only be changed by the superuser."""


class UserRelatedBase(SQLModel, table=False):
    id: UUID4 = Field(default_factory=uuid.uuid4,
                      primary_key=True, nullable=False)
    user_id: UUID4 = Field(default_factory=uuid.uuid4, foreign_key="user.id")
