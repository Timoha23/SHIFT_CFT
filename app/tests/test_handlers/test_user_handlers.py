from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import GetToken, GetUser
from db.models import User
from tests.conftest import (
    async_session_test,
    check_schemas,
    create_test_token,
    get_count_users
)
from utils.hashing import Hasher


async def test_get_users(
        admin: User,
        user: User,
        async_client: AsyncClient,
):
    """
    Тестирование получения пользователей
    """

    admin_token = await create_test_token(user_id=admin.id)

    user_token = await create_test_token(user_id=user.id)
    response_admin = await async_client.get(
        url="/users/",
        headers={"Authorization": f"bearer {admin_token}"}
    )
    response_user = await async_client.get(
        url="/users/",
        headers={"Authorization": f"bearer {user_token}"}
    )

    # Определим количество пользователей в БД
    count_users_in_database = await get_count_users()

    assert await check_schemas(
        instance=response_admin.json()[0], schema=GetUser
    ) is True
    assert len(response_admin.json()) == count_users_in_database
    assert response_admin.status_code == 200

    assert response_user.status_code == 403
    assert response_user.json() == {
      "detail": "Недостаточно прав"
    }


async def test_create_user(
        async_client: AsyncClient,
):
    """
    Тестирование регистрации пользователя
    """

    # количество пользователей до регистрации
    count_users_in_database_before = await get_count_users()

    body = {
        "username": "testuser",
        "email": "testuser@mail.ru",
        "password": "testuser",
        "first_name": "Иван",
        "last_name": "Иванов",
    }

    body_without_username = body.copy()
    body_without_username.pop("username")

    body_with_incorrect_username = body.copy()
    body_with_incorrect_username["username"] = "@*#&!()#@!@"

    body_with_incorrect_email = body.copy()
    body_with_incorrect_email["email"] = "emailnotcorrect.ru"

    body_with_incorrect_first_name = body.copy()
    body_with_incorrect_first_name["first_name"] = "Ivan"

    body_with_incorrect_last_name = body.copy()
    body_with_incorrect_last_name["last_name"] = "Ivanov"

    good_response = await async_client.post(
        url="/users/",
        json=body,
    )

    bad_response_without_username = await async_client.post(
        url="/users/",
        json=body_without_username
    )

    bad_response_with_incorrect_username = await async_client.post(
        url="/users/",
        json=body_with_incorrect_username
    )

    bad_response_with_incorrect_email = await async_client.post(
        url="/users/",
        json=body_with_incorrect_email
    )

    bad_response_with_incorrect_first_name = await async_client.post(
        url="/users/",
        json=body_with_incorrect_first_name
    )

    bad_response_with_incorrect_last_name = await async_client.post(
        url="/users/",
        json=body_with_incorrect_last_name
    )

    # количество пользователей после регистрации
    count_users_in_database_after = await get_count_users()

    assert good_response.json()["username"] == body["username"]
    assert good_response.json()["email"] == body["email"]
    assert good_response.json()["first_name"] == body["first_name"]
    assert good_response.json()["last_name"] == body["last_name"]
    assert good_response.json()["id"] is not None
    assert good_response.json()["created_date"] is not None
    assert isinstance(good_response.json()["salary"], dict) is True
    assert good_response.status_code == 201
    assert await check_schemas(
        instance=good_response.json(), schema=GetUser
    ) is True

    assert bad_response_without_username.status_code == 422
    assert bad_response_without_username.json() == {
        "detail": [
            {
                "loc": [
                    "body", "username"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }

    assert bad_response_with_incorrect_username.status_code == 422
    assert bad_response_with_incorrect_username.json() == {
        "detail": "Username может содержать только латиницу и цифры"
    }

    assert bad_response_with_incorrect_email.status_code == 422
    assert bad_response_with_incorrect_email.json() == {
        "detail": [
            {
                "loc": [
                    "body", "email"
                ],
                "msg": "value is not a valid email address",
                "type": "value_error.email"
            }
        ]
    }

    assert bad_response_with_incorrect_first_name.status_code == 422
    assert bad_response_with_incorrect_first_name.json() == {
        "detail": "Имя и фамилия могут содержать только кириллицу"
    }

    assert bad_response_with_incorrect_last_name.status_code == 422
    assert bad_response_with_incorrect_last_name.json() == {
        "detail": "Имя и фамилия могут содержать только кириллицу"
    }

    assert count_users_in_database_before + 1 == count_users_in_database_after


async def test_create_token(
        user: User,
        async_client: AsyncClient
):
    """
    Тестирование получения токена
    """

    user_password = "user"
    body = {'username': user.username, "password": user_password}

    body_without_username = {"password": user_password}
    body_without_password = {"username": user.username}
    body_with_incorrect_username = {
        "username": "incorrect_username", "password": user_password
    }
    body_with_incorrect_password = {
        "username": user.username, "password": "password"
    }

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = await async_client.post(
        url="/users/token/", data=body, headers=headers
    )
    bad_response_without_username = await async_client.post(
        url="/users/token/", data=body_without_username, headers=headers
    )
    bad_response_without_password = await async_client.post(
        url="/users/token/", data=body_without_password, headers=headers
    )
    bad_response_with_incorrect_username = await async_client.post(
        url="/users/token/", data=body_with_incorrect_username, headers=headers
    )
    bad_response_with_incorrect_password = await async_client.post(
        url="/users/token/", data=body_with_incorrect_password, headers=headers
    )

    assert response.status_code == 200
    assert response.json()["access_token"] is not None
    assert response.json()["token_type"] == "bearer"
    assert await check_schemas(
        instance=response.json(), schema=GetToken
    ) is True

    assert bad_response_without_username.status_code == 422
    assert bad_response_without_username.json() == {
        "detail": [
            {
                "loc": [
                    "body",
                    "username"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }
    assert bad_response_without_password.status_code == 422
    assert bad_response_without_password.json() == {
        "detail": [
            {
                "loc": [
                    "body",
                    "password"
                ],
                "msg": "field required",
                "type": "value_error.missing"
            }
        ]
    }
    assert bad_response_with_incorrect_username.status_code == 404
    assert bad_response_with_incorrect_username.json() == {
        "detail": f"Пользователь с {body_with_incorrect_username['username']}"
        " не найден"
    }
    assert bad_response_with_incorrect_password.status_code == 401
    assert bad_response_with_incorrect_password.json() == {
        "detail": "Некорректный пароль для пользователя "
        f"{body_with_incorrect_password['username']}"
    }


async def test_delete_user(
    admin: User,
    user: User,
    async_client: AsyncClient,
):
    """
    Тестирование удаления пользователя
    """

    session: AsyncSession = async_session_test()

    async with session.begin():
        user_for_delete = User(
            username="userdelete",
            email="userdelete@mail.ru",
            password=Hasher.hash_password("userdelete"),
            first_name="Иван",
            last_name="Иванов"
        )
        session.add(user_for_delete)

    count_users_before_delete = await get_count_users()

    admin_token = await create_test_token(user_id=admin.id)
    user_token = await create_test_token(user_id=user.id)

    response_user = await async_client.delete(
        url=f"/users/{str(user_for_delete.id)}/",
        headers={"Authorization": f"bearer {user_token}"}
    )

    response_admin = await async_client.delete(
        url=f"/users/{str(user_for_delete.id)}/",
        headers={"Authorization": f"bearer {admin_token}"}
    )
    response_admin_with_incorrect_uuid = await async_client.delete(
        url=f"/users/{str(user_for_delete.id)}/",
        headers={"Authorization": f"bearer {admin_token}"}
    )

    count_users_after_delete = await get_count_users()

    assert response_user.status_code == 403
    assert response_user.json() == {
      "detail": "Недостаточно прав"
    }

    assert response_admin.status_code == 204
    assert response_admin_with_incorrect_uuid.status_code == 404
    assert response_admin_with_incorrect_uuid.json() == {
        'detail': f'Пользователь с uuid {str(user_for_delete.id)} не найден'
    }
    assert count_users_before_delete == count_users_after_delete + 1
