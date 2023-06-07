import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.actions.salary_actions import update_user_salary_action
from api.actions.user_actions import (
    get_current_user_from_token,
    get_user_by_uuid_action
)
from api.schemas import GetSalary, GetUser, UpdateSalary
from db.models import User
from db.session import get_session
from utils.decorators import admin_required


salary_router = APIRouter()


@salary_router.patch("/{user_id}/", response_model=GetUser)
@admin_required
async def update_salary(
    user_id: uuid.UUID,
    body: UpdateSalary,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user_from_token)
):
    """
    Обработчик эндпоинта обновления данных о зарплате пользователя
    """

    user = await update_user_salary_action(
        user_id=user_id, body=body, session=session
    )
    return GetUser.from_orm(user)


@salary_router.get("/me/", response_model=GetSalary)
async def get_salary_current_user(
    current_user: User = Depends(get_current_user_from_token),
):
    """
    Обработчик эндпоинта получения данных о зарплате пользователя
    """

    return GetSalary.from_orm(current_user.salary)


@salary_router.get("/{user_id}/", response_model=GetSalary)
@admin_required
async def get_salary_user(
    user_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user_from_token),
):
    """
    Обработчик эндпоинта получения зарплаты определенного пользователя
    """

    user = await get_user_by_uuid_action(id=user_id, session=session)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail=f"Пользователь с uuid {user_id} не найден"
        )
    return GetSalary.from_orm(user.salary)
