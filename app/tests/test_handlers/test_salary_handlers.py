from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import GetSalary, GetUser
from db.models import Salary, User
from tests.conftest import (
    async_session_test,
    check_schemas,
    create_test_token
)


async def test_get_salary_me(
    user: User,
    async_client: AsyncClient,
):
    """
    Тестирование получения информации о своей ЗП
    """

    user_token = await create_test_token(user_id=user.id)
    response = await async_client.get(
        url="/salary/me/",
        headers={"Authorization": f"bearer {user_token}"}
    )

    assert response.status_code == 200
    assert response.json()["id"] == str(user.salary.id)
    assert response.json()["current_salary"] == user.salary.current_salary
    assert await check_schemas(
        instance=response.json(), schema=GetSalary
    ) is True


async def test_get_salary_user(
    user: User,
    admin: User,
    async_client: AsyncClient
):
    """
    Тестирование получения информации о ЗП пользователя
    """

    user_token = await create_test_token(user_id=user.id)
    admin_token = await create_test_token(user_id=admin.id)

    bad_uuid = "ba80c512-e114-43be-88da-0ea37b2c8a31"

    response_admin_good = await async_client.get(
        url=f"/salary/{str(user.id)}/",
        headers={"Authorization": f"bearer {admin_token}"}
    )
    response_admin_bad = await async_client.get(
        url=f"/salary/{bad_uuid}/",
        headers={"Authorization": f"bearer {admin_token}"}
    )

    response_user = await async_client.get(
        url=f"/salary/{str(admin.id)}/",
        headers={"Authorization": f"bearer {user_token}"}
    )

    assert response_admin_good.status_code == 200
    assert response_admin_good.json()["id"] == str(user.salary.id)
    assert (response_admin_good.json()["current_salary"] ==
            user.salary.current_salary)
    assert await check_schemas(
        instance=response_admin_good.json(), schema=GetSalary
    ) is True

    assert response_admin_bad.status_code == 404
    assert response_admin_bad.json() == {
        'detail': f'Пользователь с uuid {bad_uuid} не найден'
    }

    assert response_user.status_code == 403
    assert response_user.json() == {
      "detail": "Недостаточно прав"
    }


async def test_patch_salary_user(
    user: User,
    admin: User,
    async_client: AsyncClient,
):
    """
    Тестирование изменения информации о ЗП для пользователя
    """

    session: AsyncSession = async_session_test()
    user_token = await create_test_token(user_id=user.id)
    admin_token = await create_test_token(user_id=admin.id)

    body = {
        "current_salary": 100000,
        "increase_date": "2035-06-06T08:54:16.209000"
    }

    user_salary_before_response = user.salary.current_salary

    response_user = await async_client.patch(
        url=f"/salary/{str(user.id)}/",
        json=body,
        headers={"Authorization": f"bearer {user_token}"}
    )

    async with session.begin():
        query = select(Salary).where(Salary.user_id == user.id)
        salary = await session.scalar(query)
        await session.close()

    user_salary_after_user_response = salary.current_salary

    response_admin = await async_client.patch(
        url=f"/salary/{str(user.id)}/",
        json=body,
        headers={"Authorization": f"bearer {admin_token}"}
    )

    async with session.begin():
        query = select(Salary).where(Salary.user_id == user.id)
        salary = await session.scalar(query)
    user_salary_after_admin_response = salary.current_salary

    assert response_user.status_code == 403
    assert response_user.json() == {
      "detail": "Недостаточно прав"
    }

    assert response_admin.status_code == 200
    assert response_admin.json()["id"] == str(user.id)
    assert response_admin.json()["salary"]["id"] == str(user.salary.id)
    assert (response_admin.json()["salary"]["current_salary"] ==
            body["current_salary"])
    assert (response_admin.json()["salary"]["increase_date"] ==
            body["increase_date"])
    assert await check_schemas(instance=response_admin.json(), schema=GetUser)

    assert (user_salary_before_response == user_salary_after_user_response !=
            user_salary_after_admin_response)
