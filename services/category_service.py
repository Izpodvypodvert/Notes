from services.base_service import BaseService


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
