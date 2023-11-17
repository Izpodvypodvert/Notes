from pydantic import UUID4

from models.note import Note
from schemas.note_schema import TitleDescriptionBase
from services.base_service import BaseService
from utils.enums import NoteLimits
from utils.exceptions import TooManyNotesError


class NoteService(BaseService):
    """
    Service for managing notes in the application.

    This service provides methods for creating, retrieving, updating, and deleting notes,
    limited by the user ID. It uses `NoteRepository` for interaction
    with a database.

    Methods:
    - get_all_notes(user_id): Returns a list of all the user's notes.
    - create_note(note, user_id): Creates a new note for the user if the limit is not exceeded.
    - get_note_by_id(note_id, user_id): Returns a note by its ID and user ID.
    - update_note(note_id, note_data, user_id): Updates the note data by its ID.
    - delete_note(note_id, user_id): Deletes a note by its ID.

    Parameters:
    - note_repository: An instance of the NoteRepository class for accessing the notes database.

    Exceptions:
    - TooManyNotesError: Thrown if the user tries to create a note exceeding the set limit.
    """

    async def create_note(self, note: TitleDescriptionBase, user_id: UUID4) -> Note:
        notes = await self.repository.get_all(user_id)
        if len(notes) >= NoteLimits.MAX_NOTES_PER_USER.value:
            raise TooManyNotesError(NoteLimits.TOO_MANY_NOTES_ERROR_MSG.value)
        return await self.repository.create(note, user_id)
