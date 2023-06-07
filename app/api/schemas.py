import datetime
import re
import uuid

from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, validator


USERNAME_PATTERN = re.compile(r"^[a-zA-Z0-9]+$")
FIRST_LAST_NAME_PATTERN = re.compile(r"^[а-яА-Я]+$")


class CreateUser(BaseModel):
    """
    Создание пользователя
    """

    username: str
    email: EmailStr
    password: str
    first_name: str
    last_name: str

    @validator("username")
    def validate_username(cls, value: str):
        if not USERNAME_PATTERN.match(value):
            raise HTTPException(
                status_code=422,
                detail="Username может содержать только латиницу и цифры"
            )
        elif len(value) < 6 or len(value) > 30:
            raise HTTPException(
                status_code=422,
                detail="Username должен быть больше 6 символов, но меньше 30"
            )
        return value

    @validator("first_name", "last_name")
    def validate_first_and_last_name(cls, value: str):
        if not FIRST_LAST_NAME_PATTERN.match(value):
            raise HTTPException(
                status_code=422,
                detail="Имя и фамилия могут содержать только кириллицу"
            )
        return value.title()

    @validator("password")
    def validate_password(cls, value: str):
        if len(value) < 6 or len(value) > 30:
            raise HTTPException(
                status_code=422,
                detail="Пароль должен быть больше 6 символов, но меньше 30"
            )
        return value


class GetSalary(BaseModel):
    """
    Вложенная модель с зарплатой юзера
    """

    id: uuid.UUID
    current_salary: float | None
    increase_date: datetime.datetime | None
    created_date: datetime.datetime

    class Config:
        orm_mode = True


class GetUser(BaseModel):
    """
    Получение пользователя с информацией о зарплате
    """

    id: uuid.UUID
    username: str
    email: str
    first_name: str
    last_name: str
    created_date: datetime.datetime
    salary: GetSalary

    class Config:
        orm_mode = True


class GetToken(BaseModel):
    """
    Получение токена
    """

    access_token: str
    token_type: str


class UpdateSalary(BaseModel):
    """
    Обновление информации о зарплате пользователя
    """

    current_salary: float | None
    increase_date: datetime.datetime | None
