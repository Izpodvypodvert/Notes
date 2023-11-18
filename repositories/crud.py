from pydantic import UUID4
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from schemas.note_schema import TitleDescriptionBase
from schemas.user_schema import UserRelatedBase


class CRUDRepository[T: UserRelatedBase, S: TitleDescriptionBase]:
    """
    A base repository class providing basic CRUD (Create, Read, Update, Delete) 
    operations for a generic entity type in relation to a User.

    These operations are designed to interact with a database or data storage 
    system and are user-specific, ensuring that each entity is associated 
    with the correct user account.

    Methods:
        create(user_id, entity): Adds a new entity associated with a user to the repository.
        get_all(user_id): Retrieves all entities, ensuring it belongs to the user.
        get_by_id(user_id, entity_id): Retrieves an entity by its ID, ensuring it belongs to the specified user.
        update(user_id, entity): Updates an existing entity associated with a user.
        delete(user_id, entity_id): Removes an entity from the repository by its ID, ensuring it belongs to the specified user.
    """

    def __init__(self, session: AsyncSession, model: type[T]):
        self.session = session
        self.model = model

    async def get_all(self, user_id: UUID4) -> list[T]:
        statement = select(self.model).where(self.model.user_id == user_id)
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def create(self, schema: S, user_id: UUID4) -> T:
        obj = self.model(**schema.dict(), user_id=user_id)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get_by_id(self, obj_id: int, user_id: UUID4) -> T | None:
        statement = select(self.model).where(
            self.model.id == obj_id, self.model.user_id == user_id)
        result = await self.session.execute(statement)
        return result.scalars().first()

    async def update(self, obj_id: int, schema: S, user_id: UUID4) -> T | None:
        obj = await self.get_by_id(obj_id, user_id)
        if obj:
            update_data = schema.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(obj, key, value)
            self.session.add(obj)
            await self.session.commit()
            await self.session.refresh(obj)
        return obj

    async def delete(self, obj_id: int, user_id: UUID4) -> T | None:
        obj = await self.get_by_id(obj_id, user_id)
        if obj:
            await self.session.delete(obj)
            await self.session.commit()
        return obj
