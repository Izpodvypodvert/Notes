from pydantic import UUID4

from models.note import Note
from schemas.note_schema import TitleDescriptionBase
from services.base_service import BaseService
from utils.enums import CategoryLimits
from utils.exceptions import TooManyCategories


class CategoryService(BaseService):
    """
    Service class for Category-specific operations.

    This class extends the BaseService to provide Category-specific CRUD operations.
    It inherits methods from the BaseService for creating, retrieving, updating,
    and deleting Category objects, all tied to a specific user ID.

    Inherits all methods from BaseService:
    - get_all(user_id): Retrieves all Category objects for a user.
    - create(category, user_id): Creates a new Category object for a user.
    - get_by_id(category_id, user_id): Retrieves a Category object by its ID for a user.
    - update(category_id, category_data, user_id): Updates a Category object for a user.
    - delete(category_id, user_id): Deletes a Category object for a user.

    The CategoryService uses a CRUDRepository specifically designed for Category objects.
    """

    async def create_category(self, category: TitleDescriptionBase, user_id: UUID4) -> Note:
        notes = await self.repository.get_all(user_id)
        if len(notes) >= CategoryLimits.MAX_Category_PER_USER.value:
            raise TooManyCategories(
                CategoryLimits.TOO_MANY_CATEGORIES_ERROR_MSG.value
            )
        return await self.repository.create(category, user_id)
