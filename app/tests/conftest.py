import asyncio
import uuid
from datetime import datetime, timedelta

import pytest
from db.session import get_session
from httpx import AsyncClient
from main import app
from pydantic import BaseModel
from settings import ACCESS_TOKEN_EXPIRE_MINUTES, TEST_DATABASE_URL
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from db.models import Base, Salary, User
from utils.hashing import Hasher
from utils.security import create_access_token

engine_test = create_async_engine(TEST_DATABASE_URL, echo=True)

async_session_test = sessionmaker(
    engine_test,
    expire_on_commit=False,
    class_=AsyncSession
)

metadata = Base.metadata
metadata.bind = engine_test


async def get_session_test():
    try:
        session: AsyncSession = async_session_test()
        yield session
    finally:
        await session.close()

app.dependency_overrides[get_session] = get_session_test


@pytest.fixture(autouse=True, scope="session")
async def prepate_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(metadata.drop_all)


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def admin():
    session: AsyncSession = async_session_test()
    async with session.begin():
        user = User(
            username="admin",
            password=Hasher.hash_password(password="admin"),
            email="admin@mail.ru",
            first_name="admin",
            last_name="admin",
            role="admin"
        )
        salary = Salary()
        salary.user = user
        session.add(user)
        session.add(salary)
        return user


@pytest.fixture(scope="session")
async def user():
    session: AsyncSession = async_session_test()
    async with session.begin():
        user = User(
            username="user",
            password=Hasher.hash_password(password="user"),
            email="user@mail.ru",
            first_name="user",
            last_name="user",
            role="user"
        )
        salary = Salary()
        salary.user = user
        session.add(user)
        session.add(salary)
        return user


async def create_test_token(user_id: uuid.UUID):
    expire_time = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    data = {"sub": str(user_id), "exp": expire_time}

    access_token = await create_access_token(data=data)
    return access_token


async def check_schemas(instance: dict, schema: BaseModel) -> bool:
    try:
        schema(**instance)
        return True
    except Exception:
        return False


async def get_count_users():
    session: AsyncSession = async_session_test()
    async with session.begin():
        query = select(func.count()).select_from(User)
        count_users_in_database = await session.scalar(query)
    return count_users_in_database
