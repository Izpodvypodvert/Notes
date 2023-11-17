from typing import List, Optional
from pydantic import UUID4
from sqlmodel import SQLModel

from repositories.crud import CRUDRepository
from schemas.note_schema import TitleDescriptionBase


class BaseService():
    """
    A base service class for common CRUD operations.

    This service class provides common async methods for creating, retrieving,
    updating, and deleting objects, tied to a specific user ID. It relies on a
    CRUDRepository instance for database interactions.

    Methods:
    - get_all(user_id): Retrieves a list of SQLModel objects associated with a user ID.
    - create(obj, user_id): Creates a new SQLModel object associated with a user ID.
    - get_by_id(obj_id, user_id): Retrieves a specific SQLModel object by its ID and user ID.
    - update(obj_id, obj_data, user_id): Updates a SQLModel object based on its ID and user ID.
    - delete(obj_id, user_id): Deletes a SQLModel object based on its ID and user ID.

    Attributes:
    - repository (CRUDRepository): An instance of CRUDRepository for database operations.

    Parameters:
    - repository: An instance of a subclass of CRUDRepository for performing CRUD operations.
    """

    def __init__(self, repository: CRUDRepository):
        self.repository = repository

    async def get_all(self, user_id: UUID4) -> List[SQLModel]:
        return await self.repository.get_all(user_id)

    async def create(self, obj: TitleDescriptionBase, user_id: UUID4) -> SQLModel:
        objs = await self.repository.get_all(user_id)
        return await self.repository.create(obj, user_id)

    async def get_by_id(self, obj_id: int, user_id: UUID4) -> Optional[SQLModel]:
        return await self.repository.get_by_id(obj_id, user_id)

    async def update(self, obj_id: int, obj_data: TitleDescriptionBase, user_id: UUID4) -> Optional[SQLModel]:
        return await self.repository.update(obj_id, obj_data, user_id)

    async def delete(self, obj_id: int, user_id: UUID4) -> Optional[SQLModel]:
        return await self.repository.delete(obj_id, user_id)
