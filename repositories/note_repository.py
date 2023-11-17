from models.note import Note
from repositories.crud import CRUDRepository
from schemas.note_schema import TitleDescriptionBase


class NoteRepository(CRUDRepository[Note, TitleDescriptionBase]):
    """
    A repository class for managing notes associated with a User, extending 
    the basic CRUD operations. Notes are the primary entities containing textual 
    information specific to a user.
    """
