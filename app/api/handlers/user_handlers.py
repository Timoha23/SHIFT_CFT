import uuid
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from api.actions.user_actions import (
    authenticate_user_action,
    create_user_action,
    delete_user_action,
    get_current_user_from_token,
    get_users_action
)
from api.schemas import CreateUser, GetToken, GetUser
from db.models import User
from db.session import get_session
from settings import ACCESS_TOKEN_EXPIRE_MINUTES
from utils.decorators import admin_required
from utils.security import create_access_token


user_router = APIRouter()


@user_router.post("/", response_model=GetUser, status_code=201)
async def create_user(
    body: CreateUser,
    session: AsyncSession = Depends(get_session),
):
    """
    Обработчик эндпоинта для создания пользователя
    """

    user = await create_user_action(body=body, session=session)

    return GetUser.from_orm(user)


@user_router.post("/token/", response_model=GetToken)
async def get_token(
    body: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session),
):
    """
    Обработчик эндпоинта для получения токена
    """

    user = await authenticate_user_action(
        body.username,
        body.password,
        session=session
    )

    expire_time = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {
        "sub": str(user.id), "exp": expire_time,
    }

    access_token = await create_access_token(
        data=data
    )
    return GetToken(access_token=access_token, token_type="bearer")


@user_router.get("/", response_model=list[GetUser])
@admin_required
async def get_users(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user_from_token),
):
    """
    Обработчик эндпоинта для получения пользователей
    """

    users = await get_users_action(session=session)
    return [GetUser.from_orm(user) for user in users]


@user_router.delete("/{user_id}/", status_code=204)
@admin_required
async def delete_user(
    user_id: uuid.UUID,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user_from_token)
) -> None:
    """
    Обработчик эндпоинта для удаления пользователя
    """

    await delete_user_action(id=user_id, session=session)
