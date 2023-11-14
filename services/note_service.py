from typing import List, Optional

from pydantic import UUID4

from models.note import Note
from schemas.note_schema import NoteBase
from repositories.note_repository import NoteRepository
from utils.enums import NoteLimits
from utils.exceptions import TooManyNotesError


class NoteService:
    def __init__(self, note_repository: NoteRepository):
        self.note_repository = note_repository

    async def get_all_notes(self, user_id: UUID4) -> List[Note]:
        return await self.note_repository.get_all_notes(user_id)

    async def create_note(self, note: NoteBase, user_id: UUID4) -> Note:
        notes = await self.note_repository.get_all_notes(user_id)
        if len(notes) >= NoteLimits.MAX_NOTES_PER_USER.value:
            raise TooManyNotesError(NoteLimits.TOO_MANY_NOTES_ERROR_MSG.value)
        return await self.note_repository.create_note(note, user_id)

    async def get_note_by_id(self, note_id: int, user_id: UUID4) -> Optional[Note]:
        return await self.note_repository.get_note_by_id(note_id, user_id)

    async def update_note(self, note_id: int, note_data: NoteBase, user_id: UUID4) -> Optional[Note]:
        return await self.note_repository.update_note(note_id, note_data, user_id)

    async def delete_note(self, note_id: int, user_id: UUID4) -> Optional[Note]:
        return await self.note_repository.delete_note(note_id, user_id)
