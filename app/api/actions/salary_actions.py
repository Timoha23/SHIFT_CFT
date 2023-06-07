import uuid

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import UpdateSalary
from db.models import Salary, User
from api.actions.user_actions import get_user_by_uuid_action


async def update_user_salary_action(
        user_id: uuid.UUID,
        body: UpdateSalary,
        session: AsyncSession
) -> User | HTTPException:
    """
    Обновление данных о зарплате
    """

    user = await get_user_by_uuid_action(id=user_id, session=session)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail=f"Пользователь с id {user_id} не найден"
        )
    async with session.begin():
        query = select(Salary).where(Salary.user == user)
        salary = await session.scalar(query)
        if body.current_salary:
            salary.current_salary = body.current_salary
        if body.increase_date:
            salary.increase_date = body.increase_date.replace(tzinfo=None)
        return user
