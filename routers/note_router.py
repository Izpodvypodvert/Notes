from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List

from models.note import Note
from models.user import User
from schemas.note_schema import TitleDescriptionBase
from repositories.note_repository import NoteRepository
from schemas.user_schema import UserRelatedBase
from services.note_service import NoteService
from dependencies.db import get_async_session
from dependencies.user import current_user
from utils.exceptions import TooManyNotesError

router = APIRouter()


async def get_note_service(session: AsyncSession = Depends(get_async_session)) -> NoteService:
    note_repository = NoteRepository(session, Note)
    return NoteService(note_repository)


@router.get("/", response_model=List[Note])
async def read_notes(
    note_service: NoteService = Depends(get_note_service),
    user: User = Depends(current_user),
):
    return await note_service.get_all(user.id)


@router.post("/", response_model=Note, status_code=status.HTTP_201_CREATED)
async def create_note(
        note: TitleDescriptionBase,
        note_service: NoteService = Depends(get_note_service),
        user: User = Depends(current_user),
):
    try:
        new_note = await note_service.create_note(note, user.id)
    except TooManyNotesError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return new_note


@router.get("/{note_id}", response_model=Note)
async def read_note(
        note_id: int,
        note_service: NoteService = Depends(get_note_service),
        user: User = Depends(current_user),
):
    note = await note_service.get_by_id(note_id, user.id)
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.put("/{note_id}", response_model=Note)
async def update_note(
        note_id: int, note_data: TitleDescriptionBase,
        note_service: NoteService = Depends(get_note_service),
        user: User = Depends(current_user),
):
    updated_note = await note_service.update(note_id, note_data, user.id)
    if updated_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated_note


@router.delete("/{note_id}", response_model=Note)
async def delete_note(
    note_id: int,
    note_service: NoteService = Depends(get_note_service),
    user: User = Depends(current_user),
):
    deleted_note = await note_service.delete(note_id, user.id)
    if deleted_note is None:
        raise HTTPException(
            status_code=404, detail="Note not found")
    return deleted_note
