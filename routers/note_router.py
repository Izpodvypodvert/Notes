from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from models.note import Note
from models.user import User
from custom_libs.fastapi_cache.decorator import cache
from dependencies.db import get_async_session
from dependencies.user import current_user
from repositories.note_repository import NoteRepository
from schemas.note_schema import NoteBase
from services.note_service import NoteService
from utils.cache import cache_key_builder_with_user_id, clear_user_chache
from utils.constants import URL_BORED_API
from utils.exceptions import TooManyNotesError
from utils.fetching_data import fetch_activity


router = APIRouter()


async def get_note_service(session: AsyncSession = Depends(get_async_session)) -> NoteService:
    note_repository = NoteRepository(session, Note)
    return NoteService(note_repository)


@router.get("/", response_model=list[Note])
@cache(expire=3600, key_builder=cache_key_builder_with_user_id)
async def read_notes(
    note_service: NoteService = Depends(get_note_service),
    user: User = Depends(current_user),
):
    notes = await note_service.get_all(user.id)
    return notes


@router.post("/", response_model=Note, status_code=status.HTTP_201_CREATED)
async def create_note(
        note: NoteBase,
        note_service: NoteService = Depends(get_note_service),
        user: User = Depends(current_user),
):
    try:
        new_note = await note_service.create_note(note, user.id)
    except TooManyNotesError as e:
        raise HTTPException(status_code=400, detail=str(e))

    await clear_user_chache(user)
    return new_note


@router.post("/create_random_note", response_model=Note, status_code=status.HTTP_201_CREATED)
async def create_random_note_if_bored(
    note_service: NoteService = Depends(get_note_service),
    user: User = Depends(current_user)
):
    bored_note = await fetch_activity(URL_BORED_API)
    note_data = NoteBase(title=bored_note.get(
        'type'), description=bored_note.get('activity'))
    try:
        new_note = await note_service.create_note(note_data, user.id)
    except TooManyNotesError as e:
        raise HTTPException(status_code=400, detail=str(e))
    await clear_user_chache(user)
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
        note_id: int, note_data: NoteBase,
        note_service: NoteService = Depends(get_note_service),
        user: User = Depends(current_user),
):
    updated_note = await note_service.update(note_id, note_data, user.id)
    if updated_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    await clear_user_chache(user)
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
    await clear_user_chache(user)
    return deleted_note
