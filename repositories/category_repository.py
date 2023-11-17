from models.category import Category
from repositories.crud import CRUDRepository
from schemas.note_schema import TitleDescriptionBase


class CategoryRepository(CRUDRepository[Category, TitleDescriptionBase]):
    """
    A repository class for managing categories associated with a User, extending 
    the basic CRUD operations. Categories are used to group or classify notes 
    for a specific user.
    """
