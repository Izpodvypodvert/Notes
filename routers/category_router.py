from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from models.category import Category
from models.user import User
from repositories.category_repository import CategoryRepository
from schemas.note_schema import TitleDescriptionBase
from services.category_service import CategoryService
from dependencies.db import get_async_session
from dependencies.user import current_user
from utils.exceptions import TooManyCategories


router = APIRouter()


async def get_category_service(session: AsyncSession = Depends(get_async_session)) -> CategoryService:
    category_repository = CategoryRepository(session, Category)
    return CategoryService(category_repository)


@router.get("/", response_model=list[Category])
async def read_categories(
    category_service: CategoryService = Depends(get_category_service),
    user: User = Depends(current_user),
):
    return await category_service.get_all(user.id)


@router.post("/", response_model=Category, status_code=status.HTTP_201_CREATED)
async def create_category(
        category: TitleDescriptionBase,
        category_service: CategoryService = Depends(get_category_service),
        user: User = Depends(current_user),
):
    try:
        new_category = await category_service.create(category, user.id)
    except TooManyCategories as e:
        raise HTTPException(status_code=400, detail=str(e))

    return new_category


@router.get("/{category_id}", response_model=Category)
async def read_category(
        category_id: int,
        category_service: CategoryService = Depends(get_category_service),
        user: User = Depends(current_user),
):
    category = await category_service.get_by_id(category_id, user.id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.put("/{category_id}", response_model=Category)
async def update_category(
        category_id: int,
        category_data: TitleDescriptionBase,
        category_service: CategoryService = Depends(get_category_service),
        user: User = Depends(current_user),
):
    updated_category = await category_service.update(category_id, category_data, user.id)
    if updated_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated_category


@router.delete("/{category_id}", response_model=Category)
async def delete_category(
    category_id: int,
    category_service: CategoryService = Depends(get_category_service),
    user: User = Depends(current_user),
):
    deleted_category = await category_service.delete(category_id, user.id)
    if deleted_category is None:
        raise HTTPException(
            status_code=404, detail="Category not found")
    return deleted_category
