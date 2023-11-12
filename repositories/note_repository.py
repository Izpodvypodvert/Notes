from typing import List, Optional
from pydantic import UUID4
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from models.note import Note
from schemas.note_schema import NoteBase


class NoteRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_notes(self, user_id: UUID4) -> List[Note]:
        statement = select(Note).where(Note.user_id == user_id)
        result = await self.session.execute(statement)
        notes = result.scalars().all()
        return notes

    async def create_note(self, note: NoteBase, user_id: UUID4) -> Note:
        new_note = Note(title=note.title,
                        description=note.description,
                        user_id=user_id)
        self.session.add(new_note)
        await self.session.commit()
        await self.session.refresh(new_note)
        return new_note

    async def get_note_by_id(self, note_id: int, user_id: UUID4) -> Optional[Note]:
        statement = select(Note).where(
            Note.id == note_id, Note.user_id == user_id)
        result = await self.session.execute(statement)
        note = result.scalars().first()
        return note

    async def update_note(self, note_id: int, note_data: NoteBase, user_id: UUID4) -> Optional[Note]:
        statement = select(Note).where(
            Note.id == note_id, Note.user_id == user_id)
        result = await self.session.execute(statement)
        note = result.scalars().first()
        if note:
            note_data_dict = note_data.dict(exclude_unset=True)
            for key, value in note_data_dict.items():
                setattr(note, key, value)
            self.session.add(note)
            await self.session.commit()
            await self.session.refresh(note)
        return note

    async def delete_note(self, note_id: int, user_id: UUID4) -> Optional[Note]:
        statement = select(Note).where(
            Note.id == note_id, Note.user_id == user_id)
        result = await self.session.execute(statement)
        note = result.scalars().first()
        if note:
            await self.session.delete(note)
            await self.session.commit()
        return note
