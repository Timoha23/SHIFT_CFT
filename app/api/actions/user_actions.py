import uuid

from fastapi import Depends, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import CreateUser
from db.models import Salary, User
from db.session import get_session
from settings import ALGORITHM, SECRET_KEY
from utils.hashing import Hasher


# зависимость, которая дает понять FastAPI, что текущий роут
# требует аутентификации.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


async def get_user_by_uuid_action(
        id: uuid.UUID,
        session: AsyncSession
) -> User | None:
    """
    Получение пользователя по uuid
    """

    async with session.begin():
        query = select(User).where(User.id == id)
        user = await session.scalar(query)
        return user


async def create_user_action(
        body: CreateUser,
        session: AsyncSession
) -> User | HTTPException:
    """
    Создаем юзера в БД
    """

    await check_unique_username_and_email(body=body, session=session)

    async with session.begin():
        user = User(
            username=body.username,
            email=body.email,
            password=Hasher.hash_password(password=body.password),
            first_name=body.first_name,
            last_name=body.last_name
        )
        salary = Salary()
        salary.user = user
        session.add(user)
        session.add(salary)
        return user


async def authenticate_user_action(
        username: str,
        password: str,
        session: AsyncSession
) -> User | HTTPException:
    """
    Проверяем существует ли пользователь с данным логином и паролем
    """

    async with session.begin():
        query = select(User).where(User.username == username)
        user = await session.scalar(query)
        if user is None:
            raise HTTPException(
                status_code=404,
                detail=f"Пользователь с {username} не найден"
            )
        elif Hasher.verify_password(password, user.password):
            return user
        raise HTTPException(
            status_code=401,
            detail=f"Некорректный пароль для пользователя {username}"
        )


async def get_current_user_from_token(
        token: str = Depends(oauth2_scheme),
        session: AsyncSession = Depends(get_session),
) -> User | HTTPException:
    """
    Получаем текущего пользователя по токену
    """

    exception = HTTPException(
        status_code=401,
        detail="Невалидный токен"
    )

    try:
        payload = jwt.decode(
            token=token,
            key=SECRET_KEY,
            algorithms=ALGORITHM
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise exception
    except JWTError:
        raise exception

    user = await get_user_by_uuid_action(id=user_id, session=session)
    if user is None:
        raise exception
    return user


async def get_users_action(session: AsyncSession) -> list[User]:
    """
    Получение всех пользователей
    """

    async with session.begin():
        query = select(User)
        users = await session.scalars(query)
        return users


async def delete_user_action(id: uuid.UUID, session: AsyncSession) -> None:
    """
    Удаление пользователя
    """

    async with session.begin():
        query = delete(User).where(User.id == id).returning(User)
        user = await session.scalar(query)
        if user is None:
            raise HTTPException(
                status_code=404,
                detail=f"Пользователь с uuid {id} не найден"
            )


async def check_unique_username_and_email(
    body: CreateUser,
    session: AsyncSession,
) -> None | HTTPException:
    """
    Проверка является ли username и email пользователя уникальными
    """

    if "admin" == body.username or "admin@admin.ru" == body.email:
        raise HTTPException(
            status_code=422,
            detail="Недопустимые данные"
        )

    async with session.begin():
        query_username = select(User).where(User.username == body.username)
        query_email = select(User).where(User.email == body.email)
        user_with_username = await session.scalar(query_username)
        user_with_email = await session.scalar(query_email)
    if user_with_username:
        raise HTTPException(
            status_code=422,
            detail="Пользователь с данным username уже существует"
        )
    elif user_with_email:
        raise HTTPException(
            status_code=422,
            detail="Пользователь с данным email уже существует"
        )
